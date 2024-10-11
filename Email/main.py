import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage


load_dotenv()
api_key = os.getenv("API_KEY")


app = FastAPI()


llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, google_api_key=api_key)


email_formats = {
    "discount_email": """
        Dear {USER_NAME},
        Your wardrobe deserves an upgrade! Get {DISCOUNT}% off on the latest {PRODUCT_NAME} from StylishThreads. 
        With prices as low as {MSP}, there's no better time to shop!
        Happy shopping!
    """,
    "limited_offer": """
        Hey {USER_NAME},
        It's time to refresh your style! For a limited time, we're offering {DISCOUNT}% off on {PRODUCT_NAME} from StylishThreads.
        Now available at just {MSP}.
        Happy shopping!
    """,
    "no_discount_email": """
        Hey {USER_NAME},
        New arrivals just for you! Check out our latest {PRODUCT_NAME} collection from StylishThreads.
        No discounts this time, but we've got the best prices on premium fashion with MSP starting at {MSP}.
    """
}

def generate_best_email(data):
    formatted_emails = {
        "discount_email": email_formats["discount_email"].format(**data),
        "limited_offer": email_formats["limited_offer"].format(**data),
        "no_discount_email": email_formats["no_discount_email"].format(**data)
    }

    prompt = f"""
    You are an expert email copywriter. Given the following email formats, choose the best one based on the data provided.
    1. Discount email:
    {formatted_emails['discount_email']}
    2. Limited-time offer email:
    {formatted_emails['limited_offer']}
    3. No discount email:
    {formatted_emails['no_discount_email']}

    User data:
    Name: {data['USER_NAME']}
    Product: {data['PRODUCT_NAME']}
    Discount: {data['DISCOUNT']}%
    MSP: {data['MSP']}

    Based on the user's data, select the most appropriate email format and generate the final email. 
    If the discount is 0, prefer the no-discount email format. 
    Return only the final email content, without any explanations or additional text.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content


class EmailData(BaseModel):
    USER_NAME: str
    PRODUCT_NAME: str
    DISCOUNT: int
    MSP: str

@app.post("/generate-email/")
async def generate_email(data: EmailData):
    try:
        
        email_data = data.dict()
        
        
        generated_email = generate_best_email(email_data)
        return {"generated_email": generated_email}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Welcome to the Email Generator API!"}
