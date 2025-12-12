import os
import zipfile
import tarfile
from core import utils


class ArchivesPlugin:

    def __init__(self, shell):
        self.shell = shell

    def zip_cmd(self, args):
        if len(args) < 2:
            print("ERROR: Usage: zip <folder> <archive.zip>")
            utils.log_command(self.shell.log_file, "zip", False, "Incorrect number of arguments")
            return

        folder = utils.parse_path(self.shell.current_dir, args[0])
        archive = utils.parse_path(self.shell.current_dir, args[1])

        if not archive.endswith('.zip'):
            archive += '.zip'

        try:
            if not os.path.exists(folder) or not os.path.isdir(folder):
                error_msg = f"No such directory: {folder}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"zip {' '.join(args)}", False, error_msg)
                return

            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(folder))
                        zipf.write(file_path, arcname)

            print(f"Created ZIP archive: {archive}")
            utils.log_command(self.shell.log_file, f"zip {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"zip {' '.join(args)}", False, error_msg)

    def unzip(self, args):
        if len(args) < 1:
            print("ERROR: Usage: unzip <archive.zip>")
            utils.log_command(self.shell.log_file, "unzip", False, "Incorrect number of arguments")
            return

        archive = utils.parse_path(self.shell.current_dir, args[0])

        try:
            if not os.path.exists(archive):
                error_msg = f"No such file: {archive}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"unzip {' '.join(args)}", False, error_msg)
                return

            with zipfile.ZipFile(archive, 'r') as zipf:
                zipf.extractall(self.shell.current_dir)

            print(f"Extracted ZIP archive: {archive}")
            utils.log_command(self.shell.log_file, f"unzip {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"unzip {' '.join(args)}", False, error_msg)

    def tar(self, args):
        if len(args) < 2:
            print("ERROR: Usage: tar <folder> <archive.tar.gz>")
            utils.log_command(self.shell.log_file, "tar", False, "Incorrect number of arguments")
            return

        folder = utils.parse_path(self.shell.current_dir, args[0])
        archive = utils.parse_path(self.shell.current_dir, args[1])

        if not archive.endswith('.tar.gz'):
            archive += '.tar.gz'

        try:
            if not os.path.exists(folder) or not os.path.isdir(folder):
                error_msg = f"No such directory: {folder}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"tar {' '.join(args)}", False, error_msg)
                return

            with tarfile.open(archive, 'w:gz') as tarf:
                tarf.add(folder, arcname=os.path.basename(folder))

            print(f"Created TAR.GZ archive: {archive}")
            utils.log_command(self.shell.log_file, f"tar {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"tar {' '.join(args)}", False, error_msg)

    def untar(self, args):
        if len(args) < 1:
            print("ERROR: Usage: untar <archive.tar.gz>")
            utils.log_command(self.shell.log_file, "untar", False, "Incorrect number of arguments")
            return

        archive = utils.parse_path(self.shell.current_dir, args[0])

        try:
            if not os.path.exists(archive):
                error_msg = f"No such file: {archive}"
                print(f"ERROR: {error_msg}")
                utils.log_command(self.shell.log_file, f"untar {' '.join(args)}", False, error_msg)
                return

            with tarfile.open(archive, 'r:gz') as tarf:
                tarf.extractall(self.shell.current_dir)

            print(f"Extracted TAR.GZ archive: {archive}")
            utils.log_command(self.shell.log_file, f"untar {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"untar {' '.join(args)}", False, error_msg)