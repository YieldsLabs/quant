import torch.nn as nn
import torch.nn.functional as F


class AutoEncoder(nn.Module):
    def __init__(self, feature_dim, latent_dim=32, embed_dim=128, num_heads=4, dropout_prob=0.2, use_attention=True):
        super(AutoEncoder, self).__init__()
        self.use_attention = use_attention

        self.encoder = nn.Sequential(
            nn.Linear(feature_dim, 256),
            nn.LayerNorm(256),
            nn.Tanh(),
            nn.Dropout(dropout_prob),
            nn.Linear(256, 128),
            nn.LayerNorm(128),
        )

        if use_attention:
            self.attention_encoder = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, dropout=dropout_prob)

        self.encoder_fc = nn.Linear(128, latent_dim)

        self.decoder_fc = nn.Linear(latent_dim, 128)

        if use_attention:
            self.attention_decoder = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, dropout=dropout_prob)

        self.decoder = nn.Sequential(
            nn.Linear(128, 256),
            nn.LayerNorm(256),
            nn.Tanh(),
            nn.Dropout(dropout_prob),
            nn.Linear(256, feature_dim),
            nn.Tanh(),
        )

        self.residual = nn.Linear(feature_dim, feature_dim)

    def forward(self, x):
        encoded = self.encoder(x)

        if self.use_attention:
            encoded = encoded.unsqueeze(1)
            attn_encoded, _ = self.attention_encoder(encoded, encoded, encoded)
            encoded = attn_encoded.squeeze(1)

        latent = self.encoder_fc(encoded)

        decoded = self.decoder_fc(latent)

        if self.use_attention:
            decoded = decoded.unsqueeze(1)
            attn_decoded, _ = self.attention_decoder(decoded, decoded, decoded)
            decoded = attn_decoded.squeeze(1)

        output = self.decoder(decoded)
        residual_output = self.residual(x)

        return output + residual_output

    def get_latent(self, x, normalize=True):
        encoded = self.encoder(x)

        if self.use_attention:
            encoded = encoded.unsqueeze(1)
            attn_encoded, _ = self.attention_encoder(encoded, encoded, encoded)
            encoded = attn_encoded.squeeze(1)

        latent = self.encoder_fc(encoded)

        if normalize:
            latent = F.normalize(latent, p=2, dim=1)

        return latent
