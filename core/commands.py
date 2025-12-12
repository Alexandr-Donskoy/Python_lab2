import os
import shutil
import datetime
from . import utils


class EasyCommands:

    def __init__(self, shell):
        self.shell = shell

    def ls(self, args):
        path = self.shell.current_dir
        detailed = False

        for arg in args:
            if arg == "-1":
                detailed = True
            elif not arg.startswith("-"):
                path = utils.parse_path(self.shell.current_dir, arg)

        try:
            if not os.path.exists(path):
                error_msg = f"No such file or directory: {path}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"ls {' '.join(args)}", False, error_msg)
                return

            items = os.listdir(path)

            if detailed:
                for item in items:
                    item_path = os.path.join(path, item)
                    if os.path.exists(item_path):
                        stat = os.stat(item_path)
                        size = stat.st_size
                        mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        if os.path.isdir(item_path):
                            perms = "d"
                        elif os.access(item_path, os.X_OK):
                            perms = "x"
                        else:
                            perms = "-"

                        print(f"{perms} {item:20} {size:10} bytes {mtime}")
            else:
                for item in items:
                    if os.path.isdir(os.path.join(path, item)):
                        print(f"{item}/")
                    else:
                        print(item)

            utils.log_command(self.shell.log_file, f"ls {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"ls {' '.join(args)}", False, error_msg)

    def cd(self, args):
        if not args:
            new_dir = os.path.expanduser("~")
        else:
            new_dir = utils.parse_path(self.shell.current_dir, args[0])

        try:
            if os.path.exists(new_dir) and os.path.isdir(new_dir):
                os.chdir(new_dir)
                self.shell.current_dir = os.getcwd()
                utils.log_command(self.shell.log_file, f"cd {' '.join(args)}", True)
            else:
                error_msg = f"No such directory: {new_dir}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"cd {' '.join(args)}", False, error_msg)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"cd {' '.join(args)}", False, error_msg)

    def cat(self, args):
        if not args:
            print("ERROR: File name required")
            utils.log_command(self.shell.log_file, "cat", False, "File name required")
            return

        file_path = utils.parse_path(self.shell.current_dir, args[0])

        try:
            if os.path.isdir(file_path):
                error_msg = f"Is a directory: {file_path}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"cat {' '.join(args)}", False, error_msg)
                return

            if not os.path.exists(file_path):
                error_msg = f"No such file: {file_path}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"cat {' '.join(args)}", False, error_msg)
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)

            utils.log_command(self.shell.log_file, f"cat {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"cat {' '.join(args)}", False, error_msg)

    def cp(self, args):
        if len(args) < 2:
            print("ERROR: Usage: cp <source> <destination> [-r]")
            utils.log_command(self.shell.log_file, "cp", False, "Incorrect number of arguments")
            return

        recursive = "-r" in args
        source_args = [arg for arg in args if arg != "-r" and not arg.startswith("-")]

        if len(source_args) < 2:
            print("ERROR: Usage: cp <source> <destination> [-r]")
            utils.log_command(self.shell.log_file, f"cp {' '.join(args)}", False, "Incorrect number of arguments")
            return

        source = utils.parse_path(self.shell.current_dir, source_args[0])
        destination = utils.parse_path(self.shell.current_dir, source_args[1])

        try:
            if not os.path.exists(source):
                error_msg = f"No such file or directory: {source}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"cp {' '.join(args)}", False, error_msg)
                return

            if os.path.isdir(source) and not recursive:
                error_msg = f"{source} is a directory (use -r to copy recursively)"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"cp {' '.join(args)}", False, error_msg)
                return

            self.shell.last_command = 'cp'
            self.shell.last_command_args = {'source': source, 'destination': destination, 'recursive': recursive}

            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

            print(f"Copied {source} to {destination}")
            utils.log_command(self.shell.log_file, f"cp {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"cp {' '.join(args)}", False, error_msg)

    def mv(self, args):
        if len(args) < 2:
            print("ERROR: Usage: mv <source> <destination>")
            utils.log_command(self.shell.log_file, "mv", False, "Incorrect number of arguments")
            return

        source = utils.parse_path(self.shell.current_dir, args[0])
        destination = utils.parse_path(self.shell.current_dir, args[1])

        try:
            if not os.path.exists(source):
                error_msg = f"No such file or directory: {source}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"mv {' '.join(args)}", False, error_msg)
                return

            self.shell.last_command = 'mv'
            self.shell.last_command_args = {'source': source, 'destination': destination}

            shutil.move(source, destination)
            print(f"Moved {source} to {destination}")
            utils.log_command(self.shell.log_file, f"mv {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"mv {' '.join(args)}", False, error_msg)

    def rm(self, args):
        if not args:
            print("ERROR: Usage: rm <path> [-r]")
            utils.log_command(self.shell.log_file, "rm", False, "Incorrect number of arguments")
            return

        recursive = "-r" in args
        path_args = [arg for arg in args if arg != "-r" and not arg.startswith("-")]

        if not path_args:
            print("ERROR: Usage: rm <path> [-r]")
            utils.log_command(self.shell.log_file, f"rm {' '.join(args)}", False, "Incorrect number of arguments")
            return

        target = utils.parse_path(self.shell.current_dir, path_args[0])

        safe, error_msg = utils.is_safe_to_delete(target, self.shell.current_dir)
        if not safe:
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"rm {' '.join(args)}", False, error_msg)
            return

        try:
            if not os.path.exists(target):
                error_msg = f"No such file or directory: {target}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"rm {' '.join(args)}", False, error_msg)
                return

            if os.path.isdir(target) and not recursive:
                error_msg = f"{target} is a directory (use -r to remove recursively)"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"rm {' '.join(args)}", False, error_msg)
                return

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            trash_item = os.path.join(self.shell.trash_dir, f"{os.path.basename(target)}_{timestamp}")

            self.shell.last_command = 'rm'
            self.shell.last_command_args = {'target': target, 'trash_item': trash_item}

            if os.path.isdir(target):
                response = input(f"Remove directory '{target}' and all its contents? (y/n): ")
                if response.lower() != 'y':
                    print("Cancelled")
                    return

                shutil.move(target, trash_item)
                print(f"Removed directory: {target}")
            else:
                shutil.move(target, trash_item)
                print(f"Removed file: {target}")

            utils.log_command(self.shell.log_file, f"rm {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"rm {' '.join(args)}", False, error_msg)