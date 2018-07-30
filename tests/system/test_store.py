import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/{}'.format('test'))

                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/{}'.format('test'))
                response = client.post('/store/{}'.format('test'))

                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': "A store with name 'test' already exists."},
                                     json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                self.assertIsNotNone(StoreModel.find_by_name('test'))

                response = client.delete('/store/{}'.format('test'))

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'message': 'Store deleted'},
                                     json.loads(response.data))
                self.assertIsNone(StoreModel.find_by_name('test'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.get('/store/{}'.format('test'))

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test', 'items': []},
                                     json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/{}'.format('test'))

                self.assertEqual(404, response.status_code)
                self.assertDictEqual({'message': 'Store not found'},
                                     json.loads(response.data))

    def test_fstore_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()

                response = client.get('/store/{}'.format('test'))

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test', 'items': [{'name': 'test_item', 'price': 19.99}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.get('/stores')

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'stores': [{'name': 'test', 'items': []}]},
                                     json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()

                response = client.get('/stores')

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'stores': [{'name': 'test', 'items': [{'name': 'test_item', 'price': 19.99}]}]},
                                     json.loads(response.data))
