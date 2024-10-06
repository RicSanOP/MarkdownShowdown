# Week 3 Report

#### What I Did:
- Initiated **training of the DETR model with ResNet-50** backbone on the COCO dataset.
- Monitored **loss curves** and validation metrics to assess early training performance.
- Adjusted **hyperparameters** (learning rate and weight decay) based on observed convergence behavior.

#### How I Did:
- I used an initial learning rate of 1e-4, with weight decay to prevent overfitting. Based on training observations, I experimented with a **learning rate scheduler** and **early stopping criteria** to improve convergence stability.

#### Snapshot:
![[Pasted image 20241006085015.png]]

#### Problems:
- Noticed that the model was converging too quickly, potentially overfitting to early stages of training, with validation performance plateauing.

#### Resolution:
- Lowered the learning rate and introduced **gradient clipping** to stabilize the training process. Early stopping was used to prevent overfitting. I also increased the number of training epochs to allow for more robust convergence.
