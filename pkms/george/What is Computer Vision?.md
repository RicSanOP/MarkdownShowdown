# What is Computer Vision?

Computer Vision is a subfield of Deep Learning and Artificial Intelligence where humans teach computers to see and interpret the world around them. While humans and animals naturally solve vision as a problem from a very young age, helping machines interpret and perceive their surroundings via vision remains a largely unsolved problem. Limited perception of the human vision along with the infinitely varying scenery of our dynamic world is what makes Machine Vision complex at its core.

## A brief history of Computer Vision

- **1956**: "Artificial Intelligence"
- **1959**: Neuropsychology: Discover vision is hierarchical
- **1960s**: First computer vision project (MIT summer project)
- **1970s**: "AI winter"
- **1990s**: Rudimentary neural networks
- **2001**: Face detection (Viola & Jones)
- **2012**: AlexNet (Krizhevsky et al.)
  - VGG, GoogLeNet, ResNet, SENet...

## Convolutional Neural Networks

Convolutional Neural Networks (CNNs) are the most popular type of computer vision model and are particularly effective for tasks such as image classification, object detection, and facial recognition. They are inspired by the biological processes in which the connectivity pattern between neurons resembles the organization of the animal visual cortex.

The architecture of a CNN typically includes multiple layers: convolutional layers, pooling layers, and fully connected layers. One of the key advantages of CNNs is their ability to learn and extract features directly from raw image data, eliminating the need for manual feature engineering. This capability, combined with their hierarchical structure, allows CNNs to capture complex patterns and relationships within images, making them a powerful tool in the field of computer vision.

## Encoder-Decoder Transformers

Transformers are a type of model architecture introduced by Vaswani et al. in 2017, designed primarily for natural language processing tasks. Unlike recurrent neural networks (RNNs), transformers do not process data sequentially, but instead handle it all at once, making them highly parallelizable and efficient. They are based on the concept of self-attention, which allows the model to weigh the importance of different words in a sentence when encoding or decoding information.

The core components of a transformer model include the encoder and decoder, each composed of stacked layers of multi-head self-attention and feed-forward neural networks. The self-attention mechanism enables the model to understand the context and dependencies between words, regardless of their distance in the sequence. This makes transformers particularly effective for tasks like machine translation, text summarization, and question answering.

## DETR

DETR, which stands for "Detection Transformer," is a novel approach to object detection introduced by Facebook AI Research in 2020. Unlike traditional object detection methods that rely on convolutional neural networks (CNNs) and region proposal networks, DETR leverages the transformer architecture to directly predict object bounding boxes and their corresponding class labels.

DETR treats object detection as a direct set prediction problem. It uses a transformer encoder-decoder architecture, where the encoder processes the entire image, and the decoder generates a fixed-size set of predictions. The model utilizes self-attention mechanisms to capture global context and cross-attention to focus on relevant image features. This approach simplifies the object detection pipeline by eliminating the need for hand-crafted components like anchor boxes and non-maximum suppression, making DETR an end-to-end trainable model.