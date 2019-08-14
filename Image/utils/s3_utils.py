
import boto
from boto.s3.key import Key

import uuid
from django.conf import settings
import mimetypes
import os


class S3Upload(object):
    BUCKETS = {
        'default': settings.DEFAULT_BUCKET,
    }

    REGIONS = {
        'default': 'ap-south-1'
    }

    def upload(self, file_content, params=None, prepend_file_name='',
               custom_key=None, sniff=True):
        if params:
            try:
                bucket = params['bucket_key']
            except KeyError:
                bucket = self.BUCKETS['default']
        else:
            bucket = self.BUCKETS['default']

        try:
            # make fresh connection
            conn = boto.connect_s3(settings.AWS_BUCKETS_CONFIG[bucket]['access_key_id'],
                                   settings.AWS_BUCKETS_CONFIG[bucket]['secret_access_key'])
            bucket_conn = conn.get_bucket(bucket)
            # Connect to bucket and create key
            file_key = S3Upload.generate_uid_for_file()
            if prepend_file_name:
                file_key = prepend_file_name + file_key
            if custom_key:
                file_key = custom_key
            if sniff:
                file_key += S3Upload.get_file_extension(file_content)
            upload_content = bucket_conn.new_key(file_key)
            upload_content.set_contents_from_file(file_content, rewind=True)
            upload_content.make_public()
            return {'success': True,
                    'data': settings.AWS_BUCKETS_CONFIG[bucket]['url_prefix'] + file_key,
                    'file_key': file_key}
        except Exception as e:
            return {'success': False, 'data': str(e)}

    def get_bucket(self, params):
        region = params.get('region', S3Upload.REGIONS['default'])
        bucket = params.get('bucket_key')
        access_key = settings.AWS_BUCKETS_CONFIG.get(bucket, {}).get('access_key_id')
        secret = settings.AWS_BUCKETS_CONFIG.get(bucket, {}).get('secret_access_key')
        kwargs = {'aws_access_key_id': access_key, 'aws_secret_access_key': secret}
        connection = boto.s3.connect_to_region(region, **kwargs)
        balti = connection.get_bucket(bucket)
        upload_content = Key(balti)
        return upload_content

    def get_row_bucket(self, params={}):
        region = params.get('region', S3Upload.REGIONS['default'])
        bucket = params.get('bucket_key', None)
        access_key = settings.AWS_BUCKETS_CONFIG.get(bucket, {}).get('access_key_id')
        secret = settings.AWS_BUCKETS_CONFIG.get(bucket, {}).get('secret_access_key')
        kwargs = {'aws_access_key_id': access_key, 'aws_secret_access_key': secret}
        connection = boto.s3.connect_to_region(region, **kwargs)
        balti = connection.get_bucket(bucket)
        return balti

    def open(self, key, params={}):
        try:
            upload_content = self.get_bucket(params=params)
            upload_content.key = key
            upload_content.get_contents_to_filename(params.get('filename'))
            data = {'success': True, 'data': upload_content.generate_url(params.get('file_expiry'))}
        except Exception as e:

            data = {'success': False, 'data': str(e)}

        return data

    def delete(self, key, params=dict()):
        """
        :param key: The filename that was saved.
        :param params:  to get bucket
        :return: True on success and False on error
        """
        try:
            region = params.get('region', S3Upload.REGIONS['default'])
            bucket = params.get('bucket_key', S3Upload.BUCKETS['data-platform'])
            access_key = settings.AWS_BUCKETS_CONFIG[bucket]['access_key_id']
            secret = settings.AWS_BUCKETS_CONFIG[bucket]['secret_access_key']
            connection = boto.s3.connect_to_region(region, aws_access_key_id=access_key,
                                                   aws_secret_access_key=secret)
            balti = connection.get_bucket(bucket)
            delete_content = Key(balti)
            delete_content.key = key
            balti.delete_key(delete_content)
            data = {'success': True, 'data': key}
        except Exception as e:
            data = {'success': False, 'data': key}
        return data

    @staticmethod
    def generate_uid_for_file():
        return uuid.uuid1().urn.split(':')[2].replace('-', '')

    @staticmethod
    def get_file_extension(file_content):
        try:
            mimetypes.add_type('text/csv', '.csv', strict=True)
            mimetypes.add_type('image', '.*', strict=True)
            mtype = mimetypes.guess_type(file_content.name)
            if os.path.splitext(file_content.name)[1] in mimetypes.guess_all_extensions(mtype[0]):
                file_extension = os.path.splitext(file_content.name)[1]
            else:
                file_extension = mimetypes.guess_all_extensions(mtype[0])[-1]
        except Exception as e:
            raise Exception({'error': 'Unable to fetch file extension'})
        return file_extension


class S3Delete(object):
    BUCKETS = {
        'default': settings.DEFAULT_BUCKET
    }

    def delete(self, file_key, params=None):
        if params:
            try:
                bucket = params['bucket_key']
            except KeyError:
                bucket = self.BUCKETS['default']
        else:
            bucket = self.BUCKETS['default']

        try:
            conn = boto.connect_s3(settings.AWS_BUCKETS_CONFIG[bucket]['access_key_id'],
                                   settings.AWS_BUCKETS_CONFIG[bucket]['secret_access_key'])
            bucket_conn = conn.get_bucket(bucket)
            resp = bucket_conn.delete_key(file_key)
            if resp['success']:
                return {'success': True, 'data': settings.AWS_BUCKETS_CONFIG[bucket]['url_prefix'] + file_key}
        except Exception, e:
            return {'success': False, 'data': str(e)}
