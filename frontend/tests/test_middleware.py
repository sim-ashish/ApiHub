from django.test import TestCase, override_settings
from django.test.client import Client
import logging
from http import HTTPStatus

class MaintenanceModeMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        logging.disable(logging.CRITICAL)

    @override_settings(MAINTENANCE_MODE = True)
    def test_response_when_maintenance_mode_is_on(self):
        response = self.client.get('/')
        self.assertContains(
            response, 
            'Application is in Maintenance Mode, Please Come back Later'
        )

        # self.assertTemplateUsed(response, 'maintenance.html')     # IF it returns a template

    @override_settings(MAINTENANCE_MODE = False)
    def test_response_when_maintenance_mode_is_off(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'frontend/index.html')


class IPBlacklistMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(BANNED_IPS = None)
    def test_request_successful_without_blacklist_setting(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.Ok)

    @override_settings(BANNED_IPS = ['192.168.1.2'])
    def test_request_successful_without_non_blacklist_ip(self):
        response = self.client.get('/', REMOTE_ADDR="192.100.1.3")
        self.assertEqual(response.status_code, HTTPStatus.Ok)

    @override_settings(BANNED_IPS = ['192.168.1.2'])
    def test_request_successful_with_blacklist_ip(self):
        response = self.client.get('/', REMOTE_ADDR="192.168.1.2")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)