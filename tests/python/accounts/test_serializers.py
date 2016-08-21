from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from accounts.serializers import UserRegistrationSerializer
from lib.testutils import CustomTestCase
from tests.python.accounts.test_models import UserFactory


class UserRegistrationSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {'data': {'email': 'test1@mailinator.com',
                  'first_name': 'test',
                  'last_name': 'user',
                  'password': 'test'},
         'error': ('email', ['Please use a different email address provider.']),
         'label': 'Invalid email.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },

        {'data': {'email': 'test1@gmail',
                  'first_name': 'test',
                  'last_name': 'user',
                  'password': 'test'},
         'error': ('email', ['Enter a valid email address.']),
         'label': 'Bad email format.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },

        {'data': {'email': 'emailwilllogininserializer@mydomain.com',
                  'first_name': 'test',
                  'last_name': 'user',
                  'password': 'test'},
         'error': ('email', ['user with this Email address already exists.']),
         'label': 'Email is already in use.',
         'method': 'POST',
         'status': status.HTTP_400_BAD_REQUEST
         },
    ]
    VALID_DATA_DICT = [
        {'email': 'emailsuccess@gmail.com',
         'first_name': 'test',
         'last_name': 'user',
         'password': 'test'},
    ]

    def setUp(self):
        self.required_fields = ['email', 'first_name', 'last_name', 'password']
        self.not_required_fields = ['id']
        self.user = UserFactory.create(email='emailwilllogininserializer@mydomain.com')

    def test_fields(self):
        serializer = UserRegistrationSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = UserRegistrationSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_validate_success(self):
        serializer = UserRegistrationSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)


class UserLoginSerializerTest(CustomTestCase, APITestCase):
    INVALID_DATA_DICT = [
        {'data': {'email': 'emailwilllogin@mydomain.com',
                  'password': 'teste'},
         'error': ('non_field_errors', ['Unable to login with provided credentials.']),
         'label': 'Invalid login credentials.',
         'method': 'POST',
         'status': status.HTTP_401_UNAUTHORIZED
         },
    ]
    VALID_DATA_DICT = [
        {'email': 'emailwilllogin@mydomain.com', 'password': 'test'},
    ]

    def setUp(self):
        self.required_fields = ['email', 'password']
        self.not_required_fields = []

    def test_fields(self):
        serializer = JSONWebTokenSerializer()
        self.assert_fields_required(True, serializer, self.required_fields)
        self.assert_fields_required(False, serializer, self.not_required_fields)
        self.assertEqual(len(serializer.fields), len(self.required_fields) + len(self.not_required_fields))

    def test_invalid_data(self):
        serializer = JSONWebTokenSerializer
        self.assert_invalid_data(serializer, self.INVALID_DATA_DICT)

    def test_validate_success(self):
        serializer = JSONWebTokenSerializer
        self.assert_valid_data(serializer, self.VALID_DATA_DICT)
