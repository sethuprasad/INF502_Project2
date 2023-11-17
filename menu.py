# Project 2

# functions to add to class GitHUbRepAnalyser


# main function with menu 
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
                elif userchoice_sub == '2':

                elif userchoice_sub == '3':

                elif userchoice_sub == '4':

                elif userchoice_sub == '5':
                    break
                else: 
                    print("\nPLEASE SELECT A VALID OPTION\n")       

        elif userchoice == '3':

        elif userchoice == '4':

        elif userchoise == '5':
            return None, None, None  # Exit the program
        else:
            print("\nPLEASE SELECT A VALID OPTION\n")
        
        
