from controllers.deliverd import consumer, send_delived_email_message, TOPIC

consumer.listen(TOPIC, send_delived_email_message)
