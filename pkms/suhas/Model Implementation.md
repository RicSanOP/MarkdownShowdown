# Model Implementation

This architecture is implemented in the `models/detr.py` file, and each component is modularly defined for flexibility and extension.
1. **Backbone**: The model uses **ResNet-50** or **ResNet-101** as the backbone to extract image features. This is implemented using the `torchvision.models.resnet` module.   
2. **Transformer**: The core of the DETR architecture is the **Transformer encoder-decoder** model. Features from the backbone are flattened and passed through a series of **multi-head self-attention layers**.
3. **Positional Encoding**: Positional encodings are added to the input features to retain spatial information, as Transformers do not natively capture this.
4. **Object Queries**: The decoder operates on a fixed number of object queries (typically 100), which are learned embeddings that interact with the encoder’s output.
5. **Bounding Box Prediction**: Instead of generating object proposals, DETR predicts bounding boxes directly through **feed-forward networks** at the decoder output.
6. **Hungarian Matching Loss**: DETR uses a **bipartite matching loss** (Hungarian algorithm) to match predicted objects with ground truth, which includes both classification and bounding box regression losses.
7. **End-to-End Detection**: The model eliminates the need for hand-designed components like region proposals, relying entirely on the transformer for object detection.
