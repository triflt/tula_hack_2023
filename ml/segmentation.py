import os
import torch
import cv2
import supervision as sv
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

CHECKPOINT_PATH = os.path.join("weights", "sam_vit_h_4b8939.pth")
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
MODEL_TYPE = "vit_h"
IMAGE_PATH = "picture.jpg"


class Segmentator:
    def __init__(self, path, device):
        self.path = path
        self.model_type = "vit_h"
        self.device = device
        self.model = sam_model_registry[self.model_type](checkpoint=self.path).to(device=self.device)
        self.mask_generator = SamAutomaticMaskGenerator(self.model)
        self.mask_annotator = sv.MaskAnnotator(color_lookup=sv.ColorLookup.INDEX)

    def predict(self, image):
        result = [el for el in self.mask_generator.generate(image)
                  if el["stability_score"] > 0.975]
        return result

    def annotate(self, image, result):
        detections = sv.Detections.from_sam(sam_result=result)
        annotated_image = self.mask_annotator.annotate(scene=image.copy(),
                                                       detections=detections)
        return annotated_image


if __name__ == "__main__":
    # Define model
    model = Segmentator(CHECKPOINT_PATH, DEVICE)

    # Load image
    image_bgr = cv2.imread(IMAGE_PATH)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Model outputs
    result = model.predict(image_rgb)

    # Annotated image (with segmentations)
    annotation = model.annotate(image_rgb, result)

    # Красиво выводим
    sv.plot_images_grid(
        images=[image_bgr, annotation],
        grid_size=(1, 2),
        titles=['source image', 'segmented image']
    )

