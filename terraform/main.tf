provider "aws" {
  region = "eu-north-1"
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "3.0.0"

  name = "cloudbash-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["eu-north-1a", "eu-north-1b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.3.0/24", "10.0.4.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

module "eks" {
  source = "./eks"

  vpc_id            = module.vpc.vpc_id
  subnet_ids        = module.vpc.private_subnets
  public_subnet_ids = module.vpc.public_subnets
  cluster_name      = var.cluster_name
  cluster_version   = var.kubernetes_version
  node_instance_type = var.node_instance_type
  desired_capacity   = var.node_desired_capacity
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnets" {
  value = module.vpc.public_subnets
}

output "private_subnets" {
  value = module.vpc.private_subnets
}
