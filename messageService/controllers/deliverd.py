from messages import TemplateEmail
from settings import EMAIL_PORT, EMAIL_PASSWORD, SMTP_SERVER, KAFKA_SERVER
from consumer.kafkaConsumer import kafkaMessageConsumer, json_deserializer
from consumer.cosumer import MessageConsumer

TOPIC = "confirm_delivered_message"

email = TemplateEmail(
    smtp_server=SMTP_SERVER,
    port=EMAIL_PORT,
    password=EMAIL_PASSWORD,
    template_name="confirmDeliverd.html",
)


class kafkaEmailConsumer(kafkaMessageConsumer):
    pass


kafakaConsumer = kafkaMessageConsumer(KAFKA_SERVER, json_deserializer)
consumer = MessageConsumer(kafakaConsumer)


def send_delived_email_message(consumer):
    for msg in consumer:
        try:
            body_context = msg.value.get("data")
            user_email = body_context.pop("email")
            email.send_message(user_email, "entrega de pedido confirmada", body_context)
            print("entrega de pedido confirmada")
        except Exception as e:
            print(f"Error sending delivered email: {e}")
