# DETR

DETR, which stands for "Detection Transformer," is a novel approach to object detection introduced by Facebook AI Research in 2020. Unlike traditional object detection methods that rely on convolutional neural networks ([[CNN]]) and region proposal networks, DETR leverages the [[Transformers]] architecture to directly predict object bounding boxes and their corresponding class labels.

![[Pasted image 20241006020017.png]]

DETR treats object detection as a direct set prediction problem. It uses a transformer encoder-decoder architecture, where the encoder processes the entire image, and the decoder generates a fixed-size set of predictions. The model utilizes self-attention mechanisms to capture global context and cross-attention to focus on relevant image features. This approach simplifies the object detection pipeline by eliminating the need for hand-crafted components like anchor boxes and non-maximum suppression, making DETR an end-to-end trainable model.

