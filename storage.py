import requests
import uuid
from config import SUPABASE_URL, SUPABASE_KEY

def upload_pdf(file):
    file.seek(0)

    file_id = str(uuid.uuid4())

    url = f"{SUPABASE_URL}/storage/v1/object/sales_pdfs/{file_id}.pdf"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/pdf"
    }

    response = requests.put(url, headers=headers, data=file.read())

    if response.status_code not in [200, 201]:
        print(response.text)
        raise Exception("Upload failed")

    file_url = f"{SUPABASE_URL}/storage/v1/object/public/sales_pdfs/{file_id}.pdf"

    return file_id, file_url