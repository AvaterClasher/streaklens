import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("URL")
SUPABASE_KEY = os.getenv("API_KEY")


def init_supabase() -> Client:
    url = SUPABASE_URL
    key = SUPABASE_KEY
    supabase: Client = create_client(url, key)
    return supabase

# Execute a SQL query
def run_sql_query(gender : str,age_range : tuple[int,int],marketing_segment : str):
    supabase = init_supabase()
    
    # Example SQL query (adjust the query as per your needs)
    age_min = int(age_range[0])
    age_max = int(age_range[1])
    # Execute the query using RPC (Remote Procedure Call)
    response = supabase.table("data") \
        .select("*") \
        .eq("gender", gender) \
        .gte("age", age_min) \
        .lte("age", age_max) \
        .eq("marketing_segment", marketing_segment) \
        .execute()
    
    # Print the result of the query
    print(response)
    print(len(response.data))
    return response.data
