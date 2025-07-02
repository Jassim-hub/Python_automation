# Python script to automate file management tasks
import os  # This script automates file management tasks such as organizing files into directories based on their extensions.
import shutil

# Define the path to your download directory
downloads_folder = "C:\\Users\\jassi\\Downloads"

# Define target folder for different file types
folders = {
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "documents": [
        ".pdf",
        ".docx",
        ".txt",
        ".xlsx",
        ".pptx",
        ".odt",
        ".md",
        ".rtf",
        ".csv",
        ".xml",
        ".json",
        ".html",
        ".torrent",
        ".xls",
    ],
    "videos": [".mp4", ".avi", ".mov"],
    "audio": [".mp3", ".wav", ".aac"],
    "archives": [".zip", ".tar", ".gz"],
    "scripts": [".py", ".js", ".sh"],
    "installers": [".exe", ".msi"],
    "others": [],
}

# Create target folders if they do not exist
for folder in folders:
    folder_path = os.path.join(downloads_folder, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Loop through files in the downloads folder
for filename in os.listdir(downloads_folder):
    filepath = os.path.join(downloads_folder, filename)
    # skip directories
    if os.path.isdir(filepath):  # Check if it is a file
        continue
    # Check file extension and move to the appropriate folder
    for folder, extensions in folders.items():
        if any(filename.lower().endswith(ext) for ext in extensions):
            target_folder = os.path.join(downloads_folder, folder)
            shutil.move(filepath, target_folder)
            print(f"Moved {filename} to {target_folder}")
            break
