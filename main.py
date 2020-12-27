#!/usr/bin/python3

import argparse
import tempfile
import subprocess
import shutil
import os


def call_git(args):
    subprocess.run(['git'] + args, check=True)


def copy_files_and_dirs(files_and_dirs, dest_dir):
    rel_files_and_dirs = []
    for file in files_and_dirs:
        rel_path = os.path.relpath(file)
        rel_files_and_dirs.append(rel_path)
        dest_path = os.path.join(dest_dir, rel_path)
        print(dest_path)
        if os.path.isdir(file):
            shutil.copytree(file, dest_path)
        else:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(file, dest_path)

    return rel_files_and_dirs


def main():
    parser = argparse.ArgumentParser(
        description='Publishes files to the specified branch in a single commit with force push to erase history.')
    parser.add_argument('--github-token', '-t', action='store',
                        required=True, type=str, help='GitHub token to use for push operation.')
    parser.add_argument('--github-actor', '-a', action='store',
                        required=True, type=str, help='GitHub username to use for push operation.')
    parser.add_argument('--github-repository', '-r', action='store',
                        required=True, type=str, help='The GitHub repository to where the files should be published in <username/repo> format.')
    parser.add_argument('--branch', '-b', action='store', required=True, type=str,
                        help='The branch to where the files should be published.')
    parser.add_argument('--files-and-dirs', '-f', action='store', required=True, type=str,
                        nargs='+', help='List of paths (relative or absolute) of the files and directories to publish. They must be inside the current working directory. The directory structure relative to current working directory is kept for publishing.')
    parser.add_argument('--author-name', '-u', action='store', required=True,
                        type=str, help='The name that will appear in the commit.')
    parser.add_argument('--author-email', '-n', action='store', required=True,
                        type=str, help='The email that will appear in the commit.')
    parser.add_argument('--commit-message', '-c', action='store', required=True,
                        type=str, help='The commit message that will appear in the commit.')

    args = parser.parse_args()

    print('Publishing files ({}) to branch {}'.format(
        ';'.join(args.files_and_dirs), args.branch))

    with tempfile.TemporaryDirectory() as temp_dir:
        print('Working directory is {}'.format(temp_dir))

        rel_files_and_dirs = copy_files_and_dirs(args.files_and_dirs, temp_dir)
        os.chdir(temp_dir)

        remote_repo = 'https://{}:{}@github.com/{}.git'.format(
            args.github_actor, args.github_token, args.github_repository)

        call_git(['init'])
        call_git(['config', 'user.name', args.author_name])
        call_git(['config', 'user.email', args.author_email])
        call_git(['remote', 'add', 'origin', remote_repo])
        call_git(['checkout', '-b', args.branch])
        call_git(['add', '-f'] + rel_files_and_dirs)
        call_git(['commit', '-m', args.commit_message])
        call_git(['push', 'origin', '{}:{}'.format(
            args.branch, args.branch), '--force'])


if __name__ == "__main__":
    main()
