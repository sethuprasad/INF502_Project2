# Project 2
def main():
    global users

    while True:
        print("\nWelcome to the *app name* application. \nThis is the main menu; please select one of the following options.\n")
        print("1. Collect data for a specific repository")
        print("2. Show all repositories collected")
        print("3. Create and store visual representation data about all the repositories")
        print("4. Calculate the correlation between the data collected for the users")

    userchoice= input("Enter your choice: ")

    if userchoice == '1':
        rep = input("Enter the name of the repository: ")
        owner = input("Enter the name of the repository owner: ")

        rep_analyzer = GitHUbRepAnalyser()
        rep_analyzer.collect_repository_data(owner, rep)
        rep_analyzer.collect_pull_requests(owner, rep)

        print("The following are the usernames collected from pull requests: ")
        print(list(set(users)))
        username = print("If you would like to get information about one of these users, enter the username here: ")
        rep_analyzer.collect_user_data(username, rep)
        
    if userchoice == '2':

    if userchoice == '3':

    if userchoice == '4':
        
