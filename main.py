
#from github import Github

import csv
from datetime import datetime
import os
from bs4 import BeautifulSoup
import requests
import configparser


#Global Variables to carry the frequestly used values
owner_name =""
repositary_name = ""
users = []



class GitHUbRepAnalyser:

    
    def __init__(self):
       self.repositories = []
       #Access token to avoid the rate of limit for accesing the github
       tokenChunks = ["ghp_", "8hNf7", "rJKtiBNG", "snDiWVK", "WN8hRwz", "8Ia2ef6g1"]
       tokenValue = ''.join(tokenChunks)
       '''with open("secret/secret.txt") as secret:
          tokenValue = secret.readlines()[0]
       config = configparser.ConfigParser()
       config.read('config.ini')'''

       #print(os.environ.get('GITHUB_TOKEN'))
       #print(config['GitHub']['token'])
       self.access_token = tokenValue
       self.headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3+json'
       }

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

        #print("Auth is: ",self.access_token, " Header is : ", self.headers)


        #Requesting GitHUb API with required details
        response = requests.get(url, headers=self.headers)
        
        #Validating the Response Status code 
        if response.status_code == 200:
            print("Repository Data - Request Successful - Ok : ", response.status_code)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.json()['message']}")
        
            
        repo_data = response.json()

        
        description = repo_data.get('description', '')
        homepage = repo_data.get('homepage', '')
        license = repo_data.get('license', {}).get('name', '')
        forks = repo_data.get('forks_count', 0)
        watchers = repo_data.get('watchers_count', 0)
        currentDate = datetime.now()

        
        print(owner, repo_name, description, homepage, license, forks, watchers)

        #Pring the same in a readable format
        print(f"The Details of Repository \" {repo_name} \" Owned by {owner} are below")
        print(f"\t Description : {description} \n\t HomePage : {homepage} \n\t License : {license} \n\t Forks : {forks} \n\t Watchers : {watchers}, \n\t Date collected : {currentDate}")



        # Creating object for Repositary class to store the required details fetched 
        repoData_obj = Repository(owner, repo_name, description, homepage, license, forks, watchers)
        self.repositories.append(repoData_obj)

        #to check the values being passed - personal self validation 
        #repoData_obj.check()

    
    def collect_pull_requests(self, owner, repo_name):
        #GitHub API to collect pull requests data
        url = f'https://api.github.com/search/issues?q=is:pr+repo:{owner}/{repo_name}'

        #Requesting GitHUb API with required details
        response = requests.get(url,headers=self.headers)

        #Validating the Response Status code 
        if response.status_code == 200:
            print(" Pull Request - Request Successful - Ok : ", response.status_code)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.json()['message']}")
   

        pull_request_data = response.json().get('items', [])

        #print("Pull Request data is : ")
       # print(pull_request_data) 

        #To be commented
        #print("Total Pull requests fetched :", len(pull_request_data))
        

        

        #user response
        decision = input("If you would like to access only First page of Pull Requests press(Y) or Press(N) for accessing all the pages of Pull Request : ")
        every_Page_Response = input(" Would you like to receive a notification to proceed before moving to every new page Y/N : ")

        #PullRequest objects corresponding repository details
        if(decision.lower() == 'y'):

            self.print_PullRequestsData(pull_request_data, owner, repo_name)

            ''' for pr in pull_request_data:
                title = pr.get('title', '')
                number = pr.get('number', '')
                body = pr.get('body', '')
                state = pr.get('state', '')
                created_at = pr.get('created_at', '')
                closed_at = pr.get('closed_at', '')
                user = pr.get('user', {}).get('login', '')

                if(count < 5):
                    print(f"The Details of PR : {number} are :")
                    print(f"\t Title : {title} \n\t Body : {body} \n\t State : {state} \n\t Created : {created_at} \n\t Closed : {closed_at} \n\t User : {user}")
                    count += 1
                elif(count == 5):
                    print("If you want all the pull request details please, visit PullRequests.csv file in current directory/Folder.")
                    count += 1
            

                # Additional query to get details like commits, additions, deletions, changed_files
                pr_details = self.get_pull_request_details(owner, repo_name, number)

                # creating obj for PullRequest class  
                pull_request = PullRequest(title, number, body, state, created_at, closed_at, user, **pr_details)
                #self.save_as_csv('PullRequests.csv', pull_request)
                repo = next((r for r in self.repositories if r.owner == owner and r.name == repo_name), None)
                if repo:
                    repo.pull_requests.append(pull_request)'''

        elif(decision.lower() == 'n'):
            self.print_PullRequestsData(pull_request_data, owner, repo_name)
            '''for pr in pull_request_data:
                title = pr.get('title', '')
                number = pr.get('number', '')
                body = pr.get('body', '')
                state = pr.get('state', '')
                created_at = pr.get('created_at', '')
                closed_at = pr.get('closed_at', '')
                user = pr.get('user', {}).get('login', '')

                if(count < 5):
                    print(f"The Details of PR : {number} are :")
                    print(f"\t Title : {title} \n\t Body : {body} \n\t State : {state} \n\t Created : {created_at} \n\t Closed : {closed_at} \n\t User : {user}")
                    count += 1
                elif(count == 5):
                    print("If you want all the pull request details please, visit PullRequests.csv file in current directory/Folder.")
                    count += 1
            

                # Additional query to get details like commits, additions, deletions, changed_files
                pr_details = self.get_pull_request_details(owner, repo_name, number)

                # creating obj for PullRequest class  
                pull_request = PullRequest(title, number, body, state, created_at, closed_at, user, **pr_details)
                #self.save_as_csv('PullRequests.csv', pull_request)
                repo = next((r for r in self.repositories if r.owner == owner and r.name == repo_name), None)
                if repo:
                    repo.pull_requests.append(pull_request)'''

            while 'next' in response.links:
                next_page_url = response.links['next']['url']
                response = requests.get(next_page_url)
                data = response.json()
                pull_requests = data.get('items', [])
                self.print_PullRequestsData(pull_requests, owner, repo_name)
                if every_Page_Response.lower() == 'y':
                    nextpage = input("Would you like to access the next page of Pull Requests Y/N : ")
                    if nextpage.lower() == 'n':
                        break



    def get_pull_request_details(self, owner, repo_name, number):
        # query to get details like commits, additions, deletions, changed_files
        url = f'https://api.github.com/repos/{owner}/{repo_name}/pulls/{number}'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print("Request Un-Successfull : ", response.status_code)
        #else:
            # Print an error message if the request was not successful
            #print(f"Error: {response.status_code} - {response.json()['message']}")

        
        pr_details = response.json()

        commits = pr_details.get('commits', 0)
        additions = pr_details.get('additions', 0)
        deletions = pr_details.get('deletions', 0)
        changed_files = pr_details.get('changed_files', 0)

        return {'commits': commits, 'additions': additions, 'deletions': deletions, 'changed_files': changed_files}
    
    def print_PullRequestsData(self, pull_request_data,owner,repo_name):
        count =0
        for pr in pull_request_data:
                title = pr.get('title', '')
                number = pr.get('number', '')
                body = pr.get('body', '')
                state = pr.get('state', '')
                created_at = pr.get('created_at', '')
                closed_at = pr.get('closed_at', '')
                user = pr.get('user', {}).get('login', '')

                if(count < 5):
                    print("\n","*"*50)
                    print(f"The Details of PR : {number} are :")
                    print(f"\t Title : {title} \n\t Body : {body} \n\t State : {state} \n\t Created : {created_at} \n\t Closed : {closed_at} \n\t User : {user}")
                    count += 1
                elif(count == 5):
                    print("If you want all the pull request details please, visit PullRequests.csv file in current directory/Folder.")
                    count += 1
            

                # Additional query to get details like commits, additions, deletions, changed_files
                pr_details = self.get_pull_request_details(owner, repo_name, number)

                # creating obj for PullRequest class  
                pull_request = PullRequest(title, number, body, state, created_at, closed_at, user, **pr_details)
                #self.pr_csv('PullRequests.csv', pull_request)
                repo = next((r for r in self.repositories if r.owner == owner and r.name == repo_name), None)
                if repo:
                    repo.pull_requests.append(pull_request)

    def get_Data(self, url):
        response = requests.get(url,headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None


    def collect_user_data(self, username, repo_name):
        # Use GitHub API to collect user data
        url = f'https://api.github.com/repos/{username}/{repo_name}/contributors'

        response = requests.get(url,headers=self.headers)
        #To  Check the status code for the response received
        if response.status_code == 200:
            print("Request Successful - Ok : ", response.status_code)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.json()['message']}")

        user_data = response.json()

        #print("User Dtaa retrived is below : ", user_data)
        #print("Stauscode for the request under collecting user data is : ", response.status_code)

        # Print the content of the request
        #print(response.content)

        # Filter contributors by the desired_username
        user_contributions = [contributor for contributor in user_data if contributor['login'] == username]

        if user_contributions:
            print(f"Details of user {username}:")
            #print(user_contributions[0])  # Prints the details of user
        else:
            print(f"Given User {username} is inactive among the contributors. Please try with different user name")
            username = input("If you would like to get information about one of these users, enter the username here: ")
            self.collect_user_data(username, repo_name)      


        '''if isinstance(user_data, list) and user_data:
            # Check if user_data is a non-empty list
            first_user = user_data[0]  # Access the first user's data
            repositories = first_user.get('public_repos', 0)
            followers = first_user.get('followers', 0)
            following = first_user.get('following', 0)
            contributions = self.scrape_user_contributions(username)
            
        else:
            #Yet to implement Try catch for this issue
            print("Invlid format of accessing the data")'''
        

        specific_User_data = user_contributions[0]
        # Extracting relevant information
        '''repositories = specific_User_data.get('public_repos', 0)
        followers = specific_User_data.get('followers', 0)
        following = specific_User_data.get('following', 0)
        UserCOntibutions = specific_User_data.get('contributions', 0)
        contributions = self.scrape_user_contributions(username)
        #contributions = ""'''

        followers_url = f'https://api.github.com/users/{username}/followers'
        following_url = f'https://api.github.com/users/{username}/following'
        repos_url = f'https://api.github.com/users/{username}/repos'


        # Get followers count
        followers_data = self.get_Data(followers_url)
        followers_count = len(followers_data) if followers_data else 0

        # Get following count
        following_data = self.get_Data(following_url)
        following_count = len(following_data) if following_data else 0

        # Get repositories count
        repos_data = self.get_Data(repos_url)
        repos_count = len(repos_data) if repos_data else 0

        #UserContibutions = specific_User_data.get('contributions')

        #print("**********", user_contributions[0]['contributions'])
        TotalContribution = user_contributions[0]['contributions']
        contributions_lastYear = self.scrape_user_contributions(username)

        #print("-------------- Contribution details from web scraping : \n ", contributions)
        # Creating object for user class

        user = User(username, repos_count, followers_count, following_count, contributions_lastYear)

        print(f"Details of user : {username} in repository {repo_name} are : ","\nUser : ", username, "\n repositories : ", repos_count, "\nFollowers : ", followers_count, "\n Following : ", following_count, "\nContributions in last year : ", contributions_lastYear, "\nTotal Contributions : ",TotalContribution,  )
        self.save_as_csv('users1.csv', user)

    def scrape_user_contributions(self, username):
        # To Scrape the user contributions from the GitHub profile page as per requirement
    
        url = f'https://github.com/{username}?tab=overview&from={datetime.now().year - 1}-12-01'
        response = requests.get(url)
        
        soup = BeautifulSoup(response.content, 'lxml')
        contributions_tag = soup.find('h2', class_='f4 text-normal mb-2')
        
        contributions = contributions_tag.text.strip().split()[0] if contributions_tag else '0'
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
    global users
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
        users.append(user)

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



