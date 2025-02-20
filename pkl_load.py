# import pickle
import torch

# with open('trained_model.pkl', 'rb') as f:
data = torch.load('trained_model.pkl', weights_only=False)
    #for index in 
entity_embeddings = data.entity_representations[0]
print(type(entity_embeddings))
entity_embedding_tensor = entity_embeddings(indices=None)
print(entity_embedding_tensor)
# print(vars(data.relation_representations).keys())

