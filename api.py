from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from model import InsurancePolicyAnalyzer
import tempfile
import os

app = FastAPI(
    title="Insurance Policy Analyzer API",
    description="API for analyzing insurance policy PDFs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the analyzer
analyzer = InsurancePolicyAnalyzer()

@app.get("/health")
async def health_check():
    """
    Health check endpoint for Render
    """
    return {"status": "healthy"}

@app.post("/analyze-policy/")
async def analyze_policy(file: UploadFile = File(...)):
    """
    Analyze an insurance policy PDF file
    """
    try:
        # Verify file type
        if not file.filename.endswith('.pdf'):
            return JSONResponse(
                status_code=400,
                content={"error": "Only PDF files are supported"}
            )

        # Create a temporary file to store the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            # Write uploaded file content to temporary file
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            # Extract text from PDF
            policy_text = analyzer.extract_text_from_pdf(temp_path)
            
            # Analyze the policy
            analysis_result = analyzer.analyze_policy(policy_text)

            # Format the results
            formatted_result = {
                "filename": file.filename,
                "analysis": {
                    "loopholes": analysis_result["Loopholes"],
                    "benefits": analysis_result["Summary"]["Benefits"],
                    "major_exclusions": analysis_result["Summary"]["Major Exclusions"],
                    "coverage_highlights": analysis_result["Summary"]["Coverage Highlights"]
                }
            }

            return JSONResponse(content=formatted_result)

        finally:
            # Clean up: remove temporary file
            os.unlink(temp_path)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred while processing the file: {str(e)}"}
        )

@app.get("/")
async def root():
    """
    Root endpoint - provides basic API information
    """
    return {
        "message": "Insurance Policy Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze-policy/": "POST - Upload and analyze a PDF insurance policy",
            "/health": "GET - Health check endpoint",
            "/": "GET - This information"
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 