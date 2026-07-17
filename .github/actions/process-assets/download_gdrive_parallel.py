import os
import sys
import concurrent.futures
import gdown

if len(sys.argv) < 3:
    print("Usage: python download_gdrive_parallel.py <folder_id> <target_dir>")
    sys.exit(1)

folder_id = sys.argv[1]
target_dir = sys.argv[2]
url = f"https://drive.google.com/drive/folders/{folder_id}"

print(f"Fetching file list for folder: {folder_id}...")

try:
    # Use gdown's built-in skip_download feature to just get the file list!
    files = gdown.download_folder(url, output=target_dir, quiet=True, skip_download=True)
except Exception as e:
    print(f"Error while parsing folder: {e}")
    sys.exit(1)

print(f"Found {len(files)} files. Starting parallel download...")

def worker(f):
    file_url = f"https://drive.google.com/uc?id={f.id}"
    try:
        gdown.download(file_url, output=f.local_path, quiet=True)
        print(f"Downloaded: {os.path.basename(f.local_path)}")
    except Exception as e:
        print(f"Failed to download {f.local_path}: {e}")

# Download with 10 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(worker, files)

print("All downloads complete!")
