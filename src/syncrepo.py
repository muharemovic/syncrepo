#!/usr/bin/python3
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
DIRECTORY_PATH = os.getenv('DIRECTORY_PATH')
HOSTNAME = os.getenv('HOSTNAME',default='github.com')
USER = "user"
def get_folder_names(directory):
    folder_names = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            folder_names.append(entry.name)
    return folder_names

folder_names = get_folder_names(DIRECTORY_PATH)

def create_github_repository(repo_name, ACCESS_TOKEN):
    global USER
    url = 'https://api.github.com/'
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': repo_name,
        'auto_init': True,
        'private': True,
        
    }
    
    renamed_branch = {
    		
  			'new_name': 'my_renamed_branch',
             
    }
    get_user = requests.get(f'{url}user', headers=headers).json() 
    USER = get_user['login']
    response = requests.post(f'{url}user/repos', headers=headers, data=json.dumps(data))
    respone_rename= requests.post(f"{url}repos/{USER}/{repo_name}/branches/main/rename",  data=json.dumps(renamed_branch), headers=headers)
    if response.status_code == 201:
        print('Repository created successfully!')
     
    else:
        print('Failed to create repository. Status code:', response.status_code)


def get_local_branches():
    # Run the 'git branch' command to retrieve local branches
    result = os.system('git branch > branch_output.txt')

    with open('branch_output.txt', 'r') as file:
        output = file.read()

    # Get the branch names by removing leading whitespace and '*'
    branches = [line.strip().lstrip('*') for line in output.split('\n')]
    
    return branches

def checkout_all_branches():
    branches = get_local_branches()

    # Iterate through each branch and checkout
    for branch in branches:
        os.system(f'git checkout {branch}')
        os.system('git push upstream')



for folder_name in folder_names:
   create_github_repository(folder_name, ACCESS_TOKEN)
   os.chdir(f'{DIRECTORY_PATH}/{folder_name}')
   os.system("for branch in $(git branch --all | grep '^\s*remotes' | egrep --invert-match '(:?HEAD|master)$'); do git branch --track \"${branch##*/}\" \"$branch\"; done")
   if os.system(f'git remote add upstream git@{HOSTNAME}:{USER}/{folder_name}.git') == 0:
        pass   
   else:
      os.system(f'git remote set-url upstream git@{HOSTNAME}:{USER}/{folder_name}.git')
      print('Upstream url updated!')
   checkout_all_branches()
   
   
