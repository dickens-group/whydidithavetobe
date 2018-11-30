import sys
import time

import boto3

class Codebuild:
    def __init__(self, project_name, environment_variables):
        self.client = boto3.client('codebuild')
        self.project_name = project_name
        self.environment_variables  = environment_variables
        self.id = None

    def start(self):
        print("Starting build for {}".format(self.project_name))
        try:
            response = self.client.start_build(projectName=self.project_name, environmentVariablesOverride=self.environment_variables)
        except:
            sys.exit("ERROR: no response from codebuild client {}".format(sys.exc_info()[0]))

        build = response.get("build",False)
        if build:
            id = build.get("id", False)
            if id:
                self.id = id
            else:
                sys.exit("ERROR: build in response but id is missing!")
        else:
            sys.exit("ERROR: no build in response from codebuild client")

    def success(self, max_time=10):
        """check the status of the build is SUCCEEDED
        Paramters:
            max_time (int) : (optional) maximum time in minutes to keep checking
        Returns:
            bool : True if build SUCCEEDED
        """
        if self.id is None:
            self.start()

        sys.stdout.write("Checking build")
        for attempt in range(0,max_time):
            status = self._get_build_status()
            if status == "SUCCEEDED":
                sys.stdout.write("{}\n".format(status))
                return True
            else:
                sys.stdout.write(".")
                time.sleep(60)

        sys.stdout.write("{} at {} minutes!\n".format(status, max_time))
        return False

    def _get_build_status(self):
        try:
            response = self.client.batch_get_builds(ids=[self.id])
        except:
            sys.exit("ERROR: get build status for {} gave no response {}!".format(self.id, sys.exc_info()[0]))
        builds = response.get("builds",False)
        status = None
        if builds:
            if len(builds)==1:
                return builds[0].get('buildStatus')
            else:
                sys.exit("ERROR: {} batch_get_builds returned {} builds for id {}!".format(self.project_name,len(builds),self.id))
        else:
            sys.exit("ERROR: {} no builds returned for id {}".format(self.project_name, self.id))
        return status

    def get_name(self):
        return self.project_name


if __name__ == "__main__":
    pass
