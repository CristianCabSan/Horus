import json
import torch
import torchvision.transforms as T

from contextlib import suppress

from pathlib import Path

from ultralytics.yolo.utils.plotting import save_one_box

from timm.data import create_transform
from timm.models import create_model

torch.backends.cudnn.benchmark = True

class SecondClassifier():

        def __init__(self, device):
            if torch.cuda.is_available():
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.benchmark = True

            self.classifier = None
            self.device = torch.device(device)
            self.toPil = T.ToPILImage()
            self.toTensor = None
            self.imagenet_classes = json.load(open('ultralytics/yolo/cfg/clases_tr.json'))

        def load(self, model: str, checkpoint: str):
            if checkpoint:
                self.classifier = create_model(model,num_classes=6,in_chans=3,checkpoint_path=checkpoint)
            else:
                self.classifier = create_model(model,num_classes=1000,in_chans=3,pretrained=True)
            
            self.classifier.to(self.device)
            self.classifier.eval()

            self.toTensor = create_transform(input_size=self.classifier.default_cfg['input_size'], crop_pct=self.classifier.default_cfg['crop_pct'])

        def predict(self, img):
            with torch.no_grad():
                img = self.toPil(img)
                input_image = self.toTensor(img).unsqueeze(0)
                
                # resolve AMP arguments based on PyTorch / Apex availability
                amp_autocast = suppress
                with amp_autocast():
                    output = self.classifier(input_image.to('cuda:0'))
            
                # set the outputs as probabilities
                output = output.softmax(-1)
                # pick top 1 prediction
                output, index = output.topk(1)

                name = self.imagenet_classes[str(index.item())]

            return name, float(output.item())
        

def filter_results(args, imc, pred, profilers, mode='predict'):     
    CLASSES = ['assault rifle, assault gun', 'revolver, six-gun, six-shooter', 'rifle']
    indexes = []
    for ib, det in enumerate(pred):
        xyxy = det[:4]
        conf = float(det[4])
        if args.args.classifier and conf < args.args.conf_thr:
            with profilers[-1]:
                pad = abs(min(xyxy[2]-xyxy[0], xyxy[3]-xyxy[1])*0.15) if args.args.padding > 0 else 10
                # Obtain the crop where the object is in order to classify it
                if mode == 'predict':
                    crop = save_one_box(xyxy, imc, file=Path('crops/im.jpg'), BGR=True, pad=pad, save=False)
                else:
                    crop = save_one_box(xyxy, imc, file=Path('crops/im.jpg'), BGR=False, pad=pad, save=False)
                # Predict over the cropped image
                name_cls, prob = args.classifier.predict(crop)
                # If got one of these classes and a confidence greater than threshold, replace the previous confidence by the one given by the second classifier
                if name_cls in CLASSES and prob >= args.args.classifier_thr:
                    pred[ib, 4] = torch.tensor(prob).cuda()
                else:
                    ##  Add the index to the list of indexes to remove
                    indexes.append(ib)

    # Remove bad detections
    if indexes:
        pred = torch.index_select(pred, 0, torch.tensor([i for i in range(pred.shape[0]) if i not in indexes], device=args.model.device))
    
    return pred