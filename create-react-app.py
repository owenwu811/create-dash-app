import os
import shutil
import glob
import subprocess
from pathlib import Path

name = input("app name (subdomain): ")
ssh = input("ssh endpoint (ie. [NET_ID]@netvisdev.fuqua.duke.edu): ")
port = input("enter port number here: ")

#using Path class for platform flexability
project_dir = Path(f'../{name}-DEV/')
deploy_dir = Path(f'../{name}-DEPLOY/')

shutil.copytree('package/DEV/', project_dir, symlinks=False, ignore=None)
shutil.copytree('package/DEPLOY/', deploy_dir, symlinks=False, ignore=None)

# list comprehension to copy files
[shutil.copytree(src, dest, symlinks=False, ignore=None) for src, dest in [('package/DEV/', project_dir), ('package/DEPLOY/', deploy_dir)]]

for directory in [project_dir, deploy_dir]:
    for filename in glob.iglob(os.path.join(directory, '**/*.sh'), recursive=True):
        generator_dir = os.path.dirname(filename)
        generated_name = filename.split('_')[-1][0:-3]

        result = subprocess.run(['bash', f'{filename} > {generator_dir}/{generated_name} {name} {port} {ssh}'], shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            os.remove(filename)
        else:
            print(f"Error executing command: {result.stderr}")

print('')
print(f'Created project at {project_dir}')
print('Syncing for the first time..')

subprocess.run(['bash sync.sh > logs.txt'], cwd=project_dir, shell=True)

url = ssh.split('@')[-1]
print('')
print(f'{name} now deployed at https://{url}/{name}')
print(f'To run locally in the development environment, run "python main.py" in {name}-DEV/main/app')
