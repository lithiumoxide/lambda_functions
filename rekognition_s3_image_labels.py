import json
import time
import boto3

rek = boto3.client('rekognition', 'us-east-1')
s3 = boto3.client('s3')

max_labels = 5
min_confidence = 90

def lambda_handler(event, context):
    time.sleep(.250)
    message = event['Records'][0]['Sns']['Message']
    parsed_message = json.loads(message)
    
    # Find bucket and key for the S3 object
    bucket = parsed_message['Records'][0]['s3']['bucket']['name']
    for items in event["Records"]:
        key = parsed_message['Records'][0]['s3']['object']['key']

    # Find existing tags on object, create a new tagset with those
    existing_tags = s3.get_object_tagging(
        Bucket = bucket,
        Key = key
    )
    new_tagset = existing_tags['TagSet']

    # Check if image is SFW - if number of moderation labels > 0 then tag object as moderated
    moderation_response = rek.detect_moderation_labels(
        Image = { "S3Object" : { "Bucket" : bucket, "Name" : key } })
    
    if(len(moderation_response['ModerationLabels']) > 0):
        new_tagset.append( { 'Key' : 'moderated', 'Value' : 'true' } )
    else:
        new_tagset.append( { 'Key' : 'moderated', 'Value' : 'false' } )
    
    # Send request to Rekognition and return up to 5 labels that have at least a 90% confidence level
    rek_response = rek.detect_labels(
        Image = { "S3Object" : { "Bucket" : bucket, "Name" : key } },
        MaxLabels = max_labels,
        MinConfidence = min_confidence
    )
    
    # Go through the response from Rekognition and create a string of labels, separated with a dash    
    # ... then remove first character, as it's a dash by default due to the above
    labels = ''
    n = 0
    while n < len(rek_response):
        label = rek_response['Labels'][n]['Name']
        print(label)
        labels = labels + '-' + label
        n = n + 1
    label_tags = labels[1:]
    new_tagset.append( { 'Key' : 'ml-tags', 'Value' : label_tags } )

    # Apply the new tagset (which includes new and existing tags) to the object
    apply_tags_response = s3.put_object_tagging(
        Bucket = bucket,
        Key = key,
        Tagging = {
            'TagSet' : new_tagset
        }
    )
    print(apply_tags_response)