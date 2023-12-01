import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from transformers import get_cosine_schedule_with_warmup

from ml.losses import IoULoss, DiceLoss, FocalLoss


transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def train_epoch(model, loader, criterion, optimizer, scheduler, device):
    model.train()

    total_loss = 0.0

    for images, masks in loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, masks)

        total_loss += loss.item()

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()

    return total_loss / len(loader)


def eval_epoch(model, loader, criterion, device):
    model.eval()

    total_loss = 0.0

    with torch.no_grad():
        for images, masks in loader:
            outputs = model(images)
            loss = criterion(outputs, masks)

            total_loss += loss.item()

    return total_loss / len(loader)


def train_model(model, train_dataloader, criterion, optimizer, scheduler, device):
    for epoch in range(10):
        train_metrics = train_epoch(model, train_dataloader, criterion, optimizer, scheduler, device)
        eval_metrics = eval_epoch(model, train_dataloader, criterion, device)

        print(train_metrics, eval_metrics)



if __name__ == "__main__":
    lr = 1e-3
    num_epochs = 10
    DEVICE = "cuda"

    model = Model()

    train_dataset = SegmentationDataset('train_dir', transform)
    val_dataset = SegmentationDataset('val_dir', transform)

    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr)
    scheduler = get_cosine_schedule_with_warmup(optimizer,
                                                num_warmup_steps=0,
                                                num_training_steps=len(train_dataloader) * num_epochs)

    train_model(model, train_dataloader, criterion, optimizer, scheduler, DEVICE)
