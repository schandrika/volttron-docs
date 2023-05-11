from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


class FileUpdateHandler(FileSystemEventHandler):
    def on_closed(self, event):
        if event.src_path.endswith('.rst') and not 'agent-docs' in event.src_path:
            subprocess.run(['make', 'html'])
            print(f"Event closed: {event.src_path}")

if __name__ == "__main__":

    event_handler = FileUpdateHandler()

    # Create an observer.
    observer = Observer()

    # Attach the observer to the event handler.
    observer.schedule(event_handler, "source", recursive=True)

    # Start the observer.
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()