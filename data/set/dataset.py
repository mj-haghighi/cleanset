import torch
import pandas as pd
import os.path as osp
from PIL import Image
from utils import to_categorical
from configs import configs
from torch.utils.data import Dataset as TorchDataset

class GeneralDataset(TorchDataset):
    def __init__(self, dataset_name: str, label_column: str, phase: str, transform=None, data_filtering_policy=None):
        self.phase = phase
        self.dataset_name = dataset_name
        self.label_column = label_column
        self.dataset_config = configs[dataset_name]
        self.transform = transform
        self.filtering_policy = data_filtering_policy
        self.samples = self.__collect_samples()
        self.overide_getitem = None
        self.overide_len = None

    def __len__(self):
        if self.overide_len is not None:
            return self.overide_len()
        return self.dataset_length

    def __getitem__(self, idx):
        if self.overide_getitem is not None:
            return self.overide_getitem(self, idx)
        index, img_path, label = self.samples[idx]
        clabel = to_categorical.sample(label, self.dataset_config.labels)
        clabel = torch.Tensor(clabel)
        img = Image.open(img_path)

        if self.transform:
            img = self.transform(img)
        else:
            raise Exception('Transform must be set')

        return index, img, clabel

    def __collect_samples(self):
        dataset_info_path = osp.join(self.dataset_config.outdir, self.dataset_name, 'info.csv')
        df = pd.read_csv(dataset_info_path, index_col='index')
        df = df[df['phase'] == self.phase]

        if self.filtering_policy is not None:
            filter_out_samples = self.filtering_policy.filter_samples()
            print(f"Number of filtered samples: {len(filter_out_samples)}")
            print(f"Number of samples: {len(df)}")
            df = df[~df.index.isin(filter_out_samples.index)]
            print(f"Number of samples after filtering: {len(df)}")

        if self.label_column in df.columns:
            indices, paths, labels = df.index.values, df['path'], df[self.label_column]
            self.dataset_length = len(df)
            return list(zip(indices, paths, labels))
        else:
            raise Exception(f"label_column: {self.label_column} is not valid")
