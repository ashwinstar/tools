#!/usr/bin/env python3

# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import subprocess
import os

issue_number = input("MPP number:")
#TODO perform validation
if issue_number == "":
    exit()

url = "https://jira-pivotal.atlassian.net/rest/api/3/issue/" + issue_number + "/comment"

auth = HTTPBasicAuth(os.environ.get('JIRA_EMAIL'), os.environ.get('JIRA_TOKEN'))

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

#TODO, maybe even ask for number of commits (default 1) and then post details for that many commits.
# would have been good if post-commit hook can actually get the number of commits being pushed and such.
# Though seems no parameter is passed to it currently by git.
text_to_insert = subprocess.run(["git", "log", "-1", "HEAD"], check=True, stdout=subprocess.PIPE, universal_newlines=True)
commit_sha = subprocess.run(["git", "rev-parse", "HEAD"], check=True, stdout=subprocess.PIPE, universal_newlines=True)
#TODO, maybe use the git remote to generate this link
commit_link = "https://github.com/greenplum-db/gpdb/commit/" + commit_sha.stdout

payload = json.dumps( {
    "body": {
        "content": [
            {
                "content": [
                    {
                        "attrs": {
                            "url": commit_link
                        },
                        "type": "inlineCard"
                    },
                    {
                        "text": " ",
                        "type": "text"
                    }
                ],
                "type": "paragraph"
            },
            {
                "attrs": {
                    "language": "text"
                },
                "content": [
                    {
                        "text": text_to_insert.stdout,
                        "type": "text"
                    }
                ],
                "type": "codeBlock"
            }
        ],
        "type": "doc",
        "version": 1
    },
} )

response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
 )

print(response.text)
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
