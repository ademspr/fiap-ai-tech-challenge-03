# FIAP AI Tech Challenge - Phase 3

Medical Assistant with fine-tuned model and RAG (Retrieval-Augmented Generation) using the PubMedQA dataset.

## Overview

This project implements a medical assistant that compares responses between:
- **Base Model**: Llama 3.2 3B without modifications
- **Fine-tuned Model**: Llama 3.2 3B trained with medical data + RAG

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [Ollama](https://ollama.ai/) installed and running
- [Google Colab](https://colab.research.google.com/) account (for notebooks)
- [Hugging Face](https://huggingface.co/) account with Llama 3.2 access

## Notebooks (Google Colab)

Notebooks must be run on Google Colab with GPU (A100 recommended).

### 1. Model Fine-tuning (`finetune_colab.ipynb`)

**Prerequisites:**
1. Create a Hugging Face account
2. Accept the [Llama 3.2 license terms](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)
3. Create an [access token](https://huggingface.co/settings/tokens) with read permission
4. Add the token to Colab Secrets with key `HF_TOKEN`

Trains the Llama 3.2 3B model with medical data from PubMedQA and save it to Google Drive at `/MyDrive/fiap-3-model/`. After execution, download `model.gguf` from Drive and place in `outputs/` then run the command bellow to create the model in Ollama:

```bash
ollama create fiap-3 -f Modelfile
```

### 2. VectorStore Generation (`vectorstore_colab.ipynb`)

Generates embeddings for ~211k PubMedQA documents and saves to chromaDB to allow sources references. Download the `chroma_db` folder from Google Drive at `/MyDrive/fiap-3-model/` and extract to `data/`

## Running the Project

Make sure Ollama is running and that models are available:

```bash
ollama serve

# Base model
ollama pull llama3.2:3b

# Fine-tuned model (after running the notebook)
ollama list | grep fiap-3
```

Then start the bot and open [http://localhost:8501](http://localhost:8501) in your browser:

```bash
docker compose up -d
```

## Test Users

The database is pre-populated with 5 patients and their medications:

| CPF         | Name            | Condition                       | Medications                                                                 |
|-------------|-----------------|---------------------------------|-----------------------------------------------------------------------------|
| 12345678901 | Maria Silva     | Diabetes, Hypertension          | Metformin 850mg, Losartan 50mg                                              |
| 23456789012 | João Santos     | Hypertension, High Cholesterol  | Atenolol 25mg, Simvastatin 20mg, Aspirin 100mg                              |
| 34567890123 | Ana Oliveira    | Anxiety                         | Escitalopram 10mg, Clonazepam 0.5mg                                         |
| 45678901234 | Carlos Ferreira | Diabetes, Hypertension, Thyroid | NPH Insulin 20UI, Regular Insulin 10UI, Enalapril 10mg, Levothyroxine 50mcg |
| 56789012345 | Beatriz Costa   | Migraine                        | Topiramate 25mg, Sumatriptan 50mg                                           |
