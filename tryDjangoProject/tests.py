#just for a sake of testing before production

from django.test import TestCase # for testing the filesystem
import os #isse kewal .env ke andar ke cheeze import kr lenge
from django.conf import settings #settings.SECRET_KEY ,aise hi hm settings ke andar kii cheeze import kr sakte hai,yha ek bhi baar use nhi kiya hu
from django.contrib.auth.password_validation import validate_password

class TryDjangoConfigTest(TestCase):
    #https://docs.python.org/3/library/unittest.html 
    def test_secret_key_strength(self):
        SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
        #self.assertEqual(SECRET_KEY,"abc123"),it is also a way to test the strength

        try:
            is_strong = validate_password(SECRET_KEY) 
        except Exception as e:
            msg = f'Weak Secret Key {e.messages}'
            self.fail(msg)

