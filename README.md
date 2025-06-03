# BLE Scanner & QR Generator 🌐📡

This is a Flask-based web server that allows scanning of BLE devices using `bleak`, filters for devices named **ROBKIT1**, displays advertisement and RSSI data, and generates QR codes for connecting to the devices via custom deep links.

---

## 🛠️ Features

- Scan BLE devices using `bleak`
- Filter and list devices containing **ROBKIT1**
- Extract advertisement data including MAC from manufacturer data
- Cache highest RSSI seen per device
- Generate QR code for deep linking: `strobotapp://connect?address=<mac>`
- Serve a frontend from the `static/` folder

---

## 📦 Environment Setup

### 1. ✅ Prerequisites

Ensure you have the following installed:

- **Python 3.9+**
- **pip**
- **Bluetooth hardware enabled on your system**

> 💡 This script needs to be run **natively** (not in WSL) to access BLE properly.

---

### 2. 📁 Clone the Repository

```bash
git clone https://github.com/RanjeetST/AddressQRCode.git
cd robkit-ble-scanner
```

---

### 3. 🧪 Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   
 # Windows: venv\Scripts\activate
```

---

### 4. 📥 Install Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

> This includes:
> - `flask`
> - `bleak`
> - `qrcode[pil]`

---

## 🚀 Running the Server

```bash
python app.py
```

You should see:

```
* Running on http://127.0.0.1:5000/
```

Open your browser and visit: [http://localhost:5000](http://localhost:5000)

---

## 📡 API Endpoints

### 🔍 `/scan`

- **Method:** GET  
- **Description:** Scans nearby BLE devices and returns those with names containing `ROBKIT1`.

**Sample Response:**

```json
[
  {
    "name": "ROBKIT1",
    "address": "D0:39:72:44:55:66",
    "mac_in_adv": "F1:23:45:67:89:AB",
    "local_name": "ROBKIT1",
    "service_uuids": ["..."],
    "manufacturer_data": {"76": [0, 1, 2, 3]},
    "rssi": -45
  }
]
```

---

### 📱 `/generate_qr?mac=<MAC_ADDRESS>`

- **Method:** GET  
- **Description:** Generates a QR code for a given MAC address in the format:  
  `strobotapp://connect?address=<MAC>`

**Sample Response:**

```json
{
  "qr_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**How to use:**

```html
<img src="data:image/png;base64,<qr_base64>" />
```

---

## 🌐 Frontend

Place your HTML, CSS, and JS files inside the `static/` directory.

`index.html` is served as the homepage via:

```
http://localhost:5000/
```

---

## 🧹 Cleanup

To deactivate the virtual environment:

```bash
deactivate
```

To stop the server, press:

```bash
Ctrl + C
```

---

## 🧠 Troubleshooting

- **BLE Device Not Found?**
  - Make sure Bluetooth is enabled.
  - Run outside of WSL or Docker.
  - Test with a BLE-capable device (e.g., another phone).

- **Permission denied on Linux?**
  Run with `sudo` or set BLE capabilities:
  ```bash
  sudo setcap 'cap_net_raw,cap_net_admin+eip' $(readlink -f $(which python))
  ```

---

## 📄 License

MIT License – free to use, modify, and distribute.

---

## 👩‍💻 Author

Developed by STMicroelectronics(Ranjeet) at **STMicroelectronics** 🚀  
This is only for demo purpose not intended to used for the release purpose.
