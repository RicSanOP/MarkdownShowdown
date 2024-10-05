# Transformer Encoder-Decoder

The Transformer is a key component of the DETR model. It processes image features extracted by the CNN and performs object detection by learning global relationships between objects and their surroundings.

#### **Components of the Transformer:**

1. **Transformer Encoder**:
   - The encoder receives the image features from the CNN backbone and processes them with **multi-head self-attention** layers and **feed-forward neural networks**.
   - **Positional encodings** are added to the input features to retain spatial information, as Transformers lack a sense of location.

2. **Transformer Decoder**:
   - The decoder uses **object queries**, which are learnable embeddings, to predict the locations and categories of objects. These queries interact with the output of the encoder through multi-head attention layers.
   - The decoder outputs predictions for bounding boxes and class labels.

#### **Key Components:**

- **Multi-head self-attention**: Allows the model to focus on different parts of the input at each layer.
- **Positional encoding**: Adds positional information to the otherwise order-invariant Transformer.
- **Feed-forward networks**: Used after self-attention to further process the representations.

#### **Code Example:**

The Transformer architecture is implemented in the `models/transformer.py` file of the DETR repository. Below is a simplified version of the Transformer class:

```python
import torch
from torch import nn

class Transformer(nn.Module):
    def __init__(self, d_model=256, nhead=8, num_encoder_layers=6, num_decoder_layers=6):
        super().__init__()
        # Encoder
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead),
            num_layers=num_encoder_layers
        )
        
        # Decoder
        self.decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(d_model=d_model, nhead=nhead),
            num_layers=num_decoder_layers
        )
    
    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        # Positional encodings should be added to src and tgt
        memory = self.encoder(src, src_mask)
        output = self.decoder(tgt, memory, tgt_mask)
        return output
```

#### **Positional Encoding:**
Positional encodings are added to the input to ensure the model retains information about the positions of features. This is critical for object detection where spatial relationships matter:

```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return x
```

#### **Object Queries:**

In DETR, object queries are learnable embeddings that interact with the Transformer decoder output. These queries are crucial for predicting object locations and classes.

```python
# Object queries initialized as learnable parameters
object_queries = nn.Embedding(100, d_model)  # 100 queries, each of dimension d_model
```
