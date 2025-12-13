from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from core.constants import DEFAULT_CACHE_TIME


class AddCreatedByMixin:
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SetCache:
    cache_time = DEFAULT_CACHE_TIME

    @method_decorator(cache_page(cache_time))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(cache_time))
    def reatrive(self, request, *args, **kwrags):
        return super().reative(request, *args, **kwrags)


class ViewSetAddPermissionsMixin:

    permissions_class_per_action: dict = None

    def get_permissions(self):
        permissions_classes = self.permissions_class_per_action

        if not permissions_classes:
            return []

        current_permission = [permissions_classes.get(self.action)]

        if current_permission[0]:
            return [permission() for permission in current_permission]

        return []


class ViewSetAddDefaultPermissionMixin(ViewSetAddPermissionsMixin):
    default_permission = []

    def get_permissions(self):
        permission = super().get_permissions()
        if not len(permission):
            permission = [
                default_permission() for default_permission in self.default_permission
            ]

        return permission


class ViewSetGetSerializerClassMixin:
    serializers_class_per_action = None

    def get_serializers_classes_field(self):
        if not self.serializers_class_per_action:
            raise Exception(
                "You must set the 'serializers_classe_per_action' attribute or override the 'get_serializers_classes_field' method."
            )
        return self.serializers_class_per_action

    def get_serializer_class(self, *args, **kwargs):
        serializer_classes = self.get_serializers_classes_field()
        return serializer_classes.get(self.action)


class get_access_and_refresh_tokens:

    @staticmethod
    def get_tokens_for_user(user):

        refresh = RefreshToken.for_user(user)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}
