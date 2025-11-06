variable "region" {
  default = "us-east-1"
}

variable "project_prefix" {
  default = "provesi"
}

variable "instance_type" {
  default = "t2.nano"
}

provider "aws" {
  region = var.region
}

locals {
  repository_main = "https://github.com/andresjulianbolivar/provesiapp.git"
  repository_api  = "https://github.com/andresjulianbolivar/envios.git"
  branch          = "main"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# ===================================
# Security Groups
# ===================================
resource "aws_security_group" "traffic_django" {
  name        = "${var.project_prefix}-traffic-django"
  description = "Allow traffic on 8080"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "traffic_cb" {
  name        = "${var.project_prefix}-traffic-cb"
  description = "Allow Kong on 8000-8001"

  ingress {
    from_port   = 8000
    to_port     = 8001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "traffic_db" {
  name        = "${var.project_prefix}-traffic-db"
  description = "Allow PostgreSQL access"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "traffic_ssh" {
  name        = "${var.project_prefix}-traffic-ssh"
  description = "Allow SSH access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ===================================
# Kong Gateway
# ===================================
resource "aws_instance" "kong" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_cb.id, aws_security_group.traffic_ssh.id]
  tags = { Name = "${var.project_prefix}-kong" }
}

# ===================================
# Base de Datos
# ===================================
resource "aws_instance" "database" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_db.id, aws_security_group.traffic_ssh.id]
  tags = { Name = "${var.project_prefix}-db" }

  user_data = <<-EOT
    #!/bin/bash
    # ================================
    # Actualización y dependencias
    # ================================
    apt-get update -y
    apt-get install -y python3-venv python3-pip git build-essential libpq-dev python3-dev postgresql postgresql-contrib

    # ================================
    # Variables de DB
    # ================================
    export DATABASE_HOST=127.0.0.1
    export DB_USER=abolivarc
    export DB_PASS=Anjuboca200510
    export DB_NAME=provesidb

    # ================================
    # Configuración PostgreSQL
    # ================================
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
    sudo -u postgres createdb -O $DB_USER $DB_NAME
    echo "host all all 0.0.0.0/0 trust" >> /etc/postgresql/16/main/pg_hba.conf
    echo "listen_addresses='*'" >> /etc/postgresql/16/main/postgresql.conf
    echo "max_connections=2000" >> /etc/postgresql/16/main/postgresql.conf
    systemctl restart postgresql

    # ================================
    # Clonar repositorios
    # ================================
    mkdir -p /labs/provesi
    cd /labs/provesi
    git clone ${local.repository_main}
    git clone ${local.repository_api}
  EOT
}

# ===================================
# Servicios Cotización
# ===================================
resource "aws_instance" "cotizacion" {
  for_each = toset(["a", "b", "c", "d"])
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_django.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
    #!/bin/bash
    apt-get update -y
    apt-get install -y python3-venv python3-pip git build-essential libpq-dev python3-dev

    export DATABASE_HOST=${aws_instance.database.private_ip}
    export DB_USER=abolivarc
    export DB_PASS=Anjuboca200510
    export DB_NAME=provesidb

    mkdir -p /labs/provesi
    cd /labs/provesi
    git clone ${local.repository_main}
    git clone ${local.repository_api}

    # ================================
    # ProvesiApp
    # ================================
    cd /labs/provesi/provesiapp
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    nohup python manage.py runserver 0.0.0.0:8080 &

    # ================================
    # Envios
    # ================================
    cd /labs/provesi/envios
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    nohup python manage.py runserver 0.0.0.0:8000 &
  EOT

  depends_on = [aws_instance.database]
  tags = { Name = "${var.project_prefix}-cotizacion-${each.key}" }
}

# ===================================
# Servicio General
# ===================================
resource "aws_instance" "general" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_django.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
    #!/bin/bash
    apt-get update -y
    apt-get install -y python3-venv python3-pip git build-essential libpq-dev python3-dev

    export DATABASE_HOST=${aws_instance.database.private_ip}
    export DB_USER=abolivarc
    export DB_PASS=Anjuboca200510
    export DB_NAME=provesidb

    mkdir -p /labs/provesi
    cd /labs/provesi
    git clone ${local.repository_main}
    git clone ${local.repository_api}

    # ================================
    # ProvesiApp
    # ================================
    cd /labs/provesi/provesiapp
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    nohup python manage.py runserver 0.0.0.0:8080 &

    # ================================
    # Envios
    # ================================
    cd /labs/provesi/envios
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    nohup python manage.py runserver 0.0.0.0:8000 &
  EOT

  depends_on = [aws_instance.database]
  tags = { Name = "${var.project_prefix}-general" }
}

# ===================================
# Outputs
# ===================================
output "cotizacion_public_ips" {
  value = { for id, instance in aws_instance.cotizacion : id => instance.public_ip }
}

output "general_public_ip" {
  value = aws_instance.general.public_ip
}

output "database_private_ip" {
  value = aws_instance.database.private_ip
}

output "kong_public_ip" {
  value = aws_instance.kong.public_ip
}

output "cotizacion_private_ips" {
  description = "Private IP addresses for the cotizacion service instances"
  value       = { for id, instance in aws_instance.cotizacion : id => instance.private_ip }
}
