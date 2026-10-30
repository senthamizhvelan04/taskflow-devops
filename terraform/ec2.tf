resource "aws_instance" "taskflow" {
  ami                         = var.ami
  instance_type               = "t3.micro"
  key_name                    = var.key_name
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.app.id]
  associate_public_ip_address = true

  root_block_device {
    volume_size = 8
    volume_type = "gp3"
    encrypted   = true
  }



  tags = {
    Name        = "taskflow-terraform-ec2"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

