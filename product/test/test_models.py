from django.test import TestCase
from model_bakery import baker
from product.models import Product
from django.core.exceptions import FieldError , ValidationError
from django.db.utils import IntegrityError

class Product_model_Test(TestCase):
    def tearDown(self):
        Product.objects.all().delete()
            
    def test_if_product_ordering_is_correct(self):
        baker.make(Product,_quantity = 5)
        products = Product.objects.all()
        self.assertGreater(products[0].price,products[1].price)
        
    def test_if_product_price_cannot_be_negative(self):
        product = baker.make(Product, price=-100)
        with self.assertRaises(ValidationError):
            product.full_clean()
            
    def test_if_search_method_is_working(self):
        baker.make(Product , name = 'teste' , description = '')
        baker.make(Product , name = 'unico' , description = '')
        query = Product.objects.search('unico')
        self.assertEqual(len(query) , 1)
        