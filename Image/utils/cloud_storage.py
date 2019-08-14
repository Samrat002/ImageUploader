
import boto3
import boto
from boto.s3.key import Key
import boto.s3.connection
import uuid
from django.conf import settings
from .resources import modify_image

class S3Upload(object):
    BUCKETS = {
        'default': settings.DEFAULT_BUCKET,
    }

    REGIONS = {
        'default': 'ap-south-1'
    }

    def upload(self, image, key='image'):
        response = {
            'success': False,
            'data': ''
        }
        try:
            # no host no is_secure as not using ssl
            connection = boto.s3.connect_to_region('ap-south-1',
                                                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                                   calling_format=boto.s3.connection.OrdinaryCallingFormat())

            bucket = connection.get_bucket(self.BUCKETS.get('default'))
            k = Key(bucket)
            k.key = key
            try:
                k.set_contents_from_file(image.file)
                file_key = S3Upload.generate_uid_for_file()
                upload_content = bucket.new_key(file_key)
                upload_content.set_contents_from_file(image, rewind=True)
                upload_content.make_public()

            except:
                image = modify_image(image)
                client = boto3.client('s3')

                # boto3.resource('s3').ObjectAcl('bucket_name', 'object_key').put(ACL='public-read')
                file_key = client.put_object(Body=image, Bucket=self.BUCKETS.get('default'),
                                  Key='Image.aws.txt', ACL='public-read').get('ETag')[1:-2]
            return {'success': True,
                    'data': settings.BUCKET_DOMAIN + file_key,
                    'file_key': file_key}

        except Exception as e:
            # log the error in the critical section
            return response

    def delete(self, key):
        """
        :param key: The filename that was saved.
        :return: True on success and False on error
        """
        try:
            connection = boto.s3.connect_to_region(settings.AWS_LOCATION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            bucket = connection.get_bucket(self.BUCKETS.get('default'))
            # lets pour some data in balti ;)
            balti = connection.get_bucket(bucket)
            delete_content = Key(balti)
            delete_content.key = key
            balti.delete_key(delete_content)
            data = {'success': True, 'data': key}
        except Exception as e:
            data = {'success': False, 'data': key}
        return data

    def get_object(self, file_name):
        image = "my_image.jpeg"
        connection = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = connection.get_bucket(self.BUCKETS.get('default'))
        # Get the Key object of the given key, in the bucket
        k = Key(bucket, file_name)
        # Get the contents of the key into a file
        k.get_contents_to_filename(image)
    # securing the url in the s3 using uuid
    @staticmethod
    def generate_uid_for_file():
        return uuid.uuid1().urn.split(':')[2].replace('-', '')


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
        except Exception as e:
            return {'success': False, 'data': str(e)}
