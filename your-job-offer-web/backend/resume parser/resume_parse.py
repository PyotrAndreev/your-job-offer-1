import os
import json
import re
from PyPDF2 import PdfReader
from gigachat import GigaChat
from dotenv import load_dotenv
load_dotenv()


# print(response.choices[0].message.content)


# Step 2: Function to Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        # Clean up the text (optional)
        text = re.sub(r"[\s]+", " ", text)
        return text
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")

# Step 3: Function to Query OpenAI
def query_openai(prompt, model, max_tokens=1000):
    try:
        print("Sending request to GigaChat")  # Debug
        response = model.chat(prompt)

        # response = client.chat.completions.create(
        #     model=model,
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant for parsing resumes."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     max_tokens=max_tokens,
        #     temperature=0.0,  # Deterministic output
        # )
        print("Response received from GigaChat.")  # Debug
        # Extract the assistant's reply
        return response.choices[0].message.content
    except Exception as e:
        raise ValueError(f"Error querying OpenAI: {e}")

# Step 4: Generate Prompt and Parse Resume
def parse_resume(pdf_path):
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Define a simple prompt for parsing resumes
    prompt = """
    Пожалуйста, резюмируй текст ниже в формате JSON без лишних строк текста.
    Вот структура, которой ты должен следовать:
        {
        "birth_date": "",
        "first_name": "",
        "last_name": "",
        "middle_name": "",
        "gender": "",
        "phone": возможно +, затем цифры без пробелов и скобок,
        "email": "",
        "country": "",
        "city": "",
        "country": "",
        "cv": url,
        "description": "",
        "work_type": "",
        "min_salary": "",
        "max_salary": "",
        "business_trip_readiness": 0 or 1,
        "work_hours": "",
        "relocation": 0 or 1,
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
            "description: "",
            "link": ""
            },
        ]
        "work_experience": [
            {
            "job": "",
            "work_place": "",
            "description": "",
            "start_date": "",
            "finish_date": ""
            }
        ],
        "skills": [
            ""
        ]
        }

    Даты указывай в формате year-month-day
    Не добавляй никакого дополнительного текста перед или после JSON.
    Resume Text:
    """ + pdf_text
    # Debug: Check the generated prompt
    print(f"Generated Prompt:\n{prompt}\n")

    model = GigaChat(
   credentials=os.getenv("GIGA_CHAT_API_KEY"),
   scope="GIGACHAT_API_PERS",
   model="GigaChat",
   verify_ssl_certs=False
)
    
    # Query OpenAI with the prompt
    response = query_openai(prompt, model)
    
    # Parse the response into a dictionary
    try:
        parsed_data = json.loads(response)
        return parsed_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse OpenAI response into JSON: {e}")

# Step 5: Main Script to Test the Parser
if __name__ == "__main__":
    # Path to the PDF resume
    pdf_path = "../resume_samples/resume_example.pdf"  # Replace with your PDF file path

    try:
        # Parse the resume
        result = parse_resume(pdf_path)
        print("Parsed Resume Data:")
        print(json.dumps(result, indent=4))
    except Exception as e:
        print(f"Error: {e}")

