data "aws_ami" "linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "image-id"
    values = ["ami-06d2c6c1b5cbaee5f"]
  }
}

resource "aws_key_pair" "ssh_key" {
  key_name   = "ssh_key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_instance" "ec2" {
  ami           = data.aws_ami.linux.id
  instance_type = "t3.small"
  key_name      = aws_key_pair.ssh_key.key_name
  user_data     = file("${path.module}/startup.sh")
  vpc_security_group_ids = [""]
  tags = {
    Name = "spotvisor"
  }
}