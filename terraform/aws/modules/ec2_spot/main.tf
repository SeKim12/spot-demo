data "aws_ami" "linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "image-id"
    values = ["ami-06d2c6c1b5cbaee5f"]
    # ["ami-02288bc8778f3166f"]
  }
}

resource "aws_key_pair" "ssh_key_inception" {
  key_name   = "ssh_key_inception"
  public_key = file("~/.ssh/inception_rsa.pub")
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
  key_name      = aws_key_pair.ssh_key_inception.key_name
  user_data     = templatefile("${path.module}/startup.sh", {
    resume = var.resume
  })
  tags = {
    Name = "test-spot"
  }
}