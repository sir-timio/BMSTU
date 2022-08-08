import editdistance
import numpy as np
from typing import Tuple


def index(array: np.ndarray, item: int) -> Tuple:
    """Find the first ndim index of item in array

    Args:
        array (np.ndarray)
        item (int): target item

    Returns:
        Tuple: ndim of item in array
    """
    for idx, val in np.ndenumerate(array):
        if val == item:
            return idx


class CERMetric():
    def __init__(self, blank_index=None):
        self.blank = blank_index
        self.char_counter = 0
        self.cer_accumulator = 0

    def update_state(self, y_true, y_pred):
        y_true = np.array(y_true, dtype=np.int64)
        y_pred = np.array(y_pred, dtype=np.int64)

        if not self.blank:
            self.blank = np.max(y_true)

        for gt, pred, in zip(y_true, y_pred):
            gt_i = index(gt, self.blank)[0]
            pred_i = index(pred, self.blank)[0]
            char_distance = editdistance.eval(
                tuple(gt[:gt_i]),
                tuple(pred[:pred_i])
            )
            self.char_counter += gt_i
            self.cer_accumulator += char_distance

    def result(self):
        return self.cer_accumulator / self.char_counter

    def reset_states(self):
        self.cer_accumulator = 0
        self.char_counter = 0


class WERMetric():
    def __init__(self, blank_index=None, space_index=1):
        self.space = space_index
        self.blank = blank_index
        self.word_counter = 0
        self.wer_accumulator = 0

    def update_state(self, y_true, y_pred):
        y_true = np.array(y_true, dtype=np.int64)
        y_pred = np.array(y_pred, dtype=np.int64)

        if not self.blank:
            self.blank = np.max(y_true)

        def get_words(sample, space=1):
            words = []
            start = -1
            for i in range(len(sample)):
                if sample[i] == space:
                    if start >= 0:
                        words.append(tuple(sample[start:i]))
                        start = -1
                elif start == -1:
                    start = i
            if start != -1:
                words.append(tuple(sample[start:]))
            return words

        for gt, pred, in zip(y_true, y_pred):
            gt_i = index(gt, self.blank)[0]
            pred_i = index(pred, self.blank)[0]
            gt = tuple(gt[:gt_i])
            pred = tuple(pred[:pred_i])
            gt_words = get_words(gt, self.space)
            pred_words = get_words(pred, self.space)
            word_distance = editdistance.eval(gt_words, pred_words)
            self.word_counter += len(gt_words)
            self.wer_accumulator += word_distance

    def result(self):
        return self.wer_accumulator / self.word_counter

    def reset_states(self):
        self.wer_accumulator = 0
        self.word_counter = 0


class SERMetric():
    def __init__(self, blank_index=None):
        self.blank = blank_index
        self.sentences_counter = 0
        self.ser_accumulator = 0

    def update_state(self, y_true, y_pred):
        y_true = np.array(y_true, dtype=np.int64)
        y_pred = np.array(y_pred, dtype=np.int64)

        if not self.blank:
            self.blank = np.max(y_true)

        for gt, pred, in zip(y_true, y_pred):
            gt_i = index(gt, self.blank)[0]
            pred_i = index(pred, self.blank)[0]
            self.sentences_counter += 1
            if gt_i != pred_i:
                self.ser_accumulator += 1
                continue
            for i in range(gt_i):
                if gt[i] != pred[i]:
                    self.ser_accumulator += 1
                    break

    def result(self):
        return self.ser_accumulator / self.sentences_counter

    def reset_states(self):
        self.ser_accumulator = 0
        self.sentences_counter = 0


def get_metrics(y_true, y_pred, space_index=1, blank_index=None):
    """
    take y_true and y_pred arrays of batches
    Both y_true and y_pred must have at least one padding
    blank index at the end
    return dict{
        'cer': list of values,
        'wer': list of values,
        'ser': list of values
    }
    """
    metrics = dict({
        'cer': CERMetric(blank_index=blank_index),
        'wer': WERMetric(blank_index=blank_index, space_index=space_index),
        'ser': SERMetric(blank_index=blank_index),
    })
    metrics_value = dict({
        'cer': [],
        'wer': [],
        'ser': [],
    })
    for gt, pred in zip(y_true, y_pred):
        for m in metrics.keys():
            metrics[m].update_state(gt, pred)
            metrics_value[m].append(metrics[m].result())
            metrics[m].reset_states()
    return metrics_value

import string
def get_metrics_from_str(gt_batches, pred_bathces, punc=False, case=False):

    table = str.maketrans(dict.fromkeys(string.punctuation))
    cer, wer, ser = [], [], []
    
    for gt, pred in zip(gt_batches, pred_bathces):
        for gt_label, pred_label in zip(gt, pred):
            if not punc:
                gt_label = str.translate(gt_label, table)
                pred_label = str.translate(pred_label, table)
            if not case:
                gt_label = gt_label.lower()
                pred_label = pred_label.lower()

            gt_label = gt_label.rstrip()
            pred_label = pred_label.rstrip()
            
            cer.append(editdistance.distance(gt_label, pred_label) / len(gt_label))
            wer.append(editdistance.distance(gt_label.split(), pred_label.split()) / len(gt_label.split()))
            ser.append(gt_label != pred_label)

    return [np.mean(cer), np.mean(wer), np.mean(ser)]