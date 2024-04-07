import requests
from bs4 import BeautifulSoup
import json
#site:ark.intel.com inurl:processor inurl:en
def getinfo(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        processor_name_element = soup.find('h1', class_='h1')
        if processor_name_element:
            processor_name = processor_name_element.text.strip()
        else:
            print("[ERROR] Processor name not found.")
        mrvar = {}
        mrvar['Name'] = processor_name
        specifications_section = soup.find('section', class_='specs-blade', id='tab-blade-1-0-1')
        if specifications_section:
            specifications = specifications_section.find_all('li')
            for spec in specifications:
                spec_label = spec.find('span', class_='label')
                spec_value = spec.find('span', class_='value')
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
    for mrline in mrlines:
        jsonsy = getinfo(mrline.replace('\n', ""))
        print(f"[INFO] Scraped {jsonsy['Name']}")
        with open("cpuinfo.json", 'a') as mrfile2:
            json.dump(jsonsy, mrfile2, indent=4)
print('[INFO] Finished')
