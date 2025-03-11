# Data Days For Good Deeds Transcriptions

## Description:

The Hampden County Registry of Deeds holds a vast collection of historical records dating back to the early 1600s. With approximately 100,000 documents spread across 600 books (each containing around 1,000 documents), these records provide invaluable insights into property ownership, land transactions, and historical boundaries. However, due to the handwritten cursive nature of the documents, inconsistent document delineation, and the lack of a comprehensive indexing system, accessing specific records remains a challenge.

## Ideal Output & Final Deliverables:

The primary objective of this project is to create a pipeline to digitize and systematically index these historical records to facilitate efficient search and retrieval. This includes:

- **Extracting Key Information**: Identifying grantors, grantees, property descriptions, and geographical references (city, county, streets, NWSE directions).
- **Standardizing Metadata**: Ensuring documents are properly categorized (e.g., deeds, easements, mortgages, liens, plan cards).
- **Improving Searchability**: Creating an indexed system that allows for title searches, boundary dispute research, and historical property ownership tracing.
- **Enhancing Accessibility**: Providing structured access to documents for researchers, legal professionals, and genealogy enthusiasts.

## Data

All data is saved on the Shared Computing Cluster from Boston University at:  
`/projectnb/sparkgrp/mass-sec-state-deeds-data/1720-1780`

## Code

- **Claude-pipeline.ipynb**  
This code automates the digitization and analysis of historical deed documents (1720-1780) using the Anthropic Claude API. It processes TIF images by converting them to base64 encoded PNGs, which are then sent to Claude with a system prompt and structured template. Claude extracts text and specific information like document type, granter, grantee, and address, returning the data in JSON format.

- **Google-pipeline.ipynb**  
This code automates the digitization and analysis of historical deed documents (1720-1780) using the Google Cloud Document AI. It sets up a Google Cloud client with specific credentials, reads image files, and uses Document AI for OCR (Optical Character Recognition) to extract text. The extracted text is then polished using a spell-checking function and a grammar-correction function before displaying the final result.

- **Transcriptcompare.py**  
Since none of the Hampden County Registry of Deeds are transcribed, it is unclear how accurate our model is at transcribing the images into text. To address this, we compare our model's predictions with actual transcriptions of similar historical documents. Transcriptcompare.py compares the percentage match between our model's output and the actual transcription, listing any mismatched words. For example, our Claude model achieved a 99% match rate for George Washington's First Inaugural Speech (1789). In contrast, the Google model only achieved a 43% match. Based on this, we chose to use the Claude model for transcribing the remaining documents, achieving an 89.25% match for the US-Moroccan peace treaty (1786).

- **direct.ipynb**  
This script iterates through a directory of TIF files, saves the extracted text to individual files, and handles errors, creating a pipeline for converting archival documents into searchable text databases.

- **search.ipynb**  
Prepares and indexes document data for efficient searching and retrieval in Elasticsearch.

---

## Prerequisites

Before running the code, make sure you have the following libraries installed:

- Python 3.x
- Required libraries:
  - `pandas`
  - `requests`


Alternatively, you can use the following command to install the dependencies:

```bash
pip install -r requirements.txt
