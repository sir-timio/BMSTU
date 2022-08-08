from tqdm import tqdm
import torch
from torch.nn import functional as F
import numpy as np


def compute_loss(preds, labels):
    """compute ctc loss

    Args:
        preds (torch.tensor): probability over timesteps prediction
        labels (torch.tensor): gt texts

    Returns:
        float: ctc loss
    """
    blank_index = preds[0].shape[-1] - 1
    loss_fn = torch.nn.CTCLoss(
        blank=blank_index, zero_infinity=False, reduction='mean'
    )
    batch_size = labels.shape[0]
    log_probs = F.log_softmax(preds, 2)
    input_lengths = torch.full(
        size=(batch_size,), fill_value=log_probs.size(0), dtype=torch.int32
    )
    target_lengths = torch.tensor(
        [torch.sum(s != blank_index) for s in labels]
    )
    loss = loss_fn(
        log_probs, labels, input_lengths, target_lengths
    )
    return loss


def train_fn(model, data_loader, optimizer, train_frac):
    """calc loss and optim step over dataloader

    Args:
        model (torch.nn.Module): trainable model
        data_loader (torch.utils.data.Dataloader): dataloader
        optimizer (torch.optim): optimizer of loss func

    Returns:
        float: total loss on dataloader
    """
    model.train()
    total_loss = 0
    tk = tqdm(data_loader, total=len(data_loader))
    for data in tk:
        if np.random.rand() > train_frac:
            continue
        optimizer.zero_grad()
        preds = model(data['images'])
        loss = compute_loss(preds, data['labels'])
        loss.backward()
        optimizer.step()

        tk.set_description('loss: ' + str(loss.item()))

        total_loss += loss.item()

    return total_loss / len(data_loader)


def eval_fn(model, data_loader):
    """evaluate model with dataloader

    Args:
        model (torch.nn.Module): model
        data_loader (torch.utils.data.Dataloader): dataloader

    Returns:
        [
            torch.tensor: gt_labels in dataloader,
            torch.tensor: prediction matricies with probabilities over
            timesteps in dataloader,
            float: total loss on dataloader
        ]
    """
    model.eval()
    total_loss = 0
    total_preds = []
    total_gt = []

    tk = tqdm(data_loader, total=len(data_loader))
    for data in tk:
        with torch.no_grad():
            preds = model(data['images'])
            loss = compute_loss(preds, data['labels'])
            total_loss += loss.item()

            total_preds.append(preds)
            total_gt.append(data['labels'])

    return total_gt, total_preds, total_loss / len(data_loader)
