import json
# from django.test import TestCase
# from .models import Item, Review
import requests
import base64
from requests.auth import HTTPBasicAuth

# url = 'http://127.0.0.1:8000/api/v1/goods/'
# response = requests.get(url, auth=HTTPBasicAuth('Serj', '1234'))
# print(response.text)
data = json.dumps({'title': 'баклажан', 'description': 'Очень вкусный сыр, да еще и российский.', 'price': 1000000})
url = 'http://127.0.0.1:8000/api/v1/goods/'
response = requests.post(url, auth=HTTPBasicAuth('Serj', '1234'), data=data)
print(response.json())


# class TestViews(TestCase):
#     def test_post_item(self):
#         url = '/api/v1/goods/'
#         data = json.dumps({'title': 'сыр', 'description': 'Очень вкусный сыр, да еще и российский.', 'price': 1000000})
#         response = self.client.post(url, data=data, content_type='application/json')
#         item = Item.objects.get(title='сыр')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json()['id'], item.id)
#
#     def test_err_decode(self):
#         url = '/api/v1/goods/'
#         data = {'title': 'сыр', 'description': 'Очень вкусный сыр, да еще и российский.', 'price': 100}
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 400)
#
#     def test_err_valid(self):
#         url = '/api/v1/goods/'
#         data = [{json.dumps({'title': 1, 'description': 'Очень вкусный сыр, да еще и российский.', 'price': 100})},
#                 {json.dumps({'title': '', 'description': 'Очень вкусный сыр, да еще и российский.', 'price': 100})},
#                 {json.dumps({'title': 'сыр', 'description': 'Очень вкусный сыр, да еще и российский.', 'price': '100'})},
#                 {json.dumps({'title': 'сыр', 'description': '', 'price': 100})},
#                 {json.dumps({'title': 'сыр', 'description': 2, 'price': 100})},
#                 {json.dumps({'title': 'сыр', 'description': 2, 'price': ''})},
#                     {json.dumps({'title': 'сыр', 'description': 2, 'price': 1000001})}
#                 ]
#
#         for d in data:
#             response = self.client.post(url, data=d, content_type='application/json')
#             self.assertEqual(response.status_code, 400)

