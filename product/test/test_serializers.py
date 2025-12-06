from django.test import TestCase
from product.models import Product
from product.serializers import ProductCreateSerializer
from model_bakery import baker
from django.utils.text import slugify

class product_create_serializer_test(TestCase):
    def setUp(self):
        self.product = baker.prepare(Product , name = "Produto de teste")
        self.slug = slugify(self.product)
        
    def tearDown(self):
        Product.objects.all().delete()
        
    def test_if_slug_created_is_correct(self):
        data = ProductCreateSerializer(self.product).data
        serializer = ProductCreateSerializer(data = data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.slug , self.slug)