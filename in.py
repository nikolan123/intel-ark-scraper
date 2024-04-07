import requests
from bs4 import BeautifulSoup

print("[INFO] Script started")
url = "https://ark.intel.com/content/www/us/en/ark.html#@Processors"
print(f"[INFO] Scraping {url}")

response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
links = soup.find_all("span", class_="name")

alllinks = []
counter = 0
for link in links:
    a_tag = link.find("a", class_="ark-accessible-color")
    if a_tag:
        href = a_tag.get("href")
        if "processor" in href:
            alllinks.append(f"https://ark.intel.com{href}")
            counter += 1
print(f"[INFO] Found {counter} links")

for url in alllinks:
    cpulinx = []
    print(f"[INFO] Scraping {url}")
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_links = soup.find_all('a')
        counter = 0
        for link in product_links:
            href = link.get('href')
            if href and "-processor-" in href and "products" in href and "/us/en/" in href:
                if "https://ark.intel.com" in href:
                    cpulinx.append(href)
                else:
                    cpulinx.append(f"https://ark.intel.com{href}")
                counter += 1
        print(f"[INFO] Found {counter} CPUs")
        with open('cpulinks.txt', 'a') as mrfile:
            for link in cpulinx:
                mrfile.write(f"{link}\n")

    else:
        print("[ERROR] Failed to retrieve the webpage")

with open('cpulinks.txt', 'r') as file:
    links = file.readlines()

dupes = len(links) - len(set(links))
ulinks = set(links)

with open('cpulinks.txt', 'w') as file:
    file.writelines(ulinks)

print(f"[INFO] Found {dupes} duplicates, removed")
print(f"[INFO] {len(ulinks)} links total, saved to cpulinks.txt")
