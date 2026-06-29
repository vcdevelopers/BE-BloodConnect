import requests
import json
import logging
from django.utils import timezone
from api.models import BloodBank

logger = logging.getLogger(__name__)

def get_zone_from_pincode_and_district(pincode_str, district, name_str=""):
    # Normalize district name
    if not district:
        district = "Mumbai"
        
    district_clean = str(district).strip().title()
    
    # Thane and Palghar are distinct districts and map directly to their own zones
    if district_clean == "Thane":
        return "Thane"
    if district_clean == "Palghar":
        return "Palghar"
        
    # For Mumbai, we classify into "Mumbai City" vs "Mumbai Suburban"
    pincode_digits = "".join([c for c in str(pincode_str) if c.isdigit()])
    
    if pincode_digits and len(pincode_digits) >= 6:
        pin = int(pincode_digits[:6])
        
        # Thane pincodes sometimes appear under Mumbai district in the raw data, catch them
        if 400600 <= pin <= 400699 or 400700 <= pin <= 400799 or 410200 <= pin <= 410299:
            return "Thane"
            
        # Palghar pincodes
        if 401100 <= pin <= 401699:
            # 401107 is Bhayandar (Thane district), but 401201 is Vasai (Palghar district)
            if pin in {401101, 401102, 401103, 401104, 401105, 401106, 401107}:
                return "Thane"
            return "Palghar"
            
        # Mumbai City range: 400001 to 400040 (Colaba to Sion/Mahim/Worli)
        if 400001 <= pin <= 400040:
            return "Mumbai City"
            
        # Mumbai Suburban range: 400041 to 400104 (Bandra, Andheri, Borivali, Chembur, Mulund)
        if 400041 <= pin <= 400104:
            return "Mumbai Suburban"
            
    # Fallback keyword matching on name/location if pincode is missing or out of standard ranges
    name_lower = name_str.lower()
    
    # Mumbai City keywords
    city_keywords = [
        "sion", "parel", "dadar", "worli", "byculla", "colaba", "fort", "mazagaon",
        "girgaon", "grant road", "tardeo", "mumbai central", "wadala", "mahim", 
        "jj hospital", "kem", "nair", "prabhadevi", "marine lines", "cst", "churchgate"
    ]
    if any(kw in name_lower for kw in city_keywords):
        return "Mumbai City"
        
    # Mumbai Suburban keywords
    suburban_keywords = [
        "andheri", "bandra", "borivali", "malad", "kurla", "chembur", "ghatkopar", 
        "mulund", "kandivali", "santacruz", "vile parle", "goregaon", "powai", 
        "vikhroli", "dahisar", "juhu", "mankhurd", "vashi", "kanjurmarg"
    ]
    if any(kw in name_lower for kw in suburban_keywords):
        return "Mumbai Suburban"
        
    # Default fallback for Mumbai district
    if district_clean == "Mumbai":
        return "Mumbai City"
        
    return district_clean


