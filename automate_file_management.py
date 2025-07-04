# Python script to automate file management tasks such as organizing files into directories based on their extensions, renaming files, and deleting old files.
import os
import shutil


# Define the path to your download directory
downloads_folder = '/home/jeff/Downloads'


# Define target folders for different file types
folders = {
    'images': ['.jpg', '.jpeg', '.png', '.gif'],
    'documents': ['.pdf', '.docx', '.txt', '.xlsx'],
    'videos': ['.mp4', '.avi', '.mov'],
    'audio': ['.mp3', '.wav', '.flac'],
    'archives': ['.zip', '.rar', '.tar'],
    'scripts': ['.py', '.sh', '.js'],
    'installers': ['.exe', '.msi'],
    'others': []
}

# Create target folders if they don't exist
for folder in folders:
    folder_path = os.path.join(downloads_folder, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# Loop through files in the downloads folder
for filename in os.listdir(downloads_folder):
    file_path = os.path.join(downloads_folder, filename)

    # Skip directories
    if os.path.isdir(file_path):
        continue

    # Check file extension and move to the appropriate folder
    for folder, extensions in folders.items():
        if any(filename.lower().endswith(ext) for ext in extensions):
            target_folder = os.path.join(downloads_folder, folder)
            shutil.move(file_path, target_folder)
            print(f'Moved {filename} to {target_folder}')
            break
