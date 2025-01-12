class ResourceValidator:
    @staticmethod
    def validate_required(value, field_name):
        if not value:
            raise ValueError(f"{field_name} is required")
        return value

    @staticmethod
    def validate_cidr(value):
        import ipaddress
        try:
            ipaddress.ip_network(value)
            return value
        except ValueError:
            raise ValueError(f"Invalid CIDR block: {value}")

    @staticmethod
    def validate_port(value):
        port = int(value)
        if not (0 <= port <= 65535):
            raise ValueError(f"Port must be between 0 and 65535")
        return port

    @staticmethod
    def validate_boolean(value):
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)

    @staticmethod
    def validate_list(value, delimiter=','):
        if isinstance(value, str):
            return [item.strip() for item in value.split(delimiter) if item.strip()]
        return list(value) 