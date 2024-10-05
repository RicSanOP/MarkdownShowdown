# Dependency Management

1. **Primary Dependencies:**
   - **PyTorch 1.5+**: Core deep learning framework used for model implementation and training.
   - **torchvision 0.6+**: For handling datasets and model architectures.
   - **pycocotools**: Required for evaluating the model on the COCO dataset.
   - **scipy**: Used for various scientific computations during model training.
2. **Managing Dependencies:**
   - **Conda environment**: Recommended for creating isolated environments and managing Python dependencies.
   - **Install Command**: 
     ```bash
     conda install -c pytorch pytorch torchvision
     conda install cython scipy
     pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
     ```
3. **Optional Dependencies:**
   - **Panoptic API**: Required for panoptic segmentation tasks. Install with:
     ```bash
     pip install git+https://github.com/cocodataset/panopticapi.git
     ```
4. **Dependency Updates:**
   - Regularly check for updates to PyTorch, torchvision, and other packages to ensure compatibility.
   - Maintain a `requirements.txt` file for version tracking.

Managing dependencies with a clear installation process and environment management via Conda will minimize issues with mismatched versions and simplify collaboration.