import qrcode
import boto3
import random
import string

DYNAMODB_TABLE = "tokens"

session = boto3.Session(
    aws_access_key_id='AKIA4RIB2MDINIPL4Y7P',
    aws_secret_access_key='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',
)
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(DYNAMODB_TABLE)

for n in range(10):
    # URL for which you want to generate QR code
    base_url = 'http://web-test-bucket-1234.s3-website-us-east-1.amazonaws.com/?tk='
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

    final_url = base_url + token
    print(final_url)

    path = token + '/' + 'image.jpg'
    item = {
        'token': token,
        'secret': 'null',
        'path': path,
        'status': 'Issued'
    }
    
    response = table.put_item(Item=item)

    # Create QR code instance
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )


    # Add URL to QR code
    qr.add_data(final_url)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save('codes/' + token + '.png')