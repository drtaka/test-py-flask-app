from pprint import pprint

from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super().setUp()

        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                res_auth = client.post('/auth',
                                       data=json.dumps({'username': 'test', 'password': '1234'}),
                                       headers={'Content-Type': 'application/json'})
                auth_token = json.loads(res_auth.data)['access_token']
                # 'JWT ' の部分は Flask JWT 固有のフォーマット
                self.access_token = f'JWT {auth_token}'

    def testf_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                respose = client.get('/item/test')
                self.assertEqual(401, respose.status_code)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test',
                                      headers={'Authorization': self.access_token})
                self.assertEqual(404, response.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.get('/item/test', headers={'Authorization': self.access_token})
                # expected = {
                #     'name': 'test',
                #     'price': 19.99
                # }

                self.assertEqual(200, response.status_code)
                # self.assertDictEqual(expected, json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.delete('/item/test')

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'message': 'Item deleted'},
                                     json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.post('/item/test', data={'price': 18.99, 'store_id': 1})

                self.assertEqual(201, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 18.99},
                                     json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 18.99, 1).save_to_db()
                response = client.post('/item/test', data={'price': 18.99, 'store_id': 1})

                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': "An item with name 'test' already exists."},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                response = client.put('/item/test', data={'price': 18.99, 'store_id': 1})

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 18.99},
                                     json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 18.99, 1).save_to_db()

                self.assertEqual(18.99, ItemModel.find_by_name('test').price)

                response = client.put('/item/test', data={'price': 10.11, 'store_id': 1})

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 10.11},
                                     json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 18.99, 1).save_to_db()

                response = client.get('/items')

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'items': [{'name': 'test', 'price': 18.99}]},
                                     json.loads(response.data))
