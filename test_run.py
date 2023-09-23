import torch
import os

from model import GarmentClassifier
from run import TrainConfig, Trainer
from dataset import training_loader

def training_fn(model, optimizer, loss_fn, data_slice):
    inputs, labels = data_slice
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = loss_fn(outputs, labels)
    loss.backward()
    optimizer.step()
    return loss.item()


config = TrainConfig(1, os.path.join('vol', 'checkpoint.tar'))
model = GarmentClassifier()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-5)
loss_fn = torch.nn.CrossEntropyLoss()

trainer = Trainer(model, optimizer, loss_fn, training_loader, training_fn, config)
trainer.run()