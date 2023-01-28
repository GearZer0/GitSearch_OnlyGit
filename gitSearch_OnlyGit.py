import git
import subprocess
import sys

def get_repo_info(repo_dir):
    # act like cd to the repo
    repo = git.Repo(repo_dir)

    # Repo info
    print("\nRepo Details:")
    print("\tName:", repo.git.rev_parse("--show-toplevel"))
    # get user ealiest commit thr git -log revsere
    earliest_commit = subprocess.run(['git', 'log', '--pretty=format:"%ci"', '--max-parents=0'], stdout=subprocess.PIPE, cwd=repo_dir)
    print("\tEarliest Commit:", earliest_commit.stdout.decode().splitlines()[-1])
    print("\tLatest Commit:", repo.head.commit.committed_datetime)
    # get the url of the github repo
    print("\tRemote Repository URL:", repo.remote().url)
    # get the branch name
    print("\tActive Branch Name:", repo.active_branch.name)
    print()
    
    # Creator info - not that to get author/ceator of repo requires the use of API
    user = repo.head.commit.author
    print("User Details:")
    print("\tLogin:", user.email)
    print("\tName:", user.name)
    print("\tEmail:", user.email)
    # get user ealiest commit thr gitpython lib
    user_commits = list(repo.iter_commits(author=user.email))
    first_commit_datetime = user_commits[-1].authored_datetime if user_commits else None
    print("\tEarliest Commit:", first_commit_datetime)
    print("\tLatest Commit:", repo.head.commit.committed_datetime)


    # Contributor info
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
