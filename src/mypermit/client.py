from django.conf import settings
from permit import Permit

def get_permit_client():
    pdp_url = getattr(settings, 'PERMIT_PDP_URL', None)
    api_key = getattr(settings, 'PERMIT_API_KEY', None)
    if not api_key:
        raise ValueError("PERMIT_API_KEY was not set in django settings.")
    return Permit(pdp=pdp_url, token=api_key)

try:
    permit_client = get_permit_client()
    print(permit_client)
except Exception as e:
    permit_client = None
    print(f"Warning: Could not initialize Permit client: {e}")