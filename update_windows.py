import os
import subprocess
from pathlib import Path

cwd = Path(os.getcwd())
parent = cwd.parent
protected_files = []
import shutil

def copy_protected():
    with open(os.path.join(os.getcwd(), 'InfernalAdmin/protected_files.txt')) as f:
        protected_files = f.readlines()
    f.close()
    for f in protected_files:
        file_name = f.replace('\n', "")
        shutil.copy2(os.path.join(os.getcwd(), "InfernalAdmin\\" + file_name), os.getcwd() + "\\" + file_name)

if Path(os.path.join(os.getcwd()), 'InfernalAdmin').exists():
    print("Path exists")
    copy_protected()
else:
    print("Path does not exist")

git_uri = "https://github.com/PeterGibbs/InfernalAdmin.git"
cmd = "pip install --upgrade --src=" + os.getcwd() + " -e git+https://github.com/PeterGibbs/InfernalAdmin.git@origin/master#egg=InfernalAdmin"
branch = "Peter-Develop"
branch_Path = "git+https://github.com/user/repo.git@origin/" + branch + "#egg=InfernalAdmin"
# subprocess.Popen(["pip","install","--src",os.getcwd(),"-U",branch_Path],shell=True)
subprocess.call(["git", "clone", git_uri, "--branch", branch], shell=True)
