from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import ast
import asyncio
from Supabase import init_supabase,run_sql_query

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEM_API_KEY")
prompt_template = prompt_template = '''Product Name: {product_name}
Product Information: {product_information}

Please predict the following based on the product name and product information provided:
- Gender: Is this product primarily for males return M, for females return F (only give one value)?
- Age Range: What is the likely age range of the target audience (e.g., 18-24, 25-34, 35-44, etc., only give one value)?
- Marketing Segment: Based on typical market research, categorize the product's marketing segment as one of the following: ["D" for "high", "C" for "medium high", "B" for  "medium", "A" :  "low"]

Return the results as a Python list with three elements in the following format:
[gender, age range, marketing segment]
'''

# Function to handle product information and generate SQL parameters
async def SQLparameters(productInfo: dict):
    product_name = productInfo['name']
    product_description = productInfo['description']
    
    # Define the prompt
    prompt = PromptTemplate(
        input_variables=["product_name", "product_information"],
        template=prompt_template,
    )
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, google_api_key=gemini_api_key)
    
    # Use LLMChain (no need for async/await, as we will invoke synchronously)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    # Invoke the chain to get the response (synchronous call)
    response = llm_chain.invoke({
        "product_name": product_name,
        "product_information": product_description
    })
    print(response)
    # Safely parse the response to a Python list
    try:
        parsed_response = ast.literal_eval(response['text'])
        print("Parsed Response:", parsed_response)
        return parsed_response
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing the response: {e}")
        return None

# Function to generate SQL query based on parsed response
def generate_sql_query(parsed_response):
    # Extract gender, age range, and marketing segment from the parsed response
    gender = parsed_response[0]
    age_range = parsed_response[1]  # Example: '18-24' or '25-34'
    marketing_segment = parsed_response[2]

    # Split the age range into min and max ages
    age_min, age_max = map(int, age_range.split('-'))

    # Generate the SQL query with variables
    return gender,age_min,age_max,marketing_segment
# Async main function to run SQL parameters and query generation in order
async def main():
    # Await the response from SQLparameters
    response = await SQLparameters(productInfo={
        'name': "UNDIES", 
        'description': "underwear comfy and safe for men and non-binary folk"
    })
    
    # Ensure the response is not None before generating SQL query
    if response:
        gender,age_min,age_max,marketing_segment = generate_sql_query(response)
        print(age_min)
        print(age_max)
        run_sql_query(gender=gender,age_range=(age_min,age_max),marketing_segment='A')


async def getData(productInfo : dict):
    response = await SQLparameters(productInfo=productInfo)
    if response:
        gender,age_min,age_max,marketing_segment = generate_sql_query(response)
        data = run_sql_query(gender=gender,age_range=(age_min,age_max),marketing_segment=marketing_segment)
        
# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
