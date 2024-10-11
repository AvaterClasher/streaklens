import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Initialize the LLM (Google Generative AI)
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, google_api_key=api_key)

def generate_best_email(data):
    prompt = f"""
    You are an expert email copywriter. Generate a personalized promotional email for a customer based on the following details:
    
    - Customer Name: {data['USER_NAME']}
    - Product: {data['PRODUCT_NAME']}
    - Discount: {data['DISCOUNT']}%
    - Price (MSP): {data['MSP']}
    
    Create a compelling email that highlights the discount if available, and encourages the customer to purchase the product.
    If the discount is 0%, generate an email without mentioning any discount but emphasize the product's features and value.
    
    Provide the final email content directly.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# Pydantic model for input validation
class EmailData(BaseModel):
    USER_NAME: str
    PRODUCT_NAME: str
    DISCOUNT: int
    MSP: str

@app.post("/generate-email/")
async def generate_email(data: EmailData):
    try:
        # Convert Pydantic object to dictionary
        email_data = data.dict()
        
        # Generate email using the provided data
        generated_email = generate_best_email(email_data)
        return {"generated_email": generated_email}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Email Generator API!"}
