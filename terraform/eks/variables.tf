variable "vpc_id" {
  description = "The VPC ID for the EKS cluster"
  type        = string
}

variable "subnet_ids" {
  description = "The subnet IDs for the EKS cluster"
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "The public subnet IDs for the EKS cluster"
  type        = list(string)
}

variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
  default     = "cloudbash"
}

variable "kubernetes_version" {
  description = "The Kubernetes version to use for the EKS cluster"
  type        = string
  default     = "1.30.1"
}

variable "node_instance_type" {
  description = "The instance type for the EKS worker nodes"
  type        = string
  default     = "t3.small"
}

variable "desired_capacity" {
  description = "The desired number of worker nodes"
  type        = number
  default     = 1
}

variable "key_name" {
  description = "The key pair name for SSH access to nodes"
  type        = string
  default     = ""
}
