from typing import Literal
import datetime
import re

from pydantic import BaseModel, ConfigDict


class FieldType(str):
    def is_valid(self):
        raise NotImplementedError()


class Email(FieldType):
    def is_valid(self):
        return self.isascii()


FIELD_TYPES = Literal['date', 'email', 'phone', 'text']
'''
Возможные значения уникальных полей `FormTemplate`. 
Обозначают тип данных, которые будут хранится в формах этого шаблона
'''


# На самом деле эта модель нигде не используется, потому что эндпоинтов для создания или получения
# конкретного шаблона нет. Но зато сюда можно семантически засунуть функции валидации типов
class FormTemplate(BaseModel):
    '''
    Модель для шаблона форм. 
    Содержит название формы и произвольное число уникальный полей, у каждого из которых указан
    тип поля `FIELD_TYPES`, который должен быть у формы, созданной на основе шаблоны
    '''
    name: str
    '''Название формы'''

    __pydantic_extra__: dict[str, FIELD_TYPES]

    model_config = ConfigDict(extra='allow')

    @staticmethod
    def get_field_type(field: str) -> FIELD_TYPES:
        if FormTemplate.is_date(field):
            return 'date'
        if FormTemplate.is_phone(field):
            return 'phone'
        if FormTemplate.is_email(field):
            return 'email'
        return 'text'

    @staticmethod
    def is_date(field: str) -> bool:
        separated_field = field.split('.')

        if len(separated_field) != 3:
            separated_field = field.split('-')
            if len(separated_field) != 3:
                return False

        if len(separated_field[0]) != 2 or len(separated_field[1]) != 2:
            return False
        
        try:
            datetime.datetime(
                day=int(separated_field[0]), 
                month=int(separated_field[1]), 
                year=int(separated_field[2])
            )
        except ValueError:
            return False

        return True

    @staticmethod
    def is_phone(field: str) -> bool:
        return re.fullmatch(r'\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}', field) is not None

    @staticmethod 
    def is_email(field: str) -> bool:
        return re.fullmatch(r'.+@.+\.[a-z]+', field) is not None