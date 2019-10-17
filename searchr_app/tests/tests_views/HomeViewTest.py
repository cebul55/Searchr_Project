from django.test import TestCase
from django.urls import resolve
from selenium import webdriver

from searchr_app.views import home


class HomeViewTest(TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()

    def tearDown(self) -> None:
        self.driver.quit()

    def test_selenium_runs(self):
        self.resolved = resolve('/')
        self.assertEqual(self.resolved.func, home)
