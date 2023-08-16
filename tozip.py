import os
import shutil
import bz2
import pickle
from zipfile import ZipFile, ZIP_DEFLATED

def create_zip_archive_with_exclusions(directory, zip_filename, exclude_patterns=None):
    with ZipFile(zip_filename, 'w', compression=ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if not any(pattern in file for pattern in exclude_patterns):
                    arcname = os.path.relpath(file_path, directory)
                    zipf.write(file_path, arcname)


#create_zip_archive_with_exclusions(".", "application.zip", exclude_patterns=[".git", "__pycache__"])


def zipmodel_with_bz2(file):
     data = bz2.BZ2File(file, 'rb')
     data = pickle.load(data)
     return data



zipmodel_with_bz2("artifacts/model.pkl")

