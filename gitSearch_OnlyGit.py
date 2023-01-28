import subprocess
import sys
import re
import os
import git

def get_repo_info(repo_dir):
    repo = git.Repo(repo_dir)
    
    # User info
    user_email = subprocess.run(['git', 'log', '-1', '--pretty=format:"%ae"'], stdout=subprocess.PIPE, cwd=repo_dir).stdout.decode().strip('\"')
    user_name = subprocess.run(['git', 'log', '-1', '--pretty=format:"%an"'], stdout=subprocess.PIPE, cwd=repo_dir).stdout.decode().strip('\"')
    print("User Details:")
    print("\tLogin:", user_email)
    print("\tName:", user_name)
    earliest_commit = subprocess.run(['git', 'log', '--pretty=format:"%ci"', '--author=' + user_email, '--max-parents=0'], stdout=subprocess.PIPE, cwd=repo_dir)
    print("\tEarliest Commit:", earliest_commit.stdout.decode().splitlines()[-1])
    latest_commit = subprocess.run(['git', 'log', '-1', '--pretty=format:"%ci"'], stdout=subprocess.PIPE, cwd=repo_dir)
    print("\tLatest Commit:", latest_commit.stdout.decode().strip('\"'))

    # Repo info
    repo_name = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, cwd=repo_dir).stdout.decode().strip()
    print("\nRepo Details:")
    print("\tName:", repo_name)
    earliest_commit = subprocess.run(['git', 'log', '--pretty=format:"%ci"', '--max-parents=0'], stdout=subprocess.PIPE, cwd=repo_dir)
    print("\tEarliest Commit:", earliest_commit.stdout.decode().splitlines()[-1])
    latest_commit = subprocess.run(['git', 'log', '-1', '--pretty=format:"%ci"'], stdout=subprocess.PIPE, cwd=repo_dir)
    print("\tLatest Commit:", latest_commit.stdout.decode().strip('\"'))
    

    # Contributor info
    # using gitpython lib as it git requires the use of regex to extract the info of contributors
    contributors = set()
    print("\nContributor Details:")
    for commit in repo.iter_commits():
        if commit.author.email not in contributors:
            contributors.add(commit.author.email)
            author_commits = list(repo.iter_commits(author=commit.author.email))
            first_commit_datetime = author_commits[-1].authored_datetime if author_commits else None
            print("\tAuthor:", commit.author.email)
            print("\tAuthor login:", commit.author.email.split("@")[0])
            print("\tName:", commit.author.name)
            print("\tEmail:", commit.author.email)
            print("\tEarliest Commit:", first_commit_datetime)
            print("\tUpdated At:", commit.committed_datetime)
            print()

if __name__ == "__main__":
    # Get the repository link from the command line argument
    repo_link = sys.argv[1]
    # Clone the repository
    subprocess.run(["git", "clone", repo_link])
    print()
    repo_name = repo_link.split("/")[-1].split(".")[0]
    repo_dir = repo_name
    get_repo_info(repo_dir)
