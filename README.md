# INF502_Project2
Project 2 to gather and analyze the GitHub repository data

Pre-requiestisites

Install requestes
install lxml
  pip install lxml

Selected repositories:
1. Rep: piecewiseSEM Owner: jslefche
2. Rep: glmmTMB Owner: glmmTMB
3. Rep: ecology Owner: FormidableLabs


**Group leaders:**

We have planned to have every one as a group leader on weekly basis, for the **1st & 2nd week Sethuprasad Gorantla**** will be taking the leadership activites and then it will be continued by ** other team members for 3rd week**


**Initial code Access details:**

Using the **requests** library we are making the api calls(**import requests**)
**URL format being used:**   url = 'https://api.github.com/repos/{owner}/{repo_name}'

**1. Initialization**
The script begins with an initialization step, setting up necessary variables and the GitHub access token to avoid rate limits.

**2. Repository Data Collection**
Function: collect_repository_data(owner, repo_name)
This function collects details about a specified GitHub repository, such as description, homepage, license, forks, and watchers. The information is displayed in a readable format.

**3. Pull Request Data Collection**
Function: collect_pull_requests(owner, repo_name)
This function retrieves pull request data related to a specified repository. Users can choose to access only the first page or all pages of pull requests. The script provides an option to proceed before moving to each new page.

**4. User Data Collection**
Function: collect_user_data(username, repo_name)
This function collects data about a GitHub user's contributions to a specific repository. It includes information on the number of repositories, followers, following, contributions in the last year, and total contributions. If the specified user is not found, the script prompts the user to enter a different username. It also scrapes user data from their profile page.

**5. Supporting Functions**
Function: get_pull_request_details(owner, repo_name, number)
This function retrieves additional details about a specific pull request, such as commits, additions, deletions, and changed files.
Function: print_PullRequestsData(pull_request_data, owner, repo_name)
This function prints details about pull requests in a readable format, allowing users to view information about the title, body, state, created date, closed date, and user.

**6. File Saving**
The script includes functionality to save user, repository, and pull request data to CSV files.
Notes
Ensure you have the necessary permissions to access the specified repository and its data.
Use the script responsibly, taking into consideration GitHub's API usage policies.
The script provides a basic overview and can be extended for more advanced use cases or additional functionalities.

**7.Repository Class**
This class represents a GitHub repository and contains attributes such as owner, name, description, homepage, license, forks, watchers, and a list of pull requests.

**8.PullRequest Class**
This class represents a GitHub pull request and includes attributes like title, number, body, state, created_at, closed_at, user, commits, additions, deletions, and changed_files.

**9.User Class**
This class represents a GitHub user and includes attributes like username, repositories, followers, following, and contributions.

**10.main() Function**
The main function serves as a menu-driven interface for the GitHub Repository Analyzer. It allows users to perform various actions, including collecting data for a specific repository, visualizing data, calculating correlations, and exiting the program.

**11.Visualizations**
The program generates visual representations using the Matplotlib library, including boxplots, scatterplots, and bar plots, to provide a clearer understanding of the collected data.


**How to Use :**

	Collect Data for a Specific GitHub Repository: Enter the name of the repository and the owner's username. The program will gather information about the repository, its pull requests, and the users involved.
	Show All Collected Repositories: View a list of all the repositories collected. You can choose to explore specific details about each repository, such as pull requests or create visual representations.
	Create and Store Visual Representation of Data: Generate visual representations of the data collected, including boxplots, scatterplots, and bar plots. These visualizations help you better understand the characteristics of the repositories and pull requests.
	Calculate Correlation Between Collected User Data: Explore correlations between different user-related metrics, such as the number of followers, following, pull requests, and contributions. This provides insights into the relationships between these variables.
	Exit: Choose this option when you are done exploring and analyzing the repositories.
