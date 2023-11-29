import torch
import argparse
import os

from trainer import Trainer, TrainConfig
from model import GarmentClassifier
from dataset import training_set

# TODO: this is something a user would customize
def create_trainer_args():
    def atomic_train(model, optimizer, loss_fn, data_slice):
        inputs, labels = data_slice
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()
        return loss.item() 
    
    args = {'training_fn': atomic_train}
    args['model'] = GarmentClassifier()
    args['optimizer'] = torch.optim.SGD(args['model'].parameters(), lr=1e-5)
    args['loss_fn'] = torch.nn.CrossEntropyLoss()

    # set high epoch to simulate preemption
    args['config'] = TrainConfig(epochs=200, ckpt_path=os.path.join('vol', 'checkpoint.tar'))
    args['training_set'] = training_set

    return args

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', action='store_true')

    args = parser.parse_args()

    trainer = Trainer(**create_trainer_args())

    if args.resume:
        print('resuming training')
        trainer.resume()
    else:
        trainer.run()
