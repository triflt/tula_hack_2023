import torch
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import cv2
import supervision as sv
from torchvision import transforms


class Segmentator:
    def __init__(self, path, device):
        self.path = path
        self.model_type = "vit_h"
        self.device = device
        self.model = sam_model_registry[self.model_type](checkpoint=self.path).to(device=self.device)
        self.mask_generator = SamAutomaticMaskGenerator(self.model)
        self.mask_annotator = sv.MaskAnnotator(color_lookup=sv.ColorLookup.INDEX)

    def predict(self, image):
        result = [el for el in self.mask_generator.generate(image) if el["stability_score"] > 0.975]
        return result

    def annotate(self, image, result):
        detections = sv.Detections.from_sam(sam_result=result)
        annotated_image = self.mask_annotator.annotate(scene=image.copy(),
                                                       detections=detections)
        return annotated_image


class Classifier:
    def __init__(self, model, device):
        self.model = model
        self.model.eval()

        self.device = device

        self.transform = transforms.Compose([
            transforms.Resize(size=(256, 256)),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def score(self, image, result):
        self.model.to(self.device)
        image = torch.from_numpy(image).permute(2, 0, 1).to(self.device)

        for i in range(len(result)):
            x1, y1, h, w = result[i]["bbox"]
            bbox_image = image[:, x1:x1 + w, y1:y1 + h]

            if (torch.Tensor(list(bbox_image.shape)) == 0).sum().item() == 0:
                result[i]["class"] = self.model(self.transform(bbox_image.float()).unsqueeze(0)).argmax(dim=-1).item()
            else:
                result[i]["class"] = 6

        return result


class SatelliteModel:
    def __init__(self, segmentator, classifier):
        self.segmentator, self.classifier = segmentator, classifier

    def process_image(self, path_to_image):
        image_bgr = cv2.imread(path_to_image)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        result = self.segmentator.predict(image_rgb)
        result = self.classifier.score(image_rgb, result)

        return result
