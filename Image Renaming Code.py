import boto3
import os
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        original_key = record['s3']['object']['key']
        
        # Split the original key to get the file extension
        file_name, file_extension = os.path.splitext(original_key)
        
        # Ensure we're not reprocessing already renamed images
        if original_key.startswith("new-image-name"):
            print(f"The file {original_key} has already been processed.")
            return
        
        new_key = "new-image-name" + file_extension
        
        # Copy the image to a new key (renaming it)
        copy_source = {'Bucket': source_bucket, 'Key': original_key}
        s3.copy_object(Bucket=source_bucket, CopySource=copy_source, Key=new_key)
        
        # Delete the original image
        s3.delete_object(Bucket=source_bucket, Key=original_key)
        
        print(f"Renamed {original_key} to {new_key} and deleted the original.")
        
    return {
        'statusCode': 200,
        'body': json.dumps('Image processed successfully.')
    }
