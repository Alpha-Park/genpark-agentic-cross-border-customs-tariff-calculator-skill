"""
Agentic Cross-Border Customs Tariff & Landed Cost Calculator (Zero External Dependencies)
Performs HS code classification, de minimis exemption checks, and CIF landed cost computation.
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional

HS_CATALOG = {
    "electronics": {"hs_code": "8517.62.00", "category": "Smartphones, Routers & Communication Hardware", "base_duty_rate": 0.025},
    "robot": {"hs_code": "8479.89.95", "category": "Autonomous Service & Industrial Robots", "base_duty_rate": 0.035},
    "camera": {"hs_code": "8525.89.40", "category": "Digital Action & 360 Cameras", "base_duty_rate": 0.021},
    "apparel": {"hs_code": "6204.43.40", "category": "Textiles & Synthetic Apparel", "base_duty_rate": 0.120},
    "footwear": {"hs_code": "6403.99.60", "category": "Leather & Athletic Footwear", "base_duty_rate": 0.085},
    "battery": {"hs_code": "8507.60.00", "category": "Lithium-Ion Power Stations", "base_duty_rate": 0.034}
}

JURISDICTION_RULES = {
    "US": {"de_minimis_usd": 800.0, "vat_gst_rate": 0.0, "processing_fee_rate": 0.003464},
    "EU": {"de_minimis_usd": 165.0, "vat_gst_rate": 0.20, "processing_fee_rate": 0.0},
    "UK": {"de_minimis_usd": 175.0, "vat_gst_rate": 0.20, "processing_fee_rate": 0.0},
    "CA": {"de_minimis_usd": 110.0, "vat_gst_rate": 0.05, "processing_fee_rate": 0.0},
    "JP": {"de_minimis_usd": 70.0, "vat_gst_rate": 0.10, "processing_fee_rate": 0.0},
    "CN": {"de_minimis_usd": 40.0, "vat_gst_rate": 0.13, "processing_fee_rate": 0.0}
}

class AgenticCrossBorderCustomsTariffCalculator:
    def __init__(self):
        pass

    def classify_hs_code(self, product_description: str) -> Dict[str, Any]:
        """Classifies product description into 8-digit Harmonized System (HS) code."""
        desc_lower = product_description.lower()
        for kw, info in HS_CATALOG.items():
            if kw in desc_lower:
                return {
                    "matched_keyword": kw,
                    "hs_code": info["hs_code"],
                    "category": info["category"],
                    "standard_duty_rate": info["base_duty_rate"],
                    "confidence": 0.94
                }
        return {
            "matched_keyword": "general_merchandise",
            "hs_code": "9999.00.00",
            "category": "General Consumer Goods",
            "standard_duty_rate": 0.05,
            "confidence": 0.75
        }

    def calculate_landed_cost(
        self,
        product_description: str,
        declared_value_usd: float,
        shipping_insurance_usd: float = 25.0,
        destination_country: str = "US",
        incoterm: str = "DDP"
    ) -> Dict[str, Any]:
        """
        Calculates CIF value, checks de minimis exemption, computes import duty, VAT/GST,
        and determines buyer vs seller payable amounts under Incoterms.
        """
        dest = destination_country.upper()
        rules = JURISDICTION_RULES.get(dest, JURISDICTION_RULES["US"])
        hs_info = self.classify_hs_code(product_description)

        fob_val = float(declared_value_usd)
        freight = float(shipping_insurance_usd)
        cif_val = round(fob_val + freight, 2)

        is_de_minimis_exempt = fob_val <= rules["de_minimis_usd"]

        if is_de_minimis_exempt:
            duty_usd = 0.0
            mpf_usd = 0.0
        else:
            duty_usd = round(cif_val * hs_info["standard_duty_rate"], 2)
            mpf_usd = round(min(538.40, max(31.67, cif_val * rules["processing_fee_rate"])) if rules["processing_fee_rate"] > 0 else 0.0, 2)

        # VAT/GST applies on (CIF + Duty) in most non-US jurisdictions
        vat_taxable_base = cif_val + duty_usd
        vat_usd = 0.0 if (dest == "US" or (is_de_minimis_exempt and dest == "CA")) else round(vat_taxable_base * rules["vat_gst_rate"], 2)

        total_taxes_and_fees = round(duty_usd + vat_usd + mpf_usd, 2)
        total_landed_cost = round(cif_val + total_taxes_and_fees, 2)

        incoterm_norm = incoterm.upper()
        seller_collects_at_checkout = total_landed_cost if incoterm_norm == "DDP" else cif_val
        carrier_collects_on_delivery = 0.0 if incoterm_norm == "DDP" else total_taxes_and_fees

        return {
            "destination_country": dest,
            "incoterm": incoterm_norm,
            "hs_code": hs_info["hs_code"],
            "hs_category": hs_info["category"],
            "fob_value_usd": fob_val,
            "cif_value_usd": cif_val,
            "de_minimis_threshold_usd": rules["de_minimis_usd"],
            "is_de_minimis_duty_exempt": is_de_minimis_exempt,
            "import_duty_usd": duty_usd,
            "import_vat_gst_usd": vat_usd,
            "customs_processing_fee_usd": mpf_usd,
            "total_duties_and_taxes_usd": total_taxes_and_fees,
            "total_landed_cost_usd": total_landed_cost,
            "checkout_payable_usd": seller_collects_at_checkout,
            "cod_customs_payable_usd": carrier_collects_on_delivery
        }

    def generate_customs_manifest(self, calculation: Dict[str, Any], shipper_name: str = "GenPark Global Logistics") -> Dict[str, Any]:
        """Generates electronic CN22/CN23 commercial invoice manifest."""
        now = time.time()
        manifest_id = "CUS-" + hashlib.sha256(f"{calculation['hs_code']}:{calculation['total_landed_cost_usd']}:{now}".encode("utf-8")).hexdigest()[:10].upper()
        return {
            "manifest_id": manifest_id,
            "form_type": "CN23_COMMERCIAL_INVOICE" if calculation["fob_value_usd"] > 400 else "CN22_DECLARATION",
            "shipper": shipper_name,
            "hs_tariff_code": calculation["hs_code"],
            "destination": calculation["destination_country"],
            "incoterms": calculation["incoterm"],
            "declared_cif_usd": calculation["cif_value_usd"],
            "settled_taxes_usd": calculation["total_duties_and_taxes_usd"],
            "electronic_clearance_ready": True,
            "generated_at": now
        }
