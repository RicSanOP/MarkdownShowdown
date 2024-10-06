# Devlog

### Week 1 - Initial Setup and Dependency Management

**Task: Dependency Management and Environment Setup**

In the first week, my primary focus was getting the development environment up and running. After reviewing the project dependencies, it became clear that the version compatibility between **PyTorch**, **torchvision**, and the **COCO API** might be a pain point. My initial task was to ensure that all dependencies were correctly installed and working seamlessly.

I encountered version issues with the **COCO API**, specifically when attempting to load the dataset. The error message indicated that certain methods had been deprecated, which immediately pointed me to a potential version mismatch.

#### Solution:
To resolve this, I pinned the versions of the libraries in the `requirements.txt` file. This was crucial to avoid potential future compatibility issues. Below is the updated version of the `requirements.txt` file:

```plaintext
torch==1.5.0
torchvision==0.6.0
cython
pycocotools
```

Once the versions were aligned, I ran tests in a virtual environment (Conda) to verify the installation worked across multiple systems.

---

### Week 2 - Initial GPU Performance and Memory Usage

**Task: Optimizing GPU/CPU Usage**

As the project progressed, I shifted focus to monitoring GPU memory usage. Training a deep model like DETR on large datasets such as COCO can lead to substantial GPU memory overhead, especially when the **batch size** is large. The model’s architecture, which integrates both CNN and Transformer components, is memory-intensive.

I noticed a significant slowdown in training speed, accompanied by memory allocation errors. The GPU was being overwhelmed, causing out-of-memory (OOM) errors, especially with larger batches.

#### Solution:
I optimized the memory usage by experimenting with **smaller batch sizes**. Additionally, I enabled **mixed precision training** using PyTorch’s native AMP (Automatic Mixed Precision), which helped reduce the memory footprint by utilizing 16-bit floating-point precision. Here's how I implemented mixed precision training:

```python
# Mixed precision training with PyTorch AMP
scaler = torch.cuda.amp.GradScaler()

for data, targets in dataloader:
    optimizer.zero_grad()
    with torch.cuda.amp.autocast():
        outputs = model(data)
        loss = criterion(outputs, targets)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

This provided a significant improvement, allowing me to increase the batch size while maintaining memory efficiency.

---

### Week 3 - Debugging Data Loading Issues

**Task: Efficient Data Loading**

In Week 3, I turned my attention to optimizing **data loading** and pipeline efficiency. Initially, the data loading process was slow, which was bottlenecking training speed. I realized that **data augmentation** operations, such as random resizing and horizontal flipping, were being applied on the CPU during the training loop, significantly slowing down the overall process.

#### Solution:
I optimized the **`DataLoader`** by using multi-threaded data loading and moving as much of the preprocessing as possible to the GPU. PyTorch’s `DataLoader` has a `num_workers` argument, which I increased to parallelize the data loading process across multiple CPU cores.

```python
# Efficient data loading
dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=8,  # Utilize multiple cores for faster data loading
    pin_memory=True  # Pin memory to reduce transfer overhead between CPU and GPU
)
```

By increasing `num_workers`, I saw a noticeable boost in training speed. However, I had to balance this against GPU performance, as too many workers could lead to GPU starvation if not managed carefully.

---

### Week 4 - Bug Tracking and Issue Resolution

**Task: Bug Tracking & Issue Resolution**

By Week 4, I was focusing on debugging several minor issues that arose during training and inference. The model occasionally produced **NaN (Not-a-Number)** values in the loss function during training, especially when using large learning rates. This issue was difficult to track because it only occurred intermittently, which suggested that it was related to exploding gradients in the Transformer component.

#### Solution:
I implemented **gradient clipping** to prevent the gradients from becoming too large and destabilizing the training process. By capping the gradient values, I was able to prevent NaNs from appearing in the loss function:

```python
# Implementing gradient clipping to stabilize training
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.1)
```

After applying gradient clipping, the training became much more stable, and NaN values no longer appeared in the loss calculations. This allowed me to maintain a higher learning rate without destabilizing the training process.
