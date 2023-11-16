import os

from fastapi import FastAPI, Request

from db import database
from models import *

app = FastAPI()

form_templates = database.get_collection(os.getenv('FORM_TEMPLATES_COLLECTION_NAME', 'FormTemplate'))
'''Коллекция с шаблонами форм.'''

@app.post('/get_form')
def get_template_form_name(request: Request) -> str | dict[str, str]:
    '''
    Endpoint для получения имени подходящего шаблона формы

    ### Входные значения
    Произвольное количество query-параметров, каждый параметр это пара
    `<Имя поля формы>=<Значение поля>`

    ### Возвращаемое значение
    - Имя шаблона, если найден шаблон, подходящий под переданные поля формы.
    - Пары `<Имя поля формы>: <Тип поля>`, если шаблон не найден
    '''

    request_field_types: dict[str, str] = {}

    for param in request.query_params:
        field_value = request.query_params[param]
        field_type = FormTemplate.get_field_type(field_value)
        request_field_types[param] = field_type

    # Ну, это же должно быть быстрее чем перебор всех документов в питоне, да?
    aggregation =  form_templates.aggregate([
        {
            "$addFields": {
            "field_is_in_request": {
                "$map": {
                    "input": {
                        "$filter": {
                            "input": {
                                "$objectToArray": "$$ROOT"
                            },
                            "as": "unfiltered",
                            "cond": {
                                "$and": [
                                {
                                    "$not": [
                                    {
                                        "$eq": [
                                        "$$unfiltered.k",
                                        "_id"
                                        ]
                                    }
                                    ]
                                },
                                {
                                    "$not": [
                                    {
                                        "$eq": [
                                        "$$unfiltered.k",
                                        "name"
                                        ]
                                    }
                                    ]
                                }
                                ]
                            }
                        }
                    },
                    "as": "keyvalues",
                    "in": {
                        "$or": [
                            {
                                "$eq": [
                                    "$$keyvalues.k",
                                    field
                                ]
                            } for field in request_field_types
                        ]
                    }
                }
            }
            }
        },
        {
            "$addFields": {
                "allFieldsAreContained": {
                    "$allElementsTrue": [
                    "$field_is_in_request"
                    ]
                }
            }
        },
        {
            "$match": {
                "allFieldsAreContained": True, # Проверка того, что все поля шаблона находятся в запросе
                "$and": [  # проверка того, что типы полей совпадают в запросе и в документе
                    {'$or': [
                        {field: {'$exists': False}},
                        {field: 'text'},  # текстом может быть абсолютна любая строка
                        {field: request_field_types[field]}
                    ]} for field in request_field_types
                ]
            }
        }
    ])

    result = aggregation.try_next()

    if result is None:
        return request_field_types
    
    return result['name']