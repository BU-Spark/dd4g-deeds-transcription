import os
import io
import re
import json
import base64
import anthropic
from PIL import Image
from typing import Dict, List, Optional, Any

class PropertyDocumentAnalyzer:
    
    def __init__(self, model: str, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def extract_components(self, file_path: str) -> Dict[str, Any]:
        """
        Extract key components from document image using a chain-of-thought approach.
        Args:
            file_path: The image path of the property document.
        Returns:
            A dictionary containing structured information about the document.
        """

        prompt = f"""
        You are analyzing a image property document. I'll provide you with the image, and I need you to carefully extract the following content and components:

        1. Full Document Content from Image
        2. Document Type
        2. Grantors & Grantees
        3. Legal Authorities
        4. Property Descriptions
        5. Geographical References
        6. Transaction Dates

        Let's think through this step by step.

        DOCUMENT Path:
        ```
        {file_path}
        ```

        STEP 0: Extract the Content from the Historical Document
        The images are handwritten historical documents, please extract the full text from image.
        
        STEP 1: Determine the Document Type
        First, analyze what kind of document this is. Look for key terms that indicate if this is a deed, easement, mortgage, lien, plan card, etc. Consider the overall structure and purpose of the document.

        STEP 2: Identify Grantors & Grantees
        Look for sections that indicate who is selling/transferring property (grantors) and who is buying/receiving it (grantees). These are typically found near phrases like "conveyed by," "granted to," "transferred from," etc.

        STEP 3: Identify Legal Authorities
        Find any judges, witnesses, notaries, or other legal officials mentioned in the document. Look especially in signature blocks, notarization sections, or judicial proceedings.

        STEP 4: Extract Property Descriptions
        Locate detailed descriptions of the property including acreage, boundaries, lot numbers, etc. These are often in sections with precise measurements and may use surveyor's language.

        STEP 5: Collect Geographical References
        Identify all mentions of cities, counties, streets, and other location identifiers throughout the document.

        STEP 6: Extract Transaction Dates
        Find all dates related to the transaction, particularly the execution date, recording date, and any other significant timestamps.

        STEP 7: Summarize Findings
        Based on the above analysis, provide a structured summary of all components identified.

        Please think carefully about each step and provide your findings in a JSON structure with the following format:
        ```json
        {{
            "document_text": "",
            "document_type": "",
            "grantors": [],
            "grantees": [],
            "legal_authorities": [],
            "property_description": {{
                "acreage": "",
                "boundaries": [],
                "lot_info": ""
            }},
            "geographical_references": {{
                "city": "",
                "county": "",
                "streets": []
            }},
            "transaction_dates": {{
                "execution_date": "",
                "recording_date": "",
                "other_dates": []
            }}
        }}
        ```
        """
        
        # Process the image document_id.TIF
        with Image.open(file_path).convert('L') as image:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Make the API call
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            temperature=0,
            system="You are an expert in real estate historical image document analysis. Extract information accurately and completely.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        
        
        # Extract the JSON from the response
        try:
            # Look for JSON structure in the response
            json_match = re.search(r'```json\s*(.*?)\s*```', response.content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            else:
                # Try to find any JSON-like structure
                json_match = re.search(r'({.*})', response.content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                else:
                    raise ValueError("No JSON found in response")
        
        except Exception as e:
            return {"error": "Failed to parse response", "raw_response": response.content}
        


def extract_json_from_claude_response(raw_response):

    # If raw_response is an object (e.g., TextBlock), extract its text attribute
    if hasattr(raw_response, 'text'):
        raw_response = raw_response.text  # Ensure it's a string
    
    # Use regex to find the JSON block inside triple backticks ```json ... ```
    json_match = re.search(r'```json\n(.*?)\n```', raw_response, re.DOTALL)

    if json_match:
        json_string = json_match.group(1)  # Extract JSON content
        try:
            parsed_json = json.loads(json_string)  # Convert to dictionary
            return parsed_json
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format extracted."}
    else:
        return {"error": "No JSON content found in response."}

    
def get_file_id(file_path):
    
    file_name = os.path.basename(file_path)
    file_id = file_name.split('.')[0]
    return file_id


def is_already_processed(file_id, output_dir):
    # Check if the document has already been processed by looking for an existing JSON file.
    json_path = os.path.join(output_dir, f"{file_id}.json")
    return os.path.exists(json_path)


def store_json(file_path, output_dir, direct_results):

    raw_response = direct_results['raw_response']
    if isinstance(raw_response, list) and raw_response: 
        raw_response = raw_response[0]  # Extract first item if it's a list
    parsed_data = extract_json_from_claude_response(raw_response) # Process response

    file_id = get_file_id(file_path)
    json_file_path = os.path.join(output_dir, f"{file_id}.json")

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)

    print(f"JSON saved in: {json_file_path}")

    # Print the cleaned JSON output
#     print(json.dumps(parsed_data, indent=4, ensure_ascii=False))
    

def process_img(file_path, output_dir, model, api_key):
    
    file_id = get_file_id(file_path)
    
    # Check if already processed
    if is_already_processed(file_id, output_dir):
        print(f"Skipping {file_id}: already processed")
        return
    
    analyzer = PropertyDocumentAnalyzer(model, api_key)
    direct_results = analyzer.extract_components(file_path)
    store_json(file_path, output_dir, direct_results)