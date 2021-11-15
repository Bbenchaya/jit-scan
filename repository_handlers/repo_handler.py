from risk_calculator.risk_calculator import RiskCalculator


class RepositoryHandler:
    def __init__(self):
        pass


    def fetch_all_repositories(self, code_language):
        raise Exception("NotImplementedException")

    def evaluate_repos(self, limit, repositories, risk_calculator: RiskCalculator):
        raise Exception("NotImplementedException")