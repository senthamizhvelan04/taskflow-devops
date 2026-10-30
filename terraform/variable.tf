variable "region" {
  description = "AWS region for the TaskFlow environment"
  type        = string
  default     = "eu-north-1"
}

variable "key_name" {
  description = "Existing EC2 key pair name"
  type        = string
  default     = "devops"
}

variable "my_ip" {
  description = "Your public IPv4 address in CIDR notation"
  type        = string
}

variable "ami" {
  description = "AMI ID for the EC2 instance"
  type        = string
  default     = "ami-021aaf3749be66813"
}