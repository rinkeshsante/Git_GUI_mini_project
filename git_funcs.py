import subprocess
import os

INITIAL_PATH = os.getcwd()
print(INITIAL_PATH, '\n')


# TODO remove all shell=True for full string command

def cmd_call(cmd):
    msg = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out = msg.stdout.decode()
    err = msg.stderr.decode()
    if out:
        print(out)
    if err:
        print(err)


def init():
    """
    Initialises local directory for git
    :return:
    """
    cmd = 'git init'
    subdirectory = ''
    choice = int(input("Do you want to initialise:\n"
                       "1.Current directory as git\n"
                       "2.Make new directory\n"))
    if choice == 2:
        subdirectory = input("Enter the name of the directory for git to track:").strip()
        cmd += ' ' + subdirectory

    # Command is run here
    subprocess.run(cmd)

    if choice == 2:
        os.chdir(os.path.join(os.getcwd(), subdirectory))


def clone(add_link):
    """
    Clones git directory from GitHub using link
    :return: None
    """
    # TODO change remote to personal GitHub link
    # clone_link = 'https://github.com/MitanshuShaBa/email_tutorial.git'
    new_name = ''
    clone_link = add_link #input("Enter clone link:\n")
    cmd = f'git clone {clone_link}'
    '''choice = int(input("Do you want to clone:\n"
                       "1.In directory as same name\n"
                       "2.Make new directory with different name\n"))
    if choice == 2:
        new_name = input("Enter the name of the directory for git to track:").strip()
        cmd += ' ' + new_name'''

    # Command is run here
    subprocess.run(cmd)
 
    if choice == 2:
        os.chdir(os.path.join(os.getcwd(), new_name))


def git_help():
    """
    Shows help message
    :return: None
    """
    subprocess.check_call(['git', '--help'])


def status():
    """
    Show the working tree status
    :return:
    """
    subprocess.check_call(['git', 'status'])


def add():
    """
    Add file contents to the index
    :return: None
    """
    files = input("Enter file names to add or . if you want to add all files to staging area\n").strip().split()
    call = ['git', 'add'] + files
    try:
        subprocess.check_call(call)
    except subprocess.CalledProcessError as e:
        print(e)


def unstage():
    """
    Remove files from the working tree and from the index
    :return: None
    """
    # files with spaces have to be surrounded with ""
    files = input("Enter file names to remove or * if you want to remove all files from staging area\n").strip()
    cmd = 'git reset ' + files
    msg = subprocess.run(cmd, stderr=subprocess.PIPE)
    err = msg.stderr.decode()
    print(err)


# unstage()

def add_remote(name, url):
    cmd = f'git remote add {name} {url}'
    msg = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    err = msg.stderr.decode()
    if err:
        print(err)


# add_remote('origin2', 'https://github.com/MitanshuShaBa/Git-test2.git')
def rename_remote(old, new):
    cmd = f'git remote rename {old} {new}'
    msg = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    err = msg.stderr.decode()
    if err:
        print(err)
    # rename_remote('wahab', 'w')


def show_remotes():
    cmd = 'git remote show'
    out = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode()
    print(out)


# show_remotes()


def push_branch(remote, branch):
    cmd = f'git push {remote} {branch}'
    cmd_call(cmd)


# push_branch('origin2', 'remote')

def push_all(remote):
    cmd = f'git push {remote} --all'
    cmd_call(cmd)
# add_remote('origin3', 'https://github.com/MitanshuShaBa/Git-test3.git')
# push_all('origin3')

def clean():
    """
    Remove untracked files from the working tree
    :return: None
    """
    # call = ['git', 'clean', '-f', '-n', '-d']
    call = 'git clean -f -n -d'
    try:
        # for later integration with GUI
        # TODO make this kind of output for every function
        print(subprocess.run(call, stdout=subprocess.PIPE).stdout.decode())
    except subprocess.CalledProcessError as e:
        print(e)
        return
    choice = input("Do wish to clean these files from working tree (y/n):").lower()
    if choice == 'y':
        call = 'git clean -f -d'
        try:
            subprocess.run(call)
        except subprocess.CalledProcessError as e:
            print(e)
            return


