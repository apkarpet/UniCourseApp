import re 
import requests 
import time 

# Define URL:
url = "https://www.python.org"

# Fetch page content
response = requests.get(url)

# Count execution time 
start = time.time()

# Use of Regular Expressions to find the contents of <title>
title = re.findall(r'<title>(.*?)</title>', response.text)

end = time.time()

# Check if title was found and print results
if title:
    print(f"Regex found: {title[0]} in {(end-start)*1000 :.3f} ms")
else:
    print("No title found.")

