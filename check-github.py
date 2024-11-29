import requests
import config

headers = {
    "Authorization": f"token {config.GITHUB_TOKEN}"
}

url = f'https://api.github.com/user/repos'

while url:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repositories = response.json()
        
        # Print all repositories
        for repo in repositories:
            repo_name = repo['name']
            
            # Fetch branches
            branches_url = f"https://api.github.com/repos/{config.GITHUB_USERNAME}/{repo_name}/branches"
            branches_response = requests.get(branches_url, headers=headers)
            
            branches = []
            if branches_response.status_code == 200:
                branches_data = branches_response.json()
                branches = [branch['name'] for branch in branches_data]
            
            # Fetch tags
            tags_url = f"https://api.github.com/repos/{config.GITHUB_USERNAME}/{repo_name}/tags"
            tags_response = requests.get(tags_url, headers=headers)
            
            tags = []
            if tags_response.status_code == 200:
                tags_data = tags_response.json()
                tags = [tag['name'] for tag in tags_data]
            
            # Print the repository name, branches, and tags in the desired format
            print(f"\n{repo_name}")
            print(f" - branches: {', '.join(branches) if branches else ''}")
            print(f" - tags: {', '.join(tags) if tags else ''}")

        # GitHub paginated response uses a "Link" header to provide next page info
        if 'Link' in response.headers:
            links = response.headers['Link']
            next_page = [link.split(";")[0].strip("<>") for link in links.split(",") if 'rel="next"' in link]
            url = next_page[0] if next_page else None
        else:
            url = None

    else:
        print(f"Error occurred: {response.status_code} - {response.text}")
        break
