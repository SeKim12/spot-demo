import torch
import signal
import threading
import time 
import os
from collections import namedtuple

class _State:
    recv_sigterm = False
    end_train = False 
    _cv = None 

    def reset():
        _State.recv_sigterm = False
        _State.end_train = False
        _State._cv = None

    def setup(cv: threading.Condition):
        _State.reset()
        _State._cv = cv
        signal.signal(signal.SIGTERM, _State.handler)

    def handler(*args):
        with _State._cv:
            _State.recv_sigterm = True  # preempted 
            _State.end_train = True 
            _State._cv.notify()

TrainConfig = namedtuple('TrainConfig', ['epochs', 'ckpt_path'])

class Trainer:
    def __init__(self, model, optimizer, loss_fn, training_set, training_fn, config: TrainConfig):
        self._model = model
        self._optimizer = optimizer
        self._loss_fn = loss_fn

        self._training_set = training_set
        self._training_loader = torch.utils.data.DataLoader(training_set, batch_size=4, shuffle=False)
        
        self._training_fn = training_fn

        self._config = config

        self._state_cv = threading.Condition()
        _State.setup(self._state_cv)
        self._training_lock = threading.RLock()
        self._finish_ckpt_cv = threading.Condition()
    
    def resume(self):
        
        while not os.path.exists(self._config.ckpt_path):
            print(f'checkpoint file {self._config.ckpt_path} does not exist, waiting...')
            time.sleep(1)

        print(f'found checkpoint file, loading model from checkpoint...')

        ckpt = torch.load(self._config.ckpt_path)

        try:
            prev_epoch = ckpt['epoch']
            prev_index = ckpt['index']
        except KeyError:
            print(f'previous training ran to completion, exiting')
            return

        self._model.load_state_dict(ckpt['model_state_dict'])
        self._optimizer.load_state_dict(ckpt['optimizer_state_dict'])
        
        self._training_loader = torch.utils.data.Subset(self._training_set, range(prev_index + 1, len(self._training_set)))

        print(f'finished loading, start training from epoch {prev_epoch} and data index {prev_index}.')

        self.run(prev_epoch)

    def run(self, prev_epoch=0):
        t = threading.Thread(target=self._run, args=[prev_epoch])
        t.start()

        with self._state_cv:
            self._state_cv.wait_for(lambda: _State.end_train)

        if _State.recv_sigterm:
            # stop training thread from training further
            self._training_lock.acquire()
            with self._finish_ckpt_cv:
                print('waiting to finish checkpoint save...')
                self._finish_ckpt_cv.wait()
                print('done waiting')
    
    def _run(self, prev_epoch=0):
        preempted = False
        
        for epoch in range(prev_epoch, self._config.epochs):
            print(f'starting epoch {epoch} / {self._config.epochs}')
            for i, data in enumerate(self._training_loader):
                should_continue = self._training_lock.acquire(blocking=False)
                if not should_continue:
                    print('detected premption, starting checkpoint save...')
                    start = time.perf_counter()
                    torch.save({
                        'epoch': epoch,
                        'index': i,
                        'model_state_dict': self._model.state_dict(),
                        'optimizer_state_dict': self._optimizer.state_dict()
                    }, self._config.ckpt_path)
                    print(f'finished saving to {self._config.ckpt_path}')
                    end = time.perf_counter()
                    print(f'finished checkpoint save in {end - start:0.4f}s')
                    preempted = True
                    break
                self._training_lock.release()
                self._training_fn(self._model, self._optimizer, self._loss_fn, data)
            if preempted:
                break
        if not preempted:
            print('model ran to completion, exporting results...')
            start = time.perf_counter()
            torch.save({
                    'model_state_dict': self._model.state_dict(),
                    'optimizer_state_dict': self._optimizer.state_dict()
                }, self._config.ckpt_path)
            with self._state_cv:
                _State.end_train = True
                self._state_cv.notify()
        else:
            with self._finish_ckpt_cv:
                self._finish_ckpt_cv.notify()