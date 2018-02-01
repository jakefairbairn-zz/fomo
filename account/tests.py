from django.test import TestCase
from django.contrib.auth.models import Permission, Group, ContentType
from account import models as amod

class UserClassTest(TestCase):

    fixtures = [ 'data.yaml' ]

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

        superusers_emails = amod.User.objects.filter(is_superuser=True).values_list('email')
        print(superusers_emails)

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

    def create_assign_group(self):
        '''Test creating a group'''
        g1 = Group()
        g1.name = 'Salespeople'
        g1.save()
        self.u1.groups.add(g1)
        self.u1.save()

        self.assertTrue(self.u1.groups.filter(name='Salespeople'))
        print("RAN create_assign_group")

    def create_assign_permission(self):
        p1 = Permission()
        p.codename = 'change_product_price'
        p.name = 'Change the price of a product'
        p.content_type = ContentType.objects.get(id=1)
        p1.save()
        print("RAN create_assign_permission")

        #assign permission to gropu

        #assign permission to user

    def add_groups(self):
        '''Test adding a few groups'''
