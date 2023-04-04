"""
Build an MQTT packet for transmission over
"""
from enum import Enum
from dataclasses import dataclass


# http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718028
# [CONN]    [RL]   [                                                    PLEN                                        ]
# [CONN]    [RL]   [PLEN]    [MQIsdp]    [LVL]   [FL]	[KA] [CIDLEN] [clientID] [ULEN] [username] [PWLEN] [password]
# [CONN]    ControlPkgType
# [RL]      Remaining Length
# ...


class ControlPkgType(Enum):
    """Avaliable actions"""

    CONNECT = 1
    PUBLISH = 3


@dataclass
class MqttConnection:
    """Generate frame conection"""

    mqtt_client_id: str = "ABCDEF"  # Tópico MQTT para envio da mensagem / Client ID
    mqtt_username: str = "dxxkgkpp"  # Nome de usuário para autenticação
    mqtt_password: str = "qAUZBdaSIULx"  # Senha para autenticação

    def generate_request(self) -> bytes:
        """Generate bytes frame"""

        mqtt_header_info = (6).to_bytes(2, "big")  # Identificador da mensagem (opcional para QoS 0)
        mqtt_header_info += str.encode("MQIsdp")  # Protocol

        mqtt_header_info += bytes([3])  # Protocol Level
        mqtt_header_info += b"\xC2"  # FL
        mqtt_header_info += b"\x00\x3C"  # KA

        mqtt_header_info += len(self.mqtt_client_id).to_bytes(2, "big")
        mqtt_header_info += str.encode(self.mqtt_client_id)

        mqtt_header_info += len(self.mqtt_username).to_bytes(2, "big")
        mqtt_header_info += str.encode(self.mqtt_username)

        mqtt_header_info += len(self.mqtt_password).to_bytes(2, "big")
        mqtt_header_info += str.encode(self.mqtt_password)

        # Generate Connection frame
        mqtt_header = b"\x10"
        mqtt_header += len(mqtt_header_info).to_bytes(1, "big")  # Protocol lenght
        mqtt_header += mqtt_header_info

        return mqtt_header


@dataclass
class MqttPublish:
    """Publish payload"""

    topic: str = "valetron"  # Tópico MQTT para envio da mensagem / Client ID
    payload: str = "helloravi"  # Nome de usuário para autenticação

    def generate_request(self) -> bytes:
        """Generate bytes frame"""

        mqtt_header_info = len(self.topic).to_bytes(2, "big")
        mqtt_header_info += str.encode(self.topic)
        mqtt_header_info += str.encode(self.payload)

        # Generate Connection frame
        mqtt_header = b"\x30"
        mqtt_header += len(mqtt_header_info).to_bytes(1, "big")  # Protocol lenght
        mqtt_header += mqtt_header_info

        return mqtt_header


if __name__ == "__main__":
    conn = MqttConnection()
    print(conn.generate_request().hex().upper())
    
    conn = MqttPublish()
    print(conn.generate_request().hex().upper())
