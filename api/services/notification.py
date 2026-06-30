import logging
import requests
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def send_real_email(subject, message, recipient_list, html_message=None):
    """
    Sends transactional emails using Django's SMTP backend.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"[Email Service] Email sent successfully to {recipient_list}")
        return True
    except Exception as e:
        logger.error(f"[Email Service] Failed to send email: {e}")
        return False


def send_dlt_sms_msg91(mobile_number, template_id, variables_dict):
    """
    Sends a DLT-compliant SMS using MSG91 gateway API.
    
    Arguments:
    - mobile_number: Target mobile (with country code, e.g. '919876543210')
    - template_id: Approved DLT Template ID (string)
    - variables_dict: Dictionary of DLT variables, e.g. {"var1": "A+", "var2": "KEM Hospital"}
    """
    # Load credentials from settings
    auth_key = getattr(settings, 'MSG91_AUTH_KEY', None)
    sender_id = getattr(settings, 'MSG91_SENDER_ID', 'MUMBBC') # Approved DLT Header
    pe_id = getattr(settings, 'DLT_PE_ID', None) # Principal Entity ID
    
    if not auth_key or not pe_id:
        logger.warning("[SMS Service] MSG91 credentials or DLT PE ID missing. Skipping live SMS.")
        return False

    url = "https://control.msg91.com/api/v5/flow/"
    
    headers = {
        "authkey": auth_key,
        "content-type": "application/json"
    }
    
    # MSG91 Flow Payload structure for DLT template variables
    payload = {
        "template_id": template_id,
        "sender": sender_id,
        "short_url": "1", # Enables link shortening if needed
        "recipients": [
            {
                "mobiles": mobile_number,
                **variables_dict # substitutes {"var1": "A+", "var2": "KEM Hospital"}
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        res_json = response.json()
        if response.status_code == 200 and res_json.get("type") == "success":
            logger.info(f"[SMS Service] SMS successfully dispatched to {mobile_number}")
            return True
        else:
            logger.error(f"[SMS Service] SMS failed. Response: {res_json}")
            return False
    except Exception as e:
        logger.error(f"[SMS Service] Exception while sending SMS: {e}")
        return False


def send_dlt_sms_routemobile(mobile_number, message_text, template_id):
    """
    Sends a DLT-compliant SMS using Route Mobile HTTP/HTTPS API.
    Returns: (success_boolean, status_message)
    """
    username = getattr(settings, 'ROUTE_MOBILE_USERNAME', '')
    password = getattr(settings, 'ROUTE_MOBILE_PASSWORD', '')
    sender_id = getattr(settings, 'ROUTE_MOBILE_SENDER_ID', 'MUMBBC')
    entity_id = getattr(settings, 'ROUTE_MOBILE_ENTITY_ID', '')
    tmid = getattr(settings, 'ROUTE_MOBILE_TM_ID', '')
    api_url = getattr(settings, 'ROUTE_MOBILE_API_URL', 'https://sms6.rmlconnect.net:8443/bulksms/bulksms')

    # Clean destination number and prefix country code 91 if it's 10 digits
    clean_mobile = "".join([c for c in str(mobile_number) if c.isdigit()])
    if len(clean_mobile) == 10:
        clean_mobile = "91" + clean_mobile

    params = {
        'username': username,
        'password': password,
        'type': 0, # 0 = Plain text
        'dlr': 1,  # 1 = Delivery report enabled
        'destination': clean_mobile,
        'source': sender_id,
        'message': message_text,
        'entityid': entity_id,
        'tempid': template_id,
    }
    
    if tmid:
        params['tmid'] = tmid

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response_text = response.text
        # Check success code 1701 per PDF documentation
        if response.status_code == 200 and response_text.startswith("1701"):
            logger.info(f"[SMS Service] Route Mobile SMS dispatched successfully. Response: {response_text}")
            return True, f"Success: {response_text}"
        else:
            logger.error(f"[SMS Service] Route Mobile SMS failed. Response: {response_text}")
            error_msg = response_text
            if "1703" in response_text:
                error_msg = "Invalid username or password in settings.py"
            elif "1709" in response_text:
                error_msg = "User validation failed on DLT portal"
            elif "1052" in response_text:
                error_msg = "Invalid DLT Entity ID"
            elif "1051" in response_text:
                error_msg = "Invalid DLT Template ID"
            return False, f"Route Mobile Error: {error_msg}"
    except Exception as e:
        logger.error(f"[SMS Service] Exception while sending Route Mobile SMS: {e}")
        return False, f"Connection error: {str(e)}"