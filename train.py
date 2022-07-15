
import argparse
import torch.nn as nn
from enums import PHASE
from model import models
from configs import configs
from torch.optim import Adam
from data.set import datasets
from metric import Cartography
from train.trainer import Trainer
from utils import download_dataset
from data.loader import collate_fns
from data.transforms import transforms
from torch.utils.data import DataLoader

def parse_args():
    parser = argparse.ArgumentParser(description='start training on dataet')
    parser.add_argument('--task', type=str, choices=['mnist', 'cfar100'], help='choose task')
    parser.add_argument('--epochs', type=int, default=20, help='max number of epochs')
    parser.add_argument('--batch_size', type=int, default=20, help='batch size')
    parser.add_argument('--lr', type=int, default=0.0001, help='learning rate')
    parser.add_argument('--device', type=str, default='cpu', choices=['cpu', 'cuda:1', 'cuda:2', 'cuda:3', 'cuda:4', 'cuda:5', 'cuda:6'], help='learning device')

    args = parser.parse_args()
    return args

def main(argv=None):
    args = parse_args()

    config = configs[args.task]
    download_dataset(args.task)
    t_taransfm, v_transfm = transforms[args.task]
    t_dataset = datasets[args.task](phase=PHASE.train, transform=t_taransfm)
    v_dataset = datasets[args.task](phase=PHASE.validation, transform=v_transfm)

    model = models[args.task]()
    optimizer = Adam(model.parameters(), lr=args.lr)
    error = nn.CrossEntropyLoss()
    metrics = [Cartography()]
    
    t_loader =  DataLoader(
        dataset=t_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        collate_fn=collate_fns[args.task]
    )
    
    v_loader =  DataLoader(
        dataset=v_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        collate_fn=collate_fns[args.task]
    )

    trainer = Trainer(
        model=model,
        error=error,
        device=args.device,
        t_loader=t_loader,
        v_loader=v_loader,
        optimizer=optimizer,
        num_epochs=args.epochs,
        metrics=metrics,
    )


    trainer.start()

if __name__ == "__main__":
    main()