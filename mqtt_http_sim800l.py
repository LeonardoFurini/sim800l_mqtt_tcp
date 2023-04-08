from mqtt_over_tcp import MqttConnection, MqttPublish
import serial
import time


# Configurações do servidor MQTT e da mensagem MQTT
mqtt_server = "broker.hivemq.com"  # Endereço do servidor MQTT
mqtt_port = "1883"

mqtt_client_id = "dgtsim"  # Tópico MQTT para envio da mensagem
mqtt_username = "dgtleo"  # Nome de usuário para autenticação
mqtt_password = "dtg123"  # Senha para autenticação
mqtt_topic = "v1/devices/me/telemetry"


# Configurações do dispositivo SIM800L
SERIAL_PORT = "COM24"  # Porta serial do dispositivo
BAUDRATE = 9600  # Taxa de transmissão
TIMEOUT = 5  # Tempo máximo de espera para a resposta do dispositivo


def transmit(payload: bytes, endline: bool = True):
    pyl = payload
    if endline:
        pyl = pyl + b"\r\n"
    print(f"TX: {pyl}")
    ser.write(pyl)
    ser.flush()


def receive():
    response = ser.readlines()
    for i in response:
        print(f"RX: {i}")


# Create serial conection
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT)

# Start Task and Set APN, USER NAME, PASSWORD
transmit(('AT+CSTT="www","",""').encode())
receive()
time.sleep(2)

# Bring Up Wireless Connection with GPRS or CSD
transmit(("AT+CIICR").encode())
receive()
time.sleep(2)

# Get Local IP Address
transmit(("AT+CIFSR").encode())
receive()
time.sleep(2)

# Start TCP connection
transmit((f'AT+CIPSTART="TCP","{mqtt_server}","{mqtt_port}"').encode())
receive()


mqtt_message = '{"test":123}'  # Mensagem MQTT a ser enviada
frame_con = MqttConnection(mqtt_client_id, mqtt_username, mqtt_password).generate_request()
frame_pub = MqttPublish(mqtt_topic, mqtt_message).generate_request()
transmit((f"AT+CIPSEND={len(frame_con)+len(frame_pub)}").encode())
time.sleep(1)
transmit(frame_con + frame_pub, endline=False)
receive()
print(f"FULL => frame: {(frame_con+frame_pub).hex().upper()}")

# Encerramento da conexão serial
ser.close()
