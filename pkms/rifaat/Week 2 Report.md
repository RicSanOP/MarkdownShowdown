# Week 2 Report

#### What I Did:
- **Reviewed and implemented the DETR model** using a ResNet-50 backbone for feature extraction.
- Added **positional encodings** and **object queries** to the Transformer architecture.
- Preprocessed the dataset to ensure it matches the input requirements for the model.

#### How I Did:
- Based on the DETR architecture documentation, I set up the ResNet-50 backbone with pretrained ImageNet weights for faster convergence during training.
- Carefully studied positional encodings to ensure they provided the correct spatial information for the Transformer, which was critical for global feature capture.

#### Snapshot:
![[Pasted image 20241006084955.png]]

#### Problems:
- Encountered dimension mismatch errors while integrating positional encodings with the Transformer model, leading to incorrect shape handling in the forward pass.

#### Resolution:
- After reviewing the encoding's implementation, I ensured the positional encodings matched the dimension of the flattened feature map before feeding them into the Transformer layers. This required reshaping the input tensor to align with the expected shape in the model.

