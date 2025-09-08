from scrapling.fetchers import StealthyFetcher
from scrapling import Fetcher
import time

# Adaptive mod active
Fetcher.configure(adaptive=True, adaptive_domain="bbc.com")

def fetch_full_page_data(url, first_time=False):
    def scroll_page(page):
        for i in range(0, 5000, 500):
            page.mouse.wheel(0, 500)
            time.sleep(0.3) 
        return page

    # Open page with StealthyFetcher
    page = StealthyFetcher.fetch(
        url,
        headless=True,
        network_idle=False,
        timeout=120000,
        humanize=True,
        geoip=False,
        solve_cloudflare=False,
        page_action=scroll_page
    )

    # Tüm metin
    body = page.css_first(
        "body",
        auto_save=first_time,
        adaptive=not first_time
    ) or page.css_first("main") or page.css_first("article") or page.css_first("section")

    full_text = body.get_all_text(separator="\n", strip=True) if body else ""

    # Tüm başlıklar
    headers = [
        h.get_all_text(strip=True)
        for h in page.css("h1, h2, h3, h4, h5, h6", auto_save=first_time, adaptive=not first_time)
    ]

    # Tüm linkler
    links = []
    for a in page.css("a", auto_save=first_time, adaptive=not first_time):
        href = a.attrib.get("href") or a.attrib.get("data-href")
        if href and href not in links:
            links.append(href)

    # Tüm görseller
    images = []
    for img in page.css("img", auto_save=first_time, adaptive=not first_time):
        src = img.attrib.get("src") or img.attrib.get("data-src") or img.attrib.get("data-original")
        if src and src not in images:
            images.append(src)

    return {
        "text": full_text,
        "headers": headers,
        "links": links,
        "images": images
    }

#Test 
if __name__ == "__main__":
    url = "https://www.bbc.com/news"

    data = fetch_full_page_data(url, first_time=True)

    print("----- METİN -----")
    print(data["text"][:1000])
    print("\n----- BAŞLIKLAR -----")
    print(data["headers"])
    print("\n----- LİNKLER -----")
    print(data["links"][:20])
    print("\n----- GÖRSELLER -----")
    print(data["images"][:20])

    # Adaptive test
    print("\n\n--- ADAPTİF TEST ---")
    data2 = fetch_full_page_data(url, first_time=False)
    print(f"Adaptif modda bulunan başlık sayısı: {len(data2['headers'])}")
