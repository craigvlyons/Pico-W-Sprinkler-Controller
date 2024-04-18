# this project is a pico-w web server that controls a sprinkler system. 
# the pico-w controls the sprinkler system with 4 relays.
import machine
import network
import socket

# Initialize WiFi connection
ssid = 'YOUR_SSID'
password = 'YOUR_PASSWORD'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

# Setup relays
relay_pins = [machine.Pin(i, machine.Pin.OUT) for i in (YOUR_RELAY_PINS)]
def control_relay(zone, state):
    if 0 <= zone < len(relay_pins):
        relay_pins[zone].value(state)

# Simple web server
def web_page():
    if relay_pins[0].value() == 1:
        gpio_state="ON"
    else:
        gpio_state="OFF"
    
    # Read HTML content from a file
    with open('/c:/testing ideas/Pico-W-Sprinkler-Controller/sprinkler_page.html', 'r') as f:
        html = f.read().replace('{gpio_state}', gpio_state)
    
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    zone1_on = request.find('/?zone1=on')
    zone1_off = request.find('/?zone1=off')
    if zone1_on == 6:
        control_relay(0, 1)
    if zone1_off == 6:
        control_relay(0, 0)
    
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
