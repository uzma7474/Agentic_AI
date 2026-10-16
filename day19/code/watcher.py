from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from ingest import ingest_file
from config import KNOWLEDGE_BASE
import time

class MyFileSystemEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        # process the file        
        self.process_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # process the file
        self.process_file(event.src_path)
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        # remove the contents

    def process_file(self, file_path):
        ingest_file(file_path)

def start_watcher():
    # create the event handler instance
    event_handler = MyFileSystemEventHandler()

    # create an observer
    observer = Observer()
    observer.schedule(
        event_handler,
        str(KNOWLEDGE_BASE),
        recursive=True
    )
    observer.start()

    try:
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"exception: {e}")
        observer.stop()

    observer.join()

if __name__ == '__main__':
    start_watcher()
