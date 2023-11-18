import pandas
import matplotlib

# should make some of these in functions in the GitHUbRepAnalyser Class
# need to add pull requests to Users class 

# main function with menu 
def main():
    global users # declare users as global variable 

    # create instances of the GitHUbRepAnalyser class and User class 
    rep_analyzer = GitHUbRepAnalyser()
    
    while True:
        print("\nWelcome to the *APP NAME?* application. \nThis is the main menu; please select one of the following options.\n")
        print("1. Collect data for a specific GitHub repository")
        print("2. Show all repositories collected")
        print("3. Create and store visual representation data about all the repositories")
        print("4. Calculate the correlation between the data collected for the users")

        # get user input 
        userchoice= input("Enter your choice: ")
    
        # Collect data from a specific GitHub repository using owner and repository name 
        if userchoice == '1':
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

        # Show all repositories collected (with submenu of actions possible on each repo)
        elif userchoice == '2':
            # show all repositories collected 
            for rep in self.repositories:
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
                    repo = next((r for r in self.repositories if r.name == repo_name), None)
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
                    repo = next((r for r in self.repositories if r.name == repo_name), None)
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
                    repo = next((r for r in self.repositories if r.name == repo_name), None)
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
                    
                        # A boxplot that compares closed vs. open pull requests in terms of additions and deletions
                    
                        # A boxplot that compares the number of changed files grouped by the author association
                    
                        # A scatterplot that shows the relationship between additions and deletions
                    else:
                        print(f"Repository '{repo_name}' not found.")    

                    
                elif userchoice_sub == '4':
                    # Calculate the correlation between all the numeric data in the pull requests for a repository
                    repo_name = input("Enter the name of repository: ") 
                    # locate the repository using name 
                    repo = next((r for r in self.repositories if r.name == repo_name), None)
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
            # Create and store visual representation data about all the repositories

            # A line graph showing the total number of pull requests per day
            
            # A line graph comparing number of open and closed pull requests per day
            
            # A bar plot comparing the number of users per repository
            
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
                        
        elif userchoise == '5':
            return None, None, None  # Exit the program
        else:
            print("\nPLEASE SELECT A VALID OPTION\n")
        
        
