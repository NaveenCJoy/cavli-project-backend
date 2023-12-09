import boto3, json
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, JSONResponse



# AWS S3 Configuration
AWS_ACCESS_KEY = 'AKIATZHPPG3WBQAGVFRQ'
AWS_SECRET_KEY = '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'
AWS_BUCKET_NAME = 'file-upload-cavli'
AWS_REGION = 'ap-southeast-2'

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_file_to_s3(file, bucket_name, object_name):
    try:
        s3.upload_fileobj(file.file, bucket_name, object_name)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="S3 credentials not available")

def list_files_in_s3(bucket_name):
    try:
        response = s3.list_objects(Bucket=bucket_name)
        files_info = []
        for obj in response.get('Contents', []):
            file_info = {}
            file_info["key"] = obj["Key"]
            file_info["last_modified_date"] = obj["LastModified"]
            files_info.append(file_info)
        return files_info
        # files = [obj['Key'] for obj in response.get('Contents', [])]
        # return files
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="S3 credentials not available")

def download_file_from_s3(bucket_name, object_name):
    try:
        file_stream = s3.get_object(Bucket=bucket_name, Key=object_name)
        file_content = file_stream['Body'].read().decode('utf-8') 
        try: 
            json_content = json.loads(file_content)
            return JSONResponse(content=json_content)
        except Exception as ex:
            return file_content
        # return StreamingResponse(file_stream.iter_lines(), media_type="application/octet-stream")
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="S3 credentials not available")
    except ClientError:
        raise HTTPException(status_code=404, detail="File not available")
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="Server Error, Please try again later")
    
def delete_file_from_s3(bucket_name, object_name):
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="S3 credentials not available")
    except ClientError:
        raise HTTPException(status_code=404, detail="File not found")
    
    