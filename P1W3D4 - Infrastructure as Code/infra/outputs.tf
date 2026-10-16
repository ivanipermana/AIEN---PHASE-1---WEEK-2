output "bucket_name" {
  description = "Nama bucket data lake."
  value       = aws_s3_bucket.data_lake.id
}

output "bucket_arn" {
  description = "ARN bucket data lake."
  value       = aws_s3_bucket.data_lake.arn
}