#def main():
#   global users
#   print(" Choose one of the bleow options to start exploring & analysing the Repository")
#   print("1. If you would like to specify the names of Owner & the repository")
#   print("2. If you would like to provide details in below format owner/repository")
#   print("Hint: you get the above deatails from top left corner of the github page you are looking")
   
#   choice = int(input("Enter your choice of input format"))
#   if choice == 1:
#      owner_name = input("Please Enter the Owner name : ")
#      repositary_name = input("Please Enter the Repositary name : ")
#   elif choice == 2:
#      repositoryValue = input("Please, Specify the repository path in 'owner/repository' format : ")
#      values = repositoryValue.split('/')
#      owner_name = values[0]
#      repositary_name = values[1]

#   ''' #check the rate linit for the github access 
#   url = f'https://api.github.com/repos/{owner_name}/{repositary_name}/rate_limit'
#   headers = {'Authorization': 'token YOUR-OAUTH-TOKEN'}
#   response = requests.get(url, headers=headers)

#    # Print the rate limit information
#   print("Rate of limit is : \n",response.json())'''

#   repositoryAnalyser_obj = GitHUbRepAnalyser()
#   repositoryAnalyser_obj.collect_repository_data(owner_name, repositary_name)
#   repositoryAnalyser_obj.collect_pull_requests(owner_name, repositary_name)
   
