import requests
from bs4 import BeautifulSoup
import re

baseurl = 'https://www.bourbonbanter.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
}

r = requests.get('https://www.bourbonbanter.com/topic/scotch-whisky-reviews/')

soup = BeautifulSoup(r.content, 'lxml')

whiskeyList = []

productList = soup.find_all('article', class_='post')

productLinks = []

for item in productList:
    link = item.find('a', href=True)
    if link:
        full_link = baseurl + link['href']
        if full_link not in productLinks: 
            productLinks.append(full_link)

# testlink = 'https://www.bourbonbanter.com/sneaky-peat-whiskey-review/'

for link in productLinks:
    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('h1', class_='article-title').text

    all_li = soup.find_all('li')
    all_p = soup.find_all('p')

    for li in all_li:
        if 'MSRP' in li.text:
            price = li.text.split('MSRP:')[-1].strip()
        if 'PROOF' in li.text:
            proof = li.text.split('PROOF:')[-1].strip()

    for p in all_p:
        if 'APPEARANCE' in p.text:
            appearance = p.text.split('APPEARANCE:')[-1].strip()
        if 'NOSE' in p.text:
            nose = p.text.split('NOSE:')[-1].strip()
        if 'PALATE' in p.text:
            palate = p.text.split('PALATE:')[-1].strip()

    whisky = {
        'name': name,
        'proof': proof,
        'appearance': appearance,
        'nose': nose,
        'palate': palate,
        'price': price
    }

    print('Saving: ', whisky['name'])
    whiskeyList.append(whisky)

with open('index.html', 'r') as file:
    html_content = file.read()

whisky_template = """
<div class="whisky">
    <h2 class="title">{name}</h2>
    <p class="proof">{proof}</p>
    <p class="appearance">{appearance}</p>
    <p class="nose">{nose}</p>
    <p class="palette">{palate}</p>
    <p class="price">{price}</p>
</div>
"""

whisky_divs = ""

for whisky in whiskeyList:
    whisky_div = whisky_template.format(
        name=whisky['name'],
        proof=whisky['proof'] if whisky['proof'] else 'N/A',
        appearance=whisky['appearance'] if whisky['appearance'] else 'N/A',
        nose=whisky['nose'] if whisky['nose'] else 'N/A',
        palate=whisky['palate'] if whisky['palate'] else 'N/A',
        price=whisky['price'] if whisky['price'] else 'N/A'
    )
    whisky_divs += whisky_div

html_content = re.sub(r'<div class="whisky">.*?</div>', whisky_divs, html_content, flags=re.DOTALL)

with open('whiskeys.html', 'w') as file:
    file.write(html_content)

print("Data has been saved to whiskeys.html")