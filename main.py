
#from github import Github

import csv
from datetime import datetime
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Global Variables to carry the frequently used values
owner_name =""
repo_name = ""
users = []
ContributorDetailsRequByUser = []
repositoryAndOwner = {}

class GitHUbRepAnalyser:

    
    def __init__(self):
       self.repositories = []
       #Access token to avoid the rate of limit for accesing the github
       # tokenChunks = ["ghp_", "8hNf7", "rJKtiBNG", "snDiWVK", "WN8hRwz", "8Ia2ef6g1"]
       # tokenValue = ''.join(tokenChunks)
       with open("secret/secret.txt") as secret:
          tokenValue = secret.readlines()[0]

       self.access_token = tokenValue
       self.headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3+json'
       }

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
        homepage = repo_data['homepage'] if 'homepage' in repo_data and repo_data['homepage'] != '' else 'None'
        repo_license = repo_data.get('license')
        License = repo_license['name'] if repo_license and repo_license['name'] is not None else 'None'
        forks = repo_data.get('forks_count', 0)
        watchers = repo_data.get('watchers_count', 0)
        currentDate = datetime.now()
        
        #print(owner, repo_name, description, homepage, License, forks, watchers)

        # Print the same in a readable format
        print()
        print(f"The details for repository \"{repo_name}\" owned by {owner} are below")
        print(f"\t Description : {description} \n\t HomePage : {homepage} \n\t License : {License} \n\t Forks : {forks} \n\t Watchers : {watchers} \n\t Date collected : {currentDate}")



        # Creating object for Repository class to store the required details fetched 
        repoData_obj = Repository(owner, repo_name, description, homepage, License, forks, watchers)
        self.repositories.append(repoData_obj)

    
    def collect_pull_requests(self, owner, repo_name):
        #GitHub API to collect pull requests data
        url = f'https://api.github.com/search/issues?q=is:pr+repo:{owner}/{repo_name}'

        #Requesting GitHUb API with required details
        response = requests.get(url,headers=self.headers)

        #Validating the Response Status code 
        if response.status_code == 200:
            print("Pull Request - Request Successful - Ok : ", response.status_code)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.json()['message']}")
   
        self.pull_request_data = response.json().get('items')

        #user response
        decision = input(f"We collected a list of pull requests related to the repository {repo_name}. If you would like to access only the first page of the pull requests, press (Y). To access all pages, press (N) ")
        every_Page_Response = 'N' 
        if decision.lower() == 'n':
            every_Page_Response = input("Would you like to be asked to proceed before moving to every new page? (Y/N): ")

        #PullRequest objects corresponding repository details
        if(decision.lower() == 'y'):
            self.print_PullRequestsData(self.pull_request_data, owner, repo_name)

        elif(decision.lower() == 'n'):
            self.print_PullRequestsData(self.pull_request_data, owner, repo_name)

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
                body = str(pr.get('body', ''))
                state = pr.get('state', '')
                created_at = pr.get('created_at', '')
                closed_at = pr.get('closed_at', '')
                user = pr.get('user', {}).get('login', '')

                if(count < 5):
                    print("\n","*"*100)
                    print(f"The Details of PR : {number} are :")
                    print(f"\t Title : {title} \n\t Body : {body} \n\t State : {state} \n\t Created : {created_at} \n\t Closed : {closed_at} \n\t User : {user}")
                    count += 1
                    print("\n","═"*100)
                elif(count == 5):
                    print("If you want all of the pull request details, please visit the PullRequests.csv file in your current directory/folder.")
                    count += 1
            

                # Additional query to get details like commits, additions, deletions, changed_files
                pr_details = self.get_pull_request_details(owner, repo_name, number)

                # creating obj for PullRequest class  
                pull_request = PullRequest(title, number, body, state, created_at, closed_at, user, **pr_details)
                self.save_as_csv('pullrequests.csv', pull_request)
                repo = next((r for r in self.repositories if r.owner == owner and r.name == repo_name), None)
                if repo:
                    repo.pull_requests.append(pull_request)

    def get_Data(self, url):
        response = requests.get(url,headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def collect_user_data(self, username):
        # To Scrape the user contributions, followers, following, and number of repositories from the GitHub profile page
        url = f'https://github.com/{username}'
        response = requests.get(url)
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scrape contributions
        contributions_tag = soup.find('h2', class_='f4 text-normal mb-2')
        contributions = contributions_tag.text.strip().split()[0] if contributions_tag else '0'
        contributions_count = int(contributions.replace(',', ''))

        # Scrape repositories count
        repositories_tag = soup.find('span', class_='Counter')
        repos_count = int(repositories_tag.text.strip().replace(',', '')) if repositories_tag else 0

        # Scrape followers and following
        span_tags = soup.find_all('span', class_='text-bold color-fg-default')
        if span_tags:
            followers_count = span_tags[0].text.replace(',', '') if len(span_tags) > 0 else 0
            following_count = span_tags[1].text.replace(',', '') if len(span_tags) > 1 else 0
 
        print(f"The details for user {username} are: ","\nUser : ", username, "\nRepositories : ", repos_count, "\nFollowers : ", followers_count, "\nFollowing : ", following_count, "\nContributions in last year : ", contributions_count)
        user = User(username, repos_count, followers_count, following_count, contributions_count)
        self.save_as_csv('users1.csv', user)
        
    '''def collect_user_data(self, username, repo_name):
        # Use GitHub API to collect user data
        url = f'https://api.github.com/repos/{username}/{repo_name}/contributors'

        response = requests.get(url,headers=self.headers)
        #To  Check the status code for the response received
        if response.status_code == 200:
            print("Request Successful - Ok : ", response.status_code)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.json()['message']}")

        self.user_data = response.json()

        #print("User Dtaa retrived is below : ", user_data)
        #print("Stauscode for the request under collecting user data is : ", response.status_code)

        # Print the content of the request
        #print(response.content)

        # Filter contributors by the desired_username
        user_contributions = [contributor for contributor in self.user_data if contributor['login'] == username]

        if user_contributions:
            print(f"Details of user {username}:")
            #print(user_contributions[0])  # Prints the details of user
        else:
            print(f"Given User {username} is inactive among the contributors. Please try with different user name")
            username = input("If you would like to get information about one of these users, enter the username here: ")
            self.collect_user_data(username, repo_name)      


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

        print(f"Details of user : {username} in repository {repo_name} are : ","\nUser : ", username, "\nRepositories : ", repos_count, "\nFollowers : ", followers_count, "\n3Following : ", following_count, "\nContributions in last year : ", contributions_lastYear, "\nTotal Contributions : ",TotalContribution,  )
        self.save_as_csv('users1.csv', user)

    def scrape_user_contributions(self, username):
        # To Scrape the user contributions from the GitHub profile page as per requirement
    
        url = f'https://github.com/{username}?tab=overview&from={datetime.now().year - 1}-12-01'
        response = requests.get(url)
        
        soup = BeautifulSoup(response.content, 'lxml')
        contributions_tag = soup.find('h2', class_='f4 text-normal mb-2')
        
        contributions = contributions_tag.text.strip().split()[0] if contributions_tag else '0'
        return int(contributions.replace(',', ''))'''
    
    def save_as_csv(self, filename, obj):
        # Check if the file exists
        if not os.path.isfile(filename):
            # Create the file with a header
            with open(filename, 'w') as file:
                file.write(obj.get_csv_header() + '\n')

        # Append a new line with the object in CSV format
        with open(filename, 'a') as file:
            file.write(obj.to_csv() + '\n')

   

class Repository:
    def __init__(self, owner, name, description, homepage, License, forks, watchers):
        self.owner = owner
        self.name = name
        self.description = description
        self.homepage = homepage
        self.License = License
        self.forks = forks
        self.watchers = watchers
        self.pull_requests = []
        

    def get_csv_header(self):
        return "owner,name,description,homepage,license,forks,watchers"

    def to_csv(self):
        return f"{self.owner},{self.name},{self.description},{self.homepage},{self.License},{self.forks},{self.watchers}"

    def check(self):
        print("values in repository class")
        print(f"{self.owner},{self.name},{self.description},{self.homepage},{self.License},{self.forks},{self.watchers}")


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
        
    def get_csv_header(self):
        return "title,number,body,state,created_at,closed_at"

    def to_csv(self):
        body = '\n'.join(self.body)
        clean_body = body if body else ''
        clean_body = clean_body.replace('\n', ' ')
        clean_body = clean_body.replace('"', '""')
        return f'"{self.title}","{self.number}","{clean_body}","{self.state}","{self.created_at}","{self.closed_at}"'

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



### MAIN MENU ### 

# main function with menu 
def main():
    
    # declare global variables 
    global repo_name
    global owner_name
    global users 
    global ContributorDetailsRequByUser
    global repositoryAndOwner

    # create an instance of the GitHUbRepAnalyser class
    rep_analyzer = GitHUbRepAnalyser()

    # main menu
    while True:
        print("╔══════════════════════════════════════════════════╗")
        print("║     Welcome to the GitHub Repository Analyser    ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║ This is the main menu : Please select an option  ║")
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
        userchoice = input("Enter your choice : ")
    
        # Collect data from a specific GitHub repository using owner username and repository name 
        if userchoice == '1':
            try:
                print("Hint: you can get the repository name and owner's username from the top left corner of the GitHub page you are looking at")
                repo_name = input("Enter the name of the repository: ") # get repository name
                owner_name = input("Enter the username of the repository owner: ") # get owner username 

                if owner_name in repositoryAndOwner and repositoryAndOwner[owner_name] == repo_name:
                    print(f"You have already collected the required data for the given repository : {repo_name} with Owner : {owner_name}")
                    user_decision = input("if you would like to continue with the same press ('C'- continue) else press 'N' to enter a different repository: ")
                    if user_decision.lower() == 'c':
                        continue
                    elif user_decision.lower() == 'n':
                        repo_name = input("Enter the name of the repository: ") 
                        owner_name = input("Enter the username of the repository owner: ")
                        if owner_name in repositoryAndOwner and repositoryAndOwner[owner_name] == repo_name:
                            print("Sorry..!, returning to the Main Menu. Please find a new repository to explore further")
                            break
                else:
                    repositoryAndOwner.update({owner_name : repo_name})

                # get repository data 
                rep_analyzer.collect_repository_data(owner_name, repo_name)
                
                # get pull request data 
                print()
                rep_analyzer.collect_pull_requests(owner_name, repo_name)
                
                # get user data 
                print()
                print("Here are the usernames collected from list of pull requests: ")
                print(list(set(users))) 
                print()

                while True:
                    username = input("If you would like to get information about one of these users, enter the username here: ")
                    if not username:
                        break
                    else:                    
                        if username not in ContributorDetailsRequByUser:
                            ContributorDetailsRequByUser.append(username)
                            rep_analyzer.collect_user_data(username)
                        else:
                            print(f"You have already collected the required details of the user : {username}")

                        decision1 = input("Would you like to continue with a different user Y/N ?")
                        if decision1.lower() == 'y':
                            continue
                        else:
                            break
                    
            except Exception as e:
                print(f"An error occurred: {e}")

        # Show all repositories collected (with submenu of actions possible on each repo)
        elif userchoice == '2':
            # show all repositories collected 
            print("Here are all of the collected repositories: ")
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
            # user data needs to be pulled first
            if rep_analyzer.user_data:
                print(rep_analyzer.user_data)
                user_dat = {
                    'Following': [user.following for user in rep_analyzer.user_data],
                    'Followers': [user.followers for user in rep_analyzer.user_data],
                    'Num_pull': [len(user.pull_requests) if hasattr(user, 'pull_requests') else 0 for user in rep_analyzer.user_data],
                    'Num_contr': [user.contributions for user in rep_analyzer.user_data]
                    }
                
                # convert to df 
                user_df = pd.DataFrame(user_dat).fillna(0)

                # get correlations 
                corrs = user_df.corr()
                        
                # print correlations, with short explanation of what the values mean 
                print("Values close to 1.0 indicate strong positive correlation")
                print("Values close to -1.0 indicate strong negative correlation")
                print("Values near 0 indicate weak correlation")
                
                print(f"Correlations between data collected for users \n {corrs}")
                
                # Display heatmaps for correlation with each variable?
                # Definitely not necessary, but could be a nice visualization for correlations. Feel free to remove this if it's too much or not informative. 
                for column in corrs.columns:
                    plt.figure(figsize = (8,6))
                    plt.imshow([corrs[column]], 
                               cmap = 'coolwarm', 
                               aspect = 'auto', 
                               extent = [0, 1, 0, 1])
                    plt.colorbar(label = 'Correlation')
                    plt.title(f"Correlation Heatmaps for {column}")
                    plt.xticks([0.5], [column])
                    plt.yticks([])
                    plt.show()

            else:
                print("No user data found.")
                        
        elif userchoice == '5':
            return None, None, None  # Exit the program
        else:
            print("\nPLEASE SELECT A VALID OPTION\n")
        


main()
