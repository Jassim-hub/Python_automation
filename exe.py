# Exercise 1: Create an automation script that backs up files from a folder with within 3minutes of
# modification to a backup folder.
import os
import shutil
import time
from datetime import datetime, timedelta

# Define source and backup folders
source_folder = '/home/jeff/Documents/source_folder'
backup_folder = '/home/jeff/Documents/backup_folder'

# Ensure backup folder exists
os.makedirs(backup_folder, exist_ok=True)

# Define the time window (3 minutes)
time_window = timedelta(minutes=3)


def backup_modified_files():
    current_time = datetime.now()

    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path):
            # Get last modified time
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))

            # Check if modified within the last 3 minutes
            if current_time - modified_time <= time_window:
                dest_path = os.path.join(backup_folder, filename)
                shutil.copy2(file_path, dest_path)
                print(f'Backed up: {filename}')


# Run the backup check every minute
while True:
    backup_modified_files()
    print("Backup check complete. Waiting for 1 minute...")
    time.sleep(60)  # Check every 60 seconds
