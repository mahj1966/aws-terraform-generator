# AWS Resource configurations
RESOURCE_CONFIGS = {
    'ec2': {
        'instance_type': ['t2.micro', 't2.small', 't2.medium', 't3.micro', 't3.small', 't3.medium'],
        'ami': ['ami-0c55b159cbfafe1f0'],
        'subnet_id': 'text',
        'key_name': 'text',
        'vpc_id': 'text',
        'security_group_ids': 'text',
        'root_volume_size': 'number',
        'root_volume_type': ['gp2', 'gp3', 'io1', 'io2', 'standard'],
        'instance_name': 'text',
        'environment': ['production', 'staging', 'development'],
        'monitoring': ['true', 'false'],
        'ebs_optimized': ['true', 'false'],
        'instance_profile': 'text',
        'user_data': 'textarea'
    },
    's3': {
        'bucket_name': 'text',
        'versioning': ['Enabled', 'Disabled'],
        'acl': ['private', 'public-read', 'public-read-write'],
        'encryption': ['AES256', 'aws:kms'],
        'kms_master_key_id': 'text',
        'lifecycle_rule_enabled': ['true', 'false'],
        'lifecycle_days_to_glacier': 'number',
        'cors_enabled': ['true', 'false'],
        'website_enabled': ['true', 'false'],
        'index_document': 'text',
        'error_document': 'text',
        'logging_enabled': ['true', 'false'],
        'logging_target_bucket': 'text',
        'logging_target_prefix': 'text'
    },
    'rds': {
        'engine': ['mysql', 'postgres', 'oracle', 'sqlserver', 'mariadb', 'aurora'],
        'engine_version': 'text',
        'instance_class': ['db.t3.micro', 'db.t3.small', 'db.t3.medium', 'db.r5.large'],
        'allocated_storage': 'number',
        'database_name': 'text',
        'master_username': 'text',
        'master_password': 'password',
        'multi_az': ['true', 'false'],
        'backup_retention_period': 'number',
        'backup_window': 'text',
        'maintenance_window': 'text',
        'storage_encrypted': ['true', 'false'],
        'deletion_protection': ['true', 'false']
    },
    'lambda': {
        'function_name': 'text',
        'runtime': ['nodejs18.x', 'python3.9', 'java11', 'go1.x'],
        'handler': 'text',
        'memory_size': ['128', '256', '512', '1024', '2048'],
        'timeout': 'number',
        'environment_variables': 'textarea',
        'role_arn': 'text',
        'vpc_config_enabled': ['true', 'false'],
        'vpc_subnet_ids': 'text',
        'vpc_security_group_ids': 'text'
    },
    'dynamodb': {
        'table_name': 'text',
        'billing_mode': ['PROVISIONED', 'PAY_PER_REQUEST'],
        'read_capacity': 'number',
        'write_capacity': 'number',
        'hash_key': 'text',
        'range_key': 'text',
        'stream_enabled': ['true', 'false'],
        'point_in_time_recovery': ['true', 'false']
    },
    'eks': {
        'cluster_name': 'text',
        'kubernetes_version': ['1.27', '1.26', '1.25'],
        'role_arn': 'text',
        'vpc_config_subnet_ids': 'text',
        'endpoint_private_access': ['true', 'false'],
        'endpoint_public_access': ['true', 'false'],
        'security_group_ids': 'text',
        'node_group_name': 'text',
        'node_role_arn': 'text',
        'node_instance_types': ['t3.medium', 't3.large', 'm5.large']
    },
    'elasticache': {
        'cluster_id': 'text',
        'engine': ['redis', 'memcached'],
        'node_type': ['cache.t3.micro', 'cache.t3.small', 'cache.t3.medium'],
        'num_cache_nodes': 'number',
        'parameter_group_family': ['redis6.x', 'redis5.0', 'memcached1.6'],
        'port': 'number',
        'security_group_ids': 'text',
        'subnet_group_name': 'text'
    },
    'vpc': {
        'cidr_block': 'text',
        'instance_tenancy': ['default', 'dedicated'],
        'enable_dns_support': ['true', 'false'],
        'enable_dns_hostnames': ['true', 'false'],
        'subnet_cidr_blocks': 'textarea',
        'availability_zones': 'textarea',
        'enable_nat_gateway': ['true', 'false']
    },
    'cloudfront': {
        'origin_domain_name': 'text',
        'origin_id': 'text',
        'price_class': ['PriceClass_All', 'PriceClass_200', 'PriceClass_100'],
        'enabled': ['true', 'false'],
        'default_root_object': 'text',
        'aliases': 'textarea',
        'ssl_certificate_arn': 'text',
        'minimum_protocol_version': ['TLSv1', 'TLSv1.1', 'TLSv1.2']
    },
    'ecs': {
        'instance_type': ['t3.micro', 't3.small', 't3.medium', 't3.large'],
        'capacity_provider': ['FARGATE', 'EC2']
    },
    'waf': {
        'managed_rule_groups': ['CommonRuleSet', 'KnownBadInputs', 'SQLiRuleSet']
    },
    'route53': {
        'record_types': ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS']
    },
    'apigateway': {
        'endpoint_types': ['REGIONAL', 'EDGE', 'PRIVATE']
    }
} 