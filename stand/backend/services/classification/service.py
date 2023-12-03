from functools import cached_property
from pathlib import Path
from typing import Any

import torch

from ml.model.models import Classifier, SatelliteModel, Segmentator
from stand.backend.services.classification.typing import Config


class Classificator:
    def __init__(self, image_path: str | Path, config: Config):
        self.image_path = image_path
        self.config = config

    @cached_property
    def classification_result(self) -> list[dict]:
        return sorted(self.model.process_image(str(self.image_path)), key=lambda x: x['area'], reverse=True)

    @cached_property
    def _classifier_model(self) -> Any:
        return torch.load(self.config['classifier_path'], map_location=torch.device(self.config['device']))

    @cached_property
    def segmentator(self) -> Segmentator:
        return Segmentator(path=self.config['checkpoint_path'], device=self.config['device'])

    @cached_property
    def classifier(self) -> Classifier:
        return Classifier(model=self._classifier_model, device=self.config['device'])

    @cached_property
    def model(self) -> SatelliteModel:
        return SatelliteModel(self.segmentator, self.classifier)
