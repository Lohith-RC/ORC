import torch
import torch.nn as nn
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import torch.optim as optim

# ==========================================
# ADVANCED TRAINING SCRIPT FOR ORAL CANCER
# ==========================================
# This script is provided as a reference for training a highly accurate model.
# Requirements: PyTorch, Torchvision, Kaggle Oral Cancer Dataset.

def get_model(num_classes=2):
    """
    Creates an ensemble or a robust single model (EfficientNet-B4)
    EfficientNet is highly effective for medical imaging due to fine-grained feature extraction.
    """
    model = models.efficientnet_b4(weights=models.EfficientNet_B4_Weights.DEFAULT)
    
    # Freeze early layers
    for param in list(model.features.parameters())[:-10]:
        param.requires_grad = False
        
    # Replace classifier
    num_ftrs = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.5, inplace=True),
        nn.Linear(num_ftrs, 512),
        nn.ReLU(),
        nn.Dropout(p=0.3),
        nn.Linear(512, num_classes)
    )
    return model

def train_model():
    print("Initializing Training Pipeline...")
    
    # Hyperparameters
    batch_size = 32
    num_epochs = 25
    learning_rate = 1e-4
    
    # Data Augmentation & Normalization
    # Crucial for medical datasets to prevent overfitting and simulate clinical variations
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize((380, 380)), # EfficientNet-B4 native size
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation(20),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize((380, 380)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # NOTE: You must provide a path to a dataset structured like:
    # dataset/train/cancer/
    # dataset/train/non_cancer/
    data_dir = 'path_to_your_dataset' 
    
    try:
        image_datasets = {x: datasets.ImageFolder(f"{data_dir}/{x}", data_transforms[x]) for x in ['train', 'val']}
        dataloaders = {x: DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True, num_workers=4) for x in ['train', 'val']}
        dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
        print(f"Loaded {dataset_sizes['train']} training images and {dataset_sizes['val']} validation images.")
    except Exception as e:
        print("Dataset not found at 'path_to_your_dataset'. Please download the Kaggle dataset and update the path.")
        return

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = get_model(num_classes=2).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.classifier.parameters(), lr=learning_rate, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)

    best_acc = 0.0

    for epoch in range(num_epochs):
        print(f'Epoch {epoch}/{num_epochs - 1}')
        print('-' * 10)

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                torch.save(model.state_dict(), 'best_model.pth')

    print(f'Best val Acc: {best_acc:4f}')

if __name__ == '__main__':
    train_model()
