import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def fetch_emails_from_website(website_url):
    if not website_url:
        return None
    
    headers = {"User-Agent": "Mozilla/5.0"}
    checked_urls = set()

    def get_emails(url):
        try:
            print(f"擷取 {url}")
            resp = requests.get(url, headers=headers, timeout=5)
            text = resp.text
            emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))
            return emails, resp.text
        except Exception as e:
            print(f"抓取失敗: {e}")
            return set(), ""
    
    # 主頁先抓
    all_emails, html = get_emails(website_url)
    checked_urls.add(website_url)

    # 常見內頁路徑
    candidates = ["/contact", "/contact-us", "/about", "/about-us"]

    # 從主頁 HTML 抓可能內部連結
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if href and any(keyword in href.lower() for keyword in ["contact", "about", "support", "help", "faq"]):
            candidates.append(href)


    # 組成完整網址試抓
    for path in set(candidates):
        full_url = urljoin(website_url, path)
        if full_url in checked_urls:
            continue
        emails, _ = get_emails(full_url)
        all_emails.update(emails)
        checked_urls.add(full_url)
        if all_emails:
            break  # 找到就停

    # 嘗試子網域，例如 support.xxx.com
    if not all_emails:
        domain = urlparse(website_url).netloc
        scheme = urlparse(website_url).scheme
        subdomains = [f"support.{domain}", f"help.{domain}", f"faq.{domain}", f"service.{domain}"]
        for sub in subdomains:
            sub_url = f"{scheme}://{sub}"
            if sub_url in checked_urls:
                continue
            emails, _ = get_emails(sub_url)
            all_emails.update(emails)
            checked_urls.add(sub_url)
            if all_emails:
                break

    return list(all_emails) if all_emails else None
