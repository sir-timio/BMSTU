import torch

from ctcdecode import CTCBeamDecoder
from word_beam_search import WordBeamSearch


BEAM_WIDTH = 50

from configs.config import VOCAB, BLANK

NUM_TO_CHAR = dict()
for i, c in enumerate(VOCAB):
    NUM_TO_CHAR[i] = c
BLANK_ID = VOCAB.find(BLANK)

CHARS = VOCAB[:-1] #chars 
WORD_CHARS = VOCAB[21:-1]
with open('configs/corpus.txt', 'r') as f:
    CORPUS = f.read()

def _decode_sample(sample, blank_id=BLANK_ID, num_to_char=NUM_TO_CHAR):
    label = ''
    for i in sample:
        if i == blank_id:
            break
        label += num_to_char.get(i, '')
    return label
        

def decode(batch):
    return [_decode_sample(s) for s in batch]



### VANILLA BEAM SEARCH
beam_decoder = CTCBeamDecoder(
    list(VOCAB),
    model_path=None,
    alpha=0,
    beta=0,
    cutoff_top_n=40,
    cutoff_prob=1.0,
    beam_width=BEAM_WIDTH,
    num_processes=4,
    blank_id=BLANK_ID,
    log_probs_input=False
)

def beam_search_decode(batch):
    labels = []
    
    batch = torch.softmax(batch, 2)
    beam_results, _, _, out_lens = beam_decoder.decode(batch.moveaxis(0, 1))
    for i in range(len(beam_results)):
        sample  = beam_results[i][0][:out_lens[i][0]].numpy()
        label = _decode_sample(sample) 
        labels.append(label)
    return labels



### GREEDY SEARCH
def greedy_decode(batch):
    labels = []

    batch = batch.permute(1, 0, 2)
    batch = torch.softmax(batch, 2)
    batch = torch.argmax(batch, 2)
    batch = batch.detach().cpu().numpy()
    for sample in batch:
        sample = [sample[0]] + \
                [c for i, c in enumerate(sample[1:]) if c != sample[i]]
        sample = [s for s in sample if s != BLANK_ID]
        label = _decode_sample(sample)
        labels.append(label)
    return labels



### WORD BEAM SEARCH 
WBS_MODES = ['Words', 'Ngrams', 'NGramsForecast', 'NGramsForecastAndSample']

word_beam_search_decoders = dict()
for mode in WBS_MODES:
    word_beam_search_decoders[mode] = WordBeamSearch(25, mode, 0, 
                                                     CORPUS.encode('utf-8'), 
                                                     CHARS.encode('utf-8'), 
                                                     WORD_CHARS.encode('utf-8'))



def word_beam_search_decode(batch, mode='Words'):
    batch = torch.softmax(batch, 2)

    batch = [p.cpu().detach().numpy() for p in batch]
    labels = []

    decoder = word_beam_search_decoders.get(mode)
    if not decoder:
        raise Exception("unknown mode: " + mode) 

    beam_results = decoder.compute(batch)
    for sample in beam_results:
        label = _decode_sample(sample)
        labels.append(label)
    return labels

