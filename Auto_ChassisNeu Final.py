#
#
#    b'\x10\x06\x1c\xd7\x18\xa8'
#
#
#
#
import network
import espnow
from machine import Pin, PWM

# WLAN im Station-Modus aktivieren
wlan = network.WLAN(network.STA_IF)  # Station-Modus für ESP-NOW
wlan.active(True)

# ESP-NOW initialisieren
esp = espnow.ESPNow()
esp.active(True)

peer = b'\x10\x06\x1c\xd7\x18\xa8'
esp.add_peer(peer)  # Füge die MAC-Adresse des Senders ein

# Servo für Lenkung konfigurieren
servo = PWM(Pin(14), freq=50)

# def set_servo_angle(angle):
#     # Begrenze den Winkel auf den Bereich 0° bis 120°
#     angle = max(0, min(210, angle))
#     
#     # Berechne den Duty-Cycle (angepasst an 500-2500 µs für 0° bis 120°)
#     min_duty = 21  # Entspricht 500 µs (0°)
#     max_duty = 85  # Entspricht ~2000 µs (120°)
#     duty = int(16.5+min_duty + (angle / 210) * (max_duty - min_duty))
#     servo.duty(duty)
#     print(duty)
    
    
last_direction = None  # Global speichern

def set_servo_angle(angle):
    global last_direction

    # Begrenze den Winkel
    angle = max(0, min(210, angle))
    
        # Speichere die aktuelle Richtung
    if angle < 66:
        last_direction = "left"
    elif angle > 70:
        last_direction = "right"




    # Berechne den Duty-Cycle
    min_duty = 21
    max_duty = 85
    duty = int(15.5+min_duty + ((angle) / 210) * (max_duty - min_duty))
        
    #Offset rechts
    if last_direction == "right" and angle == 57:
        duty -= 9  # Korrigiere leicht nach links
    #Offset links
    if last_direction == "right" and angle == 57:
        duty += 0  # Korrigiere leicht nach rechts
        
    servo.duty(duty)
    
    print(angle)
    print(last_direction)


    print(duty)

# Motorsteuerung konfigurieren
M1_IN1 = Pin(4, Pin.OUT)
M1_IN2 = Pin(5, Pin.OUT)
M1_PWM = PWM(Pin(18), freq=18000)

def set_motor_speed(speed):
    if speed > 0:  # Vorwärts
        M1_IN1.value(1)
        M1_IN2.value(0)
    elif speed < 0:  # Rückwärts
        M1_IN1.value(0)
        M1_IN2.value(1)
    else:  # Stop
        M1_IN1.value(0)
        M1_IN2.value(0)
    M1_PWM.duty(abs(int(speed / 100 * 1023)))  # Maximaler Duty bei 100

# Empfangsverarbeitung
while True:
    if esp.any():  # Prüfen, ob Daten empfangen wurden
        peer, message = esp.recv()  # Empfangene Daten abrufen
        try:
            # Nachricht dekodieren und in Geschwindigkeit und Winkel umwandeln
            decoded = message.decode('utf-8')
            speed, angle = map(int, decoded.split(','))

            # Steuerung
            set_motor_speed(speed)
            set_servo_angle(angle)

            print(f"Empfangen: Geschwindigkeit={speed}, Lenkwinkel={angle}")
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Daten: {e}")
