import requests
from bs4 import BeautifulSoup

def get_static_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"error": f"Status code {response.status_code}"}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ""
        body_text = soup.get_text(separator=" ", strip=True)

        return {
            "title": title,
            "html": body_text  
        }
    except Exception as e:
        return {"error": str(e)}
