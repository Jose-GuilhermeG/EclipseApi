from messages import TemplateEmail
from settings import EMAIL_PORT, EMAIL_PASSWORD, SMTP_SERVER
from consumer.kafkaConsumer import KafkaConsumer, json_deserializer

TOPIC = "delivered_message"

email = TemplateEmail(
    smtp_server=SMTP_SERVER,
    port=EMAIL_PORT,
    password=EMAIL_PASSWORD,
    template_name="confirmDeliverd.html",
)


class kafkaEmailConsumer(KafkaConsumer):
    pass


kafakaConsumer = kafkaEmailConsumer("localhost:9092", json_deserializer)


def send_delived_email_message(consumer):
    for msg in consumer:
        try:
            print("entrega de pedido confirmada")
            body_context = msg.value.get("data")
            user_email = body_context.pop("email")
            email.send_message(user_email, "entrega de pedido confirmada", body_context)
        except Exception as e:
            print(f"Error sending delivered email: {e}")
