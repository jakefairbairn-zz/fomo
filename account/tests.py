from django.test import TestCase
from django.contrib.auth.models import Permission, Group, ContentType
from account import models as amod

class UserClassTest(TestCase):

    fixtures = [ 'data.yaml' ]

    def setUp(self):
        self.u1 = amod.User()
        self.u1.first_name = 'Lisa'
        self.u1.last_name = 'Simpson'
        self.u1.email = 'lisa@simpsons.com'
        self.u1.set_password('password')
        self.u1.save()

    def test_load_save(self):
        '''Test creating, saving, and reloading a user'''

        u2 = amod.User.objects.get(email='lisa@simpsons.com')
        #could also do:
            #u2 = amod.User.objects.get(email=u1.email)

        self.assertEqual(self.u1.first_name, u2.first_name)
        self.assertEqual(self.u1.last_name, u2.last_name)
        self.assertEqual(self.u1.email, u2.email)
        self.assertEqual(self.u1.password, u2.password)
        self.assertTrue(u2.check_password('password'))

        superusers_emails = amod.User.objects.filter(is_superuser=True).values_list('email')

    def test_field_changes(self):
        '''Test regular field changes (first name, last name, etc.)'''

        u2 = amod.User.objects.get(email = 'lisa@simpsons.com')

        u2.first_name = 'Bart'
        u2.last_name = 'NotSimpson'

        u2.save()

        u3 = amod.User.objects.get(email = 'lisa@simpsons.com')
        self.assertEqual(u2.first_name, u3.first_name)
        self.assertEqual(u2.last_name, u3.last_name)

    def test_create_assign_group(self):
        '''Test creating a group'''
        g1 = Group()
        g1.name = 'Salespeople'
        g1.save()

        self.u1.groups.add(g1)
        self.u1.save()

        self.assertTrue(self.u1.groups.filter(name='Salespeople'))

    def test_create_assign_permission(self):
        p1 = Permission()
        p1.codename = 'change_product_price'
        p1.name = 'Change the price of a product'
        p1.content_type = ContentType.objects.get(id=1)
        p1.save()

        self.u1.user_permissions.add(p1)
        self.u1.save()

        self.assertTrue(self.u1.user_permissions.filter(codename='change_product_price'))

    def test_create_group_permission(self):
        '''Test creating a group and adding permissions to the group'''
        # Create the group object and save
        g1 = Group()
        g1.name = 'Salespeople'
        g1.save()

        # Create the permission object and save
        p1 = Permission()
        p1.codename = 'change_product_price'
        p1.name = 'Change the price of a product'
        p1.content_type = ContentType.objects.get(id=1)
        p1.save()

        g1.permissions.add(p1)
        g1.save()

        self.assertTrue(g1.permissions.filter(codename='change_product_price').exists())
