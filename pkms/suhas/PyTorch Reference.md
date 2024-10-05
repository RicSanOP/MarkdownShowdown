# PyTorch Reference

Here’s a condensed reference to **PyTorch** for working on the DETR project:
### **1. Tensors**
   - PyTorch’s core data structure is the **Tensor**, similar to NumPy arrays but optimized for GPUs.
   ```python
   import torch
   x = torch.tensor([1.0, 2.0])
   ```

### **2. Autograd**
   - PyTorch automatically computes gradients for backpropagation using **autograd**.
   ```python
   x.requires_grad = True
   y = x * 2
   y.backward()
   ```

### **3. Modules & Models**
   - Models are created using the **`torch.nn.Module`** class. This is where layers and forward pass logic are defined.
   ```python
   class MyModel(nn.Module):
       def __init__(self):
           super(MyModel, self).__init__()
           self.fc = nn.Linear(10, 5)
       
       def forward(self, x):
           return self.fc(x)
   ```

### **4. Optimizers**
   - PyTorch provides optimizers like SGD, Adam, etc., for updating model parameters.
   ```python
   optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
   optimizer.step()
   ```

### **5. Datasets & DataLoaders**
   - The **`torch.utils.data.DataLoader`** class is used to load datasets and handle batching.
   ```python
   from torch.utils.data import DataLoader
   dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
   ```

### **6. Training Loop**
   - A typical PyTorch training loop includes:
     1. Forward pass
     2. Loss computation
     3. Backward pass
     4. Optimizer step
``
```python
for data, targets in dataloader:
       outputs = model(data)
       loss = criterion(outputs, targets)
       loss.backward()
       optimizer.step()
       optimizer.zero_grad()
```

### **7. GPU/CPU Switching**
   - Models and data can be transferred between CPU and GPU using `to()`:
```python
   device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
   model.to(device)
```

### **8. Saving and Loading Models**
   - Models are saved and loaded using `torch.save` and `torch.load`.
```python
   torch.save(model.state_dict(), "model.pth")
   model.load_state_dict(torch.load("model.pth"))
```

These concepts will help you efficiently work on DETR and manage its deep learning components.
