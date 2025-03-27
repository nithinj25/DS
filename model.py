import re
import json
import nltk
from typing import Dict, List, Any
import spacy

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

class InsurancePolicyAnalyzer:
    def __init__(self):
        # Load spaCy for advanced natural language processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy English model...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text from a PDF file using PyPDF2.
        Note: Requires PyPDF2 to be installed
        """
        try:
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except ImportError:
            print("PyPDF2 not installed. Please install it to read PDFs.")
            return ""

    def identify_loopholes(self, policy_text: str) -> Dict[str, List[str]]:
        """
        Identify potential loopholes in the insurance policy
        """
        loopholes = {
            "Ambiguous Language": [],
            "Exclusion Clauses": [],
            "Limitation Flags": [],
            "Claim Rejection Risks": []
        }

        # Analyze text with spaCy
        doc = self.nlp(policy_text)

        # Patterns to detect potential loopholes
        ambiguous_patterns = [
            r'may\s+not',
            r'subject\s+to',
            r'contingent\s+upon',
            r'at\s+discretion',
            r'as\s+determined\s+by'
        ]

        exclusion_keywords = [
            'not covered', 'excluded', 'limitation', 
            'pre-existing condition', 'waiting period'
        ]

        # Check for ambiguous language
        for pattern in ambiguous_patterns:
            matches = re.findall(pattern, policy_text, re.IGNORECASE)
            if matches:
                loopholes["Ambiguous Language"].extend(matches)

        # Check for exclusion clauses
        for keyword in exclusion_keywords:
            matches = re.findall(fr'\b{keyword}\b.*?[.!]', policy_text, re.IGNORECASE)
            if matches:
                loopholes["Exclusion Clauses"].extend(matches)

        # Identify potential claim rejection risks
        rejection_indicators = [
            'documentation required',
            'proof of',
            'must provide',
            'conditional coverage'
        ]
        for indicator in rejection_indicators:
            matches = re.findall(fr'\b{indicator}\b.*?[.!]', policy_text, re.IGNORECASE)
            if matches:
                loopholes["Claim Rejection Risks"].extend(matches)

        return loopholes

    def summarize_policy(self, policy_text: str) -> Dict[str, Any]:
        """
        Generate a simplified summary of the insurance policy
        """
        summary = {
            "Key Sections": {},
            "Coverage Highlights": [],
            "Benefits": {
                "Medical Benefits": [],
                "Financial Benefits": [],
                "Additional Benefits": []
            },
            "Major Exclusions": [],
            "Claim Process": {}
        }

        # Basic NLP processing
        doc = self.nlp(policy_text)

        # Identify key sections using section header patterns
        section_patterns = [
            "coverage", "benefits", "exclusions", 
            "claims", "terms", "conditions"
        ]

        # Extract sentences for key sections
        for section in section_patterns:
            section_sentences = [
                sent.text.strip() for sent in doc.sents 
                if section in sent.text.lower() and len(sent.text.split()) > 5
            ]
            if section_sentences:
                summary["Key Sections"][section.capitalize()] = section_sentences[:3]

        # Extract benefits with categorization
        benefit_keywords = {
            "Medical Benefits": ["treatment", "hospitalization", "surgery", "medical", "health", "care", "consultation"],
            "Financial Benefits": ["cashless", "reimbursement", "coverage", "sum insured", "premium", "discount"],
            "Additional Benefits": ["renewal", "bonus", "tax", "family", "additional"]
        }

        for sent in doc.sents:
            sent_text = sent.text.strip()
            if len(sent_text.split()) > 5:  # Ignore very short sentences
                for category, keywords in benefit_keywords.items():
                    if any(keyword in sent_text.lower() for keyword in keywords):
                        if "not " not in sent_text.lower() and "exclude" not in sent_text.lower():
                            summary["Benefits"][category].append(sent_text)

        # Remove duplicates and limit to top benefits
        for category in summary["Benefits"]:
            summary["Benefits"][category] = list(dict.fromkeys(summary["Benefits"][category]))[:5]

        # Extract coverage highlights
        summary["Coverage Highlights"] = [
            sent.text.strip() for sent in doc.sents 
            if any(keyword in sent.text.lower() for keyword in ["covered", "benefits", "include"])
            and "not " not in sent.text.lower() and "exclude" not in sent.text.lower()
        ][:5]

        # Extract major exclusions
        summary["Major Exclusions"] = [
            sent.text.strip() for sent in doc.sents 
            if any(keyword in sent.text.lower() for keyword in ["not covered", "excluded", "exclusion", "limitation"])
        ][:5]

        return summary

    def analyze_policy(self, policy_text: str) -> Dict[str, Any]:
        """
        Comprehensive policy analysis
        """
        return {
            "Loopholes": self.identify_loopholes(policy_text),
            "Summary": self.summarize_policy(policy_text)
        }

def main():
    # Example usage
    analyzer = InsurancePolicyAnalyzer()
    
    # Extract from PDF
    pdf_path = "Brochure_Star_Cardiac_Care_Insurance_Policy_V_13_Web_13e0200770.pdf"
    policy_text = analyzer.extract_text_from_pdf(pdf_path)
    
    analysis_result = analyzer.analyze_policy(policy_text)
    
    # Format and display results
    print("\n" + "="*80)
    print("INSURANCE POLICY ANALYSIS")
    print("="*80)
    
    print("\nLOOPHOLES:")
    print("-"*80)
    for category, items in analysis_result["Loopholes"].items():
        if items:  # Only print categories that have items
            print(f"\n{category}:")
            for item in items:
                print(f"  • {item.strip()}")
    
    print("\nBENEFITS:")
    print("-"*80)
    for category, benefits in analysis_result["Summary"]["Benefits"].items():
        if benefits:  # Only print categories that have benefits
            print(f"\n{category}:")
            for benefit in benefits:
                print(f"  • {benefit.strip()}")
    
    print("\nMAJOR EXCLUSIONS:")
    print("-"*80)
    for exclusion in analysis_result["Summary"]["Major Exclusions"]:
        print(f"  • {exclusion.strip()}")
    
    print("\n" + "="*80)
    
    return analysis_result

if __name__ == "__main__":
    main()