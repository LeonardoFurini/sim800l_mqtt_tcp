
import sys
sys.path.insert(0, r'G:\\Meu Drive\\Engenharia Eletrônica\\TCC - Monitoramento\\Desenvolvimento\\AuxScript\\sim800l_mqtt_tcp') 
from mqtt_over_tcp import MqttConnection, MqttPublish

# Configurações do servidor MQTT e da mensagem MQTT
# mqtt_server = "mqtt.thingsboard.cloud"  # Endereço do servidor MQTT
mqtt_server = "broker.hivemq.com"  # Endereço do servidor MQTT
mqtt_port = "1883"

mqtt_client_id = "dgtsim"  # Tópico MQTT para envio da mensagem
mqtt_username = "dgtleo"  # Nome de usuário para autenticação
mqtt_password = "dtg123"  # Senha para autenticação
mqtt_topic = "v1/devices/me/telemetry"
mqtt_message = '{"test":123}'  # Mensagem MQTT a ser enviada


frame_con = MqttConnection(mqtt_client_id, mqtt_username, mqtt_password).generate_request()
frame_publi = MqttPublish(mqtt_topic, mqtt_message).generate_request()
frame_full_req = frame_con + frame_publi

print(f"Con: {frame_con.hex().upper()}")
print(f"Pub: {frame_publi.hex().upper()}")
print(f"Full: {frame_full_req.hex().upper()}")
