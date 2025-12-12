import os
from core import utils
from core.commands import EasyCommands
from plugins.archives import ArchivesPlugin
from plugins.search import SearchPlugin
from plugins.history import HistoryPlugin


class MiniShell:

    def __init__(self):
        self.current_dir = os.getcwd()
        self.log_file = "shell.log"
        self.history_file = ".history"
        self.trash_dir = ".trash"
        self.history = []
        self.command_count = 0
        self.last_command = None
        self.last_command_args = None

        self.setup()
        self.init_modules()

    def setup(self):
        utils.setup_logging(self.log_file)
        self.setup_trash()

    def setup_trash(self):
        if not os.path.exists(self.trash_dir):
            os.makedirs(self.trash_dir, exist_ok=True)

    def init_modules(self):
        self.easy_commands = EasyCommands(self)
        self.archives = ArchivesPlugin(self)
        self.search = SearchPlugin(self)
        self.history_plugin = HistoryPlugin(self)

        self.history_plugin.load_history()

    def run(self):
        while True:
            try:
                command_input = input(f"{self.current_dir}> ").strip()

                if not command_input:
                    continue

                if command_input.lower() == 'exit':
                    print("Выход из оболочки")
                    break

                self.history_plugin.add_to_history(command_input)

                parts = command_input.split()
                cmd = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

                self.execute_command(cmd, args, command_input)

            except KeyboardInterrupt:
                print("\nДля выхода введите 'exit'")
            except EOFError:
                break
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
                utils.log_command(self.log_file,
                                  command_input if 'command_input' in locals() else "",
                                  False,
                                  f"Unexpected error: {e}")

    def execute_command(self, cmd, args, full_command):
        if cmd == "ls":
            self.easy_commands.ls(args)
        elif cmd == "cd":
            self.easy_commands.cd(args)
        elif cmd == "cat":
            self.easy_commands.cat(args)
        elif cmd == "cp":
            self.easy_commands.cp(args)
        elif cmd == "mv":
            self.easy_commands.mv(args)
        elif cmd == "rm":
            self.easy_commands.rm(args)

        elif cmd == "zip":
            self.archives.zip_cmd(args)
        elif cmd == "unzip":
            self.archives.unzip(args)
        elif cmd == "tar":
            self.archives.tar(args)
        elif cmd == "untar":
            self.archives.untar(args)
        elif cmd == "grep":
            self.search.grep(args)
        elif cmd == "history":
            self.history_plugin.history_cmd(args)
        elif cmd == "undo":
            self.history_plugin.undo(args)

        else:
            print(f"Неизвестная команда: {cmd}")
            utils.log_command(self.log_file, full_command, False, f"Unknown command: {cmd}")