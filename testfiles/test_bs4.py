import re 
import requests 
import time 
from bs4 import BeautifulSoup

url = "https://www.python.org"
response = requests.get(url)

# --- : BEAUTIFULSOUP (bs4) --- 
start_bs = time.time()
# Create analysis tree 
tree = BeautifulSoup(response.text, 'html.parser')
# Access "title"
title_bs = tree.title.string
end_bs = time.time()

print(f"BeautifulSoup found: {title_bs} in {(end_bs - start_bs)*1000:.3f} ms")
