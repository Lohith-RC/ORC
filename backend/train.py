import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix
import os, json
import matplotlib.pyplot as plt
import seaborn as sns
from torchvision.models import VGG16_Weights, ResNet50_Weights, EfficientNet_B0_Weights, MobileNet_V2_Weights

# ✅ Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# ✅ Parameters
num_epochs = 100
batch_size = 16
lr = 1e-4
image_size = 224
num_classes = 2  # set as per your dataset (update this)
results_dir = "results_merged"
os.makedirs(results_dir, exist_ok=True)

# ✅ Transforms
transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ✅ Dataset paths
data_dir = r"D:\archive (1)\Oral cancer Dataset 2.0\data_split"  # Update to your dataset path
train_dir = os.path.join(data_dir, "train")
val_dir = os.path.join(data_dir, "val")
test_dir = os.path.join(data_dir, "test")

train_dataset = datasets.ImageFolder(train_dir, transform=transform)
val_dataset = datasets.ImageFolder(val_dir, transform=transform)
test_dataset = datasets.ImageFolder(test_dir, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

# ✅ Merged Model
class MergedNet(nn.Module):
    def __init__(self, num_classes):
        super(MergedNet, self).__init__()

        self.vgg16 = models.vgg16(weights=VGG16_Weights.IMAGENET1K_V1).features
        self.resnet = nn.Sequential(*list(models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1).children())[:-2])
        self.efficientnet = models.efficientnet_b0(weights=EfficientNet_B0_Weights.IMAGENET1K_V1).features
        self.mobilenet = models.mobilenet_v2(weights=MobileNet_V2_Weights.IMAGENET1K_V1).features

        # Freeze base models (optional)
        for model in [self.vgg16, self.resnet, self.efficientnet, self.mobilenet]:
            for param in model.parameters():
                param.requires_grad = False

        self.pool = nn.AdaptiveAvgPool2d((1, 1))

        # Output features from each model:
        # VGG16: 512, ResNet50: 2048, EfficientNet: 1280, MobileNet: 1280
        self.classifier = nn.Sequential(
            nn.Linear(512 + 2048 + 1280 + 1280, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        f1 = self.pool(self.vgg16(x)).view(x.size(0), -1)
        f2 = self.pool(self.resnet(x)).view(x.size(0), -1)
        f3 = self.pool(self.efficientnet(x)).view(x.size(0), -1)
        f4 = self.pool(self.mobilenet(x)).view(x.size(0), -1)

        merged = torch.cat([f1, f2, f3, f4], dim=1)
        return self.classifier(merged)

# ✅ Training Function
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs, device):
    model.to(device)
    best_acc = 0.0

    for epoch in range(num_epochs):
        model.train()
        running_loss, correct, total = 0.0, 0, 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels).item()
            total += labels.size(0)

        epoch_loss = running_loss / total
        epoch_acc = correct / total
        print(f"Epoch {epoch+1}/{num_epochs}: Loss={epoch_loss:.4f}, Acc={epoch_acc:.4f}")

        # Validation
        model.eval()
        val_correct, val_total = 0, 0
        with torch.no_grad():
            for val_inputs, val_labels in val_loader:
                val_inputs, val_labels = val_inputs.to(device), val_labels.to(device)
                val_outputs = model(val_inputs)
                _, val_preds = torch.max(val_outputs, 1)
                val_correct += torch.sum(val_preds == val_labels).item()
                val_total += val_labels.size(0)
        val_acc = val_correct / val_total
        print(f"Validation Accuracy: {val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), os.path.join(results_dir, "merged_model.pth"))

    return model

# ✅ Instantiate Model
model = MergedNet(num_classes=num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.classifier.parameters(), lr=lr)

# ✅ Train
print("🔁 Training Merged Model (VGG16 + ResNet + EfficientNet + MobileNet)...")
model = train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs, device)

# ✅ Evaluation
model.eval()
y_true, y_pred = [], []
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        y_true.extend(labels.cpu().numpy())
        y_pred.extend(preds.cpu().numpy())

# ✅ Report
report = classification_report(y_true, y_pred, target_names=test_dataset.classes, output_dict=True)
print(f"\n✅ Final Accuracy: {report['accuracy']:.4f}")

with open(os.path.join(results_dir, "metrics_merged.json"), "w") as f:
    json.dump(report, f, indent=4)

# ✅ Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=test_dataset.classes, yticklabels=test_dataset.classes)
plt.title("Confusion Matrix: Merged Model")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.savefig(os.path.join(results_dir, "confusion_matrix_merged.png"))
plt.close()
