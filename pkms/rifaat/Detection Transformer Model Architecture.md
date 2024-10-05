# Detection Transformer Model Architecture


### **Summary of Workflow:**
1. The CNN extracts features from the image.
2. Positional encodings are added to the feature map.
3. The Transformer encoder processes these features, capturing global relationships.
4. Object queries are fed into the decoder, which outputs object predictions (bounding boxes and class labels).

By combining the CNN backbone, positional encodings, and Transformer encoder-decoder structure, DETR can efficiently perform end-to-end object detection.