#mini-rag

This is the minimal implementation of a rag model for question answering over a collection of documents.

## Requirements

- python 3.10 or later

### Install Python using Miniconda (recommended)
1. Download Miniconda from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html) 

2. create a new environment using the following command: 

```bash
$ conda create -n mini-rag python=3.12
```

3. activate the environment using the following command:

```bash
$ conda activate mini-rag
```

## installation
### install required packages

```bash
$ pip install -r requirements.txt
```
### set up environment variables

1. copy the .env.example file to .env file: 
```bash
$ cp .env.example .env
```


## run fastapi server

```bash
$ uvicorn main:app --reload --host 0.0.0.0
```