import os
import re
from core import utils


class SearchPlugin:

    def __init__(self, shell):
        self.shell = shell

    def grep(self, args):
        if len(args) < 2:
            print("ERROR: Usage: grep <pattern> <path> [-r] [-i]")
            utils.log_command(self.shell.log_file, "grep", False, "Incorrect number of arguments")
            return

        pattern = args[0]
        path = utils.parse_path(self.shell.current_dir, args[1])
        recursive = "-r" in args
        case_insensitive = "-i" in args

        flags = re.IGNORECASE if case_insensitive else 0

        try:
            if not os.path.exists(path):
                error_msg = f"No such file or directory: {path}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"grep {' '.join(args)}", False, error_msg)
                return

            def search_in_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if re.search(pattern, line, flags):
                                print(f"{file_path}:{line_num}: {line.strip()}")
                except:
                    pass

            if os.path.isfile(path):
                search_in_file(path)
            elif os.path.isdir(path) and recursive:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        search_in_file(file_path)
            elif os.path.isdir(path):
                print("ERROR: Use -r for recursive search in directories")
                utils.log_command(self.shell.log_file, f"grep {' '.join(args)}", False, "Directory without -r flag")
                return

            utils.log_command(self.shell.log_file, f"grep {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"grep {' '.join(args)}", False, error_msg)