# backup_manager.py
from utils import make_backup, list_backups, restore_backup

class BackupManager:
    def create_backup(self, prefix: str = "pps_backup") -> str:
        return make_backup(prefix)

    def list_backups(self):
        return list_backups()

    def restore(self, filename: str) -> bool:
        return restore_backup(filename)
