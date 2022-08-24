variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "topic_name" {
  type    = string
  default = "TeamEvents"
}

variable "environment" {
  type = string
}
