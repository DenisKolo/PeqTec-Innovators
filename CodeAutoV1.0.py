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
 
# Pins für die H-Brücke definieren
enable2 = machine.Pin(12, machine.Pin.OUT)  # Enable 2
input4 = machine.Pin(14, machine.Pin.OUT)  # Input 4
input3 = machine.Pin(27, machine.Pin.OUT)  # Input 3
 
enable1 = machine.Pin(19, machine.Pin.OUT)  # Enable 1
input1 = machine.Pin(18, machine.Pin.OUT)  # Input 1
input2 = machine.Pin(5, machine.Pin.OUT)   # Input 2
 
# Funktion zum Initialisieren der H-Brücke (alle Pins auf LOW setzen)
def init_hbridge():
    enable2.off()
    input4.off()
    input3.off()
    enable1.off()
    input1.off()
    input2.off()
 
# Bewegungen der H-Brücke steuern
def vorwärts():
    enable1.on()
    input1.on()
    input2.off()
    enable2.on()
    input3.on()
    input4.off()
 
def rückwärts():
    enable1.on()
    input1.off()
    input2.on()
    enable2.on()
    input3.off()
    input4.on()
 
def links():
    enable1.on()
    input1.off()
    input2.on()
    enable2.on()
    input3.on()
    input4.off()
 
def rechts():
    enable1.on()
    input1.on()
    input2.off()
    enable2.on()
    input3.off()
    input4.on()
 
# H-Brücke initialisieren
init_hbridge()
 
print("Warte auf Nachrichten...")
 
# Nachricht empfangen und darauf reagieren
try:
    while True:
        host, message = esp.recv()  # Blockiert, bis eine Nachricht empfangen wird
        if message:
            print(f"Nachricht von {host}: {message}")
            if message == b"4":
                vorwärts()
            elif message == b"3":
                rückwärts()
            elif message == b"2":
                links()
            elif message == b"1":
                rechts()
            time.sleep(0.7)  # Bewegung für 1 Sekunde ausführen
            init_hbridge()  # Nach jeder Bewegung die H-Brücke zurücksetzen
except KeyboardInterrupt:
    print("Programm beendet.")
    init_hbridge()  # Alle Pins deaktivieren