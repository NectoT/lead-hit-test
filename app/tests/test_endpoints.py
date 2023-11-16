import unittest
import json
import random

from pymongo.collection import Collection
from fastapi.testclient import TestClient

import db
import main
from main import app

test_client: TestClient = TestClient(app)


class TestGetForm(unittest.TestCase):

    test_collection: Collection

    @classmethod
    def setUpClass(cls) -> None:
        collection_name = 'TestFormTemplates' + str(random.randint(0, 100000))
        test_collection = db.database.create_collection(collection_name)
        print(__file__)
        with open('tests/mock_data.json', 'r') as file:
            mock_data: dict = json.load(file)
        test_collection.insert_many(mock_data)
        cls.test_collection = test_collection
        main.form_templates = test_collection
        
    

    @classmethod
    def tearDownClass(cls) -> None:
        cls.test_collection.drop()
    
    def _test_form(self, query_params: dict[str, str], expected_result: str | dict):
        response = test_client.post('/get_form', params=query_params)
        self.assertEqual(response.json(), expected_result)

    def test_inexistant_template_field_types(self):
        query_params = {
            'strange_phone': '+7 544 333 23 11', 
            'strange_text': 'Weird',
            'strange_email': 'wow@man.com',
            'strange_date': '13.11.1984'
        }
        response = test_client.post('/get_form', params=query_params)
        self.assertEqual(response.json(), {
            'strange_phone': 'phone', 
            'strange_text': 'text',
            'strange_email': 'email',
            'strange_date': 'date'
        })
    

    def test_concert_form(self):
        response = test_client.post('/get_form', params={'email': 'wow@man.ru'})
        self.assertEqual(response.json(), 'concertForm')
    
    def test_veterinarian_form(self):
        response = test_client.post('/get_form', params={
            'date': '12.03.2004',
            'phone': '+7 544 333 23 11',
            'petName': 'Mr Williams',
            'ownerName': 'Billy'
        })
        self.assertEqual(response.json(), 'veterinarianAppointmentForm')
    
    def test_incomplete_veterinarian_form(self):
        response = test_client.post('/get_form', params={
            'date': '12.03.2004',
            'phone': '+7 544 333 23 11',
            'petName': 'Mr Williams',
        })
        self.assertEqual(response.json(), {
            'date': 'date',
            'phone': 'phone',
            'petName': 'text'
        })
    
    def test_invalid_veterinarian_form(self):
        response = test_client.post('/get_form', params={
            'date': '204.03.2004',
            'phone': '+7 544 333 23 11',
            'petName': 'Mr Williams',
            'ownerName': 'Billy'
        })
        self.assertEqual(response.json(), {
            'date': 'text',
            'phone': 'phone',
            'petName': 'text',
            'ownerName': 'text'
        })
    
    def test_date_as_text(self):
        response = test_client.post('/get_form', params={
            'letter': 'callme@maybe.ohoh'
        })
        self.assertEqual(response.json(), 'loveLetterForm')
    
    def test_extra_fields(self):
        response = test_client.post('/get_form', params={
            'letter': 'I love you :3',
            'also': 'Can you send me your bank account details?'
        })
        self.assertEqual(response.json(), 'loveLetterForm')