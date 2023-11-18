resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "tokens"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "token"

  attribute {
    name = "token"
    type = "S"
  }
}