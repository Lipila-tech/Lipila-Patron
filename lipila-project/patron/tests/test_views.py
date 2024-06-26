from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest.mock import Mock, patch
import json
# Custom models
from accounts.models import PatronProfile, CreatorProfile
from patron.models import Tier, TierSubscriptions, Payments, Contributions


class TestPatronViewsMore(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.client = Client()
        cls.creator_user = User.objects.create(
            username='creatoruser', password='password')
        cls.client.force_login(cls.creator_user)
        data = {
            'patron_title': 'TestPatron',
            'about': 'test user about',
            'creator_category': 'artist',
        }
        cls.response = cls.client.post(
            reverse('patron:create_creator_profile'), data)
        cls.creator = CreatorProfile.objects.get(user=cls.creator_user)
        cls.response1 = cls.client.get(reverse('patron:tiers'))
        cls.tiers = Tier.objects.filter(creator=cls.creator).values()

    @classmethod
    def tearDownClass(cls):
        # Delete tiers (if any)
        for tier in cls.tiers:
            Tier.objects.get(id=tier['id']).delete()
        # Delete creator profile
        cls.creator.delete()
        # Logout client
        cls.client.logout()


    def test_edit_tier_get_request_logged_in(self):
        self.client.force_login(self.creator_user)
        tier = self.tiers[0]
        url = reverse('patron:edit_tier', kwargs={'tier_id': tier['id']})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'patron/admin/actions/edit_tiers.html')

    def test_edit_tier_post_request_valid_data(self):
        self.client.force_login(self.creator_user)
        tier = self.tiers[0]
        url = reverse('patron:edit_tier', kwargs={'tier_id': tier['id']})
        data = {'name': 'Updated Tier', 'price': 15.00,
                'description': 'New description'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        tier = Tier.objects.get(pk=tier['id'])
        self.assertEqual(tier.name, data['name'])
        self.assertEqual(tier.price, data['price'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Tier Edited Successfully.')


class TestSubscription(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.client = Client()
        staff_user = User.objects.create(username='staffuser')
        cls.creator_user1 = User.objects.create(
            username='testcreator1', password='password')
        cls.creator_user2 = User.objects.create(
            username='testcreator2', password='password')
        cls.user1 = User.objects.create(
            username='test_user', password='password')
        cls.creator1_obj = CreatorProfile.objects.create(
            user=cls.creator_user1, patron_title='testpatron1', about='test', creator_category='musician')
        cls.creator2_obj = CreatorProfile.objects.create(
            user=cls.creator_user2, patron_title='testpatron2', about='test', creator_category='musician')
        Tier().create_default_tiers(cls.creator1_obj)  # creator 1 tiers
        Tier().create_default_tiers(cls.creator2_obj)  # creator 2 tiers
        cls.tiers_1 = Tier.objects.filter(creator=cls.creator1_obj).values()
        cls.tiers_2 = Tier.objects.filter(creator=cls.creator2_obj).values()

    @classmethod
    def tearDownClass(cls):
        # Delete created objects in reverse order of creation
        for tier in cls.tiers_1:
            Tier.objects.get(id=tier['id']).delete()
        for tier in cls.tiers_2:
            Tier.objects.get(id=tier['id']).delete()
        cls.creator2_obj.delete()
        cls.creator1_obj.delete()
        cls.user1.delete()
        cls.creator_user2.delete()
        cls.creator_user1.delete()
        cls.client.logout()  # Logout if client was used for authenticated requests

    def test_join_view_valid(self):
        self.client.force_login(self.user1)
        url = reverse('patron:join_tier', kwargs={
                      'tier_id': self.tiers_1[0]['id']})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Welcome! You Joined my Onetime patrons.")
        self.assertEqual(TierSubscriptions.objects.count(), 1)

    def test_get_creator_patrons(self):
        self.client.force_login(self.creator_user1)
        user1 = User.objects.create(
            username='testuser1', password='password')
        user2 = User.objects.create(
            username='testuser_2', password='password')
        user3 = User.objects.create(
            username='testuser3', password='password')
        user4 = User.objects.create(
            username='testuser4', password='password')
        user5 = User.objects.create(
            username='testuser_5', password='password')
        tier1 = Tier.objects.get(pk=self.tiers_1[1]['id'])
        tier2 = Tier.objects.get(pk=self.tiers_1[2]['id'])
        tier3 = Tier.objects.get(pk=self.tiers_2[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)
        TierSubscriptions.objects.create(patron=user2, tier=tier1)
        TierSubscriptions.objects.create(patron=user3, tier=tier2)
        TierSubscriptions.objects.create(patron=user4, tier=tier3)
        TierSubscriptions.objects.create(patron=user5, tier=tier2)
        response = self.client.get(reverse('patron:patrons'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('patron/admin/pages/patrons.html')
        self.assertEqual(TierSubscriptions.objects.count(), 5)

    def test_get_creator_home(self):
        self.client.force_login(self.user1)
        url = reverse('patron:creator_home', kwargs={
                      'creator': self.creator1_obj})
        user1 = User.objects.create(
            username='testuser6', password='password')
        tier1 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        TierSubscriptions.objects.create(patron=self.user1, tier=tier1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch('patron.views.query_collection')
    def test_post_make_payment_valid(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': 'request accepted, wait for client approval'}
        mock_response.status_code = 202
        mock_post.return_value = mock_response

        user1 = User.objects.create(
            username='testuser7', password='password')
        self.client.force_login(user1)
        tier1 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)

        url = reverse('patron:make_payment', kwargs={'tier_id': tier1.id})
        data = {'amount': '100', 'payer_account_number': '0966443322',
                'payment_method': 'mtn', 'description': 'testdescription'}
        
        # data = json.dumps(data)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Paid ZMW 100 successfully!')
        self.assertEqual(Payments.objects.count(), 1)

    @patch('patron.views.query_collection')
    def test_get_make_payment_valid(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        user1 = User.objects.create(
            username='testuser8', password='password')
        self.client.force_login(user1)
        tier1 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)
        data = {'amount': '100', 'payer_account_number': '0966443322',
                'payment_method': 'mtn', 'description': 'testdescription'}

        url = reverse('patron:make_payment', kwargs={'tier_id': tier1.id})
        self.client.post(url, data=data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('lipila/actions/deposit.html')

    @patch('patron.views.query_collection')
    def test_post_contribute_valid(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': 'request accepted, wait for client approval'}
        mock_response.status_code = 202
        mock_post.return_value = mock_response
        user1 = User.objects.create(
            username='testuser5', password='password')
        self.client.force_login(user1)
        url = reverse('patron:contribute', kwargs={
                      'tier_id': self.creator1_obj.pk})
        data = {'amount': '100', 'payer_account_number': '0966443322',
                'payment_method': 'mtn', 'description': 'testdescription'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Payment of K100 successfull!')
        self.assertEqual(Contributions.objects.count(), 1)
        conts = Contributions.objects.filter(patron=user1)

    def test_get_contribute(self):
        self.client.force_login(self.user1)
        url = reverse('patron:contribute', kwargs={
                      'tier_id': self.creator1_obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('lipila/actions/contribute.html')

    def test_get_payment_history(self):
        user1 = User.objects.create(
            username='testuser9', password='password')
        self.client.force_login(user1)
        tier1 = Tier.objects.get(pk=self.tiers_1[0]['id'])
        TierSubscriptions.objects.create(patron=user1, tier=tier1)
        url = reverse('patron:subscriptions_history')
        self.client.get(reverse('patron:make_payment',
                        kwargs={'tier_id': tier1.id}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('patron/admin/pages/payments_made.html')


class TestPatronViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.client = Client()
        cls.creatoruser1 = User.objects.create(
            username='testuser_1', password='password')
        cls.user2 = User.objects.create(
            username='testuser2', password='password')
    
    @classmethod
    def tearDownClass(cls):
        cls.user2.delete()
        cls.creatoruser1.delete()


    def test_choose_profile_type(self):
        url = "patron:choose_profile_type"
        creator_data = {'profile_type': 'creator'}
        patron_data = {'profile_type': 'patron'}
        self.client.force_login(self.creatoruser1)
        response = self.client.post(reverse(url), creator_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/patron/accounts/profile/create/creator")
        response = self.client.post(reverse(url), patron_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/patron/accounts/profile/create/patron")

    def test_redirect_unauthenticated_user(self):
        """
        Test that an unathenticated user is redirected to the login page.
        """
        response = self.client.get(reverse('patron:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/patron/accounts/profile/")

    def test_get_profile(self):
        """
        Test that a user is redirected to choose a profile type
        view, if they don't have one.
        """
        self.client.force_login(self.creatoruser1)
        response = self.client.get(reverse('patron:profile'))
        self.assertEqual(response.status_code, 200)
        

    def test_create_patron_profile(self):
        """
        Test the creation of a new user.patron_profile
        """
        self.client.force_login(self.creatoruser1)
        account_number = '77477838'
        city = 'Kitwe'
        data = {'account_number': account_number, 'city': city}
        response = self.client.post(reverse('patron:create_patron_profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/patron/accounts/profile/")
        self.assertEqual(PatronProfile.objects.count(), 1)
        patron = PatronProfile.objects.get(user=self.creatoruser1)
        self.assertEqual(patron.account_number, '77477838')
        res = self.client.get(reverse('patron:profile'))
        self.assertEqual(res.status_code, 200)

    def test_create_creator_profile(self):
        """
        Test the creation of a new user.creator_profile
        """
        self.client.force_login(self.creatoruser1)
        data = {
            'patron_title': 'TestPatron',
            'about': 'test user about',
            'creator_category': 'artist',
        }
        response = self.client.post(reverse('patron:create_creator_profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/patron/accounts/profile/")
        self.assertEqual(CreatorProfile.objects.count(), 1)
        creator = CreatorProfile.objects.get(user=self.creatoruser1)
        self.assertEqual(creator.patron_title, 'TestPatron')
        res = self.client.get(reverse('patron:profile'))
        self.assertEqual(res.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Your profile data has been saved.")

    def test_create_default_tiers(self):
        """
        Test the creation of a default creator tiers.
        """
        self.client.force_login(self.creatoruser1)
        data = {
            'patron_title': 'TestPatron',
            'about': 'test user about',
            'creator_category': 'artist',
        }
        # create a creator profile
        self.client.post(reverse('patron:create_creator_profile'), data)
        creator = CreatorProfile.objects.get(user=self.creatoruser1)
        # query the view_tiers view
        response = self.client.get(reverse('patron:tiers'))
        # get tiers
        tiers = Tier.objects.filter(creator=creator).values()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("patron/admin/pages/view_tiers.html")
        self.assertIn({"name": "Onetime"}, tiers.values('name'))
        self.assertIn({"name": "Fan"}, tiers.values('name'))
        self.assertIn({"name": "Superfan"}, tiers.values('name'))
        self.assertEqual(tiers.count(), 3)
        self.assertEqual(tiers[0]['name'], 'Onetime')
        self.assertEqual(tiers[1]['name'], 'Fan')
        self.assertEqual(tiers[2]['name'], 'Superfan')
        self.assertEqual(tiers[0]['price'], 100)
        self.assertEqual(tiers[1]['price'], 25)
        self.assertEqual(tiers[2]['price'], 50)
        desc = {
            "one": "Make a one-time Contribution to support the creator's work.",
            "two": "Support the creator and get access to exclusive content.",
            "three": "Enjoy additional perks and behind-the-scenes content."
        }
        self.assertEqual(tiers[0]['description'], desc['one'])
        self.assertEqual(tiers[1]['description'], desc['two'])
        self.assertEqual(tiers[2]['description'], desc['three'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), "Default tiers created. Please edit them.")

        response = self.client.get(reverse('patron:tiers'))
        messages = list(get_messages(response.wsgi_request))
        self.assertNotIn("Default tiers created. Please edit them.", messages)

    def test_create_default_tiers_different_user_tier_exists(self):
        """
        Test the creation of a default creator tiers.
        """
        data = {
            'patron_title': 'TestPatron',
            'about': 'test user about',
            'creator_category': 'artist',
        }

        creator1 = CreatorProfile.objects.create(
            user=self.creatoruser1, patron_title='testpatron', about='test', creator_category='musician')
        Tier().create_default_tiers(creator1)
        # login user 2 and create tiers
        self.client.force_login(self.user2)
        self.client.post(reverse('patron:create_creator_profile'), data)
        creator2 = CreatorProfile.objects.get(user=self.user2)
        response = self.client.get(reverse('patron:tiers'))
        # get tiers
        tiers = Tier.objects.filter(creator=creator2).values()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("patron/admin/pages/view_tiers.html")
        desc = {
            "one": "Make a one-time Contribution to support the creator's work.",
            "two": "Support the creator and get access to exclusive content.",
            "three": "Enjoy additional perks and behind-the-scenes content."
        }
        self.assertEqual(tiers[0]['description'], desc['one'])
        self.assertEqual(tiers[1]['description'], desc['two'])
        self.assertEqual(tiers[2]['description'], desc['three'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), "Default tiers created. Please edit them.")


class TestCreateDefaultTiers(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.client = Client()
        user1 = User.objects.create(
            username='testuser', password='password')
        user2 = User.objects.create(
            username='test_user_2', password='password')
        cls.user3 = User.objects.create(
            username='test_user_3', password='password')
        creator1 = CreatorProfile.objects.create(
            user=user1, patron_title='test_patron', about='test', creator_category='musician')
        creator2 = CreatorProfile.objects.create(
            user=user2, patron_title='testpatron3', about='test', creator_category='musician')
        Tier().create_default_tiers(creator1)
        Tier().create_default_tiers(creator2)

    
    def test_create_default_tiers_multiple_users_tiers_exists(self):
        """
        Test the creation of a default creator tiers.
        """
        data = {
            'patron_title': 'TestPatron3',
            'about': 'test user about',
            'creator_category': 'artist',
        }

        # login user 2 and create tiers
        self.client.force_login(self.user3)
        self.client.post(reverse('patron:create_creator_profile'), data)
        creator2 = CreatorProfile.objects.get(user=self.user3)
        response = self.client.get(reverse('patron:tiers'))
        # get tiers
        tiers = Tier.objects.filter(creator=creator2).values()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("patron/admin/pages/view_tiers.html")
        desc = {
            "one": "Make a one-time Contribution to support the creator's work.",
            "two": "Support the creator and get access to exclusive content.",
            "three": "Enjoy additional perks and behind-the-scenes content."
        }
        self.assertEqual(tiers[0]['description'], desc['one'])
        self.assertEqual(tiers[1]['description'], desc['two'])
        self.assertEqual(tiers[2]['description'], desc['three'])
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[1]), "Default tiers created. Please edit them.")
