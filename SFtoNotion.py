# SFtoNotion.py

# Importing necessary modules and credentials
import pandas as pd
from simple_salesforce import Salesforce
from API.config import sf_credentials, notion_credentials

# Use notion_credentials instead of undefined variables
notion_token = notion_credentials["notion_token"]
notion_database_id = notion_credentials["notion_database_id"]

# Notion API endpoint URLs
NOTION_API_URL = "https://api.notion.com/v1"

# Headers for Notion API request
headers = {
    "Authorization": f"Bearer {notion_token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",  # Update to the latest version
}

# Authenticate with Salesforce
sf = Salesforce(
    username=sf_credentials["username"],
    password=sf_credentials["password"],
    security_token=sf_credentials["security_token"],
    consumer_key=sf_credentials["consumer_key"],
    consumer_secret=sf_credentials["consumer_secret"],
)

# Query active cases from Salesforce
query = "SELECT Id, CaseNumber, Subject FROM Case WHERE Status = 'New'"
result = sf.query_all(query)
records = result["records"]

# Transform Salesforce data to a DataFrame
df = pd.DataFrame([{"CaseNumber": record["CaseNumber"], "Subject": record["Subject"]} for record in records])

import requests

# Create a Notion card
def create_notion_card(title, description):
    # Construct the page URL directly
    page_url = f"{NOTION_API_URL}/pages"

    data = {
        "parent": {"database_id": notion_database_id},
        "properties": {
            "title": [{"text": {"content": title}}],
            "Description": [{"text": {"content": description}}],
        },
    }

    response = requests.post(page_url, headers=headers, json=data)

    if response.status_code == 200:
        print("Notion card created successfully.")
    else:
        print(f"Failed to create Notion card. Status code: {response.status_code}")
        print(response.json())

# Create a Notion card with Salesforce data
for _, row in df.iterrows():
    case_number, subject = row["CaseNumber"], row["Subject"]
    title, description = f"Case: {case_number}", f"{subject}"

    create_notion_card(description, title)
    # Additional print statements for debugging
    print(f"\nCreating Notion card for Case: {case_number}")
    print(f"Title: {description}")
    print(f"Description: {title}")
