import boto
import json
import io

DEFAULT_FORMAT = 'JPEG'


def push_obj_to_s3(key, s3_object, bucket, config):
    try:
        s3_client = boto.client('s3', region_name=config['region_name'])
        resp = s3_client.put_object(Body=json.dumps(s3_object), Key=key, Bucket=bucket)
        return {'success': True, 'data': 'Push to s3 successful'}
    except Exception as e:
        return {'success': False, 'data': str(e)}


def modify_image(image):
    name = image.name
    ext = name.split('.')[-1]
    in_mem_file = io.BytesIO()
    try:
        image.save(in_mem_file, format=ext.upper())
    except:
        image.save(in_mem_file, format=DEFAULT_FORMAT)
    return in_mem_file.getvalue()