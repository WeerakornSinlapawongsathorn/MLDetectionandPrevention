# Read log from suricata and send to API
import time
import json
import requests

LOG_FILE = "/var/log/suricata/eve.json"
API_URL = "http://127.0.0.1:5000/detect-log"

# Tail -f for suricata
# Read Log File
def tail_log(file_path):
    with open(file_path, 'r') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.strip()

# Read Log File
# Find 'Alert'
# Create Payload, send to API
def main():
    print("[🔍] Watching Suricata log for alerts...")
    for line in tail_log(LOG_FILE):
        if '"alert"' in line:
            try:
                data = json.loads(line)
                src_ip = data.get("src_ip", "N/A")
                dst_ip = data.get("dest_ip", "N/A")
                signature = data.get("alert", {}).get("signature", "Unknown Threat")
                threat_type = f"{signature} from Suricata"

                payload = {
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "threat_type": threat_type 
                }

                res = requests.post(API_URL, json=payload)
                if res.ok:
                    print(f"[✅] Alert sent: {threat_type} from {src_ip} to {dst_ip}")
                else:
                    print(f"[❌] Failed to send alert: {res.text}")
            except Exception as e:
                print(f"[⚠️] JSON parse error: {e}")

if __name__ == "__main__":
    main()
