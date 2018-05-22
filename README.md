# PDF to TXT

Python code to do OCR recognition of a PDF file and export text to TXT file.

* **LocalOCR**: based on [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
* **CloudOCR**: based on [Google Vision API](https://cloud.google.com/vision/)


## Setup for LocalOCR on Ubuntu

    apt-get install python-pyocr python-wand imagemagick
    apt-get install libleptonica-dev tesseract-ocr-dev
    apt-get install tesseract-ocr-ita
    pip install requirements.txt


## Setup CloudOCR on Ubuntu
   
Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/#deb)


    apt-get install pdfimages google-cloud-sdk-app-engine-python
    pip install requirements.txt


