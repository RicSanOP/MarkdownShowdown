# COCO Dataset

The COCO (Common Objects in Context) dataset is a large-scale image dataset designed for object detection, segmentation, keypoint detection, and captioning. It consists of over 200,000 labeled images and 80 object categories, with more than 1.5 million object instances. COCO is unique due to its focus on object detection in complex, cluttered scenes with multiple objects per image. The dataset also provides annotations for object segmentation, making it valuable for tasks like instance and panoptic segmentation. COCO is widely used for benchmarking machine learning models in object detection and segmentation.

## Data Preparation

1. **Dataset: COCO (Common Objects in Context)**
   - DETR is primarily trained on the COCO dataset, which contains images with labeled objects for object detection tasks.
   - **COCO 2017 Dataset**: Download and unzip the train and validation splits. The dataset can be found [here](https://cocodataset.org/#download).
2. **Dataset Structure**:
   - Images and annotations are separated into the following folders:
     - `train2017/`: contains training images.
     - `val2017/`: contains validation images.
     - `annotations/`: contains JSON files with corresponding annotations.
3. **Data Loading**:
   - Utilize **torchvision’s COCO dataset wrapper** for data loading:
     ```python
     from torchvision.datasets import CocoDetection
     dataset = CocoDetection(root='path/to/train2017', annFile='path/to/annotations/instances_train2017.json', transform=...)
     ```
   - This will automatically parse COCO images and annotations into a usable format for training.
4. **Data Augmentation and Preprocessing**:
   - DETR uses **random resizing** and **horizontal flipping** for data augmentation during training. You can find the augmentations in the `detr.datasets.transforms` module.
   - Example of applying augmentations:
     ```python
     from transforms import RandomResize, RandomHorizontalFlip
     transforms = [RandomResize([800], max_size=1333), RandomHorizontalFlip()]
     ```
5. **Handling Annotations**:
   - Ensure the annotations are loaded in the correct format using COCO's `loadAnns` method. COCO uses bounding boxes and segmentation masks, which are key for training DETR.
6. **Class and Label Mapping**:
   - Map COCO’s 80 classes to the corresponding object classes in the DETR model. This is handled automatically when using the `torchvision.datasets.CocoDetection`.
