import argparse
import torch
import signal
import threading
import os

from dataset import training_loader
from model import GarmentClassifier

model = GarmentClassifier()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-5)
loss_fn = torch.nn.CrossEntropyLoss()

ckpt_path = os.path.join('vol', 'checkpoint.tar')

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--epochs', default=5)

    return parser.parse_args()

def atomic_train(data):
    inputs, labels = data
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = loss_fn(outputs, labels)
    loss.backward()
    optimizer.step()
    return loss.item()


def train_wrapper(epochs, lock: threading.RLock, state_cv: threading.Condition):
    preempted = False 
    for epoch in range(epochs):
        mean_loss_per_epoch = 0
        for i, data in enumerate(training_loader):
            cont = lock.acquire(blocking=False)
            if not cont:
                print('preempted, starting checkpoint save...')
                torch.save({
                    'epoch': epoch,
                    'index': i,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict()
                }, ckpt_path)
                print('finished checkpoint save')
                preempted = True 
                break
            lock.release()
            mean_loss_per_epoch += atomic_train(data)
        print(f'mean loss for epoch {epoch}: {mean_loss_per_epoch / len(training_loader)}')
    
    if not preempted:
        torch.save({
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict()
                }, ckpt_path)
        with state_cv:
            State.sigterm = True
            state_cv.notify()
        

class State:
    sigterm = False
    _cv = None 

    def setup(cv):
        State._cv = cv
        signal.signal(signal.SIGTERM, State.handler)

    def handler(*args):
        with State._cv:
            State.sigterm = True
            State._cv.notify()


if __name__ == '__main__':
    args = parse_args()
    epochs = args.epochs

    state_cv = threading.Condition()
    State.setup(state_cv)

    train_lock = threading.RLock()
    train_thread = threading.Thread(target=train_wrapper, args=[epochs, train_lock, state_cv])
    train_thread.start()
    with state_cv:
        while not State.sigterm:
            state_cv.wait()
    
    train_lock.acquire()