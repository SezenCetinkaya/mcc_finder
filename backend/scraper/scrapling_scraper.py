from scrapling.fetchers import StealthyFetcher
import time

def fetch_full_page_data(url):
    def scroll_page(page):
        for i in range(0, 10000, 500):  
            page.mouse.wheel(0, 500)
            time.sleep(0.3) 
        return page

    page = StealthyFetcher.fetch(
        url,
        headless=True,
        network_idle=True,
        timeout=60000,  
        humanize=True,
        geoip=False,
        solve_cloudflare=False,
        page_action=scroll_page
    )

    # Tüm metin
    body = page.css_first("body")
    full_text = body.get_all_text(separator="\n", strip=True) if body else ""

    # Tüm başlıklar
    headers = [h.get_all_text(strip=True) for h in page.css("h1, h2, h3, h4, h5, h6")]

    # Tüm linkler
    links = [a.attrib.get("href") for a in page.css("a") if a.attrib.get("href")]

    # Tüm görseller
    images = []
    for img in page.css("img"):
        src = img.attrib.get("src") or img.attrib.get("data-src")
        if src:
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
    data = fetch_full_page_data(url)

    print("----- METİN -----")
    print(data["text"][:1000])  
    print("\n----- BAŞLIKLAR -----")
    print(data["headers"])
    print("\n----- LİNKLER -----")
    print(data["links"][:20])
    print("\n----- GÖRSELLER -----")
    print(data["images"][:20]) 