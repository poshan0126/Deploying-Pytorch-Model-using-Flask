import torch
import io
from torch import nn
import torch.nn.functional as F
from torchvision import models
from PIL import Image
import torchvision.transforms as transforms
from collections import OrderedDict

# Loading a trained model
# TODO: Write a function that loads a checkpoint and rebuilds the model
def get_model(filepath):
    checkpoint = torch.load(filepath, map_location='cpu')
    model = models.densenet169(pretrained=False)
    for param in model.parameters():
        param.requires_grad = False
    
    num_features = 1664 # See the classifier part in the printed model above, it consist in_features=1664


    classifier = nn.Sequential(OrderedDict([
                              ('fc1', nn.Linear(num_features, 512)),
                              ('relu_1', nn.ReLU()),
                              ('drpot', nn.Dropout(p=0.5)),
                              ('hidden', nn.Linear(512, 100)),
                              ('relu_2', nn.ReLU()),
                              ('drpot_2', nn.Dropout(p=0.5)),
                              ('fc2', nn.Linear(100, 102)),
                              ('output', nn.LogSoftmax(dim=1)),
                              ]))

    model.classifier = classifier

    model.load_state_dict(checkpoint['state_dict'], strict=False)
    
    return model

def get_tensor(image_bytes):
    my_transforms = transforms.Compose([
        transforms.RandomRotation(30),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                            [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)