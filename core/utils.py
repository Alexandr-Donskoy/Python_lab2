import os
import datetime


def parse_path(current_dir, path):
    if path == "..":
        return os.path.dirname(current_dir)
    elif path == "~":
        return os.path.expanduser("~")
    elif path.startswith("/"):
        return path
    else:
        return os.path.join(current_dir, path)


def setup_logging(log_file):
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write("Shell Log\n")
            f.write("=" * 50 + "\n")


def log_command(log_file, command, success=True, error_msg=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {command}\n")
        if not success:
            f.write(f"[{timestamp}] ERROR: {error_msg}\n")


def is_safe_to_delete(target, current_dir):
    if target in ["/", "\\"] or os.path.abspath(target) == "/":
        return False, "Cannot delete root directory"

    if target == ".." or os.path.abspath(target) == os.path.dirname(current_dir):
        return False, "Cannot delete parent directory"

    return True, ""