# clean()
def branch_create():
    """
    Creates a branch
    :return: None
    """
    name = input("Enter name of branch:").strip()
    # case: empty name or name with space
    if name == '' or ' ' in name or not name.isalnum():
        print()
        branch_create()
        return
    cmd = f'git branch {name}'
    branch_exists_msg = f"fatal: A branch named '{name}' already exists."
    try:
        message = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = message.stderr.decode()
        # case: branch name exists
        if err.strip() == branch_exists_msg:
            print(branch_exists_msg.replace('fatal: ', ''))
            print("Try again\n")
            branch_create()
        else:
            print('branch', name, 'created')
    except subprocess.CalledProcessError as e:
        print(e)


# branch_create()

def branch_delete(branch):
    """
    deletes a branch
    :return: None
    """
    name = branch
    # name = input("Enter name of branch to be deleted:").strip()
    cmd = f'git branch {name} -d'
    try:
        message = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = message.stdout.decode()
        err = message.stderr.decode()
        if err:
            print(err)
        else:
            print(out)
    except subprocess.CalledProcessError as e:
        print(e)


# branch_delete()
def branch_rename():
    """
    Renames a branch
    :return: None
    """
    name = input("Enter name of branch:").strip()
    new_name = input("Enter name of new branch:").strip()
    # case: empty name or name with space
    if new_name == '' or ' ' in new_name or not new_name.isalnum():
        print('Rename failed: Improper name')
        return
    cmd = f'git branch -m {name} {new_name}'
    branch_exists_msg = f"fatal: A branch named '{new_name}' already exists."
    try:
        message = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = message.stderr.decode()
        # case: branch name exists
        if err.strip() == branch_exists_msg:
            print(branch_exists_msg.replace('fatal: ', ''))
        elif err:
            print(f'branch {name} does not exist')
        else:
            print('branch', name, 'renamed to', new_name)
    except subprocess.CalledProcessError as e:
        print(e)


# branch_rename()
def branch_list():
    """
    Lists all branches
    :return:
    """
    try:
        print('Branches:\n', subprocess.run('git branch', stdout=subprocess.PIPE).stdout.decode())
    except:
        pass


# branch_list()
def checkout_branch(branch: str) -> None:
    """
    Checks out to a branch
    :parameter branch
    :type str
    :return None
    """
    msg = subprocess.run(f'git checkout {branch}', stderr=subprocess.PIPE)
    err = msg.stderr.decode()
    branch_not_msg = f"error: pathspec '{branch}' did not match any file(s) known to git"
    if err.strip() == branch_not_msg:
        print('branch does not exist')


# checkout_branch('master')


def checkout_commit(commit_addr: str) -> None:
    """
    Checks out to a branch
    :parameter commit_addr
    :type str
    :return None
    """
    msg = subprocess.run(f'git checkout {commit_addr}', stderr=subprocess.PIPE)
    err = msg.stderr.decode()
    commit_not_msg = f"error: pathspec '{commit_addr}' did not match any file(s) known to git"
    if err.strip() == commit_not_msg:
        print('commit_addr does not exist')


# checkout_commit('cswwe')


def merge(branch1, branch2):
    """
    Merges 2 branches together
    :parameter: branch1
    :type: str
    :parameter: branch2
    :type: str
    :return: None
    """
    checkout_branch(branch1)
    cmd = f'git merge {branch2}'
    msg = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = msg.stdout.decode()
    err = msg.stderr.decode()
    if out:
        print(out)
    if err:
        print(err)
        return

    branch_delete(branch2)


# merge('master', 'b1')
# merge('master', 'b2')


def commit():
    """
     Record changes to the repository
    :return: None
    """
    message = 'Initial commit_addr'
    choice = input(f'{message} as commit_addr message [y/n]').strip().lower()
    if choice == 'n':
        message = input("Commit message:")
    try:
        subprocess.check_call(['git', 'commit_addr', f'-m"{message}"'])
    except subprocess.CalledProcessError as e:
        print(e)


# git_help()

def git():
    """
    Main function through which every function is handled
    :return: None
    """
    pass


def boot():
    """
    Sets up the directory for git
    :return: None
    """
    choice = int(input("1.If you want to stay in current directory\n"
                       "2.To change directory\n"))
    if choice == 2:
        path = input("Give path to directory\n")
        if not os.path.isdir(path):
            print('Wrong directory path, enter correct directory\n')
            boot()
            return
        os.chdir(path)
        print(os.getcwd())
    is_tracking = (os.path.exists(os.path.join(os.getcwd(), '.git')))
    if not is_tracking:
        start = int(input("1.Init\n"
                          "2.Clone\n"))
        if start == 1:
            init()
        elif start == 2:
            clone()
    git()

# boot()
