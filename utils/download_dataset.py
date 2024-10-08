import os
import sys
import wget
import argparse
import os.path as osp
sys.path.append('.')

from configs import configs
from utils.extract import extract

def download_dataset(dataset_name: str, outdir=None):
    if dataset_name not in configs.keys():
        raise Exception("Unknown dataset '{}'".format(dataset_name))
    
    config = configs[dataset_name]
    outdir = osp.join(config.outdir, dataset_name) if outdir is None else outdir
    if osp.isdir(outdir):
        print("Dataset already exist in {}".format(osp.join(outdir)))
        return

    if not osp.isdir(outdir):
        os.makedirs(outdir, exist_ok=True)

    outpath = osp.join(outdir, dataset_name+"."+config.filetype)
    wget.download(url=config.download_link, out=outpath)
    extract(path=outpath, to=outdir, type=config.filetype)

    if config.reform:
        print("Reforming dataset")
        config.reform(reform_dir=outdir, data_dir = osp.join(outdir, config.raw_data_folder))

##: To use directly
def parse_args():
    parser = argparse.ArgumentParser(description='download dataset')
    parser.add_argument('--dataset', type=str, choices=['mnist', 'cifar10', 'cifar100', 'cifar10nag', 'cifar10nws'], help='choose dataset')

    args = parser.parse_args()
    return args

def main(argv=None):
    args = parse_args()
    download_dataset(dataset_name=args.dataset)

if __name__ == "__main__":    
    main()