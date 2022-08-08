from dataclasses import dataclass
from typing import List, Any
import torch

@dataclass
class ModelConfig:
    input_img_shape: List
    vocab_len: int
    CNN: torch.nn.Module
    RNN: torch.nn.Module
    CNN_config: dataclass
    RNN_config: dataclass
    dropout: float = 0.2


@dataclass
class CNNConfig:
    out_features: int


@dataclass
class RNNConfig:
    in_out_features: int
    num_layers: int
    dropout: float
