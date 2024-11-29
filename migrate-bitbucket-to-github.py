import os
import requests
import subprocess
import config

GITHUB_API_URL = "https://api.github.com/user/repos"
BITBUCKET_API_URL = f"https://api.bitbucket.org/2.0/repositories/{config.BITBUCKET_WORKSPACE}"

def get_bitbucket_repos():
    repos = []
    url = BITBUCKET_API_URL
    while url:
        response = requests.get(url, auth=(config.BITBUCKET_USERNAME, config.BITBUCKET_APP_PASSWORD))
        if response.status_code == 200:
            data = response.json()
            repos.extend(data['values'])
            url = data.get('next')  # Fetch the next page if it exists
        else:
            print(f"Error fetching Bitbucket API: {response.status_code}")
            break
    return repos

def create_github_repo(repo_name):
    url = GITHUB_API_URL
    headers = {
        "Authorization": f"token {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "name": repo_name,
        "private": True
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"GitHub repo created: {repo_name}")
        return True
    else:
        print(f"Error creating GitHub repo: {response.status_code}")
        return False

def migrate_repo(repo):
    repo_name = repo['name']
    print(f"\nMigrating repository: {repo_name}")
    
    if create_github_repo(repo_name):
        # Git clone from Bitbucket repository
        clone_url = f"https://{config.BITBUCKET_USERNAME}:{config.BITBUCKET_APP_PASSWORD}@bitbucket.org/{config.BITBUCKET_WORKSPACE}/{repo_name}.git"
        subprocess.run(["git", "clone", clone_url])
        os.chdir(repo_name)

        # Fetch all branches
        subprocess.run(["git", "fetch", "--all"])

        # Fetch all tags
        subprocess.run(["git", "fetch", "--tags"])

        # GitHub push
        github_url = f"https://{config.GITHUB_USERNAME}:{config.GITHUB_TOKEN}@github.com/{config.GITHUB_USERNAME}/{repo_name}.git"
        subprocess.run(["git", "remote", "set-url", "origin", github_url])

        # Push all branches explicitly
        remote_branches = subprocess.check_output(["git", "branch", "-r"]).decode().splitlines()
        for branch in remote_branches:
            # Exclude local (origin/branch) branches
            if "->" not in branch:  # If it's not an alias, it's a real branch
                branch_name = branch.strip().split("origin/")[-1]
                print(f"Pushing to the following branch: {branch_name}")
                
                # Checkout to the appropriate branch
                subprocess.run(["git", "checkout", branch_name])
                
                # Push the branch to GitHub
                subprocess.run(["git", "push", "origin", branch_name])

        # Push all tags
        subprocess.run(["git", "push", "--tags", "origin"])

        os.chdir("..")  # Go back to the previous directory
        print(f"'{repo_name}' repository successfully migrated to GitHub.")
    else:
        print(f"'{repo_name}' repository was not successfully created on GitHub.")

def main():
    repos = get_bitbucket_repos()
    print(f"{len(repos)} repositories found on Bitbucket.")
    
    migrate_all = False  # Flag to control if all remaining repositories should be migrated without prompts

    for repo in repos:
        # Migrate the current repository
        migrate_repo(repo)

        if not migrate_all:
            # Ask if the user wants to continue with the next repositories
            continue_migration_input = input("Do you want to continue migrating the next repository? (y/n/all) ")
            if continue_migration_input.lower() == 'all':
                migrate_all = True  # Set flag to migrate all repositories without further prompts
                print("Continuing migration for all remaining repositories.")
            elif continue_migration_input.lower() == 'n':
                print("Migration stopped.")
                break
            elif continue_migration_input.lower() != 'y':
                print("Invalid input. Migration stopped.")
                break

if __name__ == "__main__":
    main()
