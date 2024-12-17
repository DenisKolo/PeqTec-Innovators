import network
import espnow
from machine import ADC, Pin
import time

# WLAN im STA-Modus aktivieren
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# ESP-NOW initialisieren
esp = espnow.ESPNow()
esp.active(True)

esp.add_peer(b'\xcc{\\\x97\xd7L')  # Füge die MAC-Adresse des Empfängers ein

# Joystick-Konfiguration
joystick_y = ADC(Pin(36))  # Y-Achse für Vorwärts/Rückwärts
joystick_y.atten(ADC.ATTN_11DB)

joystick_x = ADC(Pin(39))  # X-Achse für Links/Rechts
joystick_x.atten(ADC.ATTN_11DB)

# Kalibrierung der ADC-Werte
min_adc = 0
max_adc = 4095
mid_adc = (min_adc + max_adc) // 2

# Hauptschleife
while True:
    #Debugging Joystickwerte auslesen
    #print(joystick_y.read(), joystick_x.read())
    #print()
    # Joystick-Werte auslesen
    forward_value = joystick_y.read()  # Vorwärts/Rückwärts
    steering_value = joystick_x.read()  # Links/Rechts
    
    # Geschwindigkeit berechnen (-100 bis 100)
    if forward_value > mid_adc:  # Vorwärts
        speed = int(((forward_value - mid_adc) / (max_adc - mid_adc) * 100))
    elif forward_value < mid_adc:  # Rückwärts
        speed = int(((forward_value - mid_adc) / (mid_adc - min_adc) * 100))
    else:
        speed = 0

    # Lenkwinkel berechnen (0 bis 180 Grad)
    angle = int(((steering_value / max_adc) * 140))

    # Datenpaket erstellen
    data = f"{speed},{angle}"
    esp.send(b'\xcc{\\\x97\xd7L', data.encode('utf-8'))  # Senden
    print(f"Gesendet: Geschwindigkeit={speed}, Lenkwinkel={angle}")

    time.sleep(0.1)  # Update-Intervall
