# imports
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _


from users.models import ShoppingCarItem, Purchased
from product.serializers import ProductListSerializer

USER = get_user_model()


# serializers
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only="true")

    class Meta:
        model = USER
        fields = ["username", "email", "password"]

    def create(self, validated_data: dict):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class SetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only="true")

    class Meta:
        model = USER
        fields = ["password"]

    def save(self, **kwargs):
        password = self.validated_data["password"]
        user = self.instance
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ["photo", "username", "email", "first_name", "last_name"]


class AuthenticationSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = USER.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError(_("Credenciais inválidas"))

        is_password_correct = user.check_password(password)

        if not is_password_correct:
            raise serializers.ValidationError(_("Senha invalida"))

        refresh = self.get_token(user)

        data = dict()
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class ShoppingCarItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCarItem
        fields = ["product", "quantity"]


class ShoppingCarItemsSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    item_url = serializers.HyperlinkedIdentityField(
        view_name="auth:user-shopping-car-detail", lookup_field="pk"
    )

    class Meta:
        model = ShoppingCarItem
        fields = ["product", "quantity", "total", "item_url"]


class ShoppingCarItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = ShoppingCarItem
        fields = ["product", "quantity", "total"]


class PurchasedListSerializer(serializers.ModelSerializer):
    purchased_url = serializers.HyperlinkedIdentityField(
        view_name="auth:user-purchased-detail", lookup_field="id"
    )
    product = ProductListSerializer()
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = Purchased
        fields = ["product", "quantity", "total", "status", "purchased_url"]


class PurchasedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchased
        fields = ["product", "quantity"]


class PurchasedDetailSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    status = serializers.CharField(source="get_status_display")
    confirm_delivered = serializers.HyperlinkedIdentityField(
        view_name="auth:user-purchased-confirm-delivered", lookup_field="id"
    )

    class Meta:
        model = Purchased
        fields = [
            "product",
            "quantity",
            "total",
            "status",
            "created_at",
            "submit_date",
            "confirm_delivered",
        ]
