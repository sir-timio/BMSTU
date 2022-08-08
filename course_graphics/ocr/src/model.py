import torch
from torch import nn



class CTCModel(nn.Module):
    def __init__(self, config):
        """construct CTC model based on CRNN

        Args:
            config (dataclass):
                vocab_len (int): length of vocabulary included UNK and blank
                input_img_shape (list): img shape (1, height, width)
                RNN_config (dataclass): config for LSTM block
                CNN_config (dataclass): config for CNN block
        """
        super(CTCModel, self).__init__()
        self.vocab_len = config.vocab_len
        self.blank_index = self.vocab_len - 1
        self.dropout = config.dropout


        self.cnn = config.CNN(config.CNN_config)
        self.cnn.eval()

        self.lstm = config.RNN(config.RNN_config)
        self.lstm.eval()

        self.input_img_shape = config.input_img_shape
        self.input_channels = self.input_img_shape[0]
        self.input_height = self.input_img_shape[1]
        self.input_width = self.input_img_shape[2]
        self.w_reduction = self.cnn.w_reduction
        self.h_reduction = self.cnn.h_reduction

        
        self.cnn_features = self.cnn.out_features * self.input_height // self.h_reduction
        self.lstm_features = self.lstm.features

        self.linear = nn.Sequential(
            nn.Linear(self.cnn_features, self.lstm_features),
            nn.Dropout(p=self.dropout)
        )

        self.output = nn.Linear(self.lstm_features, self.vocab_len)

        
    def forward(self, images):
        """pass forward model

        Args:
            images (torch.tensor): batch of images in shape of (bs, 1, h, w)


        Returns:
            x (torch.tensor): probability over timesteps model prediction
        """
        batch_size, c, h, w = images.size()
        x = self.cnn(images)

        x = x.permute(0, 3, 1, 2)
        _, new_w, f, new_h = x.shape

        x = torch.reshape(x, 
                          shape=(batch_size, new_w, new_h * f))
        x = self.linear(x)

        x = self.lstm(x)
        
        x = self.output(x)
        x = x.permute(1, 0, 2)

        return x


def count_model_parameters(model):
    total_params = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad: 
            continue
        param = parameter.numel()
        total_params+=param
    print(f"Total Trainable Params: {total_params:,}")
    return total_params


def cold_run():
    import sys, os
    sys.path.append('..')
    from configs import config as config
    model = CTCModel(config.model_config)
    img = torch.rand(4, *config.RESIZED_IMG_SHAPE)
    from src.engine import compute_loss
    cnn = model.cnn
    print(cnn(img).shape)
    x = model(img)
    loss = compute_loss(x, torch.rand(4, 40))
    print(f'loss: {loss}')
    count_model_parameters(model)
    print(x.shape)




if __name__ == '__main__':
    cold_run()