# Data Days For Good Deeds Transcriptions

## Introduction

The Hampden County Registry of Deeds holds a vast collection of historical records dating back to the early 1600s. With approximately 100,000 documents spread across 600 books (each containing around 1,000 documents), these records provide invaluable insights into property ownership, land transactions, and historical boundaries. However, due to the handwritten cursive nature of the documents, inconsistent document delineation, and the lack of a comprehensive indexing system, accessing specific records remains a challenge.

The primary objective of this project is to create a pipeline to digitize and systematically index these historical records to facilitate efficient search and retrieval. This includes:

- **Extracting Key Information**: Identifying grantors, grantees, property descriptions, and geographical references (city, county, streets, NWSE directions).
- **Standardizing Metadata**: Ensuring documents are properly categorized (e.g., deeds, easements, mortgages, liens, plan cards).
- **Improving Searchability**: Creating an indexed system that allows for title searches, boundary dispute research, and historical property ownership tracing.
- **Enhancing Accessibility**: Providing structured access to documents for researchers, legal professionals, and genealogy enthusiasts.

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Model Training & Evaluation](#model-training--evaluation)
- [Using the API](#using-the-api)
- [Streamlit Feature](#streamlit-feature)
- [How to Continue](#how-to-continue)

## Installation

To set up the project locally, follow these steps:

1. **Prerequisites**:
   - Python 3.x
   - Jupyter Notebook (for running `.ipynb` files)
   - Access to Boston University’s Shared Computing Cluster (for data)

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Configure API Credentials**:
  - Obtain an Anthropic Claude API key and set it in Claude-pipeline.ipynb
  - Set up Google Cloud credentials for Document AI and configure them in Google-pipeline.ipynb


## Project Structure


* .github/
* Data/
  * raw/
  * processed/
* Jupyter-Notebooks/
  * microsoft-text-generator.ipynb
  * Claude-pipeline.ipynb
  * Google-pipeline.ipynb
  * direct.ipynb
  * search.ipynb
* Scripts/
  * Transcriptcompare.py
  * app.py
* requirements.txt
* README.md


- **`Claude-pipeline.ipynb`**  
  Automates the digitization of historical deed documents (1720–1780) using the Anthropic Claude API. It converts TIF images to base64-encoded PNGs, sends them to Claude with a prompt, and extracts structured data (e.g., grantor, grantee, address) into JSON.

- **`Google-pipeline.ipynb`**  
  Processes TIF images of historical deeds (1720–1780) using Google Cloud Document AI for OCR. It extracts text and refines it with spell-checking and grammar correction functions.

- **`direct.ipynb`**  
  Iterates through a directory of TIF files, extracts text using a chosen model, and saves it to individual files for a searchable text database.

- **`search.ipynb`**  
  Prepares transcribed data and indexes it in Elasticsearch for efficient search and retrieval.

- **`Transcriptcompare.py`**  
  Evaluates transcription accuracy by comparing model outputs to known historical transcriptions (e.g., 99% match for Claude on Washington’s 1789 speech). Outputs percentage matches and mismatched words.

## Model Training and Evaluation
  - Since the Hampden County deeds lack transcriptions, we evaluated our models using similar historical documents:
1. Transcriptcompare.py
This script is programmed to compare two text chunks. We used this script to compare the text transcribed by the Claude AI model to the original transcribed text available on the website. By applying this method to historical documents, we aimed to check whether the model provides an accurate transcription.

The script performs the following tasks:

Counts the number of matching words between the two chunks of text. Calculates the percentage of matching words relative to the total words in the first chunk. Lists the non-matching words for both chunks, highlighting differences.

The script uses Python's collections.Counter to efficiently count occurrences of each word and identify the matching and non-matching words.

2. HistoricalDocsClaude-pipeline.ipynb
Description: This Jupyter notebook processes historical document images (JPEG format), compresses them, and sends them to the Anthropic Claude AI API to transcribe the text. It extracts key details like:

The Treaty Title or Subject. The Date of the document. Key Phrases or Names. Significant Clauses or terms. This pipeline can be used for transcribing and extracting important details from images of historical treaties, letters, or any other document type.

    - Claude Model
      - Achieved 99% match on George Washington’s First Inaugural Speech (1789).
    - Google Model
      - Achieved 43% match on George Washington’s First Inaugural Speech (1789).
    - Microsoft Model
      - Was only able to transcribe the first 7 words in a given text

  - Based on these results, the Claude model was selected for its superior performance on cursive handwriting. Future evaluations will use manually transcribed Hampden County deeds once available.
  

## Using the API

The project leverages two APIs for transcription:

### Anthropic Claude API (in `Claude-pipeline.ipynb`)
- Converts TIF images to PNGs and encodes them in base64.
- Sends the encoded images to Claude with a prompt to extract text and structured data.
- Receives JSON responses containing the transcription and extracted fields.

### Google Cloud Document AI (in `Google-pipeline.ipynb`)
- Sets up a Google Cloud client with credentials.
- Sends TIF images directly to Document AI for OCR.
- Processes the extracted text with spell-checking and grammar correction.

## Streamlit Feature

A Streamlit interface is planned to provide a user-friendly way to upload images, view transcriptions, and search the indexed database. This feature is currently under development.

## How to Continue

Future work includes:

- Expanding the transcription pipeline to additional centuries (e.g., 1600s, 1800s).
- Improving OCR accuracy for faded or damaged documents.
- Developing a Streamlit dashboard for easy access and search functionality.
- Validating transcriptions against ground-truth data from Hampden County once available.
