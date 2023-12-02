import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from transformers import get_cosine_schedule_with_warmup

from dataset import SatelliteDataset

def train_epoch(model, loader, criterion, optimizer, scheduler, device):
    model.train()

    total_loss = 0.0

    all_labels = []
    all_probas = []

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)

        all_labels.append(labels)
        all_probas.append(outputs.softmax(dim=-1))

        total_loss += loss.item()

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()

    all_labels = torch.cat(all_labels, dim=0)
    all_probas = torch.cat(all_probas, dim=0)

    metrics = {
        "Loss": total_loss / len(loader),
        "Accuracy": (all_probas.argmax(dim=-1) == all_labels).sum() / all_labels.shape[0]
    }

    return metrics


def eval_epoch(model, loader, criterion, device):
    model.eval()

    total_loss = 0.0

    all_labels = []
    all_probas = []

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            all_labels.append(labels)
            all_probas.append(outputs.softmax(dim=-1))

            total_loss += loss.item()

    all_labels = torch.cat(all_labels, dim=0)
    all_probas = torch.cat(all_probas, dim=0)

    metrics = {
        "Loss": total_loss / len(loader),
        "Accuracy": (all_probas.argmax(dim=-1) == all_labels).sum() / all_labels.shape[0]
    }

    return metrics


def train_model(model, train_dataloader, criterion, optimizer, scheduler, device):
    for epoch in range(10):
        train_metrics = train_epoch(model, train_dataloader, criterion, optimizer, scheduler, device)
        eval_metrics = eval_epoch(model, train_dataloader, criterion, device)

        print(train_metrics, eval_metrics)


if __name__ == "__main__":
    lr = 1e-3
    num_epochs = 10
    batch_size = 32
    DEVICE = "cuda"

    # model = torchvision.models.resnet50(torchvision.models.ResNet50_Weights)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        transforms.Resize(size=(256, 256)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(degrees=(5, 30))
    ])

    dataset = SatelliteDataset("data/labeled_shapshots_small")
    print(dataset[0])
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, lengths=[0.8, 0.2])

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr)
    scheduler = get_cosine_schedule_with_warmup(optimizer,
                                                num_warmup_steps=0,
                                                num_training_steps=len(train_dataloader) * num_epochs)

    train_model(model, train_dataloader, criterion, optimizer, scheduler, DEVICE)
