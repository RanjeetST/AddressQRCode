import asyncio
from bleak import BleakScanner
from flask import Flask, jsonify, request, send_from_directory
import qrcode
import io
import base64

app = Flask(__name__, static_folder="static")

# In-memory cache for RSSI tracking
device_cache = {}

def extract_mac_from_adv_data(manufacturer_data):
    for _, data_bytes in manufacturer_data.items():
        if len(data_bytes) >= 12:
            mac_bytes = data_bytes[6:12]
            mac_str = ':'.join(f"{b:02X}" for b in mac_bytes)
            return mac_str
    return None

async def scan_devices():
    devices = await BleakScanner.discover(timeout=5.0)
    result = []

    for device in devices:
        address = device.address
        name = device.name or "Unknown"
        rssi = device.rssi

        metadata = device.metadata
        mdata = metadata.get('manufacturer_data', {})
        mac_in_adv = extract_mac_from_adv_data(mdata)
        if "ROBKIT1" in name:
            print("Found ROBKIT1") 
            if address not in device_cache or device_cache[address]['rssi'] < rssi:
                device_cache[address] = {
                  "name": name,
                  "address": address,
                   "mac_in_adv": mac_in_adv,
                    "local_name": metadata.get("local_name", ""),
                    "service_uuids": metadata.get("uuids", []),
                    "manufacturer_data": {str(k): list(v) for k, v in mdata.items()},
                   "rssi": rssi
            }
        else:
            print("Not Found ROBKIT1") 


    return list(device_cache.values())

@app.route("/scan")
def scan():
    devices = asyncio.run(scan_devices())
    return jsonify(devices)

@app.route("/generate_qr")
def generate_qr():
    mac = request.args.get("mac")
    if not mac:
        return "MAC address is required", 400

    data = f"strobotapp://connect?address={mac}"
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return jsonify({"qr_base64": img_base64})

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(debug=True)
