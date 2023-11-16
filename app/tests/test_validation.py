import unittest

from models import FormTemplate

class TestFormTemplateValidation(unittest.TestCase):

    def test_date(self):
        self.assertTrue(FormTemplate.is_date('12.03.2002'))
        self.assertTrue(FormTemplate.is_date('31-12-2020'))
        self.assertFalse(FormTemplate.is_date('no-12-2020'))
        self.assertFalse(FormTemplate.is_date('1-12-2020'))
        self.assertFalse(FormTemplate.is_date('61-12-2020'))
        self.assertFalse(FormTemplate.is_date('61/12/2020'))
        self.assertFalse(FormTemplate.is_date('12.2020'))
    
    def test_email(self):
        self.assertTrue(FormTemplate.is_email('cool@stuff.io'))
        self.assertFalse(FormTemplate.is_email('@stuff.io'))
        self.assertFalse(FormTemplate.is_email('random'))
        self.assertFalse(FormTemplate.is_email('should@not.wo-rk'))
        self.assertFalse(FormTemplate.is_email('should@not.WORK'))
    
    def test_phone(self):
        self.assertTrue(FormTemplate.is_phone('+7 322 232 22 32'))
        self.assertTrue(FormTemplate.is_phone('+73222322232'))
        self.assertFalse(FormTemplate.is_phone('+7     3222322232'))
        self.assertFalse(FormTemplate.is_phone('+7 not num be rs'))
        self.assertFalse(FormTemplate.is_phone('+7 222'))