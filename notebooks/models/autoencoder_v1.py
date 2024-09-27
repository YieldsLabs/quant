import torch.nn as nn
import torch.nn.functional as F

class AutoEncoder(nn.Module):
    def __init__(self, feature_dim, latent_dim=32, dropout_prob=0.2):
        super(AutoEncoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(feature_dim, 128),
            nn.BatchNorm1d(128),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Dropout(dropout_prob),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(64, latent_dim)
        )

        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.BatchNorm1d(64),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Dropout(dropout_prob),
            nn.Linear(64, 128),
            nn.BatchNorm1d(128),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(128, feature_dim),
            nn.Tanh()
        )

        self.residual = nn.Linear(feature_dim, feature_dim)

    def forward(self, x):
        encoded = self.encoder(x)

        decoded = self.decoder(encoded)

        residual_output = self.residual(x)

        output = decoded + residual_output

        return output

    def get_latent(self, x, normalize=True):
        latent = self.encoder(x)

        if normalize:
            latent = F.normalize(latent, p=2, dim=1)

        return latent