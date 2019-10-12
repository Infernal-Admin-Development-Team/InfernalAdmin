import os
import subprocess
from pathlib import Path

cwd = Path(os.getcwd())
parent = cwd.parent
protected_files = []


def copy_protected():
    with open(os.path.join(os.getcwd(), 'InfernalAdmin/protected_files.txt')) as f:
        protected_files.append(f.readlines())


if Path(os.path.join(os.getcwd()), 'InfernalAdmin').exists():
    print("Path exists")
else:
    print("Path does not exist")
git_uri = "https://github.com/PeterGibbs/InfernalAdmin.git"
cmd = "pip install --upgrade --src=" + os.getcwd() + " -e git+https://github.com/PeterGibbs/InfernalAdmin.git@origin/master#egg=InfernalAdmin"
branch = "master"
branch_Path = "git+https://github.com/user/repo.git@origin/" + branch + "#egg=InfernalAdmin"
# subprocess.Popen(["pip","install","--src",os.getcwd(),"-U",branch_Path],shell=True)
subprocess.call(["git", "clone", git_uri, "--branch", branch, ], shell=True)
