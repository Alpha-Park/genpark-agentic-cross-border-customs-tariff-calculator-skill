# genpark-agentic-cross-border-customs-tariff-calculator-skill

[![GenPark AI](https://img.shields.io/badge/GenPark_AI-www.genpark.ai-blue.svg)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark_Company_92955550-0077B5.svg)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Autonomous Cross-Border E-Commerce Customs Tariff & Landed Cost Calculator. Classifies Harmonized System (HS) codes, evaluates de minimis duty exemption thresholds across global jurisdictions (US, EU, UK, JP, CN), computes ad valorem duties and import VAT/GST under DDP/DAP Incoterms, and generates customs manifests.

---

## 🌐 Official GenPark AI Ecosystem Links

- **GenPark Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Official Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) ([https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550))

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
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

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License & Community

Licensed under the [MIT License](LICENSE). Copyright © 2026 [GenPark AI](https://www.genpark.ai).
Follow us on LinkedIn: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) | [https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550)