def run_live_scraper():
    print("[Scraper] Starting live blood stock sync...")
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })

    view_url = "https://bloodcenter.mahasbtc.org/api/v1/consolidated-api/view?defaultPageId=64f1f1e1f5afeb2a04416ee7"
    headers_view = {
        "Referer": "https://bloodcenter.mahasbtc.org/applications/64f1f1e1f5afeb2a04416ee4/pages/64f1f1e1f5afeb2a04416ee7?embed=true",
        "Origin": "https://bloodcenter.mahasbtc.org"
    }
    
    try:
        response = session.get(view_url, headers=headers_view, timeout=20)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"[Scraper] Failed to establish session: {e}")
        return False

    xsrf_token = session.cookies.get("XSRF-TOKEN")
    if not xsrf_token:
        logger.error("[Scraper] XSRF-TOKEN cookie not found.")
        return False

    execute_url = "https://bloodcenter.mahasbtc.org/api/v1/actions/execute"
    headers_execute = {
        "x-appsmith-version": "v1.99",
        "x-appsmith-environmentid": "unused_env",
        "x-xsrf-token": xsrf_token,
        "Referer": "https://bloodcenter.mahasbtc.org/applications/64f1f1e1f5afeb2a04416ee4/pages/64f1f1e1f5afeb2a04416ee7?embed=true",
        "Origin": "https://bloodcenter.mahasbtc.org",
    }
    
    payload = {
        "executeActionDTO": (
            '{"actionId":"64f1f1e1f5afeb2a04416eeb",'
            '"viewMode":true,'
            '"paramProperties":{},'
            '"analyticsProperties":{"isUserInitiated":false}}'
        )
    }

    try:
        res = session.post(execute_url, headers=headers_execute, files=payload, timeout=30)
        res.raise_for_status()
        api_data = res.json()
    except Exception as e:
        logger.error(f"[Scraper] Failed execute: {e}")
        return False

    body = api_data.get("data", {}).get("body", [])
    if not body:
        logger.error("[Scraper] Body is empty.")
        return False

    mumbai_districts = {"Mumbai", "Thane", "Palghar"}
    saved_count = 0
    
    for record in body:
        district = record.get("district", "")
        if district not in mumbai_districts:
            continue
            
        bb_id = record.get("username") or record.get("bloodbank")
        if not bb_id:
            continue
            
        name = record.get("name", "Unknown Blood Bank")
        pincode = str(record.get("pincode", "") or "").replace(" ", "").strip()
        zone = get_zone_from_pincode_and_district(pincode, district, name)
        
        clean_pin = "".join([c for c in str(pincode) if c.isdigit()])
        p_suffix = clean_pin[-4:] if len(clean_pin) >= 4 else "1234"
        contact_no = f"+91 22 6155 {p_suffix}"
        location = record.get("location") or f"{name.split(',')[0]}, {district}"

        defaults = {
            'name': name,
            'location': location,
            'zone': zone,
            'contact': contact_no,
            'pincode': pincode,
            'district': district,
            'timestamp': record.get("timestamp", ""),
            
            'wb_a_pos': int(record.get('wb_a_pos', 0) or 0),
            'wb_a_neg': int(record.get('wb_a_neg', 0) or 0),
            'wb_b_pos': int(record.get('wb_b_pos', 0) or 0),
            'wb_b_neg': int(record.get('wb_b_neg', 0) or 0),
            'wb_ab_pos': int(record.get('wb_ab_pos', 0) or 0),
            'wb_ab_neg': int(record.get('wb_ab_neg', 0) or 0),
            'wb_o_pos': int(record.get('wb_o_pos', 0) or 0),
            'wb_o_neg': int(record.get('wb_o_neg', 0) or 0),
            
            'prbc_a_pos': int(record.get('prbc_a_pos', 0) or 0),
            'prbc_a_neg': int(record.get('prbc_a_neg', 0) or 0),
            'prbc_b_pos': int(record.get('prbc_b_pos', 0) or 0),
            'prbc_b_neg': int(record.get('prbc_b_neg', 0) or 0),
            'prbc_ab_pos': int(record.get('prbc_ab_pos', 0) or 0),
            'prbc_ab_neg': int(record.get('prbc_ab_neg', 0) or 0),
            'prbc_o_pos': int(record.get('prbc_o_pos', 0) or 0),
            'prbc_o_neg': int(record.get('prbc_o_neg', 0) or 0),
            
            'total_units': int(record.get('total_units', 0) or 0),
            'bombay_pos': int(record.get('bombay_pos', 0) or 0),
            'bombay_neg': int(record.get('bombay_neg', 0) or 0),
            'sd_platelets': int(record.get('sd_platelets', 0) or 0),
            'sd_plasma': int(record.get('sd_plasma', 0) or 0),
            'ffp': int(record.get('ffp', 0) or 0),
            'cryo_pp': int(record.get('cryo_pp', 0) or 0),
            'liquid_plasma': int(record.get('liquid_plasma', 0) or 0),
            'rdp': int(record.get('rdp', 0) or 0),
            'cryo_pre': int(record.get('cryo_pre', 0) or 0),
        }

        try:
            BloodBank.objects.update_or_create(id=bb_id, defaults=defaults)
            saved_count += 1
        except Exception as ex:
            logger.error(f"[Scraper] Failed to save {name}: {ex}")

    print(f"[Scraper] Successfully synchronized {saved_count} blood banks in Mumbai region.")
    return True