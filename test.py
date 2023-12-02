
from unittest import TestCase
from main import GitHubRepAnalyser


class MainTests(TestCase):
    def setUp(self):
        self.repo_analyser = GitHubRepAnalyser()
        self.repo_name = 'INF502_Tests'
        self.user = 'Clockwork-Rat'

    def test_basic(self):
        
        self.repo_analyser.collect_repository_data(
            self.user,
            self.repo_name
        )

        self.assertEqual(len(self.repo_analyser.repositories), 1)

    def test_pull_requests(self):

        self.repo_analyser.collect_pull_requests(
            self.user,
            self.repo_name
        )

        self.assertEqual(len(self.repo_analyser.pull_request_data), 2)

    def test_pull_request_details(self):
        
        self.repo_analyser.collect_pull_requests(
            self.user,
            self.repo_name
        )

        pull_request_names = [x.get('title', '') for 
                            x in self.repo_analyser.pull_request_data]

        self.assertTrue('open pr' in pull_request_names)
        self.assertTrue('add hello file' in pull_request_names)


    def test_failed_request(self):
        
        self.repo_analyser.collect_repository_data(
            self.user,
            'NOTREAL'
        )

        self.assertTrue(self.repo_analyser.response.status_code != 200)

    def test_csv_output(self):

        #print csv information

        self.repo_analyser.collect_pull_requests(
            self.user,
            self.repo_name
        )

        with open("pullrequests.csv") as fopen:
            text = fopen.read()
            self.assertTrue('open pr' in text)
            self.assertTrue('add hello file' in text)


        
