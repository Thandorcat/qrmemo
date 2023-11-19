import qrcode
import random
import string

# URL for which you want to generate QR code
base_url = 'http://web-test-bucket-1234.s3-website-us-east-1.amazonaws.com/?tk='
token = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
secret = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

final_url = base_url + token + "&s=" + secret
print(final_url)

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