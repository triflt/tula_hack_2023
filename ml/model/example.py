import os

import yaml
import torch

from models import Segmentator, Classifier, SatelliteModel


if __name__ == "__main__":
    CHECKPOINT_PATH = os.path.join("weights", "sam_vit_h_4b8939.pth")
    IMAGE_PATH = "picture.jpg"

    with open("config.yaml", 'r') as stream:
        CONFIG = yaml.safe_load(stream)

    print(CONFIG)
    DEVICE = CONFIG["device"]
    CLASSIFIER_PATH = CONFIG["classifier_path"]

    segmentator = Segmentator(path=CHECKPOINT_PATH, device=DEVICE)

    classifier_model = torch.load(CLASSIFIER_PATH)
    classifier = Classifier(model=classifier_model, device=DEVICE)

    gigamodel = SatelliteModel(segmentator, classifier)
    print(gigamodel.process_image("picture.jpg"))