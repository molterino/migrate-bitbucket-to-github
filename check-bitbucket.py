import requests
import config
from requests.auth import HTTPBasicAuth

url = f"https://api.bitbucket.org/2.0/repositories/{config.BITBUCKET_WORKSPACE}"
auth = HTTPBasicAuth(config.BITBUCKET_USERNAME, config.BITBUCKET_APP_PASSWORD)

while url:
    # Fetch the current page
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        repositories = response.json()
        
        # Print all repositories
        for repo in repositories['values']:
            repo_name = repo['name']
            
            # Fetch branches
            branches_url = f"https://api.bitbucket.org/2.0/repositories/{config.BITBUCKET_WORKSPACE}/{repo_name}/refs/branches"
            branches_response = requests.get(branches_url, auth=auth)
            
            branches = []
            if branches_response.status_code == 200:
                branches_data = branches_response.json()
                if 'values' in branches_data:
                    branches = [branch['name'] for branch in branches_data['values']]
            
            # Fetch tags
            tags_url = f"https://api.bitbucket.org/2.0/repositories/{config.BITBUCKET_WORKSPACE}/{repo_name}/refs/tags"
            tags_response = requests.get(tags_url, auth=auth)
            
            tags = []
            if tags_response.status_code == 200:
                tags_data = tags_response.json()
                if 'values' in tags_data:
                    tags = [tag['name'] for tag in tags_data['values']]
            
            # Print the repository name, branches, and tags in the desired format
            print(f"\n{repo_name}")
            
            # Print branches (if available)
            print(f" - branches: {', '.join(branches) if branches else ''}")
            
            # Print tags (if available)
            print(f" - tags: {', '.join(tags) if tags else ''}")

        # If there is a next page, set the new URL
        url = repositories.get('next', None)

    else:
        print(f"Error occurred: {response.status_code} - {response.text}")
        break
