# This script checks if CUDA is available and selects the appropriate device (GPU or CPU) for performing tensor operations with PyTorch.
# Additionally, it prints the selected device to the console.

import torch

def check_tensor_operations():
    """
    Checks the availability of CUDA and selects the appropriate device.

    Returns:
        torch.device: The selected device (GPU or CPU).
    """
    # Check if CUDA is available
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    
    return device