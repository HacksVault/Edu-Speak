import google.generativeai as genai
api_key = 'AIzaSyDHs6a-KYnyF2Eyfw11QEscDfTAcqU-aWM'
genai.configure(api_key=api_key)
response = """
    Good morning everyone! Before we start, there is an announcement about the library closing early today.
    Now, let's talk about the main topic, which is machine learning. Machine learning is a subset of artificial intelligence that focuses on...
    Oh, one more thing, there will be a break in 15 minutes.
"""

def clean_text_with_gemini(response_text):
    prompt = (
        "Clean this text by removing all irrelevant content such as announcements, distractions, "
        "and non-teaching parts. Only keep the main teaching material . Dont add your own concepts if there is grammar mistakes correct that otherwise just the teacher teaching style and speech. if the teacher teaches with a story dont modify the story just enhance and keep the main content.:\n\n" + response_text
    )
    model = genai.GenerativeModel('gemini-pro')
    cleaned_response = model.generate_content(prompt)
    
    return cleaned_response.text
cleaned_response = clean_text_with_gemini(response)
print("Cleaned Response:\n", cleaned_response)
