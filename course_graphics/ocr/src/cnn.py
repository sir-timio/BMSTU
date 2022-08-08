from torch import nn


class CNN(nn.Module):

    def __init__(self, config):
        """construct feature extraction cnn block with w_reduction
        and h_reduction

        Args:
            config (dict):
                out_features (int):  out_channels of last Conv2d
        """
        super(CNN, self).__init__()
        self.w_reduction = 8
        self.h_reduction = 16
        self.out_features = config.out_features
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),

            nn.Conv2d(16, 32, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),

            nn.Conv2d(32, 32, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2)),

            nn.Conv2d(32, 64, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),

            nn.Conv2d(64, 64, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),

            nn.Conv2d(64, 128, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2)),

            nn.Conv2d(128, 128, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),

            nn.Conv2d(128, 128, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 1)),

            nn.Conv2d(128, self.out_features, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(self.out_features),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2))
        )

    def forward(self, images):
        """pass forward CNN

        Args:
            images (torch.tensor): batch of images in shape of (bs, 1, w, h)
        Returns:
            torch.tensor: extracted features in shape (bs,
            self.out_features, w // w_reduction, h // h_reduction)
        """
        batch_size, channels, w, h = images.size()
        x = self.cnn(images)
        return x
