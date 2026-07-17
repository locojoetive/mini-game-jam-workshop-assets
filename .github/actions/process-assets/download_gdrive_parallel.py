import os
import sys
import concurrent.futures
import gdown
import gdown.folder

if len(sys.argv) < 3:
    print("Usage: python download_gdrive_parallel.py <folder_id> <target_dir>")
    sys.exit(1)

folder_id = sys.argv[1]
target_dir = sys.argv[2]
url = f"https://drive.google.com/drive/folders/{folder_id}"

print(f"Fetching file list for folder: {folder_id}...")

files_to_download = []

# Save original function
original_download = gdown.download

def mock_download(url, output, quiet=False, fuzzy=False, resume=False, **kwargs):
    files_to_download.append((url, output))
    return output

# Apply monkey patch to intercept downloads
gdown.download = mock_download
if hasattr(gdown.folder, 'download'):
    gdown.folder.download = mock_download

try:
    # Use gdown's built-in folder parser. It will call our mock_download instead of actually downloading.
    gdown.download_folder(url, output=target_dir, quiet=True)
except Exception as e:
    print(f"Error while parsing folder: {e}")

# Restore original function
gdown.download = original_download
if hasattr(gdown.folder, 'download'):
    gdown.folder.download = original_download

print(f"Found {len(files_to_download)} files. Starting parallel download...")

def worker(task):
    file_url, output_path = task
    try:
        original_download(file_url, output=output_path, quiet=True)
        print(f"Downloaded: {os.path.basename(output_path)}")
    except Exception as e:
        print(f"Failed to download {output_path}: {e}")

# Download with 10 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(worker, files_to_download)

print("All downloads complete!")
