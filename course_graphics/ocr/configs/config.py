from configs._dataclasses.ModelConfig import (
    ModelConfig,
    CNNConfig,
    RNNConfig
)
from configs._dataclasses.DatasetConfig import DatasetConfig

from src.cnn import CNN
from src.lstm import LSTM

# GENERAL
DEVICE = 'cpu'
SEED = 42
PROJECT_PATH = '/home/parallels/Desktop/Parallels Shared Folders/Home/course/ocr'

# DATASET
BLANK = '#'
VOCAB = " !(),-./0123456789:;?ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяё#"
DATASET_DIR = f'{PROJECT_PATH}/data/val'
ANN_PATH = f'{PROJECT_PATH}/data/val.csv'

MAX_LABEL_LEN = 44
BATCH_SIZE = 32
IMG_CHANNELS = 1
IMG_HEIGHT = 128
IMG_WIDTH = 1536
RESIZE_FACTOR = 2


# CNN
CNN_FEATURES = 256

# RNN
RNN_NUM_LAYERS = 2
RNN_DROPOUT = 0.2
# FROM CNN TO RNN
RNN_FEATURES = 512

# MODEL
RESIZED_IMG_SHAPE = [IMG_CHANNELS,
                     IMG_HEIGHT // RESIZE_FACTOR,
                     IMG_WIDTH // RESIZE_FACTOR]
# critical moment
VOCAB_LEN = len(VOCAB)
DROPOUT = 0.2
CNN = CNN
CNN_name = 'cnn_long'
RNN = LSTM
PARAMETERS = '4.5M'



model_config = ModelConfig(
    input_img_shape=RESIZED_IMG_SHAPE,
    vocab_len=VOCAB_LEN,
    dropout=DROPOUT,
    CNN = CNN,
    RNN = RNN,
    CNN_config=CNNConfig(CNN_FEATURES),
    RNN_config=RNNConfig(
        in_out_features=RNN_FEATURES,
        num_layers=RNN_NUM_LAYERS,
        dropout=RNN_DROPOUT
    )
)

dataset_config = DatasetConfig(
    device=DEVICE,
    ds_path=DATASET_DIR,
    ann_path=ANN_PATH,
    vocab=VOCAB,
    blank_symbol=BLANK,
    batch_size=BATCH_SIZE,
    max_len=MAX_LABEL_LEN,
    img_channels=IMG_CHANNELS,
    img_height=IMG_HEIGHT,
    img_width=IMG_WIDTH,
    resize_factor=RESIZE_FACTOR,
    seed=SEED
)
