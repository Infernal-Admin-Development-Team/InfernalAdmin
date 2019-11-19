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
from time import sleep

print("waiting for bot to die")
sleep(6)
print("Starting update")
def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

def copy_protected():
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
branch_Path = "git+https://github.com/Infernal-Admin-Development-Team/InfernalAdmin.git@origin/" + branch + "#egg=InfernalAdmin"
subprocess.call(["pip", "install", "--src", os.getcwd(), "-e", branch_Path], shell=True)

subprocess.call(["pip", "install", "-U", "-r", os.path.join(os.getcwd(), 'InfernalAdmin/requirements.txt')], shell=True)

move_protected_back()
os.chdir(str(cwd) + "\\infernaladmin")
subprocess.Popen(["python", os.path.join(os.getcwd(), 'infernal_admin_main.py')], shell=True)
print("exiting updater")
exit(0)
