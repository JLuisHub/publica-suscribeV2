import json, time, stomp, sys

class Message(stomp.ConnectionListener):
    def on_message(self, message):
        data = json.loads(message.body)
        print(f"ADVERTENCIA!!!\n[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}...\nssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")


class Notifier:
    
    def __init__(self):
        self.topic = "notifier"
        self.token = ""
        self.chat_id = ""

    def suscribe(self):
        print("Inicio de gestión de notificaciones...")
        print()
        self.consume(queue=self.topic)

    def consume(self, queue):
        try:
            conn = stomp.Connection(host_and_ports=[('localhost', 61613)])
            conn.set_listener('callback', Message())
            conn.connect(wait=True)
            conn.subscribe(destination=queue, headers='', id=1)
            while True:
                time.sleep(1)
        
        except (KeyboardInterrupt, SystemExit):
            #channel.close()
            conn.disconnect()
            sys.exit("Conexión finalizada...")

    def callback(self, ch, method, properties, body):
        print("enviando notificación de signos vitales...")
        if self.token and self.chat_id:
            data = json.loads(body.decode("utf-8"))
            message = f"ADVERTENCIA!!!\n[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}...\nssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}"
            bot = telepot.Bot(self.token)
            bot.sendMessage(self.chat_id, message)
        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    notifier = Notifier()
    notifier.suscribe()