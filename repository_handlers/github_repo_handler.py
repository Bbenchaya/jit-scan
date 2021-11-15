import concurrent
from concurrent.futures import ThreadPoolExecutor

from flask import jsonify
from git import Repo, List
from gtrending import fetch_repos

from repository_handlers.repo_handler import RepositoryHandler
from risk_calculator.risk_calculator import RiskCalculator


class GithubRepositoryHandler(RepositoryHandler):
    def __init__(self, code_lang):
        super().__init__()
        self.code_lang = code_lang

    def fetch_all_repositories(self, limit) -> List[dict]:
        futures = []
        repos = fetch_repos(language=self.code_lang)  # get the result as a dict
        with ThreadPoolExecutor(max_workers=10) as executor:
            for repository in zip(range(limit), repos):
                path = "../repositories_to_inspect/" + repository[1]["name"]
                futures.append(executor.submit(Repo.clone_from, repository[1]["url"], path))
            try:
                for future in concurrent.futures.as_completed(futures, timeout=1):
                        future.result(timeout=1)
            except Exception as e:
                print(e)
            executor.shutdown()
        return repos

    def print_repo_details(self, repo, risk):
        print(f'Repo - {repo["fullname"]}')
        print(repo["author"])
        print(repo["description"])
        print(repo["language"])
        print(f'{repo["url"]}')
        if risk == -1:
            print(f'Could not calculate risk for repo \n')
        else:
            print(f'Risk for repo is {risk} \n')

    def create_repo_response(self, repo, risk) -> dict:
        repositoriy_data = {}
        repositoriy_data['name'] = repo["fullname"]
        repositoriy_data['author'] = repo["author"]
        repositoriy_data['description'] = repo["description"]
        repositoriy_data['language'] = repo["language"]
        repositoriy_data['url'] = repo["url"]
        if risk == -1:
            repositoriy_data['risk'] = 'Could not calculate risk for repo'
        else:
            repositoriy_data['risk'] = risk
        return repositoriy_data

    def evaluate_repos(self, limit, repositories, risk_calculator: RiskCalculator) -> dict:
        repository_list = {}
        for index, repo in zip(range(limit), repositories):
            risk = risk_calculator.calculate_risk(repo, repo["name"])
            repository_list[repo["name"]] = self.create_repo_response(repo, risk)
            self.print_repo_details(repo, risk)
        return jsonify(repository_list)