from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI
def get_openai_api_key():
    # apikey.object.get(provider='openai',org='CEF)
    return settings.OPENAI_API_KEY

# def get_openai_model(model="gpt-40-mini"):
#     return ChatOpenAI(
#     model=model,
#     temperature=0,
#     max_retries = 2,
#     api_key=settings.OPENAI_API_KEY
# )

def get_openai_model(model="gemini-3.5-flash"):
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0,
        max_retries=1,  # Do not loop retrying for minutes
        timeout=600,
        google_api_key=settings.GOOGLE_API_KEY,
    )