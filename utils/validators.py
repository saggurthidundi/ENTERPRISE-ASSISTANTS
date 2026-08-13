def validate_api_key(api_key):
  if not api_key or len(api_key.strip()) < 10:
    return False
  return True