# lambda_functions
Some AWS Lambda functions

## rekognition_s3_image_labels.py
This uses S3 and Rekognition to detect labels in an image uploaded to S3 and then apply them to the object. As it is, it will apply up to five labels in a single tag to the object with a minimum confidence level of 90%. This can be altered in the code. The function will also check to see if the image should be moderated, and add a true or false value to a moderated tag.

To use, create an event on the S3 bucket to trigger the function when an object is PUT into the bucket. Give the function's IAM role permission to read and write tags in S3, and to use Rekognition.
