# GitSearch_OnlyGit
Display information of a repo using only Git

## Usage
python3 gitSearch_OnlyGit.py "insert_git_clone_link"

## Extra Information
1. If you want to find the creator of a repository, you will need to use the `GitHub API` to get the repository's information, where you can find the creator's information.
2. Git requires regex to retrieve information of contributor. Using `GitPython` lib to address this
3. information of open pull requests requires API
4. If the repo has any forks, it will continue to be accessble. Only API can check if a repo has any Fork https://stackoverflow.com/questions/48918302/how-to-check-whether-i-have-a-fork-of-a-given-github-repo 
