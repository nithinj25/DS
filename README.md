# Insurance Policy Analyzer

A Python-based API for analyzing insurance policy PDFs. This tool extracts and analyzes key information from insurance policy documents, including benefits, loopholes, and exclusions.

## Features

- PDF text extraction and analysis
- Identification of policy loopholes
- Extraction of benefits and coverage details
- Analysis of major exclusions
- RESTful API interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nithinj25/DS.git
cd DS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the API server:
```bash
python api.py
```

2. Access the API documentation at `http://localhost:8000/docs`

3. Use the API endpoints:
   - `POST /analyze-policy/`: Upload and analyze a PDF insurance policy
   - `GET /`: Get API information

## API Endpoints

### POST /analyze-policy/
Upload a PDF insurance policy for analysis.

**Request:**
- Content-Type: multipart/form-data
- Body: PDF file

**Response:**
```json
{
    "filename": "policy.pdf",
    "analysis": {
        "loopholes": {...},
        "benefits": {...},
        "major_exclusions": [...],
        "coverage_highlights": [...]
    }
}
```

## Dependencies

- fastapi
- uvicorn
- python-multipart
- spacy
- pytesseract
- numpy
- pandas
- pillow
- pymupdf
- opencv-python
- pdf2image

## License

MIT License 