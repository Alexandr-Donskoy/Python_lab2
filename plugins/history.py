import os
import json
import shutil
import datetime
from core import utils


class HistoryPlugin:

    def __init__(self, shell):
        self.shell = shell

    def load_history(self):
        if os.path.exists(self.shell.history_file):
            try:
                with open(self.shell.history_file, 'r') as f:
                    self.shell.history = json.load(f)
                    self.shell.command_count = len(self.shell.history)
            except:
                self.shell.history = []

    def save_history(self):
        with open(self.shell.history_file, 'w') as f:
            json.dump(self.shell.history, f)

    def add_to_history(self, command):
        self.shell.history.append({
            'id': len(self.shell.history) + 1,
            'command': command,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        if len(self.shell.history) > 100:
            self.shell.history = self.shell.history[-100:]
        self.save_history()

    def history_cmd(self, args):
        try:
            n = 10
            if args and args[0].isdigit():
                n = int(args[0])
                n = min(n, 100)

            start_idx = max(0, len(self.shell.history) - n)
            for i, entry in enumerate(self.shell.history[start_idx:], start=start_idx + 1):
                print(f"{i}: [{entry['timestamp']}] {entry['command']}")

            utils.log_command(self.shell.log_file, f"history {' '.join(args)}", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, f"history {' '.join(args)}", False, error_msg)

    def undo(self, args):
        try:
            if not self.shell.last_command:
                print("ERROR: No command to undo")
                utils.log_command(self.shell.log_file, "undo", False, "No command to undo")
                return

            if self.shell.last_command == 'cp':
                if os.path.exists(self.shell.last_command_args['destination']):
                    if os.path.isdir(self.shell.last_command_args['destination']):
                        shutil.rmtree(self.shell.last_command_args['destination'])
                    else:
                        os.remove(self.shell.last_command_args['destination'])
                    print(f"Undo cp: removed {self.shell.last_command_args['destination']}")

            elif self.shell.last_command == 'mv':
                if os.path.exists(self.shell.last_command_args['destination']):
                    shutil.move(self.shell.last_command_args['destination'], self.shell.last_command_args['source'])
                    print(f"Undo mv: moved back to {self.shell.last_command_args['source']}")

            elif self.shell.last_command == 'rm':
                if os.path.exists(self.shell.last_command_args['trash_item']):
                    shutil.move(self.shell.last_command_args['trash_item'], self.shell.last_command_args['target'])
                    print(f"Undo rm: restored {self.shell.last_command_args['target']}")

            else:
                print(f"ERROR: Cannot undo command: {self.shell.last_command}")
                utils.log_command(self.shell.log_file, "undo", False, f"Cannot undo command: {self.shell.last_command}")
                return

            self.shell.last_command = None
            self.shell.last_command_args = None
            utils.log_command(self.shell.log_file, "undo", True)

        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            utils.log_command(self.shell.log_file, "undo", False, error_msg)