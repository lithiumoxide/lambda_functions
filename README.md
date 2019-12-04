# lambda_functions
Some AWS Lambda functions

## rekognition_s3_image_labels.py
This uses S3 and Rekognition to detect labels in an image uploaded to S3 and then apply them to the object. As it is, it will apply up to five labels in a single tag to the object with a minimum confidence level of 90%. This can be altered in the code. The function will also check to see if the image should be moderated, and add a true or false value to a moderated tag.

To use, create an event on the S3 bucket to trigger the function when an object is PUT into the bucket. Give the function's IAM role permission to read and write tags in S3, and to use Rekognition.

Note: there is a short sleep function in place at the beginning of the function. I found originally that sometimes Rekognition would not be able to find the image in S3, despite being already sent the object key. I believe this may be due to S3's eventual consistency model. The sleep function allows for a short period to ensure that theimage is available on S3 for Rekognition to use.

## stop-rds.py
AWS automatically start RDS instances after they've been stopped for one week. This function will check to see if any RDS instances have the tag 'StayOffline' appled (no value required): if the tag is present, it will attempt to stop the instance.

You could run this on a CloudWatch cron job to execute daily, for example. The IAM role should be triggered by CloudWatch and have access to read RDS details and to stop an RDS instance.
