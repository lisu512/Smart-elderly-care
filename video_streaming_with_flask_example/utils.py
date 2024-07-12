import uuid

import boto3
import os


def get_DroidCam_url(ip='192.168.102.100', port=4747, res='720p'):
    res_dict = {
        '240p': '320x240',
        '480p': '640x480',
        '720p': '1280x720',
        '1080p': '1920x1080',
    }
    url = f'http://{ip}:{port}/mjpegfeed?{res_dict[res]}'
    return url


def upload_file_to_s3(file_path):
    s3 = boto3.resource('s3',
                        endpoint_url='https://b829bb97b7c005c37fd468daa0324f13.r2.cloudflarestorage.com',
                        aws_access_key_id='66c70e1754be14a1f831409efdda415e',
                        aws_secret_access_key='fd17cd4be324d88bd202ab468deb1d350949f87caa9774c4f9b6eccf414d6968'
                        )
    bucket_name = 'image'
    file_name = os.path.basename(file_path)
    s3.Bucket(bucket_name).upload_file(file_path, file_name)
    print(f'File uploaded to {bucket_name}/{file_name}')


