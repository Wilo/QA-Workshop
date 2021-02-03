# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate
from selenium.common.exceptions import NoSuchElementException
from django.contrib.auth import models
import time
import os.path
from app.catalog.models import Product
import pandas as pd

class TestFront(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.browser.wait = WebDriverWait(self.browser, 10)
        activate('en')
        # Create a fixture user
        user = models.User(
            username='familiaaycart', email='', is_staff=True, is_superuser=True)
        user.set_password('Ma1995.Ma1995.')
        user.save()
        # Creación masiva de catalogo de productos a partir de un archivo CSV
        df = pd.read_csv(f"{os.getcwd()}/app/catalog/catalog_fixture.csv")
        row_items = df.iterrows()

        products = [
            Product(
                name=row["name"],
                link=row["link"],
                classification=row["classification"],
                product_type=row["product_type"],
                brand=row["brand"],
                vendor_link=row["vendor_link"],
                vendor_name=row["vendor_name"],
                vendor_sales=row["vendor_sales"],
                vendor_location=row["vendor_location"],
                )
                for _, row in row_items
                ]
       
        Product.objects.bulk_create(products) #noqa

    def tearDown(self):
        self.browser.quit()

    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
            (By.ID, element_id)))

    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
            (By.ID, element_id)))

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def get_full_path_url(self, url):
        return self.live_server_url + url

    def test_submit_form_using_url_type(self):

        self.browser.get(self.get_full_path_url(
            '/admin/login/'))
        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys('familiaaycart')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('Ma1995.Ma1995.')
        login_btn = self.browser.find_element_by_xpath(
            "//input[@type='submit']")
        login_btn.click()

        time.sleep(5)
        self.assertEqual(
            f"{self.live_server_url}/admin/", self.browser.current_url)
        self.browser.get(self.get_full_path_url(
            '/admin/catalog/product/'))
        time.sleep(5)