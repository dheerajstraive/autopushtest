import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import os

# Path to your local repo
REPO_PATH = r"C:\Users\e413995\Documents\GenAICourse\autopushtest"
COMMIT_MESSAGE = "Auto-update from local changes"

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, repo_path):
        self.repo = Repo(repo_path)

    def on_any_event(self, event):
        # Ignore temporary files like .swp, .tmp, etc.
        if event.src_path.endswith(('.swp', '.tmp', '~')):
            return
        print(f"Change detected: {event.src_path}")
        self.repo.git.add(all=True)
        self.repo.index.commit(COMMIT_MESSAGE)
        origin = self.repo.remote(name='origin')
        try:
            origin.push()
            print("Changes pushed successfully!")
        except Exception as e:
            print("Error pushing changes:", e)

if __name__ == "__main__":
    event_handler = ChangeHandler(REPO_PATH)
    observer = Observer()
    observer.schedule(event_handler, path=REPO_PATH, recursive=True)
    observer.start()
    print(f"Watching {REPO_PATH} for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
