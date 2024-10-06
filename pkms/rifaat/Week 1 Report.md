# Week 1 Report

#### What I Did:
- **Downloaded and structured the COCO 2017 dataset** for training and validation.
- Implemented **basic data augmentations** such as random resizing and horizontal flipping to ensure model generalization.
- Integrated the COCO dataset loader using `torchvision.datasets.CocoDetection`.

#### How I Did:
- Followed COCO API and PyTorch’s documentation, ensuring correct folder structure and format.
- Augmentations were applied using PyTorch `transforms` to optimize preprocessing steps for the model.

#### Snapshot:
![[Pasted image 20241006085354.png]]

#### Problems:
- Faced issues with the version compatibility between the **COCO API** and PyTorch, causing data loading errors.

#### Resolution:
- I updated the `requirements.txt` file, adjusting the API versions for **COCO** and PyTorch, which resolved the compatibility issues. Additionally, I ran environment tests to ensure smooth integration with the COCO dataset.
