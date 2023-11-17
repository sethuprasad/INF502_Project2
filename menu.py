# Project 2

# functions to add to class GitHUbRepAnalyser
def show_repositories(self):
    for rep in self.repositories
        print(rep.name)

def main():
    global users # declare users as global variable 

    # create an instance of the GitHUbRepAnalyser class
    rep_analyzer = GitHUbRepAnalyser()
    
    while True:
        print("\nWelcome to the *app name* application. \nThis is the main menu; please select one of the following options.\n")
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
        username = print("If you would like to get information about one of these users, enter the username here: ")
        rep_analyzer.collect_user_data(username, rep)
        
    elif userchoice == '2':

    elif userchoice == '3':

    elif userchoice == '4':

    elif userchoise == '5':
        return None, None, None  # Exit the program
    else:
        print("\nPLEASE SELECT A VALID OPTION\n")
        
        
