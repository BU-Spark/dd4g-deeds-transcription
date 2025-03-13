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
* dataset/
  * sample-images/
  * sample-output/
  * DATASETDOC
  * standardized_land_deeds
* notebooks/
  * EDA_MMDDFG_cfgpm.ipynb
  * extract_image_info.ipynb
  * HistoricalDocsClaude-pipeline.ipynb
  * json_to_csv.ipynb
  * microsoft-text-generator.ipynb
  * visualization.ipynb
  * web_scrape.ipynb
* scripts/
  * app.py
  * extract.py
  * mapIndex.py
  * transcriptcompare.py
* LICENSE
* COLLABORATORS
* requirements.txt
* README.md


- **`EDA_MMDDFG_cfgpm.ipynb`**  

- **`extract_image_info.ipynb`**  

- **`HistoricalDocsClaude-pipeline.ipynb`**  

- **`json_to_csv.ipynb`** 

- **`microsoft-text-generator.ipynb`** 
  Uses a model generated by microsoft to convert handwritten scripts into computer generated text. However, this model was only able to output 7 words at a time

- **`json_to_csv.ipynb`** 

- **`visualization.ipynb`**  

- **`web_scrape.ipynb`** 

- **`app.py`**

- **`extract.py`**

- **`mapIndex.py`**

- **`Transcriptcompare.py`**  
  Evaluates transcription accuracy by comparing model outputs to known historical transcriptions (e.g., 99% match for Claude on Washington’s 1789 speech). Outputs percentage matches and mismatched words.

## Model Training and Evaluation
  - Since the Hampden County deeds lack transcriptions, we evaluated our models using similar historical documents:

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
