
#from github import Github

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
      repositoryValue = input("Please, Specify the repository path in 'owner/repository' format  ")
      values = repositoryValue.split('/')
      owner_name = values[0]
      repositary_name = values[1]

   repositoryAnalyser_obj = GitHUbRepAnalyser()
   repositoryAnalyser_obj.collect_repository_data(owner_name, repositary_name)
   #repositoryAnalyser_obj.collect_pull_requests(owner_name, repositary_name)



main()