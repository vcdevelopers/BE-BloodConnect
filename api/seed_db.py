import os
import sys
from pathlib import Path

# Add project root to Python path dynamically
sys.path.append(str(Path(__file__).resolve().parent.parent))

import django
from datetime import datetime, date, timedelta

# Initialize Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_api.settings")
django.setup()

from api.models import BloodBank, Donor, BloodRequest, Camp, Campaign
from api.scraper import run_live_scraper

def seed_database():
    print("[Seed] Clearing existing database tables...")
    BloodBank.objects.all().delete()
    Donor.objects.all().delete()
    BloodRequest.objects.all().delete()
    Camp.objects.all().delete()
    Campaign.objects.all().delete()

    print("[Seed] Seeding mock donors...")
    donors_data = [
        {
            "name": "Rajesh Kumar",
            "blood_group": "O+",
            "zone": "Andheri",
            "phone": "+91 98765 43210",
            "email": "rajesh@email.com",
            "gender": "Male",
            "age": 32,
            "last_donation": date(2025, 12, 15),
            "total_donations": 8,
            "eligible": True,
            "next_eligible": date(2026, 3, 15),
            "status": "active"
        },
        {
            "name": "Priya Sharma",
            "blood_group": "A+",
            "zone": "Bandra / Khar",
            "phone": "+91 98765 43211",
            "email": "priya@email.com",
            "gender": "Female",
            "age": 28,
            "last_donation": date(2025, 11, 20),
            "total_donations": 5,
            "eligible": True,
            "next_eligible": date(2026, 3, 20),
            "status": "active"
        },
        {
            "name": "Amit Patel",
            "blood_group": "B+",
            "zone": "Dadar / Worli",
            "phone": "+91 98765 43212",
            "email": "amit@email.com",
            "gender": "Male",
            "age": 45,
            "last_donation": date(2025, 10, 10),
            "total_donations": 12,
            "eligible": True,
            "next_eligible": date(2026, 1, 10),
            "status": "active"
        },
        {
            "name": "Ananya Desai",
            "blood_group": "O-",
            "zone": "South Mumbai",
            "phone": "+91 98765 43213",
            "email": "ananya@email.com",
            "gender": "Female",
            "age": 31,
            "last_donation": date(2026, 2, 1),
            "total_donations": 20,
            "eligible": False,
            "next_eligible": date(2026, 5, 1),
            "status": "active"
        },
        {
            "name": "Meera Joshi",
            "blood_group": "A-",
            "zone": "Goregaon / Malad",
            "phone": "+91 98765 43215",
            "email": "meera@email.com",
            "gender": "Female",
            "age": 26,
            "last_donation": date(2025, 9, 15),
            "total_donations": 2,
            "eligible": True,
            "next_eligible": date(2026, 1, 13),
            "status": "active"
        },
        {
            "name": "Vikram Malhotra",
            "blood_group": "AB+",
            "zone": "Borivali",
            "phone": "+91 98765 43216",
            "email": "vikram@email.com",
            "gender": "Male",
            "age": 39,
            "last_donation": date(2025, 8, 10),
            "total_donations": 6,
            "eligible": True,
            "next_eligible": date(2025, 11, 10),
            "status": "active"
        },
        {
            "name": "Siddharth Shah",
            "blood_group": "O+",
            "zone": "Thane",
            "phone": "+91 98765 43217",
            "email": "sid@email.com",
            "gender": "Male",
            "age": 29,
            "last_donation": date(2026, 1, 5),
            "total_donations": 4,
            "eligible": True,
            "next_eligible": date(2026, 4, 5),
            "status": "active"
        },
        {
            "name": "Sneha Patil",
            "blood_group": "B-",
            "zone": "Navi Mumbai",
            "phone": "+91 98765 43218",
            "email": "sneha@email.com",
            "gender": "Female",
            "age": 34,
            "last_donation": date(2025, 11, 5),
            "total_donations": 7,
            "eligible": True,
            "next_eligible": date(2026, 3, 5),
            "status": "active"
        }
    ]

    for d in donors_data:
        Donor.objects.create(**d)

    print("[Seed] Seeding mock emergency blood requests...")
    requests_data = [
        {
            "patient_name": "Suresh Mehta",
            "blood_group": "O+",
            "units": 3,
            "hospital": "Lilavati Hospital",
            "hospital_address": "Bandra / Khar",
            "attendant_name": "Ramesh Mehta",
            "phone": "+91 98765 11111",
            "urgency": "Emergency",
            "status": "approved",
            "matched_donors_count": 5
        },
        {
            "patient_name": "Anita Verma",
            "blood_group": "AB-",
            "units": 2,
            "hospital": "Kokilaben Hospital",
            "hospital_address": "Andheri",
            "attendant_name": "Rahul Verma",
            "phone": "+91 98765 22222",
            "urgency": "Urgent",
            "status": "pending",
            "matched_donors_count": 0
        },
        {
            "patient_name": "Manoj Tiwari",
            "blood_group": "B+",
            "units": 1,
            "hospital": "Hinduja Hospital",
            "hospital_address": "Dadar / Worli",
            "attendant_name": "Sunita Tiwari",
            "phone": "+91 98765 33333",
            "urgency": "Normal",
            "status": "completed",
            "matched_donors_count": 3
        },
        {
            "patient_name": "Kavita Nair",
            "blood_group": "A+",
            "units": 2,
            "hospital": "Jaslok Hospital",
            "hospital_address": "South Mumbai",
            "attendant_name": "Vinod Nair",
            "phone": "+91 98765 44444",
            "urgency": "Emergency",
            "status": "matched",
            "matched_donors_count": 4
        }
    ]

    for r in requests_data:
        BloodRequest.objects.create(**r)

    print("[Seed] Seeding mock donation camps...")
    camps_data = [
        {
            "name": "World Blood Donor Day Drive",
            "organizer": "Red Cross Mumbai",
            "location": "Dadar TT Circle, Mumbai",
            "zone": "Dadar / Worli",
            "date": date.today() + timedelta(days=15),
            "time": "9:00 AM - 5:00 PM",
            "slots": 100,
            "slots_booked": 67,
            "description": "Join us for the annual World Blood Donor Day mega drive.",
            "status": "upcoming"
        },
        {
            "name": "Corporate Blood Drive",
            "organizer": "TCS Foundation",
            "location": "BKC, Bandra East",
            "zone": "Bandra / Khar",
            "date": date.today() + timedelta(days=20),
            "time": "10:00 AM - 4:00 PM",
            "slots": 50,
            "slots_booked": 23,
            "description": "A corporate blood donation initiative for TCS employees and public.",
            "status": "upcoming"
        },
        {
            "name": "College Blood Donation Camp",
            "organizer": "NSS Mumbai University",
            "location": "Kalina Campus, Santacruz",
            "zone": "Andheri",
            "date": date.today() + timedelta(days=25),
            "time": "8:00 AM - 2:00 PM",
            "slots": 200,
            "slots_booked": 145,
            "description": "Annual student blood donation camp organized by NSS.",
            "status": "upcoming"
        },
        {
            "name": "Emergency O- Drive",
            "organizer": "Mumbai Blood Connect",
            "location": "Andheri Sports Complex",
            "zone": "Andheri",
            "date": date.today() + timedelta(days=30),
            "time": "9:00 AM - 6:00 PM",
            "slots": 75,
            "slots_booked": 12,
            "description": "Urgent need for O- blood type donors. Walk-ins welcome.",
            "status": "upcoming"
        }
    ]

    for c in camps_data:
        Camp.objects.create(**c)

    print("[Seed] Seeding mock campaign logs...")
    campaigns_data = [
        {
            "type": "sms",
            "message": "Urgent: O+ blood needed at Lilavati Hospital, Bandra.",
            "recipients": 45,
            "blood_group": "O+",
            "zone": "Bandra / Khar",
            "status": "sent"
        },
        {
            "type": "whatsapp",
            "message": "Emergency: AB- blood required within 3 hours at Kokilaben Hospital.",
            "recipients": 12,
            "blood_group": "AB-",
            "zone": "Andheri",
            "status": "sent"
        },
        {
            "type": "email",
            "message": "Blood donation camp at Dadar TT Circle on March 15. Register now!",
            "recipients": 230,
            "blood_group": None,
            "zone": "Dadar / Worli",
            "status": "sent"
        }
    ]

    for camp in campaigns_data:
        Campaign.objects.create(**camp)

    print("[Seed] Triggering live scraper to fetch active blood bank stock...")
    run_live_scraper()
    
    # Inject mock Bombay Blood Group stock into the first two blood banks for testing
    banks = BloodBank.objects.all()
    if banks.count() >= 1:
        first_bank = banks[0]
        print(f"[Seed] Injecting mock Bombay Blood Group stock into {first_bank.name} for testing...")
        first_bank.bombay_pos = 4
        first_bank.bombay_neg = 2
        first_bank.save()
    if banks.count() >= 2:
        second_bank = banks[1]
        print(f"[Seed] Injecting mock Bombay Blood Group stock into {second_bank.name} for testing...")
        second_bank.bombay_pos = 1
        second_bank.bombay_neg = 1
        second_bank.save()
        
    print("[Seed] Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
