from rest_framework.test import APIClient


class ObjectsDeleteMixin:
    model = None

    def get_model(self):
        if not self.model:
            raise Exception("Model it's not defined")

        return self.model

    def tearDown(self):
        self.get_model().objects.all().delete()


class ClientLoggedMixin:
    @staticmethod
    def get_logged_client(user):
        client = APIClient()
        client.force_login(user)
        return client


class ReqGetMixin:
    def get_url(self):
        if not self.url:
            raise Exception("url it's not defined")

        return self.url

    def get_client(self):
        if not self.client:
            raise Exception("client it's not defined")

        return self.client

    def get_req(self):
        data = self.get_client().get(self.get_url())
        return data, data.json()


class ObjectDataMixin:
    serializer = None

    def get_serializer(self):
        if not self.serializer:
            raise Exception("serializer it's not defined")

        return self.serializer

    def parse_obj_to_json(self, obj):
        serializer = self.get_serializer()(obj)
        return serializer.data
