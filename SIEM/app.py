# Flow: Suricata --> log.py --> app.py
# Flow: Dashboard --> file --> app.py --> dashboard
# Create API
# Jsonify = JSON
# Load models
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from joblib import load
from datetime import datetime
import os

# Build an app
# Upload folder
app = Flask(__name__)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load model, scaler, feature, and features
model = load('model.pkl')
scaler = load('scaler.pkl')
encoder = load('encoder.pkl')
features = list(load('features.pkl'))

# In case, some files do not have an exact feature as model
rename_map = {
    'Tot Fwd Pkts': 'Total Fwd Packets',
    'Tot Bwd Pkts': 'Total Backward Packets',
    'TotLen Fwd Pkts': 'Total Length of Fwd Packets',
    'TotLen Bwd Pkts': 'Total Length of Bwd Packets',
    'Fwd IAT Tot': 'Fwd IAT Total',
    'Fwd Header Len': 'Fwd Header Length',
    'Dst Port': 'Destination Port',
    'Src Port': 'Source Port',
    'Flow Byts/s': 'Flow Bytes/s',
    'Flow Pkts/s': 'Flow Packets/s',
    'Pkt Len Var': 'Packet Length Variance',
}

# Check features and rename to match
def preprocess(df):
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    df.columns = df.columns.str.strip()
    df.rename(columns=rename_map, inplace=True)

    if 'Fwd Header Length' in df.columns and 'Fwd Header Length.1' not in df.columns:
        df['Fwd Header Length.1'] = df['Fwd Header Length']

    x = df[[col for col in features if col in df.columns]].copy()
    for col in features:
        if col not in x.columns:
            x[col] = 0.0

    x = x[features]
    return scaler.transform(x), df

# Create logs during the detection
# Format Timestamp, prediction, source IP, and destination IP
def log_alert(alert):
    with open('alerts.log', 'a') as f:
        f.write(f"[{alert['timestamp']}] ALERT - {alert['prediction']} from {alert['src_ip']} to {alert['dst_ip']}\n")

# Check request from endpoint
# When an endpoint upload CSV via POST
# Save file
# Read file as DataFrame
# Pass the file into preprocess (adjust features)
# Turn prediction into labels (model convert labels into number)
# Find Source IP and Destination IP
# Alerts save prediction that does not 'BENIGN'
@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    saved_path = os.path.join(UPLOAD_DIR, f"uploaded_{timestamp_str}.csv")
    file.save(saved_path)

    try:
        df = pd.read_csv(saved_path)
        print(f"File loaded: {saved_path} | Shape: {df.shape}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return jsonify({'error': f'Failed to read CSV: {str(e)}'}), 500

    try:
        x_scaled, original = preprocess(df)
        predictions = model.predict(x_scaled)
        labels = encoder.inverse_transform(predictions)
        original['Prediction'] = labels

        # Flexible column name detection
        src_col = next((c for c in original.columns if c.lower() in ['src ip', 'source ip']), None)
        dst_col = next((c for c in original.columns if c.lower() in ['dst ip', 'destination ip']), None)

        if not src_col or not dst_col:
            return jsonify({'error': 'Missing Src IP or Dst IP columns'}), 400

        alerts = []
        for _, row in original[original['Prediction'] != 'BENIGN'].iterrows():
            alert = {
                'timestamp': datetime.now().strftime("%Y:%m:%d %H:%M:%S"),
                'src_ip': row.get(src_col, 'N/A'),
                'dst_ip': row.get(dst_col, 'N/A'),
                'prediction': row['Prediction']
            }
            alerts.append(alert)
            log_alert(alert)

        print(f"{len(alerts)} threats detected")
        return jsonify(alerts)

    except Exception as e:
        print(f"Processing failed: {e}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

# Real-time alert
# Receive JSON, logs
# Build alerts.log
@app.route('/detect-log', methods=['POST'])
def detect_log():
    try:
        data = request.get_json()
        src_ip = data.get("src_ip", "N/A")
        dst_ip = data.get("dst_ip", "N/A")
        prediction = data.get("threat_type", "SURICATA_ALERT")
        timestamp = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

        alert = {
            "timestamp": timestamp,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "prediction": prediction

        }

        log_alert(alert)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Run App ===
if __name__ == '__main__':
    app.run(debug=True)
