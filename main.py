
#from github import Github

import datetime
import os
from bs4 import BeautifulSoup
import requests

owner_name =""
repositary_name = ""

class GitHUbRepAnalyser:
    
    def __init__(self):
       self.repositories = []

    '''
   #alternate code to get the required details from the content received
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.g = Github()
        self.repo = self.g.get_repo(repo_name)
        self.repositories = []
    #alternate code to get the required details from the content received
    def get_details(self):
        details = {}
        details['name'] = self.repo.name
        details['description'] = self.repo.description
        details['url'] = self.repo.html_url
        details['created_at'] = self.repo.created_at.strftime('%Y-%m-%d %H:%M:%S')
        details['updated_at'] = self.repo.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        details['language'] = self.repo.language
        details['forks'] = self.repo.forks_count
        details['stars'] = self.repo.stargazers_count
        details['watchers'] = self.repo.watchers_count
        details['open_issues'] = self.repo.open_issues_count
        return details
   
    '''   

    def collect_repository_data(self, owner, repo_name):
        # Using GitHub API to collect repository data
        url = f'https://api.github.com/repos/{owner}/{repo_name}'
        response = requests.get(url)
        repo_data = response.json()

        
        description = repo_data.get('description', '')
        homepage = repo_data.get('homepage', '')
        license = repo_data.get('license', {}).get('name', '')
        forks = repo_data.get('forks_count', 0)
        watchers = repo_data.get('watchers_count', 0)

        
        print(owner, repo_name, description, homepage, license, forks, watchers)

        # Creating object for Repositary class to store the required details fetched 
        repoData_obj = Repository(owner, repo_name, description, homepage, license, forks, watchers)
        self.repositories.append(repoData_obj)

        #to check the values being passed
        repoData_obj.check()

    
    def collect_pull_requests(self, owner, repo_name):
        #GitHub API to collect pull requests data
        url = f'https://api.github.com/search/issues?q=is:pr+repo:{owner}/{repo_name}'
        response = requests.get(url)
        pull_request_data = response.json().get('items', [])

        #PullRequest objects corresponding repository details
        for pr in pull_request_data:
            title = pr.get('title', '')
            number = pr.get('number', '')
            body = pr.get('body', '')
            state = pr.get('state', '')
            created_at = pr.get('created_at', '')
            closed_at = pr.get('closed_at', '')
            user = pr.get('user', {}).get('login', '')
            
            # Additional query to get details like commits, additions, deletions, changed_files
            pr_details = self.get_pull_request_details(owner, repo_name, number)

            # creating obj for PullRequest class  
            pull_request = PullRequest(title, number, body, state, created_at, closed_at, user, **pr_details)
            repo = next((r for r in self.repositories if r.owner == owner and r.name == repo_name), None)
            if repo:
                repo.pull_requests.append(pull_request)

    def get_pull_request_details(self, owner, repo_name, number):
        # query to get details like commits, additions, deletions, changed_files
        url = f'https://api.github.com/repos/{owner}/{repo_name}/pulls/{number}'
        response = requests.get(url)
        pr_details = response.json()

        commits = pr_details.get('commits', 0)
        additions = pr_details.get('additions', 0)
        deletions = pr_details.get('deletions', 0)
        changed_files = pr_details.get('changed_files', 0)

        return {'commits': commits, 'additions': additions, 'deletions': deletions, 'changed_files': changed_files}
    
    def collect_user_data(self, username):
        # Use GitHub API to collect user data
        url = f'https://api.github.com/users/{username}'
        response = requests.get(url)
        user_data = response.json()

        # Extracting relevant information
        repositories = user_data.get('public_repos', 0)
        followers = user_data.get('followers', 0)
        following = user_data.get('following', 0)
        contributions = self.scrape_user_contributions(username)

        # Creating object for user class
        user = User(username, repositories, followers, following, contributions)
        self.save_as_csv('users.csv', user)

    def scrape_user_contributions(self, username):
        # To Scrape the user contributions from the GitHub profile page as per requirement
        url = f'https://github.com/{username}?tab=overview&from={datetime.datetime.now().year - 1}-12-01'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        #contributions_tag = soup.find('h2', class_='f4 text-normal mb-2')
        contributions = soup.find('h2', class_='f4 text-normal mb-2').text.strip().split()[0]
        #contributions = contributions_tag.text.strip().split()[0] if contributions_tag else '0'
        return int(contributions.replace(',', ''))
    
    def save_as_csv(self, filename, obj):
        # Check if the file exists
        if not os.path.isfile(filename):
            # Create the file with a header
            with open(filename, 'w') as file:
                file.write(obj.get_csv_header() + '\n')

        # Append a new line with the object in CSV format
        with open(filename, 'a') as file:
            file.write(obj.to_csv() + '\n')

#repo = GitHUbRepAnalyser('google/jax')
#details = repo.get_details()
#print(details)


class Repository:
    def __init__(self, owner, name, description, homepage, license, forks, watchers):
        self.owner = owner
        self.name = name
        self.description = description
        self.homepage = homepage
        self.license = license
        self.forks = forks
        self.watchers = watchers
        self.pull_requests = []

    def csv_Headers(self):
        return "owner,name,description,homepage,license,forks,watchers"

    def to_CSV(self):
        return f"{self.owner},{self.name},{self.description},{self.homepage},{self.license},{self.forks},{self.watchers}"

    def check(self):
        print("values in repository class")
        print(f"{self.owner},{self.name},{self.description},{self.homepage},{self.license},{self.forks},{self.watchers}")


class PullRequest:
    def __init__(self, title, number, body, state, created_at, closed_at, user, commits, additions, deletions, changed_files):
        self.title = title
        self.number = number
        self.body = body
        self.state = state
        self.created_at = created_at
        self.closed_at = closed_at
        self.user = user
        self.commits = commits
        self.additions = additions
        self.deletions = deletions
        self.changed_files = changed_files

class User:
    def __init__(self, username, repositories, followers, following, contributions):
        self.username = username
        self.repositories = repositories
        self.followers = followers
        self.following = following
        self.contributions = contributions

    def get_csv_header(self):
        return "username,repositories,followers,following,contributions"

    def to_csv(self):
        return f"{self.username},{self.repositories},{self.followers},{self.following},{self.contributions}"



def main():
   print(" Choose one of the bleow options to start exploring & analysing the Repository")
   print("1. If you would like to specify the names of Owner & the repository")
   print("2. If you would like to provide details in below format owner/repository")
   print("Hint: you get the above deatails from top left corner of the github page you are looking")
   


   choice = int(input("Enter your choice of input format"))
   if choice == 1:
      owner_name = input("Please Enter the Owner name : ")
      repositary_name = input("Please Enter the Repositary name : ")
   elif choice == 2:
      repositoryValue = input("Please, Specify the repository path in 'owner/repository' format : ")
      values = repositoryValue.split('/')
      owner_name = values[0]
      repositary_name = values[1]

   repositoryAnalyser_obj = GitHUbRepAnalyser()
   repositoryAnalyser_obj.collect_repository_data(owner_name, repositary_name)
   repositoryAnalyser_obj.collect_pull_requests(owner_name, repositary_name)
   
   #Code to display the list of uses that are gathered from Full requests



   #To the user name as input to collect the details
   UserName_to_collectDetails = input("Enter the User name from the above list that you are interested in collect the details :  ")
   repositoryAnalyser_obj.collect_user_data(UserName_to_collectDetails)


main()