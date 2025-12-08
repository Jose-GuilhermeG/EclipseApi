#imports
from rest_framework.test import APITestCase , APIClient
from django.contrib.auth import get_user_model
from model_bakery import baker
from product.models import Product , Category
from django.urls import reverse , resolve
from django.utils.text import slugify
from core.constants import DEFAULT_PAGE_NUMBER_LIST
from .mixins import ObjectsDeleteMixin , ClientLoggedMixin , ObjectDataMixin , ReqGetMixin
from product.serializers import ProductCreateSerializer
from rest_framework import status

USER = get_user_model()
def get_next_page(page) : return f"?limit={DEFAULT_PAGE_NUMBER_LIST}&limite={DEFAULT_PAGE_NUMBER_LIST}&offeset={DEFAULT_PAGE_NUMBER_LIST}&offset={DEFAULT_PAGE_NUMBER_LIST}&ofset={DEFAULT_PAGE_NUMBER_LIST}&page={page}"

#base test
class ProductTestBase(
    ObjectsDeleteMixin,
    ClientLoggedMixin,
    ObjectDataMixin,
    APITestCase,
):
    model = Product
    serializer = ProductCreateSerializer
    
class CategoryTestBase(
    ObjectsDeleteMixin,
    ReqGetMixin,
    APITestCase,
):
    model = Category

class product_list_test(
    ProductTestBase,
):    
    def setUp(self):
        self.url = reverse("product:product-list")
        
    def test_if_view_returned_max_allowed(self):
        productsCreatedNumber = DEFAULT_PAGE_NUMBER_LIST
        baker.make(Product,_quantity=productsCreatedNumber)
        data : dict = self.client.get(self.url).json()
        productsNumber = len(data["results"])
        self.assertEqual(productsNumber,productsCreatedNumber)
        
    def test_if_view_has_next_page(self):
        productsCreatedNumber = 2 * DEFAULT_PAGE_NUMBER_LIST
        baker.make(Product,_quantity=productsCreatedNumber)
        data : dict = self.client.get(self.url).json()
        self.assertTrue(data['next'])
        
    def test_if_view_has_previous_page(self):
        productsCreatedNumber = 2 * DEFAULT_PAGE_NUMBER_LIST
        baker.make(Product,_quantity=productsCreatedNumber)
        data : dict = self.client.get(self.url + get_next_page(1)).json()
        self.assertTrue(data.get("previous"))
        
class product_detail_test(
    ProductTestBase,
):
    def setUp(self):
        self.product_name = 'Produto de teste'
        self.product_slug = slugify(self.product_name)
        self.product = baker.make(Product , name= self.product_name, slug = self.product_slug)
        self.url = reverse("product:product-detail" , kwargs={'slug' : self.product_slug})
        
    def test_if_product_is_find_by_slug(self):
        data = self.client.get(self.url)
        self.assertEqual(200 , data.status_code)
        self.assertTrue(data.json())
        
class product_created_test(
    ProductTestBase,
):
    def setUp(self):
        self.url = reverse("product:product-list")
        self.user = baker.make(USER)
        self.product_data = baker.prepare(self.model , name="Teste")
        
    def test_if_user_anonimous_acess_is_denied(self):
        post_data = self.parse_obj_to_json(self.product_data)
        post_data.pop("image")
        req = self.client.post(self.url ,post_data )
        self.assertEqual(req.status_code,401)
        self.assertEqual(len(self.model.objects.all()) , 0)
        
    def test_if_user_authenticate_can_access_view(self):
        client = self.get_logged_client(self.user)
        post_data = self.parse_obj_to_json(self.product_data)
        post_data.pop("image")
        req = client.post(self.url ,post_data )
        self.assertEqual(req.status_code,201)
        
    
class product_delete_test(
    ProductTestBase
):
    def setUp(self):
        self.user = baker.make(USER)
        self.product = baker.make(self.model ,created_by = self.user)
        self.url = reverse("product:product-detail" , kwargs={"slug" : self.product.slug})
        
    def test_if_product_is_deleted(self):
        client = self.get_logged_client(self.user)
        req = client.delete(self.url)
        self.assertEqual(req.status_code,204)
        self.assertEqual( 0 , len(self.model.objects.all()))
        
    def test_if_user_anonimous_acess_is_denied(self):
        req = self.client.delete(self.url)
        self.assertEqual(req.status_code,401)
        self.assertEqual( 1 , len(self.model.objects.all()))
        
    def test_if_only_the_owner_of_product_can_delete(self):
        another_user = baker.make(USER)
        client = self.get_logged_client(another_user)
        req = client.delete(self.url)
        self.assertEqual(req.status_code,403)
        self.assertEqual( 1 , len(self.model.objects.all()))
        
        
class category_list_test(
    CategoryTestBase
):
    def setUp(self):
        self.url = reverse("product:category-list")
    
    def test_if_max_obj_by_page_is_correct(self):
        category_number = len(baker.make(self.model , _quantity = DEFAULT_PAGE_NUMBER_LIST))
        data , data_json = self.get_req()
        result_number = len(data_json.get("results"))
        self.assertEqual(category_number,result_number)
        self.assertEqual(data.status_code , 200)
        
    def test_if_pagination_next_page_is_correct(self):
        total_categories = 2 * DEFAULT_PAGE_NUMBER_LIST
        baker.make(self.model , _quantity = total_categories)
        data = self.client.get(self.url + get_next_page(1))
        data_json = data.json()
        self.assertTrue(data_json.get("previous"))
        self.assertEqual(data.status_code , 200)