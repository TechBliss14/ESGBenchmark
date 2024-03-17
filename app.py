from flask import Flask, request, jsonify
import PyPDF2
import spacy

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text


# Function to extract ESG information from the PDF text
def extract_esg_information(text):
    esg_data = {
        "environmental": [],
        "social": [],
        "governance": []
    }

    doc = nlp(text)

    # Extracting environmental initiatives
    environmental_keywords = ["environmental", "sustainability", "green", "carbon footprint"]
    for sentence in doc.sents:
        for keyword in environmental_keywords:
            if keyword in sentence.text.lower():
                esg_data["environmental"].append(sentence.text)
                break

    # Extracting social initiatives
    social_keywords = ["social", "community", "diversity", "equality", "employee"]
    for sentence in doc.sents:
        for keyword in social_keywords:
            if keyword in sentence.text.lower():
                esg_data["social"].append(sentence.text)
                break

    # Extracting governance practices
    governance_keywords = ["governance", "transparency", "ethics", "accountability"]
    for sentence in doc.sents:
        for keyword in governance_keywords:
            if keyword in sentence.text.lower():
                esg_data["governance"].append(sentence.text)
                break

    return esg_data


def analyze_questions(questions):
    """Analyze questions to identify ESG-related keywords."""
    # Example: You may use keyword matching or other NLP techniques to identify ESG-related questions
    esg_keywords = ["environmental", "social", "governance"]
    relevant_questions = []
    for question in questions:
        if any(keyword in question.lower() for keyword in esg_keywords):
            relevant_questions.append(question)
    return relevant_questions


def analyze_esg(text, questions):
    # Implement NLP processing and ESG analysis based on questions
    # This could involve using libraries like spaCy, NLTK, or custom logic
    # For example, searching for keywords related to ESG topics
    esg_data = {}
    for question in questions:
        # Analyze text to find answers to questions
        # Populate esg_data dictionary with relevant information
        pass
    return esg_data


@app.route('/analyze', methods=['POST'])
def analyze_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the uploaded PDF file
        pdf_file_path = 'uploaded_file.pdf'
        file.save(pdf_file_path)

        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_file_path)

        # Step 2: Extract ESG information
        esg_info = extract_esg_information(pdf_text)
        print(esg_info)

        # Define questions to analyze ESG data
        questions = ["What environmental initiatives are mentioned?",
                     "What social responsibility efforts are described?",
                     "How is governance addressed in the report?"]

        # Step 3: Analyze questions
        relevant_questions = analyze_questions(questions)

        # Analyze ESG data
        esg_data = analyze_esg(pdf_text, relevant_questions)
        print(esg_data)

        return jsonify(esg_data)


@app.route('/ping', methods=['GET'])
def ping():
    return "App up and running"


if __name__ == '__main__':
    app.run(debug=True)
