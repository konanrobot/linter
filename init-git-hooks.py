#!/usr/bin/env python
# Disable pylint filename and missing module member complaints.
# pylint: disable=C0103,E1101
""" Initializes git hooks for current project folder. """

import os
import requests
import shutil
import subprocess
import sys

cpplint_url = 'https://raw.githubusercontent.com/google/styleguide/cf4071cf5de83c006b08bf8f62e1450d17a9ce07/cpplint/cpplint.py'
pylint_url = 'https://raw.githubusercontent.com/vinitkumar/googlecl/6dc04b489dba709c53d2f4944473709617506589/googlecl-pylint.rc'


def download_file_from_url(url, file_path):
  request = requests.get(url, verify=False, stream=True)
  request.raw.decode_content = True
  with open(file_path, 'w') as downloaded_file:
    shutil.copyfileobj(request.raw, downloaded_file)


def get_root_git_repo(some_folder_in_root_repo='./'):
  get_repo_call = subprocess.Popen("git rev-parse --show-toplevel",
                                   shell=True,
                                   cwd=some_folder_in_root_repo,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)

  stdout, stderr = get_repo_call.communicate()
  repo_root = stdout.rstrip()
  return repo_root


def main():
  """ Download cpplint.py and pylint.py and installs the git hooks"""
  script_directory = os.path.dirname(sys.argv[0])
  script_directory = os.path.abspath(script_directory)

  # Download linter files.
  download_file_from_url(cpplint_url, script_directory + "/cpplint.py")
  download_file_from_url(pylint_url, script_directory + "/pylint.rc")

  # Get git root folder of parent repository.
  repo_root = get_root_git_repo(script_directory + '/../')

  # Copy git hooks.
  cp_params = repo_root + "/linter/pre-commit " + repo_root + "/.git/hooks/"
  if subprocess.call("cp " + cp_params, shell=True) != 0:
    print("Failed to copy githooks to {}...".format((repo_root + "/.git/hooks/")))

  print("Success!")


if __name__ == "__main__":
  main()
