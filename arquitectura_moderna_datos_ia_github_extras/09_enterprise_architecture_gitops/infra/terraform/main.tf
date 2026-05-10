terraform {
  required_version = ">= 1.5.0"
}

variable "environment" {
  type        = string
  description = "Deployment environment: dev, test, prod"
}

variable "location" {
  type        = string
  description = "Cloud region"
  default     = "westeurope"
}

locals {
  name_prefix = "logistics-data-${var.environment}"
}

# Ejemplo conceptual:
# resource "azurerm_resource_group" "rg" {
#   name     = "${local.name_prefix}-rg"
#   location = var.location
# }
