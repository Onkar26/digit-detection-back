import torch
import sys
import base64
from PIL import Image
import torchvision.transforms as transforms
from io import BytesIO
import numpy as np
import torch.nn as nn
import os

# Hyper-parameters 
input_size = 784 # 28x28
hidden_size = 500 
num_classes = 10
num_epochs = 2
batch_size = 100
learning_rate = 0.001

class Model(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(Model, self).__init__()
        self.input_size = input_size
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(hidden_size, num_classes)  
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        # no activation and no softmax at the end
        return out

try:
    file_path = "image64.txt"

    with open(file_path, "r") as file:
        file_contents = file.read()

    # Your base64-encoded image string
    base64_image = file_contents

    os.remove(file_path)

    image_data = base64.b64decode(base64_image.split(',')[1])

    # Open the image from bytes
    image = Image.open(BytesIO(image_data))

    image = image.resize((28,28))

    image = image.convert('L')

    image.save("output.png")


    transform = transforms.ToTensor()
    image_tensor = transform(image)


    model = Model(input_size=784, hidden_size=500, num_classes=10)

    # Load the model
    model.load_state_dict(torch.load('mnist-model.pth'))

    with torch.no_grad():
        output = model(image_tensor.reshape(-1, 28*28))

    # Convert the output to a human-readable format
    predicted_class = output.argmax().item()

    print(predicted_class)

except Exception as e:
    print("An error occurred:", str(e))

