import subprocess
import shutil
from git import Repo

from risk_calculator.risk_calculator import RiskCalculator


class UnusedReqRiskCalculator(RiskCalculator):

    def calculate_risk(self, repo_to_inspect: Repo, repo_name) -> int:
        path_to_repo = f'../repositories_to_inspect/{repo_name}'
        try:
            print(f'evaluating repo: {path_to_repo}')
            p = subprocess.Popen(["pip-extra-reqs", path_to_repo], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stderr = p.stderr.read()
            if "Traceback" in stderr.decode('utf-8'):
                risk = -1
            else:
                risk = stderr.decode('utf-8').count('requirements.txt')
        except Exception:
            risk = -1
        finally:
            print(f'removing dir from path: {path_to_repo}')
            shutil.rmtree(path_to_repo)
        return risk


