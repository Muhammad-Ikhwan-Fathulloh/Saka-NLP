import json
import os
from typing import List, Dict, Any
from huggingface_hub import HfApi, login

HF_TOKEN = os.environ.get("HF_TOKEN")
REPO_ID = "Muhammad-Ikhwan-Fathulloh/Saka-Eval"

def upload_to_hf():
    """Uploads the generated data and README to HuggingFace Datasets."""
    print(f"Authenticating with token...")
    login(token=HF_TOKEN)
    
    api = HfApi()
    
    # 1. Create Repository if it doesn't exist
    try:
        api.create_repo(repo_id=REPO_ID, repo_type="dataset", exist_ok=True)
        print(f"Repository {REPO_ID} is ready.")
    except Exception as e:
        print(f"Error creating repo: {e}")

    # 2. Upload Dataset README (with configs to fix schema mismatch)
    readme_path = "DATASET_README.md"
    if os.path.exists(readme_path):
        print(f"Uploading {readme_path} as README.md...")
        api.upload_file(
            path_or_fileobj=readme_path,
            path_in_repo="README.md",
            repo_id=REPO_ID,
            repo_type="dataset"
        )
    else:
        print(f"Warning: {readme_path} not found, skipping README upload.")

    # 3. Upload Data Files
    files_to_upload = {
        "data/saka_sentiment_eval.jsonl": "sentiment/saka_sentiment_eval.jsonl",
        "data/saka_ner_eval.jsonl": "ner/saka_ner_eval.jsonl"
    }
    
    for local_path, repo_path in files_to_upload.items():
        if os.path.exists(local_path):
            print(f"Uploading {local_path} -> {repo_path}...")
            api.upload_file(
                path_or_fileobj=local_path,
                path_in_repo=repo_path,
                repo_id=REPO_ID,
                repo_type="dataset"
            )
        else:
            print(f"Warning: {local_path} not found, skipping.")

    print("Upload complete!")

if __name__ == "__main__":
    upload_to_hf()
