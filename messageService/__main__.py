from controllers.deliverd import kafakaConsumer, send_delived_email_message, TOPIC

kafakaConsumer.listen(TOPIC, send_delived_email_message)
