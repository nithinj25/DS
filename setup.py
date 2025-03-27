from setuptools import setup, find_packages

setup(
    name="pdf_analyzer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytesseract",
        "spacy",
        "numpy",
        "pandas",
        "pillow",
        "pymupdf",
        "opencv-python",
        "pdf2image"
    ],
) 