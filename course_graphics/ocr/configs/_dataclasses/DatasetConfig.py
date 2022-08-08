from dataclasses import dataclass


@dataclass
class DatasetConfig:
    device: str
    ds_path: str
    ann_path: str
    vocab: str
    blank_symbol: str
    batch_size: int
    max_len: int
    img_channels: int
    img_height: int
    img_width: int
    resize_factor: int
    img_folder: str = ''
    shuffle: bool = True
    num_workers: int = 0
    max_ratio: float = None
    need_preproc: bool = False
    seed: int = 42
