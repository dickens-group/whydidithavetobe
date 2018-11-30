import boto3

class Ecr:
    def __init__(self, repo_name):
        self.client = boto3.client("ecr")
        self.repo_name = repo_name
        self.validate_repo()

    def repo_exists(self):
        response = self.client.describe_repositories()
        repo_list = []
        if "repositories" in response:
            for repository in response['repositories']:
                # print(repository['repositoryName'])
                repo_list.append(repository['repositoryName'])

        if self.repo_name in repo_list:
            return True
        else:
            return False

    def create_repo(self):
        response = self.client.create_repository(repositoryName=self.repo_name)

    def validate_repo(self):
        if self.repo_exists():
            return True
        else:
            self.create_repo()

if __name__ == "__main__":
    pass
