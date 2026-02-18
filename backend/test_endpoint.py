
import urllib.request
import json
import urllib.parse

try:
    base_url = "http://127.0.0.1:8000/api/houses/search_recommend/"
    params = {
        "price": 25000,
        "beds": 2,
        "baths": 1
    }
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"
    
    print(f"Testing {url}...")
    
    with urllib.request.urlopen(url) as response:
        if response.status == 200:
            data = json.loads(response.read().decode())
            print(f"Success! Got {len(data)} recommendations.")
            if len(data) > 0:
                print("First recommendation:", data[0]['title'])
        else:
            print(f"Failed with status {response.status}")

except Exception as e:
    print(f"Error: {e}")
