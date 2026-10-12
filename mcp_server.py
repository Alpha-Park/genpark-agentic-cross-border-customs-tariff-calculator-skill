"""MCP Server for Agentic Cross-Border Customs Tariff Calculator."""
import sys
import json
import time
from client import AgenticCrossBorderCustomsTariffCalculator

calculator = AgenticCrossBorderCustomsTariffCalculator()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "calculate_customs_landed_cost":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "calculate_landed_cost")
    desc = args.get("product_description", "Smart Robot")
    val = float(args.get("declared_value_usd", 500.0))
    ship = float(args.get("shipping_insurance_usd", 30.0))
    dest = args.get("destination_country", "EU")
    incoterm = args.get("incoterm", "DDP")

    if action == "classify_hs_code":
        return calculator.classify_hs_code(desc)
    elif action == "calculate_landed_cost":
        return calculator.calculate_landed_cost(desc, val, ship, dest, incoterm)
    elif action == "generate_customs_manifest":
        calc = calculator.calculate_landed_cost(desc, val, ship, dest, incoterm)
        return calculator.generate_customs_manifest(calc)
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        # 1. US de minimis exempt (< $800)
        us_res = calculator.calculate_landed_cost("Action camera 360", 450.0, 20.0, "US", "DDP")
        assert us_res["is_de_minimis_duty_exempt"] is True
        assert us_res["import_duty_usd"] == 0.0

        # 2. EU above de minimis (> $165)
        eu_res = calculator.calculate_landed_cost("Lithium battery power station", 1000.0, 50.0, "EU", "DDP")
        assert eu_res["is_de_minimis_duty_exempt"] is False
        assert eu_res["import_duty_usd"] > 0.0
        assert eu_res["import_vat_gst_usd"] > 0.0
        manifest = calculator.generate_customs_manifest(eu_res)
        assert manifest["electronic_clearance_ready"] is True
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "AgenticCrossBorderCustomsTariffCalculator", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "calculate_customs_landed_cost",
                            "description": "Classify HS codes, check de minimis thresholds, calculate import duties and VAT/GST, and generate cross-border customs declaration manifests.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["classify_hs_code", "calculate_landed_cost", "generate_customs_manifest"]},
                                    "product_description": {"type": "string"},
                                    "declared_value_usd": {"type": "number"},
                                    "destination_country": {"type": "string"},
                                    "incoterm": {"type": "string"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
