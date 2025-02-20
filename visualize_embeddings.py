import torch
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Sample PyTorch tensor, to be replaced with output from pykeen
torch.manual_seed(0) 
tensor = torch.randn(100, 50)
tensor_np = tensor.numpy()

# Perform t-SNE
tsne = TSNE(n_components=2, random_state=0, perplexity=30, n_iter=5000)
tensor_tsne = tsne.fit_transform(tensor_np)

# Plot results
plt.figure(figsize=(8, 6))
plt.scatter(tensor_tsne[:, 0], tensor_tsne[:, 1], c='blue', alpha=0.5)
plt.title('visualize PyTorch tensors with t-SNE')
plt.xlabel('t-SNE component 1')
plt.ylabel('t-SNE component 2')
plt.grid(True)
plt.show()
