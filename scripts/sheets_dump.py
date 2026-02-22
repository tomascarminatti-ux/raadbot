import os
import sqlite3
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Config
DB_PATH = os.getenv("DB_PATH", "infra/db/gem_v3.sqlite")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "config/service_account.json")
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_db_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        entity_id, current_stage, state, last_score, 
        human_required, updated_at, agent_responsible 
    FROM entity_state
    UNION ALL
    SELECT 
        entity_id, stage_at_discard as current_stage, 'DISCARDED' as state, 
        score_at_discard as last_score, 0 as human_required, 
        created_at as updated_at, agent_responsible
    FROM discarded_entities
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def sync_to_sheets():
    if not SPREADSHEET_ID or not os.path.exists(SERVICE_ACCOUNT_FILE):
        print("Missing Sheets config. Skipping sync.")
        return

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    df = get_db_data()
    values = [df.columns.tolist()] + df.values.tolist()

    body = {
        'values': values
    }
    
    # Clear and update (Production mode: Overwrite whole sheet as dashboard)
    range_name = 'Dashboard!A1'
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID, range='Dashboard!A:Z').execute()
    
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption='RAW', body=body).execute()
    
    print(f"{result.get('updatedCells')} cells updated in Google Sheets.")

if __name__ == "__main__":
    sync_to_sheets()
