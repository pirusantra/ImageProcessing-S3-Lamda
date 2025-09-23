import os
import boto3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

s3 = boto3.client('s3')

OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
MAX_WIDTH = int(os.environ.get('MAX_WIDTH', '1024'))
WATERMARK_TEXT = os.environ.get('WATERMARK_TEXT', '© MyApp')
WATERMARK_OPACITY = float(os.environ.get('WATERMARK_OPACITY', '0.45'))

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        try:
            # Download the image from S3
            obj = s3.get_object(Bucket=bucket, Key=key)
            img = Image.open(BytesIO(obj['Body'].read()))
            
            # Resize if needed
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                img = img.resize((MAX_WIDTH, int(img.height * ratio)), Image.ANTIALIAS)
            
            # Add watermark
            watermark = Image.new('RGBA', img.size, (0,0,0,0))
            draw = ImageDraw.Draw(watermark)
            font_size = int(img.width/20)
            font = ImageFont.load_default()
            draw.text((10, img.height - font_size - 10), WATERMARK_TEXT, fill=(255,255,255,int(255*WATERMARK_OPACITY)), font=font)
            watermarked = Image.alpha_composite(img.convert('RGBA'), watermark)
            
            # Save to bytes
            out_buffer = BytesIO()
            watermarked.convert('RGB').save(out_buffer, format='JPEG', quality=85)
            out_buffer.seek(0)
            
            # Upload to output bucket
            output_key = f"processed/{os.path.basename(key)}"
            s3.put_object(Bucket=OUTPUT_BUCKET, Key=output_key, Body=out_buffer, ContentType='image/jpeg')
            
            print(f"Processed {key} -> {output_key}")
        except Exception as e:
            print(f"Error processing {key}: {e}")
            raise e

