import json
import torch
import argparse
import numpy as np
import pandas as pd
import transformers

from utils import *
from tqdm import tqdm
from datasets import load_dataset
from os import path, makedirs, getenv
from huggingface_hub import login as hf_login


#-----------------------
# Main Function
#-----------------------
def main():
    
    #-------------------
    # parameters
    #-------------------    
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_id', type=str, default='meta-llama/Llama-3.1-8B-Instruct')
    parser.add_argument('--dataset', type=str, default='beanham/spatial_join')
    parser.add_argument('--finetuned', type=str, default='True')
    parser.add_argument('--use_model_prompt_defaults', type=str, default='llama3')
    args = parser.parse_args()
    
    args.suffix = MODEL_SUFFIXES[args.use_model_prompt_defaults]
    args.model_path = MODEL_PATHS[args.use_model_prompt_defaults]
    args.save_path=f'inference_results/'
    if not path.exists(args.save_path):
        makedirs(args.save_path)
    
    hf_login()    
        
    # ----------------------
    # Load Data
    # ----------------------
    print('Downloading and preparing data...')
    data = get_dataset_slices(args.dataset)
    test = data['test']
    
    #-----------------------
    # load model & tokenizer
    #-----------------------
    print('Getting model and tokenizer...')
    model, tokenizer = get_model_and_tokenizer(args.model_id,
                                               gradient_checkpointing=False,
                                               quantization_type='4bit',
                                               device='auto')
    if args.finetuned=='True':
        model = PeftModel.from_pretrained(model, args.model_path)

    #------------
    # inference
    #------------
    model.eval()
    model_outputs  = evaluate_model(model=model,
                                    tokenizer=tokenizer,
                                    data=test,
                                    max_new_tokens=5,
                                    remove_suffix=args.suffix)
    np.save(args.save_path+f"{args.use_model_prompt_defaults}_finetuned_{args.finetuned}.npy", model_outputs)

if __name__ == "__main__":
    main()
