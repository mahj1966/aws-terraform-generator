def generate_terraform_config(resource_type, config):
    generators = {
        'ec2': generate_ec2_config,
        's3': generate_s3_config,
        'rds': generate_rds_config,
        'lambda': generate_lambda_config,
        'dynamodb': generate_dynamodb_config,
        'eks': generate_eks_config,
        'elasticache': generate_elasticache_config,
        'vpc': generate_vpc_config,
        'cloudfront': generate_cloudfront_config
    }
    
    generator = generators.get(resource_type)
    if generator:
        return generator(config)
    return ''

def generate_ec2_config(config):
    return f'''
resource "aws_instance" "example" {{
  ami                    = "{config.get('ami', '')}"
  instance_type         = "{config.get('instance_type', '')}"
  subnet_id             = "{config.get('subnet_id', '')}"
  key_name             = "{config.get('key_name', '')}"
  vpc_security_group_ids = ["{config.get('security_group_ids', '')}"]
  
  root_block_device {{
    volume_size = {config.get('root_volume_size', '8')}
    volume_type = "{config.get('root_volume_type', 'gp2')}"
  }}

  monitoring           = {config.get('monitoring', 'false')}
  ebs_optimized        = {config.get('ebs_optimized', 'false')}
  iam_instance_profile = "{config.get('instance_profile', '')}"

  user_data = <<-EOF
    {config.get('user_data', '')}
  EOF

  tags = {{
    Name        = "{config.get('instance_name', '')}"
    Environment = "{config.get('environment', '')}"
  }}
}}'''

def generate_s3_config(config):
    website_enabled = '[]' if config.get('website_enabled') != 'true' else '[1]'
    return f'''
resource "aws_s3_bucket" "example" {{
  bucket = "{config.get('bucket_name', '')}"
  acl    = "{config.get('acl', 'private')}"
  
  versioning {{
    enabled = {config.get('versioning', '') == 'Enabled'}
  }}

  server_side_encryption_configuration {{
    rule {{
      apply_server_side_encryption_by_default {{
        sse_algorithm     = "{config.get('encryption', 'AES256')}"
        kms_master_key_id = "{config.get('kms_master_key_id', '')}"
      }}
    }}
  }}

  lifecycle_rule {{
    enabled = {config.get('lifecycle_rule_enabled', 'false')}
    transition {{
      days          = {config.get('lifecycle_days_to_glacier', '90')}
      storage_class = "GLACIER"
    }}
  }}

  dynamic "website" {{
    for_each = {website_enabled}
    content {{
      index_document = "{config.get('index_document', '')}"
      error_document = "{config.get('error_document', '')}"
    }}
  }}

  logging {{
    target_bucket = "{config.get('logging_target_bucket', '')}"
    target_prefix = "{config.get('logging_target_prefix', '')}"
  }}
}}''' 

def generate_rds_config(config):
    return f'''
resource "aws_db_instance" "example" {{
  engine                = "{config.get('engine', '')}"
  engine_version       = "{config.get('engine_version', '')}"
  instance_class      = "{config.get('instance_class', '')}"
  allocated_storage   = {config.get('allocated_storage', '20')}
  
  db_name             = "{config.get('database_name', '')}"
  username           = "{config.get('master_username', '')}"
  password           = "{config.get('master_password', '')}"
  
  multi_az            = {config.get('multi_az', 'false')}
  backup_retention_period = {config.get('backup_retention_period', '7')}
  backup_window      = "{config.get('backup_window', '')}"
  maintenance_window = "{config.get('maintenance_window', '')}"
  
  storage_encrypted  = {config.get('storage_encrypted', 'true')}
  deletion_protection = {config.get('deletion_protection', 'false')}
  
  skip_final_snapshot = true
}}'''

def generate_lambda_config(config):
    return f'''
resource "aws_lambda_function" "example" {{
  filename         = "lambda_function_payload.zip"
  function_name    = "{config.get('function_name', '')}"
  role            = "{config.get('role_arn', '')}"
  handler         = "{config.get('handler', '')}"
  runtime         = "{config.get('runtime', '')}"
  
  memory_size     = {config.get('memory_size', '128')}
  timeout         = {config.get('timeout', '3')}
  
  environment {{
    variables = {config.get('environment_variables', '{}')}
  }}

  vpc_config {{
    subnet_ids         = [{config.get('vpc_subnet_ids', '')}]
    security_group_ids = [{config.get('vpc_security_group_ids', '')}]
  }}
}}'''

