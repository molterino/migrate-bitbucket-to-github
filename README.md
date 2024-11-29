
# Bitbucket to GitHub Migration Scripts

This package was created to simplify the migration process from Bitbucket to GitHub, as no straightforward, user-friendly solution was readily available. The scripts aim to make the transition as simple as possible, requiring minimal effort.

## Prerequisites

Before using the scripts, ensure you have the following:

1. **Bitbucket App Password**: Create an app password in Bitbucket with the necessary permissions to read repository information.
2. **GitHub Personal Access Token (PAT)**: Generate a PAT in GitHub with the required permissions to create new repositories.

## How to Use the Scripts

1. **Install Python 3**: Ensure Python 3 is installed on your system.
2. **Update the Configuration File**: Edit the `config.py` file to include your user credentials and other necessary details.
3. **Run the Desired Script**: Choose and execute the script that meets your needs. For example:  
   ```bash
   python check-bitbucket.py
   ```

## Script Descriptions

- **`config.py`**  
  Contains configuration fields for user credentials and settings. Fill these fields appropriately, as other scripts will rely on this file.

- **`check-bitbucket.py`**  
  Lists repositories, branches, and tags associated with a specified Bitbucket workspace.

- **`check-github.py`**  
  Lists repositories, branches, and tags linked to a GitHub account.

- **`migrate-bitbucket-to-github.py`**  
  The main script that performs the migration. It starts migrating repositories based on the provided configuration. After processing the first repository, it pauses and prompts the user to choose whether to:
  - Continue with the next repository.
  - Stop the migration process.
  - Migrate all remaining repositories without further prompts.

- **`purge-github.py`**  
  **Use with caution!** This script deletes all repositories linked to the specified GitHub account. Only use if you're certain about the action.

## Example Workflow

1. Generate the required app password and PAT.
2. Update the `config.py` file with your credentials.
3. Verify the repositories in Bitbucket using:
   ```bash
   python check-bitbucket.py
   ```
4. Optionally, review existing repositories in GitHub:
   ```bash
   python check-github.py
   ```
5. Begin the migration:
   ```bash
   python migrate-bitbucket-to-github.py
   ```
6. If necessary, clean up GitHub repositories with:
   ```bash
   python purge-github.py
   ```

## Notes

- The scripts were designed for ease of use, but ensure you understand the consequences of running them, especially destructive ones like `purge-github.py`.
- Make backups of your repositories before starting the migration process.

## License

This project is open-source and available under the [MIT License](LICENSE).
