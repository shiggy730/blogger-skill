#!/usr/bin/env python3
"""
Blogger API Client - Handles authentication and API calls
"""

import json
import requests
from pathlib import Path
from datetime import datetime, timedelta

class BloggerClient:
    def __init__(self, credentials_path=None, token_path=None):
        self.credentials_path = credentials_path or Path.home() / "Documents/blogger_credentials.json"
        self.token_path = token_path or Path.home() / "Documents/blogger_token.json"
        
        self.credentials = self._load_credentials()
        self.tokens = self._load_tokens()
        
    def _load_credentials(self):
        with open(self.credentials_path, 'r') as f:
            return json.load(f)['installed']
    
    def _load_tokens(self):
        with open(self.token_path, 'r') as f:
            return json.load(f)
    
    def _save_tokens(self):
        with open(self.token_path, 'w') as f:
            json.dump(self.tokens, f, indent=2)
    
    def _refresh_access_token(self):
        """Refresh the access token using refresh token"""
        if 'refresh_token' not in self.tokens:
            raise Exception("No refresh token available. Re-run blogger_auth.py")
        
        data = {
            'client_id': self.credentials['client_id'],
            'client_secret': self.credentials['client_secret'],
            'refresh_token': self.tokens['refresh_token'],
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(self.credentials['token_uri'], data=data)
        
        if response.status_code == 200:
            new_tokens = response.json()
            self.tokens['access_token'] = new_tokens['access_token']
            self.tokens['expires_in'] = new_tokens['expires_in']
            self._save_tokens()
            print("✅ Access token refreshed")
        else:
            raise Exception(f"Failed to refresh token: {response.text}")
    
    def get_access_token(self):
        """Get valid access token, refreshing if needed"""
        # For simplicity, always refresh before API calls
        # In production, check expiry timestamp
        try:
            self._refresh_access_token()
        except:
            pass  # Use existing token if refresh fails
        
        return self.tokens['access_token']
    
    def create_post(self, blog_id, title, content, labels=None, is_draft=True, published_date=None):
        """Create a new blog post"""
        url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts"
        
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
        
        post_data = {
            'kind': 'blogger#post',
            'blog': {'id': blog_id},
            'title': title,
            'content': content
        }
        
        if labels:
            post_data['labels'] = labels if isinstance(labels, list) else [l.strip() for l in labels.split(',')]
        
        if published_date:
            post_data['published'] = published_date
        
        # Draft vs published
        params = {'isDraft': 'true' if is_draft else 'false'}
        
        response = requests.post(url, headers=headers, json=post_data, params=params)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Failed to create post: {response.status_code} - {response.text}")
    
    def list_posts(self, blog_id, max_results=10):
        """List recent posts"""
        url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts"
        
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}'
        }
        
        params = {'maxResults': max_results}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to list posts: {response.status_code} - {response.text}")
    
    def update_post(self, blog_id, post_id, title=None, content=None, labels=None):
        """Update an existing post"""
        url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/{post_id}"
        
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
        
        post_data = {}
        if title:
            post_data['title'] = title
        if content:
            post_data['content'] = content
        if labels:
            post_data['labels'] = labels if isinstance(labels, list) else [l.strip() for l in labels.split(',')]
        
        response = requests.patch(url, headers=headers, json=post_data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update post: {response.status_code} - {response.text}")
    
    def delete_post(self, blog_id, post_id):
        """Delete a post"""
        url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/{post_id}"
        
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}'
        }
        
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 204:
            return True
        else:
            raise Exception(f"Failed to delete post: {response.status_code} - {response.text}")
