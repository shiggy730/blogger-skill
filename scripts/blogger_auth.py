#!/usr/bin/env python3
"""
Blogger API OAuth 2.0 Authorization Flow
"""

import json
import webbrowser
from urllib.parse import urlencode
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Load credentials
creds_path = Path.home() / '.blogger-skill' / 'blogger_credentials.json'
with open(creds_path, 'r') as f:
    creds = json.load(f)['installed']

# OAuth parameters
auth_params = {
    'client_id': creds['client_id'],
    'redirect_uri': 'http://localhost:8080',
    'response_type': 'code',
    'scope': 'https://www.googleapis.com/auth/blogger',
    'access_type': 'offline',
    'prompt': 'consent'
}

auth_url = f"{creds['auth_uri']}?{urlencode(auth_params)}"

print("=" * 70)
print("BLOGGER API AUTHORIZATION")
print("=" * 70)
print("\n1. Opening authorization URL in browser...")
print(f"\nURL: {auth_url}\n")
print("2. After authorizing, you'll be redirected to localhost:8080")
print("3. The authorization code will be captured automatically\n")

# Simple HTTP server to catch the redirect
class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authorization successful!</h1><p>You can close this window.</p></body></html>')
            print(f"\n✅ Authorization code received: {auth_code[:20]}...")
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress HTTP logs

auth_code = None

# Open browser
webbrowser.open(auth_url)

# Start server to catch redirect
PORT = 8080
with socketserver.TCPServer(("", PORT), OAuthHandler) as httpd:
    print(f"Listening on http://localhost:{PORT} for OAuth callback...")
    while auth_code is None:
        httpd.handle_request()

print("\n" + "=" * 70)
print("EXCHANGING CODE FOR TOKEN")
print("=" * 70)

# Exchange code for token
import requests

token_data = {
    'code': auth_code,
    'client_id': creds['client_id'],
    'client_secret': creds['client_secret'],
    'redirect_uri': 'http://localhost:8080',
    'grant_type': 'authorization_code'
}

response = requests.post(creds['token_uri'], data=token_data)

if response.status_code == 200:
    tokens = response.json()
    
    # Save tokens
    token_file = Path.home() / '.blogger-skill' / 'blogger_token.json'
    with open(token_file, 'w') as f:
        json.dump(tokens, f, indent=2)
    
    print(f"\n✅ Access token saved to: {token_file}")
    print(f"\nAccess Token: {tokens['access_token'][:30]}...")
    if 'refresh_token' in tokens:
        print(f"Refresh Token: {tokens['refresh_token'][:30]}...")
    print(f"\nExpires in: {tokens.get('expires_in', 'unknown')} seconds")
else:
    print(f"\n❌ Failed to exchange code for token")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
