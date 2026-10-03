import os
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from app.config import settings

logger = logging.getLogger("digital_fossil.collector")

FORBIDDEN_SYSTEM_PATHS = ["windows", "system32", "program files", "program files (x86)", "appdata/local/microsoft"]

class SafeFolderEventHandler(FileSystemEventHandler):
    def __init__(self, base_dir: Path, event_callback: Callable[[dict], None]):
        super().__init__()
        self.base_dir = base_dir
        self.event_callback = event_callback

    def _process_event(self, event_type: str, src_path: str, dest_path: Optional[str] = None):
        try:
            # Skip hidden temporary files or IDE swap files
            fname = os.path.basename(src_path)
            if fname.startswith("~$") or fname.endswith(".tmp") or fname.startswith("."):
                return

            rel_path = os.path.relpath(src_path, self.base_dir).replace("\\", "/")
            directory = os.path.dirname(src_path).replace("\\", "/")
            _, ext = os.path.splitext(fname)
            extension = ext.lower().lstrip(".") if ext else "none"

            file_size = 0
            if os.path.exists(src_path) and not os.path.isdir(src_path):
                try:
                    file_size = os.path.getsize(src_path)
                except OSError:
                    file_size = 0

            safe_record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": event_type,
                "path": src_path.replace("\\", "/"),
                "file_name": fname,
                "extension": extension,
                "directory": directory,
                "file_size": file_size,
                "source": "watchdog_live",
                "process_name": "explorer.exe",
                "metadata": {
                    "relative_path": rel_path,
                    "dest_path": dest_path.replace("\\", "/") if dest_path else None,
                    "privacy_scope": "SAFE_METADATA_ONLY"
                }
            }
            self.event_callback(safe_record)
        except Exception as e:
            logger.error(f"Error handling watchdog event: {e}")

    def on_created(self, event: FileSystemEvent):
        if not event.is_directory:
            self._process_event("FILE_CREATED", event.src_path)

    def on_modified(self, event: FileSystemEvent):
        if not event.is_directory:
            self._process_event("FILE_MODIFIED", event.src_path)

    def on_moved(self, event: FileSystemEvent):
        if not event.is_directory:
            dest = getattr(event, "dest_path", None)
            self._process_event("FILE_MOVED", event.src_path, dest_path=dest)

    def on_deleted(self, event: FileSystemEvent):
        if not event.is_directory:
            self._process_event("FILE_DELETED", event.src_path)

class SafeFolderMonitor:
    def __init__(self):
        self.observer: Optional[Observer] = None
        self.monitored_directory: str = str(settings.TEST_MONITOR_DIR.resolve())
        self.is_running: bool = False
        self.events_captured: int = 0
        self.event_callback: Optional[Callable[[dict], None]] = None

    def start(self, directory_path: Optional[str] = None, event_callback: Optional[Callable[[dict], None]] = None) -> bool:
        if self.is_running:
            logger.info("Collector is already active.")
            return True

        target_dir = Path(directory_path).resolve() if directory_path else settings.TEST_MONITOR_DIR.resolve()
        
        # Security validation: Prevent system-wide surveillance
        path_str = str(target_dir).lower()
        if any(f in path_str for f in FORBIDDEN_SYSTEM_PATHS) or target_dir == Path(target_dir.anchor):
            raise ValueError("Target directory is a restricted system path. Monitoring is limited to explicit user test directories.")

        target_dir.mkdir(parents=True, exist_ok=True)
        self.monitored_directory = str(target_dir)
        self.event_callback = event_callback or (lambda x: None)

        def wrapped_callback(rec):
            self.events_captured += 1
            if self.event_callback:
                self.event_callback(rec)

        handler = SafeFolderEventHandler(base_dir=target_dir, event_callback=wrapped_callback)
        self.observer = Observer()
        self.observer.schedule(handler, path=str(target_dir), recursive=True)
        self.observer.start()
        self.is_running = True
        logger.info(f"Safe folder collector started on: {self.monitored_directory}")
        return True

    def stop(self) -> bool:
        if self.observer and self.is_running:
            self.observer.stop()
            self.observer.join(timeout=2.0)
            self.observer = None
        self.is_running = False
        logger.info("Safe folder collector stopped.")
        return True

    def get_status(self) -> dict:
        return {
            "is_running": self.is_running,
            "monitored_directory": self.monitored_directory,
            "events_captured": self.events_captured,
            "privacy_notice": (
                "Monitoring is strictly limited to the selected test directory. "
                "Only safe filesystem metadata (timestamps, actions, extensions, sizes) is collected. "
                "No keystrokes, contents, credentials, or covert telemetry are recorded."
            ),
            "message": f"Collector is {'active' if self.is_running else 'idle'} on {self.monitored_directory}"
        }

# Global singleton
folder_monitor = SafeFolderMonitor()