#   #Code to display the list of uses that are gathered from pull requests
#   '''url = f'https://api.github.com/users'
#   response = requests.get(url)
#   user_data = response.json()
#   print("User Data is : \n")

#   print(user_data)'''

#   print("Below are the list of User Names  : \n ")
#   new_names = list(set(users))
#   print(new_names)

#   #To the user name as input to collect the details
#   UserName_to_collectDetails = input("Enter the User name from the above list that you are interested in collect the details :  ")
#   repositoryAnalyser_obj.collect_user_data(UserName_to_collectDetails, repositary_name)



### MAIN MENU ### 
import pandas as pd
import matplotlib.pyplot as plt

# should make some of these in functions in the GitHUbRepAnalyser Class
# need to add pull requests to Users class 

# main function with menu 
def main():
    global users # declare users as global variable 

    # create instances of the GitHUbRepAnalyser class and User class 
    rep_analyzer = GitHUbRepAnalyser()
    
    while True:
        '''print("\nWelcome to the *GIT HUB Repository analyser* application. \nThis is the main menu; please select one of the following options.\n")
        print("1. Collect data for a specific GitHub repository")
        print("2. Show all repositories collected")
        print("3. Create and store visual representation data about all the repositories")
        print("4. Calculate the correlation between the data collected for the users")
        print("5. To Exit")'''

        print("╔══════════════════════════════════════════════════╗")
        print("║     Welcome to the GIT HUB Repository Analyser   ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║ This is the main menu : please select an option  ║")
        print("║                                                  ║")
        print("║ 1. Collect data for a specific GitHub repository ║")
        print("║                                                  ║")
        print("║ 2. Show all collected repositories               ║")
        print("║                                                  ║")
        print("║ 3. Create and store visual representation of data║")
        print("║    for all repositories                          ║")
        print("║                                                  ║")
        print("║ 4. Calculate correlation between collected       ║")
        print("║     user data                                    ║")
        print("║                                                  ║")
        print("║ 5. Exit                                          ║")
        print("╚══════════════════════════════════════════════════╝")

        # get user input 
        userchoice= input("Enter your choice : ")
    
        # Collect data from a specific GitHub repository using owner and repository name 
        if userchoice == '1':
            try:
                print("Hint: you can get the owner and repository name from the top left corner of the GitHub page you are looking at")
                rep = input("Enter the name of the repository: ") # get repository name
                owner = input("Enter the name of the repository owner: ") # get owner name 
    
                # get repository data 
                rep_analyzer.collect_repository_data(owner, rep)
                # get pull request data 
                rep_analyzer.collect_pull_requests(owner, rep)
                # get user data 
                print("The following are the usernames collected from pull requests: ")
                print(list(set(users))) 
                username = input("If you would like to get information about one of these users, enter the username here: ")
                rep_analyzer.collect_user_data(username, rep)
            except Exception as e:
                print(f"An error occurred: {e}")

        # Show all repositories collected (with submenu of actions possible on each repo)
        elif userchoice == '2':
            # show all repositories collected 
            for rep in rep_analyzer.repositories:
                print(rep.name)
            while True:
                # submenu options
                print("\nPlease select one of the following submenu options: ")
                print("1. Show all pull requests from a certain repository")
                print("2. Show the summary of a repository")
                print("3. Create and store visual representation data about the repository")
                print("4. Calculate the correlation between all the numeric data in the pull requests for a repository")
                print("5. Return to the main menu")

                # get user input 
                userchoice_sub = input("Enter your choice: ")

                if userchoice_sub == '1':
                    # Show all pull requests from a certain repository
                    repo_name = input("Enter the name of repository: ") 
                    # locate the repository using name 
                    repo = next((r for r in rep_analyzer.repositories if r.name == repo_name), None)
                    if repo:
                        # print each pull request number and title
                        for pull in repo.pull_requests:
                            print(f"Pull request {pull.number}, {pull.title}") 
                    else:
                        print(f"Repository '{repo_name}' not found.")
                    
                elif userchoice_sub == '2':
                    # Show the summary of a repository
                    repo_name = input("Enter the name of repository: ") 
                    # locate the repository using name 
                    repo = next((r for r in rep_analyzer.repositories if r.name == repo_name), None)
                    if repo:
                        # Number of pull requests in `open` state
                        num_open = sum(1 for pull in repo.pull_requests if pull.state == 'open')
                        # Number of pull requests in `closed` state
                        num_close = sum(1 for pull in repo.pull_requests if pull.state == 'closed')
                        # Number of users
                        num_users = len(set(pull.user for pull in repo.pull_requests))
                        # Date of the oldest pull request
                        old_date = min(pull.created_at for pull in repo.pull_requests)                        
                    else:
                        print(f"Repository '{repo_name}' not found.")    
                        
                    # print summary 
                    print(f"Summary for {repo_name}")
                    print(f"Number of pull requests in `open` state: {num_open}")
                    print(f"Number of pull requests in `closed` state: {num_close}")
                    print(f"Number of users: {num_users}")
                    print(f"Date of the oldest pull request: {old_date}")
                
                elif userchoice_sub == '3':
                    # Create and store visual representation data about the repository
                    repo_name = input("Enter the name of repository: ") 
                    # locate the repository using name 
                    repo = next((r for r in rep_analyzer.repositories if r.name == repo_name), None)
                    if repo:
                        # get all data
                        rep_dat = {
                            'State': [pull.state for pull in repo.pull_requests], 
                            'Commits': [pull.commits for pull in repo.pull_requests], 
                            'Additions': [pull.additions for pull in repo.pull_requests], 
                            'Deletions': [pull.deletions for pull in repo.pull_requests], 
                            'Changed_files': [pull.changed_files for pull in repo.pull_requests], 
                            'Author_assoc': [pull.user for pull in repo.pull_requests], 
                        }

                        # convert to df 
                        rep_df = pd.DataFrame(rep_dat)
                                        
                        # A boxplot that compares closed vs. open pull requests in terms of number of commits
                        plt.figure(figsize=(min(12, len(rep_df) * 0.8), 8))
                        rep_df.boxplot(column = "Commits", by="State", grid = False)
                        plt.title("Boxplot Comparing Closed vs. Open Pull Requests")
                        plt.xlabel("Pull Request State")
                        plt.ylabel("Number of Commits")
                        plt.show()
                        
                        # A boxplot that compares closed vs. open pull requests in terms of additions and deletions
                        plt.figure(figsize=(min(12, len(rep_df) * 0.8), 8))
                        rep_df[["Additions", "Deletions", "State"]].boxplot(by="State", grid = False)
                        plt.title("Boxplot of Additions and Deletions for Open vs. Closed Pull Requests")
                        plt.xlabel("Pull Request State")
                        plt.ylabel("Count")
                        plt.show()
                        
                        # A boxplot that compares the number of changed files grouped by the author association
                        plt.figure(figsize=(min(12, len(rep_df) * 0.8), 8))
                        rep_df.boxplot(column = "Changed_files", by = "Author_assoc", grid=False)
                        plt.title("Boxplot of Changed Files Grouped by Author Associations")
                        plt.xlabel("Author Association")
                        plt.ylabel("Number of Changed Files")
                        plt.show()
                        
                        # A scatterplot that shows the relationship between additions and deletions
                        plt.figure(figsize=(min(12, len(rep_df) * 0.8), 8))
                        plt.scatter(rep_df["Additions"], rep_df["Deletions"])
                        plt.title("Scatterplot of Additions vs. Deletions")
                        plt.xlabel("Number of Additions")
                        plt.ylabel("Number of Deletions")
                        plt.show()
                        
                    else:
                        print(f"Repository '{repo_name}' not found.")    

                    
                elif userchoice_sub == '4':
                    # Calculate the correlation between all the numeric data in the pull requests for a repository
                    repo_name = input("Enter the name of repository: ") 
                    # locate the repository using name 
                    repo = next((r for r in rep_analyzer.repositories if r.name == repo_name), None)
                    if repo:
                        # get all data
                        rep_dat = {
                            'Commits': [pull.commits for pull in repo.pull_requests], 
                            'Additions': [pull.additions for pull in repo.pull_requests], 
                            'Deletions': [pull.deletions for pull in repo.pull_requests], 
                            'Changed_files': [pull.changed_files for pull in repo.pull_requests],
                        }

                        # convert to df 
                        rep_df = pd.DataFrame(rep_dat)

                        # get correlations 
                        corrs = rep_df.corr()
                        
                        # print 
                        print(f"Correlations for {repo_name} \n {corrs}")                     

                elif userchoice_sub == '5':
                    break
                else: 
                    print("\nPLEASE SELECT A VALID OPTION\n")       

        elif userchoice == '3':
            # Create and store visual representation data to a data frame for all the repositories
            if rep_analyzer.repositories:
                all_repo_data = []
                for repo in rep_analyzer.repositories:
                    rep_dat = {
                        'Name': repo.name,
                        'Num_pulls': len(repo.pull_requests),
                        'Num_open_pulls': sum(1 for pull in repo.pull_requests if pull.state == 'open'),
                        'Num_closed_pulls': sum(1 for pull in repo.pull_requests if pull.state == 'closed'),
                        'Num_users': len(set(pull.user for pull in repo.pull_requests)),
                    }
                    all_repo_data.append(rep_dat)
                    
                all_repo_df = pd.DataFrame(all_repo_data)
                    
                # A line graph showing the total number of pull requests per day
                plt.figure(figsize = (min(12, len(all_repo_df) * 0.8), 8))
                plt.plot(all_repo_df['Name'], all_repo_df['Num_pulls'], marker = 'o')
                plt.title("Total number of Pull Requests per Repository per Day")
                plt.xlabel("Repository Name")
                plt.ylabel("Number of Pull Requests")
                plt.xticks(rotation=45, ha = 'right')
                plt.show()
                
                # A line graph comparing number of open and closed pull requests per day
                plt.figure(figsize = (min(12, len(all_repo_df) * 0.8), 8))
                plt.plot(all_repo_df["Name"], all_repo_df["Num_open_pulls"], marker = "o", label = "Open Pull Requests")
                plt.plot(all_repo_df["Name"], all_repo_df["Num_closed_pulls"], marker = "o", label = "Closed Pull Requests")
                plt.title("Number of Open and Closed Pull Requests per Repository per Day")
                plt.xlabel("Repository Name")
                plt.ylabel("Number of Pull Requests")
                plt.legend()
                plt.xticks(rotation = 45, ha = 'right')
                plt.show()
                
                # A bar plot comparing the number of users per repository
                plt.figure(figsize=(min(12, len(all_repo_df) * 0.8), 8))
                plt.bar(all_repo_df["Name"], all_repo_df["Num_users"])
                plt.title("Number of Users per Repository")
                plt.xlabel("Repository Name")
                plt.ylabel("Number of Users")
                plt.xticks(rotation = 45, ha ="right")
                plt.show()
                
            else:
                print("No repositories found, please input a repository to learn more.")
            
        elif userchoice == '4':
            # Calculate the correlation between the data collected for the users - following, followers, 
            # number of pull requests, number of contributions, etc.
            if users:
                user_dat = {
                    'Following': [user.following for user in users], 
                    'Followers': [user.followers for user in users], 
                    'Num_pull' : [len(user.pull_requests) for user in users],     
                    'Num_contr' : [user.contributions for user in users]}
                
                # convert to df 
                user_df = pd.DataFrame(user_dat)

                # get correlations 
                corrs = user_df.corr()
                        
                # print 
                print(f"Correlations between data collected for users \n {corrs}")   

            else:
                print("No user data found.")
                        
        elif userchoice == '5':
            return None, None, None  # Exit the program
        else:
            print("\nPLEASE SELECT A VALID OPTION\n")
        
        




main()
