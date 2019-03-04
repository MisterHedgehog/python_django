from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from catalog.models import Item, Brand, Hat
from catalog.views import BaseBasket


class DealTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        User.objects.create_user('costumer', 'kek@gmail.com', 'Pass')
        seller = User.objects.create_user('seller', 'lol@gmail.com', 'Pass')
        Brand.objects.create(name="Xiaomi")
        Hat.objects.create(name='hat', owner=seller.profile, price=1)
        pass


    def setUp(self):
        pass


    def test_balance(self):
        money = User.objects.get(username="costumer").profile.balance
        self.assertEquals(money, 100)


    def test_profile_link(self):
        User = get_user_model()
        response = self.client.get(reverse('catalog:profile'))
        self.assertEqual(response.status_code, 302)
        seller = User.objects.get(username="seller")
        self.client.login(username='seller', password='Pass')
        # Проверка, что пользователь залогинился
        response = self.client.get(reverse('catalog:profile'), follow=True)
        self.assertEqual(str(response.context['user']), 'seller')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        seller = User.objects.get(username="seller")
        result = self.client.get(reverse('catalog:item', kwargs={'pk': 1}))
        self.assertEquals(result.status_code, 200)
        self.client.login(username='seller', password='Pass')
        result = self.client.post(reverse('catalog:item', kwargs={'pk': 1}), data=dict(amount=3), follow=True)
        self.assertEquals(result.status_code, 200)
        basket = BaseBasket(result.session)
        print(result.session)
        self.assertEqual(basket.get_total_price(), 3)
    #
    #
    # def test_deal(self):
    #     costumer = User.objects.get(username="user1")
    #     seller = User.objects.get(username="user2")
    #     self.assertEquals(money, 100)
