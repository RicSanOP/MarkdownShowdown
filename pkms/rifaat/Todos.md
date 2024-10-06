# Todos


- [ ] **Data Preparation:**
  - [x] Downloaded the [[COCO Dataset]] (train and validation splits).
  - [x] Preprocessed and structured the dataset.
  - [x] Implemented basic data augmentations (random resizing, flipping).
  - [x] Integrated dataset loading via `torchvision.datasets.CocoDetection`.
  - [ ] Experiment with additional augmentation techniques (cropping, scaling).
- [x] **Model Implementation:**
  - [x] Reviewed the [[Detection Transformer Model Architecture]].
  - [x] Fine-tuned the model architecture with ResNet-50 [[Convolutional Neural Network]].
  - [x] Integrated positional encodings and object queries into the model.
- [ ] **Model Training:**
  - [x] Train [[Detection Transformer Model Architecture|DETR]] on [[COCO Dataset||COCO]] with ResNet-50 and ResNet-101.
  - [ ] Fine-tune hyperparameters (learning rate, weight decay) for optimal performance.
  - [ ] Monitor training progress (loss curves, validation accuracy).
  - [ ] Perform transfer learning using pretrained weights.
- [ ] **Evaluation and Testing:**
  - [x] Evaluate trained models on the COCO validation set.
  - [ ] Benchmark performance (mAP, IoU) against other object detection models.
  - [ ] Analyze false positives and negatives to further fine-tune the model.
