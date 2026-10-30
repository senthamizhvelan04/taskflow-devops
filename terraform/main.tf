
# Dedicated network for the new TaskFlow environment
resource "aws_vpc" "taskflow" {
  cidr_block           = "10.20.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "taskflow-terraform-vpc"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

# Public subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.taskflow.id
  cidr_block              = "10.20.1.0/24"
  availability_zone       = "${var.region}a"
  map_public_ip_on_launch = true

  tags = {
    Name      = "taskflow-public-subnet"
    ManagedBy = "Terraform"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "taskflow" {
  vpc_id = aws_vpc.taskflow.id

  tags = {
    Name      = "taskflow-terraform-igw"
    ManagedBy = "Terraform"
  }
}

# Route table for internet access
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.taskflow.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.taskflow.id
  }

  tags = {
    Name      = "taskflow-public-rt"
    ManagedBy = "Terraform"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security group for the future application server
resource "aws_security_group" "app" {
  name        = "taskflow-terraform-app-sg"
  description = "Security group for TaskFlow application server"
  vpc_id      = aws_vpc.taskflow.id

  # HTTP application access
  ingress {
    description = "TaskFlow application"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH from my IP only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  # Allow outbound connections
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name      = "taskflow-terraform-app-sg"
    ManagedBy = "Terraform"
  }
}
