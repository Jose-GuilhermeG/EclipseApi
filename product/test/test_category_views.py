#imports
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from product.models import Category
from django.urls import reverse
from core.constants import DEFAULT_PAGE_NUMBER_LIST
from rest_framework import status

USER = get_user_model()

class CategoryListViewTest(APITestCase):

    def setUp(self):
        self.categories = [
            Category.objects.create(name=f"Category {i}", slug=f"category-{i}")
            for i in range(DEFAULT_PAGE_NUMBER_LIST + 5)
        ]

        self.list_url = reverse("product:category-list")

    def test_list_returns_paginated_results(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), DEFAULT_PAGE_NUMBER_LIST)

        self.assertIsNotNone(response.data.get("next"))

    def test_list_second_page(self):
        response : dict = self.client.get(self.list_url)
        next_page_url : str = response.data.get("next")
        second_page_response : dict = self.client.get(next_page_url)
        
        self.assertEqual(second_page_response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(second_page_response.data["results"]), 5)

    def test_list_serializer_fields(self):
        response = self.client.get(self.list_url)
        first_item = response.data["results"][0]

        expected_fields = {"name", "slug", "category_url"}

        self.assertEqual(set(first_item.keys()), expected_fields)

        self.assertTrue(first_item["category_url"].startswith("http"))

    def test_list_cache_returns_same_content(self):
        # Primeira requisição (gera cache)
        response1 = self.client.get(self.list_url)
        data1 = response1.data

        # Segunda requisição (deve vir do cache)
        response2 = self.client.get(self.list_url)
        data2 = response2.data

        self.assertEqual(data1, data2)

    def test_list_is_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class CategoryDetailViewTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Category Detail Test",
        )

        self.detail_url = reverse(
            "product:category-detail",
            args=[self.category.slug]
        )

    def test_detail_returns_correct_fields(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_fields = {"name","product"}
        self.assertEqual(set(response.data.keys()), expected_fields)

        self.assertEqual(response.data["name"], self.category.name)

class CategoryCreateViewTest(APITestCase):
    
    def setUp(self):
        self.create_url = reverse("product:category-list")
        self.adminData = {
            "username":"adminTest", 
            "password":"123456",
            "email":"adminEmail@teste.com"
        }
    
    def test_new_create_category(self):
        admin = USER.objects.create_superuser(**self.adminData)
        self.client.force_login(admin)

        response = self.client.post(self.create_url, {"name": "New Category"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Category")
        self.assertIn("slug", response.data)
        self.assertEqual(Category.objects.count(), 1)
        
class CategoryDeleteViewTest(APITestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="New Category")
        self.delete_url = reverse("product:category-detail",args=[self.category.slug])
        self.adminData = {
            "username":"adminTest", 
            "password":"123456",
            "email":"adminEmail@teste.com"
        }
    
    def test_delete_category(self):
        admin = USER.objects.create_superuser(**self.adminData)
        self.client.force_login(admin)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

class CategoryPermissionsTest(APITestCase):

    def setUp(self):
        self.userData = {
            "username":"user", 
            "password":"123456",
            "email":"userEmail@teste.com"
        }
        
        self.adminData = {
            "username":"adminTest", 
            "password":"123456",
            "email":"adminEmail@teste.com"
        }
        
        self.user = USER.objects.create_user(**self.userData)

        self.admin = USER.objects.create_superuser(**self.adminData)

        self.category = Category.objects.create(name="Test Category")

        self.list_url = reverse("product:category-list")
        self.detail_url = reverse("product:category-detail", args=[self.category.slug])

    # CREATE
    def test_non_admin_cannot_create(self):
        self.client.force_login(self.user)
        response = self.client.post(self.list_url, {"name": "New"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.list_url, {"name": "New"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # UPDATE
    def test_non_admin_cannot_update(self):
        self.client.force_login(self.user)
        response = self.client.put(self.detail_url, {"name": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update(self):
        self.client.force_login(self.admin)
        response = self.client.put(self.detail_url, {"name": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # PARTIAL UPDATE
    def test_admin_can_partial_update(self):
        self.client.force_login(self.admin)
        response = self.client.patch(self.detail_url, {"name": "Partial"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # DELETE
    def test_non_admin_cannot_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete(self):
        self.client.force_login(self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # LIST & RETRIEVE
    def test_list_is_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_is_public(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)