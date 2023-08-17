import os
import shutil
import bz2
import pickle
from zipfile import ZipFile, ZIP_DEFLATED
import dill
import gzip

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



#zipmodel_with_bz2("artifacts/model.pkl")

def chceck_validity_of_model_pkl_gz(file):
    with gzip.open(file, 'rb') as f:
        try:
            f.read(1)
            print('File is a valid gzip file')
        except OSError:
            print('File is not a valid gzip file')

#chceck_validity_of_model_pkl_gz("artifacts/model.pkl.gz")

#serialized_model = dill.dumps(model)
#
## Compress the serialized model using gzip
#with gzip.open('model2.pkl.gz', 'wb') as f:
#    f.write(serialized_model)



#def gzip_compress(file_in_pkl, buffer_size=65536):
#    with open(file_in_pkl, 'rb') as file_in, gzip.open('artifacts/model.pkl.gz', 'wb', compresslevel=9, buffer_size=buffer_size) as file_out:
#        shutil.copyfileobj(file_in, file_out)

def gzip_compress(file_in_pkl, buffer_size=65536):
    with open(file_in_pkl, 'rb') as file_in, gzip.open('artifacts/model.pkl.gz', 'wb', compresslevel=9) as file_out:
        while True:
            buf = file_in.read(buffer_size)
            if not buf:
                break
            file_out.write(buf)
            #return file_out

#gzip_compress("artifacts/model.pkl")


