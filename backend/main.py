import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

app = FastAPI()

load_dotenv()

supabase_url = os.getenv("URL")
supabase_key = os.getenv("API_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class FileInfo(BaseModel):
    product_name: str
    file_url: str
    uid: str

expected_columns = {
    'user_id': 'bigint',
    'name': 'text',
    'email': 'text',
    'gender': 'text',
    'age': 'bigint',
    'location': 'text',
    'total_spent': 'float',
    'transaction_frequency': 'bigint',
    'average_transaction_value': 'float',
    'number_of_transactions': 'bigint',
    'favorite_payment_method': 'text',
    'purchase_channel': 'text',
    'preferred_device': 'text',
    'preferred_language': 'text',
    'time_on_site': 'bigint',
    'page_views_per_session': 'bigint',
    'average_cart_value': 'float',
    'abandoned_cart_count': 'text',
    'product_browsing_history': 'text',
    'loyalty_program_member': 'boolean',
    'loyalty_points_balance': 'bigint',
    'email_open_rate': 'float',
    'email_click_rate': 'float',
    'sms_opt_in': 'boolean',
    'sms_click_rate': 'float',
    'best_time_in_the_day': 'text',
    'best_day_in_a_week': 'text',
    'best_week_in_a_month': 'bigint',
    'coupon_usage_frequency': 'float',
    'social_media_engagement': 'bigint',
    'number_of_reviews_written': 'bigint',
    'average_review_rating': 'float',
    'referral_count': 'text',
    'customer_service_interactions': 'text',
    'live_chat_use_frequency': 'bigint',
    'marketing_segment': 'text',
    'campaign_engagement_score': 'bigint',
    'preferred_communication_channel': 'text',
    'click_through_rate': 'float',
    'conversion_rate': 'float',
    'discount_usage_rate': 'float',
    'preferred_brand': 'text',
    'brand_loyalty_index': 'bigint',
    'lifetime_value_estimate': 'float',
    'frequency_of_visits_per_week': 'bigint',
    'returning_customer': 'boolean',
    'shopping_basket_value': 'float',
    'cart_conversion_rate': 'float',
    'purchase_value_category': 'text',
    'transaction_frequency_category': 'text',
    'product_affinity': 'text',
    'discount_affinity': 'text'
}

def clean_and_validate_data(df):
    df.columns = df.columns.str.lower()
    
    df = df.reindex(columns=expected_columns.keys())
    
    for col, dtype in expected_columns.items():
        if dtype == 'bigint':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        elif dtype == 'float':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('float64')
        elif dtype == 'boolean':
            df[col] = df[col].astype('boolean')
        else:
            df[col] = df[col].astype('object')
    
    return df

@app.post("/process_file")
async def process_file(file_info: FileInfo):
    try:
        response = requests.get(file_info.file_url)
        response.raise_for_status()
        temp_file_path = f"temp_{file_info.uid}.csv"
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(response.content)
        
        df = pd.read_csv(temp_file_path)
        
        df = clean_and_validate_data(df)
        
        records = df.to_dict('records')
        result = supabase.table("data").insert(records).execute()        
        os.remove(temp_file_path)
        
        return {"message": "File processed and data inserted successfully", "product_name": file_info.product_name, "uid": file_info.uid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))