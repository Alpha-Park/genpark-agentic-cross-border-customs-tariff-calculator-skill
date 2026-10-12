"""Example usage for AgenticCrossBorderCustomsTariffCalculator."""
import sys
import json
from client import AgenticCrossBorderCustomsTariffCalculator

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Agentic Cross-Border Customs Tariff & Landed Cost Calculator Demo ===")
    calc = AgenticCrossBorderCustomsTariffCalculator()

    # 1. Classify HS Code
    print("\n--- 1. Harmonized System (HS) Classification ---")
    hs = calc.classify_hs_code("Unitree Quadruped Autonomous Robot Dog")
    print(f"HS Code: {hs['hs_code']} | Category: {hs['category']} | Base Tariff: {hs['standard_duty_rate']*100:.1f}%")

    # 2. Compute DDP Landed Cost to European Union
    print("\n--- 2. Calculating DDP Landed Cost to EU ($1,200 Value + $60 Freight) ---")
    landed = calc.calculate_landed_cost(
        product_description="Unitree Quadruped Autonomous Robot Dog",
        declared_value_usd=1200.0,
        shipping_insurance_usd=60.0,
        destination_country="EU",
        incoterm="DDP"
    )
    print(f"CIF Value: ${landed['cif_value_usd']:.2f} | De Minimis Exempt: {landed['is_de_minimis_duty_exempt']}")
    print(f"Import Duty: ${landed['import_duty_usd']:.2f} | Import VAT (20%): ${landed['import_vat_gst_usd']:.2f}")
    print(f"Total Landed Cost Payable at Checkout (DDP): ${landed['checkout_payable_usd']:.2f}")

    # 3. Generate Electronic CN23 Customs Declaration Manifest
    print("\n--- 3. Generating CN23 Electronic Customs Manifest ---")
    manifest = calc.generate_customs_manifest(landed)
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
