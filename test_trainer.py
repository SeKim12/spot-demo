import torch
import threading
import time

from model import GarmentClassifier
from dataset import training_loader
from trainer import Trainer, TrainConfig

def _training_fn(model, optimizer, loss_fn, data_slice):
    inputs, labels = data_slice
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = loss_fn(outputs, labels)
    loss.backward()
    optimizer.step()
    return loss.item()

class TestTrainer:
    def test_run(self, tmp_path):
        ckpt_dir = tmp_path / 'ckpt'
        ckpt_dir.mkdir()

        ckpt_path = ckpt_dir / 'checkpoint.tar'

        config = TrainConfig(1, str(ckpt_path))
        model = GarmentClassifier()
        optimizer = torch.optim.SGD(model.parameters(), lr=1e-5)
        loss_fn = torch.nn.CrossEntropyLoss()
        
        trainer = Trainer(model, optimizer, loss_fn, training_loader, _training_fn, config)
        trainer.run()

        assert ckpt_path.is_file()

    def test_sigterm(self, tmp_path):

        from trainer import _State 

        def _target():
            time.sleep(3)
            _State.handler()

        ckpt_dir = tmp_path / 'ckpt'
        ckpt_dir.mkdir()

        ckpt_path = ckpt_dir / 'checkpoint.tar'

        # give ample time for preemption
        config = TrainConfig(30, str(ckpt_path))
        model = GarmentClassifier()
        optimizer = torch.optim.SGD(model.parameters(), lr=1e-5)
        loss_fn = torch.nn.CrossEntropyLoss()

        trainer = Trainer(model, optimizer, loss_fn, training_loader, _training_fn, config)
        simulator = threading.Thread(target=_target, name='hallo')
        simulator.start()

        trainer.run()
        
        assert ckpt_path.is_file()


