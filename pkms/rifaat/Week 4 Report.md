# Week 4 Report

#### What I Did:
- **Completed training** on ResNet-50 and **started training** with ResNet-101 backbone to test deeper feature extraction capabilities.
- Conducted **evaluation on the COCO validation set** to calculate metrics such as **mAP** and **IoU**.
- Started benchmarking DETR’s performance against traditional models for comparison.

#### How I Did:
- Transferred the pretrained weights from the ResNet-50 model to the ResNet-101 backbone, leveraging transfer learning to accelerate training on the deeper architecture.
- Used COCO's evaluation scripts to generate detailed **precision-recall curves** and **IoU-based performance** metrics.

#### Snapshot:
![[Pasted image 20241006085047.png]]

#### Problems:
- The [[Convolutional Neural Network|ResNet-101]] model's higher memory requirements caused **GPU memory limitations**, especially when using larger batch sizes, resulting in out-of-memory errors during training.

#### Resolution:
- Reduced the batch size to fit within the available GPU memory and used **gradient accumulation** to compensate for the smaller batch size, maintaining training stability. Additionally, I optimized the data loader to prefetch smaller batches efficiently to reduce overhead.
