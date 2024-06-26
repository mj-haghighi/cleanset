from enums import EXT
from configs.ConfigInterface import IConfig

class Config(IConfig):
    download_link = "https://github.com/mj-haghighi/mnist_png/raw/master/mnist.zip"
    filetype = EXT.ZIP
    datatype = EXT.PNG
    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    labels = list(range(10))
    mean = (0.1307,)
    std = (0.3081,)
    trainset='training/'
    validationset='testing/'
    testset='testing/'