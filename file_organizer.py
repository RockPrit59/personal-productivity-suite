# file_organizer.py
import os
import shutil

class FileOrganizer:
    def organize(self, target_dir: str, dry_run: bool = True):
        """
        Organize files by extension in the target directory.
        Returns list of (source, destination) actions.
        If dry_run is False, moves files.
        """
        if not os.path.isdir(target_dir):
            raise ValueError("Target directory does not exist")
        mapping = {}
        for fname in os.listdir(target_dir):
            full = os.path.join(target_dir, fname)
            if os.path.isdir(full):
                continue
            ext = os.path.splitext(fname)[1].lower().strip('.') or "no_ext"
            mapping.setdefault(ext, []).append(full)

        actions = []
        for ext, files in mapping.items():
            folder = os.path.join(target_dir, ext + "_files")
            for f in files:
                dest = os.path.join(folder, os.path.basename(f))
                actions.append((f, dest))
                if not dry_run:
                    os.makedirs(folder, exist_ok=True)
                    shutil.move(f, dest)
        return actions
