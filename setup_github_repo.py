import os
from github import Github
from github.GithubException import GithubException

def main():
    # Try to get the token from environment variable
    token = os.environ.get("GITHUB_TOKEN")
    
    # If not found, look for it in the access-token.txt file
    if not token:
        try:
            with open("access-token.txt", "r") as f:
                token = f.read().strip()
        except FileNotFoundError:
            pass
            
    if not token:
        token = input("Please enter your GitHub Personal Access Token: ").strip()

    if not token:
        print("Error: GitHub token is required.")
        return

    try:
        # Authenticate to GitHub
        g = Github(token)
        user = g.get_user()
        
        repo_name = "PhonePe-Transaction-Insights"
        repo_desc = "End-to-end data science project on PhonePe Pulse dataset — EDA, ML models, and interactive Streamlit dashboard"
        
        print(f"Authenticated as {user.login}")
        print(f"Creating repository '{repo_name}'...")
        
        # Create a new public repository
        try:
            repo = user.create_repo(
                name=repo_name,
                description=repo_desc,
                private=False,
                auto_init=False # We will push our local files
            )
            print(f"Repository successfully created! URL: {repo.html_url}")
        except GithubException as e:
            if e.status == 422:
                print(f"Repository '{repo_name}' already exists. Attempting to use existing repo...")
                repo = user.get_repo(f"{user.login}/{repo_name}")
            else:
                raise e
        
        # Files to upload
        files_to_upload = [
            "config.py",
            "data_extraction.py",
            "sql_schema.sql",
            "EDA_Notebook.ipynb",
            "ML_Notebook.ipynb",
            "app.py",
            "requirements.txt",
            "README.md",
            ".gitignore"
        ]
        
        print("Uploading files to GitHub...")
        for file_path in files_to_upload:
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    content = file.read()
                    
                file_name = os.path.basename(file_path)
                try:
                    # Check if file already exists in repo
                    try:
                        contents = repo.get_contents(file_name)
                        repo.update_file(contents.path, f"Update {file_name}", content, contents.sha)
                        print(f"Updated {file_name}")
                    except GithubException:
                        # File doesn't exist, create it
                        repo.create_file(file_name, f"Add {file_name}", content)
                        print(f"Added {file_name}")
                except Exception as e:
                    print(f"Failed to upload {file_name}: {e}")
            else:
                print(f"Warning: File {file_path} not found locally. Skipping.")
                
        print(f"\nAll done! Check your repository here: {repo.html_url}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
