# Serverless Image Processing with AWS S3 & Lambda

This project implements a serverless image processing pipeline. I created a system where images uploaded to an S3 input bucket are automatically resized and watermarked by a Lambda function, then stored in an S3 output bucket.

# Technologies Used

Amazon S3: Stores input and output images.

AWS Lambda: Processes images (resize, watermark) automatically on upload.

Python 3.8 – Language for Lambda function.

Pillow – Image processing library.

Boto3 – AWS SDK for Python.

CloudWatch – Monitoring and logging.


## ⚙️ Deployment Steps
### 1️⃣ S3 Buckets Setup
- I created an input bucket (my-image-input) to store uploaded images.
- I created an output bucket (my-image-output) to store processed images.
- Configured the bucket policies to allow my Lambda function to read from the input bucket and write to the output bucket.

### 2️⃣ IAM Role Creation
- I created an IAM role for Lambda with the minimum required permissions.
- Attached policies allowing Lambda to:
 GetObject and ListBucket from the input bucket.
 PutObject into the output bucket.
 Write logs to CloudWatch.

### 3️⃣ Lambda Function Development

 - I wrote the Python Lambda function (lambda_function.py) with the following features:
   Resize images to a maximum width while maintaining aspect ratio.
   Add a semi-transparent watermark with configurable text and opacity.
   Save processed images to the output S3 bucket.
   ( Code attached in lambda_function.py )

### 4️⃣ Lambda Deployment
- I packaged the Lambda function along with dependencies (Pillow and Boto3) into a ZIP file.
- I deployed it to AWS Lambda using the Python 3.8 runtime.
- I set environment variables for:
  OUTPUT_BUCKET
  MAX_WIDTH
  WATERMARK_TEXT
  WATERMARK_OPACITY

### 5️⃣ Event Trigger Configuration
- I configured the input S3 bucket to trigger the Lambda function on object creation events.
- Verified that each uploaded image automatically invoked the Lambda function.

---
### Final Output
- The system automatically resized and watermarked images upon upload.
- Processed images were stored in the output S3 bucket.

