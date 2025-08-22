from scraper.static_scraper import get_static_content
from scraper.dynamic_scraper import get_dynamic_content

url = "https://www.example.com"

static = get_static_content(url)
dynamic = get_dynamic_content(url)

print("STATIC:\n", static)
print("DYNAMIC:\n", dynamic)
