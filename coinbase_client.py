from coinbase.rest import RESTClient

def get_client(key_file="cdp_api_key.json"):
    return RESTClient(key_file=key_file)
