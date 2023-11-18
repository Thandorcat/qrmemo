resource "aws_s3_bucket" "web_bucket" {
  bucket = "web-test-bucket-1234"
}

resource "aws_s3_object" "index_file" {
  bucket = aws_s3_bucket.web_bucket.id
  key = "index.html"
  source = "../index.html"
  etag = filemd5("../index.html")
}

resource "aws_s3_object" "js_file" {
  bucket = aws_s3_bucket.web_bucket.id
  key = "s3_upload.js"
  source = "../s3_upload.js"
  etag = filemd5("../s3_upload.js")
}

resource "aws_s3_bucket_website_configuration" "example" {
  bucket = aws_s3_bucket.web_bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "allow_public_access" {
  bucket = aws_s3_bucket.web_bucket.id
  policy = data.aws_iam_policy_document.allow_public_access.json
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.web_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

data "aws_iam_policy_document" "allow_public_access" {
  statement {
    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "${aws_s3_bucket.web_bucket.arn}/*",
    ]
  }
}

resource "aws_s3_bucket" "test_bucket" {
  bucket = "target-bucket-test-123"
}

resource "aws_s3_bucket_cors_configuration" "allow_requests" {
  bucket = aws_s3_bucket.test_bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["HEAD", "GET", "PUT", "POST", "DELETE"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
  }
}