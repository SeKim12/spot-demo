data "aws_ami" "linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "image-id"
    values = ["ami-02288bc8778f3166f"]
  }
}

resource "aws_key_pair" "ssh_key" {
  key_name   = "ssh_key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_instance" "ec2_spot" {
  ami = data.aws_ami.linux.id
  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = 0.0090
    }
  }
  instance_type = "t3.small"
  key_name      = aws_key_pair.ssh_key.key_name
  user_data = file("${path.module}/startup.sh")
  tags = {
    Name = "test-spot"
  }
}