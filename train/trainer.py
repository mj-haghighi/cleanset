from torch.nn.functional import softmax
from typing import List
from metric.IMetric import IMetric
from .dynamics import Dynamics

class Trainer:
    def __init__(
        self,
        model,
        error,
        device,
        t_loader,
        v_loader,
        optimizer,
        num_epochs,
        metrics: List[IMetric]
        ) -> None:
        self.model = model
        self.error = error
        self.device = device
        self.metrics = metrics
        self.t_loader = t_loader
        self.v_loader = v_loader
        self.dynamics = Dynamics()
        self.optimizer = optimizer
        self.num_epochs = num_epochs

    def start(self):
        self.model.to(self.device)
        for epoch in range(self.num_epochs):
            self.dynamics.epoch = epoch
            self.dynamics.iteration = -1
            self.model.train()
            for idx, data, labels in self.t_loader:
                self.dynamics.iteration +=1
                self.optimizer.zero_grad()
                data = data.to(self.device)
                prediction_values = self.model(data) # (B, C)
                prediction_probs = softmax(prediction_values, dim=1) # (B, C)
                loss = self.error(prediction_probs, labels)
                self.dynamics.b_loss = loss.item()
                loss.backward()
                self.optimizer.step()
                
                for metric in self.metrics:
                    metric.calculate(self.dynamics, prediction_probs, labels, idx)
            print('loss: {:.4f}: '.format(self.dynamics.loss))                
            