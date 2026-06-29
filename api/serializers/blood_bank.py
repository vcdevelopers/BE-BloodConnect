from rest_framework import serializers
from api.models import BloodBank

class BloodBankSerializer(serializers.ModelSerializer):
    inventory = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = BloodBank
        fields = [
            'id', 'name', 'location', 'zone', 'contact', 
            'pincode', 'district', 'last_updated', 'timestamp', 
            'inventory', 'distance'
        ]
    def get_inventory(self, instance):
        inventory = []
        
        # 1. Whole Blood Mappings
        wb_mappings = [
            ("A+", instance.wb_a_pos),
            ("A-", instance.wb_a_neg),
            ("B+", instance.wb_b_pos),
            ("B-", instance.wb_b_neg),
            ("AB+", instance.wb_ab_pos),
            ("AB-", instance.wb_ab_neg),
            ("O+", instance.wb_o_pos),
            ("O-", instance.wb_o_neg),
        ]
        for grp, val in wb_mappings:
            inventory.append({
                "component": "Whole Blood",
                "group": grp,
                "units": val or 0
            })
                
        # 2. Packed Red Blood Cells (PRBC) Mappings
        prbc_mappings = [
            ("A+", instance.prbc_a_pos),
            ("A-", instance.prbc_a_neg),
            ("B+", instance.prbc_b_pos),
            ("B-", instance.prbc_b_neg),
            ("AB+", instance.prbc_ab_pos),
            ("AB-", instance.prbc_ab_neg),
            ("O+", instance.prbc_o_pos),
            ("O-", instance.prbc_o_neg),
        ]
        for grp, val in prbc_mappings:
            inventory.append({
                "component": "PRBC",
                "group": grp,
                "units": val or 0
            })
                
        # 3. Other Components (Platelets, Plasma, etc.)
        other_mappings = [
            ("Single Donor Platelets", instance.sd_platelets),
            ("Random Donor Platelets (RDP)", instance.rdp),
            ("Fresh Frozen Plasma (FFP)", instance.ffp),
            ("Liquid Plasma", instance.liquid_plasma),
            ("Single Donor Plasma", instance.sd_plasma),
            ("Cryoprecipitate", instance.cryo_pp or instance.cryo_pre),
            ("Bombay Blood Group (+)", instance.bombay_pos),
            ("Bombay Blood Group (-)", instance.bombay_neg),
        ]
        for name, val in other_mappings:
            inventory.append({
                "component": name,
                "group": "All",
                "units": val or 0
            })
                
        return inventory

    def get_distance(self, instance):
        hash_val = abs(hash(instance.name))
        distance_km = 0.5 + (hash_val % 145) / 10.0
        return f"{distance_km:.1f} km"
