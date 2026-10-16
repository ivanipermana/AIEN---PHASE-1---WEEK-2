provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "data_lake" {
  bucket        = var.bucket_name
  force_destroy = false

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
    Project     = "aien-p1w3d4"
  }
}

resource "aws_s3_bucket_public_access_block" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
