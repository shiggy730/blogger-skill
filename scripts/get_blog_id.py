#!/usr/bin/env python3
"""
Get your Blogger blog ID
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blogger_client import BloggerClient

def main():
    client = BloggerClient()
    
    url = "https://www.googleapis.com/blogger/v3/users/self/blogs"
    headers = {
        'Authorization': f'Bearer {client.get_access_token()}'
    }
    
    import requests
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'items' in data:
            print("📝 Your Blogger blogs:\n")
            for blog in data['items']:
                print(f"Name: {blog['name']}")
                print(f"URL: {blog['url']}")
                print(f"Blog ID: {blog['id']}")  # <-- This is what we need!
                print()
        else:
            print("No blogs found")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == '__main__':
    main()
