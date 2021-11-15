import shutil

from repository_handlers.github_repo_handler import GithubRepositoryHandler
from risk_calculator.unused_req_risk_calculator import UnusedReqRiskCalculator
from flask import Flask, jsonify


def verify_input(repo_type, repos_to_scan):
    res = {}

    if repos_to_scan < 1 or repos_to_scan > 25:
        res["repo-num-error"] = "Please enter a number between 1-25"

    if repo_type.lower() != "github":
        res["repo-src-error"] = "Currently only github is supported"

    return res

app = Flask(__name__)
@app.route('/')
def welcome():
    return "Welcome please issue a request in the following format /reporisk/repo-src/num-or-repos-to-process"

@app.route('/reporisk/<repotype>/<int:repostoscan>')
def process_request(repotype, repostoscan):
    res = verify_input(repotype, repostoscan)
    if not res:
        fetcher = GithubRepositoryHandler("Python")
        unused_risk_calculator = UnusedReqRiskCalculator()
        try:
            repos = fetcher.fetch_all_repositories(repostoscan)
            json_response = fetcher.evaluate_repos(repostoscan, repos, unused_risk_calculator)
        finally:
            print("cleaning up tmp dir")
            shutil.rmtree("../repositories_to_inspect/")
        print(json_response)
        return json_response
    else:
        return jsonify(res)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
