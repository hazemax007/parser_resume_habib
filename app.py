# from flask import Flask, request, jsonify
# from PyPDF2 import PdfReader
# import google.generativeai as genai
# import os
# import json

# # Set up API key for Google Generative AI
# genai.configure(api_key="AIzaSyDdNW__tgHsI7GVh0MdXDfQTv8T4F7_DX8")

# # Initialize Flask app
# app = Flask(__name__)

# # Load the generative AI model
# model = genai.GenerativeModel("models/gemini-1.5-flash")


# def parse_resume(resume_text):
#     """Parses the resume using a generative AI model."""
#     prompt = f"""
#     You are a resume parsing assistant. Given the following resume text, extract all the important details and return them in a well-structured JSON format.

#     The resume text:
#     {resume_text}

#     Extract and include the following:
#     - Full Name
#     - Contact Number
#     - Email Address
#     - Location
#     - Skills (Technical and Non-Technical, separately if possible)
#     - Education
#     - Work Experience (including company name, role, and responsibilities)
#     - Certifications
#     - Languages spoken
#     - Suggested Resume Category (based on the skills and experience)
#     - Recommended Job Roles (based on the candidate's skills and experience)

#     Return the response in JSON format.
#     """
#     response = model.generate_content(prompt).text
#     return response


# def find_attribute(attributes, keyword):
#     """Search for an attribute containing the keyword."""
#     for key, value in attributes.items():
#         if isinstance(key, str) and keyword.lower() in key.lower():
#             return value
#     return None


# def standardize_response(parsed_data):
#     """Standardize the parsed resume data to consistent attribute names."""
#     standardized_data = {}

#     # Search for attributes containing specific keywords
#     standardized_data["fullName"] = find_attribute(parsed_data, "name")
#     standardized_data["contactNumber"] = find_attribute(parsed_data, "contact")
#     standardized_data["emailAddress"] = find_attribute(parsed_data, "email")
#     standardized_data["location"] = find_attribute(parsed_data, "location")
#     standardized_data["skills"] = find_attribute(parsed_data, "skills")
#     standardized_data["education"] = find_attribute(parsed_data, "education")
#     standardized_data["workExperience"] = find_attribute(parsed_data, "work") or find_attribute(parsed_data, "experience")
#     standardized_data["certifications"] = find_attribute(parsed_data, "certification")
#     # standardized_data["languages"] = find_attribute(parsed_data, "language")
#     # standardized_data["suggestedResumeCategory"] = find_attribute(parsed_data, "category") or find_attribute(parsed_data, "suggest")
#     standardized_data["recommendedJobRoles"] = find_attribute(parsed_data, "role")

#     return standardized_data


# @app.route('/api/upload_resume', methods=['POST'])
# def upload_resume():
#     """Handles resume upload and parsing."""
#     if 'resume' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files['resume']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     if file and file.filename.endswith('.pdf'):
#         # Extract text from the uploaded PDF
#         text = ""
#         reader = PdfReader(file)
#         for page in reader.pages:
#             text += page.extract_text()

#         # Parse resume using the generative AI model
#         response = parse_resume(text)

#         # Clean and parse JSON response
#         try:
#             response_clean = response.replace("```json", "").replace("```", "").strip()
#             parsed_data = json.loads(response_clean)

#             # Standardize the parsed data into a consistent format
#             standardized_data = standardize_response(parsed_data)

#         except Exception as e:
#             return jsonify({"error": "Failed to parse AI response", "details": str(e)}), 500

#         return jsonify(standardized_data)

#     return jsonify({"error": "Unsupported file type. Please upload a PDF."}), 400


# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """Health check endpoint."""
#     return jsonify({"status": "API is running"}), 200


# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, render_template, redirect, url_for
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
import json

# Configurez la clé API pour Google Generative AI
genai.configure(api_key="AIzaSyDdNW__tgHsI7GVh0MdXDfQTv8T4F7_DX8")

# Initialisez l'application Flask
app = Flask(__name__)

# Chargez le modèle génératif AI
model = genai.GenerativeModel("models/gemini-1.5-flash")

def parse_resume(resume_text):
    """Parses the resume using a generative AI model."""
    prompt = f"""
    You are a resume parsing assistant. Given the following resume text, extract all the important details and return them in a well-structured JSON format.

    The resume text:
    {resume_text}

    Extract and include the following:
    - Full Name
    - Contact Number
    - Email Address
    - Location
    - Skills (Technical and Non-Technical, separately if possible)
    - Education
    - Work Experience (including company name, role, and responsibilities)
    - Certifications
    - Languages spoken
    - Suggested Resume Category (based on the skills and experience)
    - Recommended Job Roles (based on the candidate's skills and experience)

    Return the response in JSON format.
    """
    response = model.generate_content(prompt).text
    return response

def find_attribute(attributes, keyword):
    """Recherche d'un attribut contenant le mot-clé"""
    for key, value in attributes.items():
        if isinstance(key, str) and keyword.lower() in key.lower():
            return value
    return None

def standardize_response(parsed_data):
    """Standardiser les données de CV pour des noms d'attributs cohérents"""
    standardized_data = {}
    standardized_data["fullName"] = find_attribute(parsed_data, "name")
    standardized_data["contactNumber"] = find_attribute(parsed_data, "contact")
    standardized_data["emailAddress"] = find_attribute(parsed_data, "email")
    standardized_data["location"] = find_attribute(parsed_data, "location")
    standardized_data["skills"] = find_attribute(parsed_data, "skills")
    standardized_data["education"] = find_attribute(parsed_data, "education")
    standardized_data["workExperience"] = find_attribute(parsed_data, "work") or find_attribute(parsed_data, "experience")
    standardized_data["certifications"] = find_attribute(parsed_data, "certification")
    standardized_data["recommendedJobRoles"] = find_attribute(parsed_data, "role")
    return standardized_data

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return redirect(url_for('home'))

    file = request.files['resume']
    if file.filename == '':
        return redirect(url_for('home'))

    if file and file.filename.endswith('.pdf'):
        # Extraire le texte du PDF
        text = ""
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

        # Analyser le CV avec le modèle AI
        response = parse_resume(text)

        try:
            response_clean = response.replace("```json", "").replace("```", "").strip()
            parsed_data = json.loads(response_clean)

            # Standardiser les données du CV
            standardized_data = standardize_response(parsed_data)

        except Exception as e:
            return render_template('upload.html', error=f"Erreur de parsing : {str(e)}")

        # Afficher les résultats dans une page HTML
        return render_template('result.html', data=standardized_data)

    return redirect(url_for('home'))

@app.route('/api/health', methods=['GET'])
def health_check():
    return "API is running"

if __name__ == '__main__':
    app.run(debug=True)
