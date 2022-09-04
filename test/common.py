import os


def get_api_ip():
    api_ip = "127.0.0.1"  # Default
    if "API_IP" in os.environ:
        api_ip = os.environ["API_IP"]
    return api_ip


def get_api_port():
    api_port = "5000"  # Default
    if "API_PORT" in os.environ:
        api_port = os.environ["API_PORT"]
    return api_port
