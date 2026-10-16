variable "aws_region" {
  description = "Region untuk resource latihan."
  type        = string
  default     = "ap-southeast-1"
}

variable "bucket_name" {
  description = "Nama bucket S3 yang unik secara global. Gunakan huruf kecil, angka, dan tanda hubung."
  type        = string
}

variable "environment" {
  description = "Environment latihan."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging"], var.environment)
    error_message = "Lab ini hanya menggunakan dev atau staging."
  }
}
