import os
import json
import re
import pdfplumber
from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv()

# Initialize GigaChat once
model = GigaChat(
    credentials=os.getenv("GIGA_CHAT_API_KEY"),
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False
)

# Function to Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return re.sub(r"[\s]+", " ", text)  # Clean whitespace
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")

# Function to Query GigaChat
def query_gigachat(prompt):
    try:
        print("Sending request to GigaChat...")  # Debug
        response = model.chat(prompt)
        print("Response received from GigaChat.")  # Debug
        return response  # Handle response parsing in next step
    except Exception as e:
        raise ValueError(f"Error querying GigaChat: {e}")

# Function to Parse Resume
def parse_resume(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    
    prompt = """
    Пожалуйста, резюмируй текст ниже в формате JSON без лишних строк текста.
    Вот структура, которой ты должен следовать:
    {
        "birth_date": "",
        "first_name": "",
        "last_name": "",
        "middle_name": "",
        "gender": "",
        "phone": "",  
        "email": "",
        "country": "",
        "city": "",
        "cv": "url",
        "description": "",
        "work_type": "",
        "min_salary": "",
        "max_salary": "",
        "business_trip_readiness": 0,
        "work_hours": "",
        "relocation": 0,
        "project_experience": [
            {
                "title": "",
                "description": "",
                "link": ""
            }
        ],
        "achievements": [
            {
                "title": "",
                "description": "",
                "link": ""
            }
        ],
        "work_experience": [
            {
                "job": "",
                "work_place": "",
                "description": "",
                "start_date": "",
                "finish_date": ""
            }
        ],
        "skills": []
    }

    Даты указывай в формате YYYY-MM-DD.
    Не добавляй никакого дополнительного текста перед или после JSON.

    Resume Text:
    """ + pdf_text

    # Debug: Print the generated prompt
    print(f"Generated Prompt:\n{prompt[:1000]}...\n")  # Limit output for debugging

    response = query_gigachat(prompt)
    
    # Handle JSON Parsing
    try:
        parsed_data = json.loads(response.strip())
        return parsed_data
    except json.JSONDecodeError as e:
        print("Raw response:", response)  # Debugging
        raise ValueError(f"Failed to parse response into JSON: {e}")

# Main Script to Test the Parser
if __name__ == "__main__":
    pdf_path = "./resume-example.pdf" 
    # print(os.path.exists(pdf_path))
    # result = parse_resume(pdf_path)
    try:
        result = parse_resume(pdf_path)
        print("Parsed Resume Data:")
        print(json.dumps(result, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
