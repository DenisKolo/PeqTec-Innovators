import network
import espnow
import machine
import time

# WLAN im STA-Modus aktivieren
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# ESP-NOW initialisieren
esp = espnow.ESPNow()
esp.active(True)

# MAC-Adresse des Empfängers hinzufügen
peer_mac = b'\xc4\xd8\xd5\x94\x92|'  # Ersetze mit der MAC-Adresse des Empfängers
esp.add_peer(peer_mac)

# Taster an den GPIO-Pins einrichten
taster_vorwärts = machine.Pin(23, machine.Pin.IN, machine.Pin.PULL_UP)
taster_rückwärts = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
taster_links = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
taster_rechts = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)

print("Warte auf Tasteneingaben...")

# Hauptschleife
try:
    while True:
        if not taster_vorwärts.value():  # Vorwärts-Taster gedrückt (LOW)
            message = "1"
            esp.send(peer_mac, message.encode())
            print(f"Nachricht gesendet: {message}")
            time.sleep(0.1)  # Entprellung

        if not taster_rückwärts.value():  # Rückwärts-Taster gedrückt (LOW)
            message = "2"
            esp.send(peer_mac, message.encode())
            print(f"Nachricht gesendet: {message}")
            time.sleep(0.1)

        if not taster_links.value():  # Links-Taster gedrückt (LOW)
            message = "3"
            esp.send(peer_mac, message.encode())
            print(f"Nachricht gesendet: {message}")
            time.sleep(0.1)

        if not taster_rechts.value():  # Rechts-Taster gedrückt (LOW)
            message = "4"
            esp.send(peer_mac, message.encode())
            print(f"Nachricht gesendet: {message}")
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Programm beendet.")
