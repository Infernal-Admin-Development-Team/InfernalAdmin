"""Short and ugly script to install and re install the bot on windows"""
import os
import subprocess
import sys
from pathlib import Path

cwd = Path(os.getcwd())
parent = cwd.parent
protected_files = []
import shutil
import stat


def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

def copy_protected():
    file_list = []
    if Path(os.path.join(os.getcwd(), 'InfernalAdmin/protected_files.txt')).exists():
        with open(os.path.join(os.getcwd(), 'InfernalAdmin/protected_files.txt')) as f:
            file_list = f.readlines()
        f.close()
        for f in file_list:
            protected_files.append(f.replace('\n', ""))
        for f in protected_files:
            shutil.copy2(os.path.join(os.getcwd(), "InfernalAdmin\\" + f), os.getcwd() + "\\" + f)


def move_protected_back():
    for f in protected_files:
        shutil.copy2(os.getcwd() + "\\" + f, os.path.join(os.getcwd(), "InfernalAdmin\\" + f))

if Path(os.path.join(os.getcwd()), 'InfernalAdmin').exists():
    print("Path exists")
    copy_protected()
    shutil.rmtree(os.path.join(os.getcwd(), 'InfernalAdmin'), onerror=on_rm_error)

else:
    print("Path does not exist")

branch = sys.argv[1]
print("BRANCH IS :", branch)
branch_Path = "git+https://github.com/PeterGibbs/InfernalAdmin.git@origin/" + branch + "#egg=InfernalAdmin"
subprocess.call(["pip", "install", "--src", os.getcwd(), "-e", branch_Path], shell=True)

subprocess.call(["pip", "install", "-U", "-r", os.path.join(os.getcwd(), 'InfernalAdmin/requirements.txt')], shell=True)

move_protected_back()

subprocess.call(["python", os.path.join(os.getcwd(), 'InfernalAdmin/main.py')], shell=True)
