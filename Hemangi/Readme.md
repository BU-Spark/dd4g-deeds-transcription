#Transcriptcompare.py
This script is programmed to compare two text chunks. We used this script to compare the text transcribed by the Claude AI model to the original transcribed text available on the website. By applying this method to historical documents, we aimed to check whether the model provides an accurate transcription.

The script performs the following tasks:

Counts the number of matching words between the two chunks of text.
Calculates the percentage of matching words relative to the total words in the first chunk.
Lists the non-matching words for both chunks, highlighting differences.

The script uses Python's collections.Counter to efficiently count occurrences of each word and identify the matching and non-matching words.


2. HistoricalDocsClaude-pipeline.ipynb

Description:
This Jupyter notebook processes historical document images (JPEG format), compresses them, and sends them to the Anthropic Claude AI API to transcribe the text. It extracts key details like:

The Treaty Title or Subject.
The Date of the document.
Key Phrases or Names.
Significant Clauses or terms.
This pipeline can be used for transcribing and extracting important details from images of historical treaties, letters, or any other document type.