def generate_dynamodb_config(config):
    return f'''
resource "aws_dynamodb_table" "example" {{
  name           = "{config.get('table_name', '')}"
  billing_mode   = "{config.get('billing_mode', 'PROVISIONED')}"
  read_capacity  = {config.get('read_capacity', '5')}
  write_capacity = {config.get('write_capacity', '5')}
  hash_key       = "{config.get('hash_key', '')}"
  range_key      = "{config.get('range_key', '')}"

  attribute {{
    name = "{config.get('hash_key', '')}"
    type = "S"
  }}

  attribute {{
    name = "{config.get('range_key', '')}"
    type = "S"
  }}

  stream_enabled   = {config.get('stream_enabled', 'false')}
  point_in_time_recovery {{
    enabled = {config.get('point_in_time_recovery', 'false')}
  }}
}}'''

def generate_eks_config(config):
    return f'''
resource "aws_eks_cluster" "example" {{
  name     = "{config.get('cluster_name', '')}"
  role_arn = "{config.get('role_arn', '')}"
  version  = "{config.get('kubernetes_version', '')}"

  vpc_config {{
    subnet_ids = [{config.get('vpc_config_subnet_ids', '')}]
    endpoint_private_access = {config.get('endpoint_private_access', 'true')}
    endpoint_public_access  = {config.get('endpoint_public_access', 'true')}
    security_group_ids     = [{config.get('security_group_ids', '')}]
  }}
}}

resource "aws_eks_node_group" "example" {{
  cluster_name    = aws_eks_cluster.example.name
  node_group_name = "{config.get('node_group_name', '')}"
  node_role_arn   = "{config.get('node_role_arn', '')}"
  instance_types  = ["{config.get('node_instance_types', '')}"]

  scaling_config {{
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }}
}}'''

def generate_elasticache_config(config):
    return f'''
resource "aws_elasticache_cluster" "example" {{
  cluster_id           = "{config.get('cluster_id', '')}"
  engine              = "{config.get('engine', '')}"
  node_type           = "{config.get('node_type', '')}"
  num_cache_nodes     = {config.get('num_cache_nodes', '1')}
  parameter_group_family = "{config.get('parameter_group_family', '')}"
  port                = {config.get('port', '6379')}
  
  security_group_ids  = ["{config.get('security_group_ids', '')}"]
  subnet_group_name   = "{config.get('subnet_group_name', '')}"
}}'''

def generate_vpc_config(config):
    return f'''
resource "aws_vpc" "example" {{
  cidr_block           = "{config.get('cidr_block', '')}"
  instance_tenancy     = "{config.get('instance_tenancy', 'default')}"
  enable_dns_support   = {config.get('enable_dns_support', 'true')}
  enable_dns_hostnames = {config.get('enable_dns_hostnames', 'true')}
}}

resource "aws_subnet" "example" {{
  count             = length(split("\\n", "{config.get('subnet_cidr_blocks', '')}"))
  vpc_id            = aws_vpc.example.id
  cidr_block        = trim(split("\\n", "{config.get('subnet_cidr_blocks', '')}")[count.index])
  availability_zone = trim(split("\\n", "{config.get('availability_zones', '')}")[count.index])
}}

resource "aws_internet_gateway" "example" {{
  vpc_id = aws_vpc.example.id
}}'''

def generate_cloudfront_config(config):
    return f'''
resource "aws_cloudfront_distribution" "example" {{
  origin {{
    domain_name = "{config.get('origin_domain_name', '')}"
    origin_id   = "{config.get('origin_id', '')}"
  }}

  enabled             = {config.get('enabled', 'true')}
  default_root_object = "{config.get('default_root_object', '')}"
  aliases             = {config.get('aliases', '[]')}

  default_cache_behavior {{
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "{config.get('origin_id', '')}"

    forwarded_values {{
      query_string = false
      cookies {{
        forward = "none"
      }}
    }}

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }}

  price_class = "{config.get('price_class', 'PriceClass_100')}"

  viewer_certificate {{
    acm_certificate_arn      = "{config.get('ssl_certificate_arn', '')}"
    minimum_protocol_version = "{config.get('minimum_protocol_version', 'TLSv1.2_2021')}"
    ssl_support_method       = "sni-only"
  }}

  restrictions {{
    geo_restriction {{
      restriction_type = "none"
    }}
  }}
}}''' 