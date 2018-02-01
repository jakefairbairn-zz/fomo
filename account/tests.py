from django.test import TestCase
from account import models as amod

class UserClassTest(TestCase):

    def test_load_save(self):
        '''Test creating, saving, and reloading a user'''
        u1 = amod.User()
        u1.first_name = 'Lisa'
        u1.last_name = 'Simpson'
        u1.email = 'lisa@simpsons.com'
        u1.set_password('password')
        u1.save()

        u2 = amod.User.objects.get(email='lisa@simpsons.com')
        #could also do:
            #u2 = amod.User.objects.get(email=u1.email)

        self.assertEqual(u1.first_name, u2.first_name)
        self.assertEqual(u1.last_name, u2.last_name)
        self.assertEqual(u1.email, u2.email)
        self.assertEqual(u1.password, u2.password)
        self.assertTrue(u2.check_password('password'))

    def test_field_changes(self):
        '''Test regular field changes (first name, last name, etc.)'''
        u1 = amod.User()
        u1.first_name = 'Lisa'
        u1.last_name = 'Simpson'
        u1.email = 'lisa@simpsons.com'
        u1.save()

        u2 = amod.User.objects.get(email = 'lisa@simpsons.com')

        u2.first_name = 'Bart'
        u2.last_name = 'NotSimpson'

        u2.save()

        u3 = amod.User.objects.get(email = 'lisa@simpsons.com')
        self.assertEqual(u2.first_name, u3.first_name)
        self.assertEqual(u2.last_name, u3.last_name)

    def add_groups(self):
        '''Test adding a few groups'''
