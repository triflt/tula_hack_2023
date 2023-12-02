import os

import cv2
import torch
from torch.utils.data import Dataset

class2id = {
    'greenhouse': 0,
    'private_house': 1,
    'public_building': 2,
    'public_house': 3,
    'barn': 4,
    'pool': 5,
    'nothing': 6
}

id2class = {
    0: 'greenhouse',
    1: 'private_house',
    2: 'public_building',
    3: 'public_house',
    4: 'barn',
    5: 'pool',
    6: 'nothing',
}

class SatelliteDataset(Dataset):
    def __init__(self, root):
        self.root = root

        self.paths = []
        self.labels = []
        self.encoded_labels = []

        for folder in os.listdir(self.root):
            if os.path.isdir(f"{self.root}/{folder}"):
                for file in os.listdir(f"{self.root}/{folder}"):
                    if file != ".DS_Store":
                        self.paths.append(f"{self.root}/{folder}/{file}")
                        self.labels.append(folder)
                        self.encoded_labels.append(class2id[folder])

    def __getitem__(self, idx):
        img = torch.from_numpy(cv2.imread(self.paths[idx]))
        label = self.encoded_labels[idx]

        return img, label

    def __len__(self) -> int:
        return len(self.paths)
