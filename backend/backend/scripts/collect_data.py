from dataloader import DataLoader

import os
import yaml


with open(os.getenv("CONFIG_PATH"), 'r') as cfg:
    conf_dict = yaml.safe_load(cfg)
    
    if 'dataset_path' in conf_dict:
        DATASET_PATH = conf_dict['dataset_path']

    if 'embedding_model_name' in conf_dict:
        EMBEDDING_MODEL_NAME = conf_dict['embedding_model_name']


loader = DataLoader(os.getenv("DATA_PATH"), DATASET_PATH, EMBEDDING_MODEL_NAME)

loader.load()