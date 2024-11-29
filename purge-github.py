import requests
import config

# Warning message before executing
print("WARNING: This script will delete ALL repositories on the specified GitHub account. Are you sure you want to proceed? (yes/no)")

# Ask for confirmation
confirmation = input().strip().lower()

if confirmation != 'yes':
    print("Aborted. No repositories were deleted.")
    exit()

API_URL = "https://api.github.com"

def get_repositories(username, token):
    """Fetches all repositories of the specified user."""
    url = f"{API_URL}/user/repos"
    headers = {"Authorization": f"token {token}"}
    params = {"type": "owner", "per_page": 100}  # Only repositories owned by the user
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching repositories: {response.status_code}")
        print(response.json())
        return []

def delete_repository(username, token, repo_name):
    """Deletes a repository from the specified user."""
    url = f"{API_URL}/repos/{username}/{repo_name}"
    headers = {"Authorization": f"token {token}"}
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"Successfully deleted: {repo_name}")
    else:
        print(f"Error deleting {repo_name}: {response.status_code}")
        print(response.json())

def main():
    repositories = get_repositories(config.GITHUB_USERNAME, config.GITHUB_TOKEN)

    if not repositories:
        print("No repositories available for deletion.")
        return

    print(f"{len(repositories)} repositories found. Starting deletion...")
    for repo in repositories:
        repo_name = repo["name"]
        delete_repository(config.GITHUB_USERNAME, config.GITHUB_TOKEN, repo_name)

    print("All repositories have been deleted!")

if __name__ == "__main__":
    main()
