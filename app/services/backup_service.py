import os
import shutil
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class BackupService:

    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_FILE = DATABASE_URL.replace(
        "sqlite:///./",
        ""
    )

    BACKUP_FOLDER = "backups"

    @staticmethod
    def backup():

        os.makedirs(
            BackupService.BACKUP_FOLDER,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_file = os.path.join(
            BackupService.BACKUP_FOLDER,
            f"clinic_backup_{timestamp}.db"
        )

        shutil.copy2(
            BackupService.DATABASE_FILE,
            backup_file
        )

        return backup_file

    @staticmethod
    def restore(
        backup_file: str
    ):

        if not os.path.exists(backup_file):
            return False

        shutil.copy2(
            backup_file,
            BackupService.DATABASE_FILE
        )

        return True

    @staticmethod
    def list_backups():

        os.makedirs(
            BackupService.BACKUP_FOLDER,
            exist_ok=True
        )

        backups = []

        for file in os.listdir(
            BackupService.BACKUP_FOLDER
        ):

            if file.endswith(".db"):

                backups.append(file)

        backups.sort(reverse=True)

        return backups