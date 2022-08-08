from torch.utils.data import Dataset, DataLoader, Subset
import torch
import numpy as np
import pandas as pd

from dataclasses import dataclass

import os
import cv2
import json


from collections import namedtuple
Sample = namedtuple('Sample', 'label, path')



class OCRDataset(Dataset):
    def __init__(self, config: dataclass):
        """Init torch dataset

        Args:
            config (dataclass): see app/configs/_dataclasses
        """
        super(OCRDataset, self).__init__()
        self.config = config
        self.device = config.device
        self.ds_path = config.ds_path
        self.ann_path = config.ann_path
        self.vocab = config.vocab
        self.blank_symbol = config.blank_symbol
        
        self._set_mapping()

        self.batch_size = config.batch_size
        self.shuffle = config.shuffle
        self.num_workers = config.num_workers

        self.max_len = config.max_len

        self.channels = config.img_channels
        self.height = config.img_height
        self.width = config.img_width
        self.resize_factor = config.resize_factor
        self.max_ratio = config.max_ratio
        self.t_h = int(self.height / self.resize_factor)
        self.t_w = int(self.width / self.resize_factor)

        np.random.seed = config.seed

        self.samples = self._read_data()


    def _set_mapping(self):
        """ makes encoder and decoder for labels

            Returns:
            None
        """
        self.char_to_num = dict()
        self.num_to_char = dict()
        for i, c in enumerate(self.vocab):
            self.num_to_char[i] = c
            self.char_to_num[c] = i

        self.blank_index = self.char_to_num[self.blank_symbol]
        self.space_index = self.char_to_num[' ']

    def get_train_val_loaders(self, batch_size=None):
        """create train valid Dataloaders

        Returns:
            list of Dataloaders: [train_loader, val_loader]
        """
        if batch_size is None:
            batch_size = self.batch_size

        datasets = {}
        datasets['train'] = Subset(self, self.train_idx)
        datasets['val'] = Subset(self, self.val_idx)
        return [DataLoader(ds, batch_size=batch_size,
                           shuffle=self.shuffle, num_workers=self.num_workers)
                for ds in datasets.values()]

    def _read_data(self):
        samples = []
        self.train_idx = []
        self.val_idx = []
        self.test_idx = []
        """make list of samples with fields label, path, h, w, label_len

        Returns:
            [Sample]: list of samples
        """
        ann = pd.read_csv(self.ann_path)
        # don't change to "i, row" cause skip some with bad ratio
        # maybe fix with pd.series
        i = 0
        for _, row in ann.iterrows():

            if row['part'] == 'train':
                self.train_idx.append(i)
            elif row['part'] == 'val':
                self.val_idx.append(i)
            else:
                self.test_idx.append(i)

            samples.append(Sample(
                label=row['label'],
                path=os.path.join(self.ds_path, row['path']),
            ))
            i += 1
        return samples

    def __len__(self):
        """len of Dataset

        Returns:
            int: len(samples)
        """
        return len(self.samples)

    def read_sample_img(self, i):
        img_path = self.samples[i].path
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        return np.array(img, dtype=np.float)


    def resize_img_keep_aspect(self, img, height=None, width=None, ratio=None):
        h, w = img.shape
        dim = None
        if ratio:
            dim = (w // ratio, h // ratio)
        elif width and height:
            dim = (width, height)
        elif height:
            r = height / float(h)
            dim = (int(w * r), height)
        elif width:
            r = width / float(w)
            dim = (width, int(h * r))
        else:
            dim = (w // self.resize_factor, h // self.resize_factor)
        return cv2.resize(img, dim, cv2.INTER_AREA)


    def normalize_img(self, img):
        img /= 255
        img -= 0.5
        return img

    def pad_label(self, label):
        return np.pad(
            np.vectorize(self.char_to_num.get)(list(label)),
            (0, self.max_len - len(label)),
            mode='constant', constant_values=self.blank_index
        )

    def __getitem__(self, i):
        """get one item by index, read img
        and make compatible with pytorch
        (channel, height, width), encode pad label with blank

        Args:
            i (int): index of sample

        Returns:
            dict: {
                'images': torch.tensor(dtype=torch.float),
                'labels': torch.tensor(dtype=torch.float)
            }
        """

        img = self.read_sample_img(i)
        img = self.resize_img_keep_aspect(img, height=self.t_h, width=self.t_w)
        img = self.normalize_img(img)
        img = np.expand_dims(img, axis=0)

        label = self.pad_label(self.samples[i].label)

        return {
            'images': torch.tensor(img, dtype=torch.float).to(self.device),
            'labels': torch.tensor(label, dtype=torch.float).to(self.device)
        }
