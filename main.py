import requests
from bs4 import BeautifulSoup
import json
from time import sleep
#site:ark.intel.com inurl:processor inurl:en
def getinfo(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        processor_name_element = soup.find('title')
        if processor_name_element:
            processor_name = processor_name_element.text.strip()
        else:
            print("[ERROR] Processor name not found.")
        mrvar = {}
        mrvar['Name'] = processor_name
        mrvar['Ark URL'] = url
        specifications_section = soup.find('div', class_='tech-section', id='specs-1-0-1')
        if specifications_section:
            specifications = specifications_section.find_all('div', class_="tech-section-row")
            for spec in specifications:
                spec_label = spec.find('div', class_='tech-label').find('span')
                spec_value = spec.find('div', class_='tech-data').find('span')
                if spec_label and spec_value:
                    spec_label_text = spec_label.text.strip()
                    spec_value_text = spec_value.text.strip()
                    mrvar[spec_label_text] = spec_value_text
                else:
                    return "[ERROR] Specification data not found"
        else:
            return "[ERROR] Specifications section not found"
        return mrvar
    else:
        return "[ERROR] Failed to retrieve data from the website"
print("[INFO] Getting links from cpulinks.txt")
with open('cpulinks.txt', 'r') as mrfile:
    mrlines = mrfile.readlines()
    counter = 0
    for line in mrlines:
        counter += 1
    print(f"[INFO] Found {counter} links")
    for mrline in mrlines:
        counter -= 1
        try:
            jsonsy = getinfo(mrline.replace('\n', ""))
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Failed to get {mrline}")
        except Exception as e:
            print(f"[ERROR] Failed to get info for {mrline}: {e}")
        try:
            print(f"[INFO] Scraped {jsonsy['Name']}, {counter} more to do")
        except Exception as e:
            print(f"[INFO] Error {e}")
        with open("cpuinfo.json", 'a') as mrfile2:
            json.dump(jsonsy, mrfile2, indent=4)
            mrfile2.write(',')
print('[INFO] Finished')
