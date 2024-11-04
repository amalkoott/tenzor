import os
import json
import zipfile
import urllib.request
import shutil
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def download_repo_archive(url: str) -> str:
    archive_url = url.replace('github.com', 'codeload.github.com') + '/zip/refs/heads/main'
    archive_name = 'repo_archive.zip'
    logging.info(f'downloading archive from hte {archive_url}...')
    urllib.request.urlretrieve(archive_url, archive_name)
    logging.info(f'archive {archive_name} downloaded successfully.')
    return archive_name

def extract_archive(archive_name: str) -> str:
    logging.info(f'unpacking the archive {archive_name}...')
    with zipfile.ZipFile(archive_name, 'r') as zip_ref:
        zip_ref.extractall()
    extracted_dir = zip_ref.namelist()[0]
    logging.info(f'archive unpacked into {extracted_dir}.')
    return extracted_dir


def clean_directories(repo_name: str, keep_dir: str) -> None:
    logging.info(f'removing all directories except {keep_dir}...')
    for item in os.listdir(repo_name):
        item_path = os.path.join(repo_name, item)
        if os.path.isdir(item_path) and item != keep_dir.split('/')[0]:
            shutil.rmtree(item_path)
            logging.info(f'removed: {item_path}')


def create_version_file(path: str, version_str: str) -> None:
    logging.info(f'creating file version.json in {path}...')
    files = [f for f in os.listdir(path) if f.endswith(('.py', '.js', '.sh'))]
    version_info = {
        "name": "hello world",
        "version": version_str,
        "files": files
    }

    with open(os.path.join(path, 'version.json'), 'w') as f:
        json.dump(version_info, f, indent=4)
    logging.info(f'file version.json with content {version_info} created')


def create_zip_archive(path: str) -> None:
    archive_name = f"{os.path.basename(path)}{datetime.datetime.now().strftime('%d%m%Y')}.zip"
    logging.info(f'creating archive {archive_name}...')
    with zipfile.ZipFile(archive_name, 'w') as zipf:
        for root, _, files in os.walk(path):
            for file in files:
                # code file filter for adding from src/path
                if file.endswith(('.py', '.js', '.sh')) or file == 'version.json':
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, path))

                 # adding all files from src/path
                 # zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), src_path))
    logging.info(f'archive created: {archive_name}')


def main(url: str, path: str, version_str: str):
    archive_name = download_repo_archive(url)
    extracted_dir = extract_archive(archive_name)

    clean_directories(extracted_dir, path)

    create_version_file(os.path.join(extracted_dir, path), version_str)

    create_zip_archive(os.path.join(extracted_dir, path))

    os.remove(archive_name)
    shutil.rmtree(extracted_dir)
    logging.info(f'temporary directory removed: {extracted_dir}')


if __name__ == "__main__":
    repo_url = "https://github.com/paulbouwer/hello-kubernetes"
    src_path = "src/app"
    version = "25.3000"
    main(repo_url, src_path, version)