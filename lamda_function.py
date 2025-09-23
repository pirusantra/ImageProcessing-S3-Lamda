import os
import boto3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

s3 = boto3.client('s3')
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        obj = s3.get_object(Bucket=bucket, Key=key)
        img = Image.open(BytesIO(obj['Body'].read()))
        img = img.resize((1024, int(1024 * img.height / img.width))) if img.width > 1024 else img
        draw = ImageDraw.Draw(img)
        draw.text((10, img.height - 30), "© MyApp", fill=(255,255,255,128))
        out_buffer = BytesIO()
        img.save(out_buffer, format='JPEG')
        out_buffer.seek(0)
        s3.put_object(Bucket=OUTPUT_BUCKET, Key=f"processed/{key}", Body=out_buffer)
