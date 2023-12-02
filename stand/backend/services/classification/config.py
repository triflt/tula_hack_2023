from pathlib import Path

from stand.backend.services.classification.typing import Config

DEFAULT_CONFIG: Config = {
    'device': 'cpu',
    'classifier_path': Path('ml/model/classifier.pt'),
    'checkpoint_path': Path('ml/model/weights/sam_vit_h_4b8939.pth'),
}
