import pandas as pd
import tiktoken
import torch
import os
import random

class HPP_DatasetLoader:
    """
    The sensory input system for the Hyper-Plasticity Protocol.
    Converts raw text/math into latent tensors for the Infant Core.
    """
    def __init__(self, vocab_size=50257, dim=512):
        self.enc = tiktoken.get_encoding("gpt2")
        self.vocab_size = vocab_size
        self.dim = dim
        # The embedding layer to convert Token ID -> Latent Tensor
        self.embedding = torch.nn.Embedding(vocab_size, dim)
        
    def load_math_batch(self, file_path, batch_size=4, max_length=32):
        """Loads a batch of math equations from a parquet file."""
        if not os.path.exists(file_path):
            print(f"[!] Math Dataset not found: {file_path}")
            return None, None
            
        print(f"      [Loader] Reading parquet: {file_path}")
        df = pd.read_parquet(file_path)
        col_name = df.columns[0]
        
        # Sample random rows
        samples = df.sample(batch_size)[col_name].tolist()
        print(f"      [Loader] Sampled {len(samples)} rows. Tokenizing...")
        
        return self._tokenize_and_embed(samples, max_length)

    def load_jailbreak_batch(self, file_path, batch_size=4, max_length=32):
        """Loads a batch of jailbreak vectors from the CSV file."""
        if not os.path.exists(file_path):
            print(f"[!] Jailbreak Dataset not found: {file_path}")
            return None, None, None
            
        print(f"      [Loader] Reading CSV: {file_path}")
        df = pd.read_csv(file_path)
        
        # Sample random rows
        samples = df.sample(batch_size)
        text_list = samples['text'].tolist()
        labels = samples['label'].tolist()
        
        print(f"      [Loader] Sampled {len(text_list)} vectors. Tokenizing...")
        tokens, latent = self._tokenize_and_embed(text_list, max_length)
        return tokens, latent, labels

    def load_text_batch(self, file_path, batch_size=4, max_length=32):
        """Loads a batch of text from a file efficiently."""
        if not os.path.exists(file_path):
            print(f"[!] File not found: {file_path}")
            return None, None
            
        print(f"      [Loader] Reading text: {file_path}")
        samples = []
        # We read a small random chunk to simulate streaming sensory input
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for _ in range(batch_size):
                import random
                # Jump to a random spot in the file
                f.seek(random.randint(0, file_size - 10000))
                # Read until we hit a newline to align, then grab the next chunk
                f.readline()
                chunk = f.read(2000) # grab a chunk of characters
                samples.append(chunk.strip()[:500]) # keep it reasonable
        
        print(f"      [Loader] Sampled {len(samples)} chunks. Tokenizing...")
        return self._tokenize_and_embed(samples, max_length)
        
    def _tokenize_and_embed(self, text_list, max_length):
        """
        Translates raw text into token IDs, then into the exact [Batch, Seq, Dim] 
        tensor structure required by the HPP Infant Core.
        """
        token_batch = []
        for text in text_list:
            # Handle list of dicts (like 'messages' column in some HF datasets)
            if isinstance(text, list):
                # Flatten the conversation into a single string for the "infant" to digest
                text = " ".join([f"{m['role']}: {m['content']}" for m in text])
            
            tokens = self.enc.encode(str(text), allowed_special="all")
            # Pad or truncate
            if len(tokens) < max_length:
                tokens = tokens + [self.enc.eot_token] * (max_length - len(tokens))
            else:
                tokens = tokens[:max_length]
            token_batch.append(tokens)
            
        # Convert to tensor: Shape [Batch, SeqLen]
        token_tensor = torch.tensor(token_batch, dtype=torch.long, device=self.embedding.weight.device)
        
        # Pass through embedding to get Latent Thought: Shape [Batch, SeqLen, Dim]
        # print(f"      [Loader] Embedding tokens (Max ID: {token_tensor.max().item()})...")
        latent_thought = self.embedding(token_tensor)
        
        # The HPP Core currently expects [SeqLen, Batch, Dim] for nn.TransformerEncoderLayer
        # So we permute it
        latent_thought = latent_thought.permute(1, 0, 2)
        
        # Return both the raw tokens (for loss calculation) and the embedded tensor
        return token_tensor, latent_thought

    def load_hf_batch(self, dataset_name, batch_size=4, max_length=32, text_col="text", label_col=None, data_dir=None):
        """
        HPP Local Bridge: Fetches batches from pre-cached JSONL files.
        Bypasses HF connection for maximum stability on Windows.
        """
        import json
        file_path = f"datasets/hf_local/{dataset_name}.jsonl"
        
        if not os.path.exists(file_path):
            print(f"[!] Local Dataset not found: {file_path}")
            return None, None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        samples = [json.loads(random.choice(lines)) for _ in range(batch_size)]
        
        if isinstance(text_col, list):
            text_list = ["\n".join([str(s[col]) for col in text_col]) for s in samples]
        else:
            text_list = [s[text_col] for s in samples]
            
        labels = [s[label_col] for s in samples] if label_col else None
        
        tokens, latent = self._tokenize_and_embed(text_list, max_length)
        
        if label_col:
            return tokens, latent, labels
        return tokens, latent

if __name__ == "__main__":
    print("[HPP DATASET] Initializing Sensory Input...")
    loader = HPP_DatasetLoader()
    
    # Test Math Parquet
    print("Loading Math...")
    tokens, tensor = loader.load_math_batch("datasets/toy_math_train-00000-of-00001.parquet")
    if tensor is not None:
        print(f"Math Tensor Shape: {tensor.shape}")
        
    # Test Story TXT
    print("Loading Story...")
    tokens, tensor = loader.load_text_batch("datasets/TinyStoriesV2-GPT4-valid.txt")
    if tensor is not None:
        print(f"Story Tensor Shape: {tensor.shape}")
