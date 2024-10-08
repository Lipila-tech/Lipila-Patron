from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse, reverse_lazy
from ..base import FunctionalTest
from django.conf import settings
from django.test import override_settings
from django.contrib.auth.hashers import make_password
from unittest.mock import Mock, patch
from accounts.models import CreatorProfile
from patron.models import WithdrawalRequest, Tier, TierSubscriptions
from django.contrib.auth import get_user_model


class SubscriptionPaymentTest(FunctionalTest):
    @override_settings(DEBUG=True)
    def setUp(self):
        super().setUp()
        # Create a super user default api-user
        super_user = get_user_model().objects.create_user(
            username='staff', email='test@bot.io', password='testpassword', is_superuser=True, is_staff=True)

        # create patron user
        self.user1 = get_user_model().objects.create_user(
            username='testpatron', email='test3@bot.io', password='testpassword')

        # create a user with a creatorprofile
        self.user2 = get_user_model().objects.create_user(
            username='testcreator', email='test6@bot.io', password='testpassword')
        self.creator_user = CreatorProfile.objects.create(
            user=self.user2, patron_title='testpatron1', about='test', creator_category='musician')

        # create tier and subscriptions
        Tier().create_default_tiers(self.creator_user)  # creator 2 tiers
        self.tiers = Tier.objects.filter(creator=self.creator_user).values()
        tier1 = Tier.objects.get(pk=self.tiers[1]['id'])
        TierSubscriptions.objects.create(patron=self.user1, tier=tier1)

        self.base_url = self.live_server_url
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testpatron')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='signin']")
        login_button.click()

    @override_settings(DEBUG=True)
    @patch('lipila.views.query_collection')
    @patch('lipila.views.check_payment_status')
    def test_pay_subscription_mtn(self, mock_status, mock_post):
        """User selects MTN"""
        mock_response = Mock()
        mock_status.return_value = 'success'
        mock_response.json.return_value = {
            'data': 'request accepted, wait for client approval'}
        mock_response.status_code = 202
        mock_post.return_value = mock_response

        url = self.base_url + '/patron/home/testcreator'
        self.BROWSER.get(url)

        # Wait for the element to be present and visible
        wait = WebDriverWait(self.BROWSER, 10)
        link = self.BROWSER.find_element(By.CLASS_NAME, 'read-tier')

        # Scroll the element into view using JavaScript
        self.BROWSER.execute_script("arguments[0].scrollIntoView(true);", link)

        # Alternatively, you can use ActionChains to scroll and click
        actions = ActionChains(self.BROWSER)
        actions.move_to_element(link).click().perform()

        pay_button = self.wait_for(element_id='send-money')
        pay_button.click()

        modal = self.wait_for(element_id='modal')
        form = modal.find_element(By.TAG_NAME, 'form')

        amount_field = form.find_element(By.ID, 'id_amount')
        msisdn_field = form.find_element(
            By.ID, 'id_msisdn')
        description_field = form.find_element(By.ID, 'id_description')
        wallet_type_field = form.find_element(By.ID, 'id_wallet_type')

        amount_field.send_keys('122')
        msisdn_field.send_keys('0966774433')
        description_field.send_keys('test descriptions')
        wallet_type_field.send_keys('mtn')
        form.submit()

        success_msg = self.wait_for(class_name='alert').text
        self.assertEqual(f"Payment of K122 successful!", success_msg)
        redirect_url = self.BROWSER.current_url
        self.assertRegex(redirect_url, '/patron/history/contribute/')


class ContributionModalTest(FunctionalTest):
    @override_settings(DEBUG=True)
    def setUp(self):
        super().setUp()
        # Create a creator user and a withdrawal request
        super_user = get_user_model().objects.create_user(
            username='staff', email='test@bot1.io', password='testpassword', is_superuser=True, is_staff=True)
        self.user1 = get_user_model().objects.create_user(
            username='testpatron', email='test@bot2.io', password='testpassword')
        self.user2 = get_user_model().objects.create_user(
            username='testcreator', email='test@bot4.io', password='testpassword')
        self.creator_user = CreatorProfile.objects.create(
            user=self.user2, patron_title='testpatron1', about='test', creator_category='musician')

        self.base_url = self.live_server_url
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testpatron')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='signin']")
        login_button.click()

    @override_settings(DEBUG=True)
    def test_create_contribution_airtel(self):
        """
        User selects AIRTEL
        """
        url = self.base_url + '/patron/home/testcreator'
        self.BROWSER.get(url)

        # User sees the creators home page
        header_text = self.BROWSER.find_elements(By.TAG_NAME, 'h3')

        # User opens payment form
        WebDriverWait(self.BROWSER, 10).until(EC.element_to_be_clickable(
            (By.ID, "send-contribution"))).click()
        # pay_button = self.wait_for(element_id='send-contribution')
        # pay_button.click()

        modal = self.wait_for(element_id='modal')
        form = modal.find_element(By.TAG_NAME, 'form')

        amount_field = form.find_element(By.ID, 'id_amount')
        msisdn_field = form.find_element(
            By.ID, 'id_msisdn')
        description_field = form.find_element(By.ID, 'id_description')
        wallet_type_field = form.find_element(By.ID, 'id_wallet_type')

        amount_field.send_keys('122')
        msisdn_field.send_keys('0966774433')
        description_field.send_keys('test descriptions')
        wallet_type_field.send_keys('airtel')
        form.submit()

        failure_msg = self.wait_for(class_name='message').text[:-2]
        self.assertEqual(
            'Sorry only mtn is suported at the moment', failure_msg)
        redirect_url = self.BROWSER.current_url
        self.assertRegex(redirect_url, '/patron/home/testcreator')

    @ override_settings(DEBUG=True)
    @ patch('lipila.views.query_collection')
    @ patch('lipila.views.check_payment_status')
    def test_create_contribution_mtn(self, mock_status, mock_post):
        """User selects MTN"""
        mock_response = Mock()
        mock_status.return_value = 'success'
        mock_response.json.return_value = {
            'data': 'request accepted, wait for client approval'}
        mock_response.status_code = 202
        mock_post.return_value = mock_response

        url = self.base_url + '/patron/home/testcreator'
        self.BROWSER.get(url)
        pay_button = self.BROWSER.find_element(By.ID, 'send-contribution')
        pay_button.click()

        modal = self.wait_for(element_id='modal')
        form = modal.find_element(By.TAG_NAME, 'form')

        amount_field = form.find_element(By.ID, 'id_amount')
        msisdn_field = form.find_element(
            By.ID, 'id_msisdn')
        description_field = form.find_element(By.ID, 'id_description')
        wallet_type_field = form.find_element(By.ID, 'id_wallet_type')

        amount_field.send_keys('122')
        msisdn_field.send_keys('0966774433')
        description_field.send_keys('test descriptions')
        wallet_type_field.send_keys('mtn')
        form.submit()

        success_msg = self.wait_for(class_name='alert').text
        self.assertEqual(f"Payment of K122 successful!", success_msg)
        redirect_url = self.BROWSER.current_url
        self.assertRegex(redirect_url, '/patron/history/contribute/')

        # User sees created contribtion in table
        table_entries = self.wait_for_table_rows()
        self.assertEqual(len(table_entries), 1)

        # Check content of second table entry
        self.check_table_row(
            table_entries[1],
            7,
            ['Life of Jane Doe', 'Jane Doe', 'Hardcover',
                'Jan. 1, 2019', '464', '21.00', None],
        )


class GetHomePageTest(FunctionalTest):
    def test_get_index(self):
        url = self.live_server_url
        self.BROWSER.get(url)
        self.assertIn('Lipila-Home', self.BROWSER.title)


class ApproveWithdrawalTest(FunctionalTest):
    @ override_settings(DEBUG=True)
    def setUp(self):
        super().setUp()
        # Create a creator user and a withdrawal request
        self.user1 = get_user_model().objects.create_user(
            username='testuser', email='tes2t@bot.io', password='testpassword', is_staff=True)
        self.user2 = get_user_model().objects.create_user(
            username='testcreator', email='te1st@bot.io', password='testpassword')
        self.creator_user = CreatorProfile.objects.create(
            user=self.user2, patron_title='testpatron1', about='test', creator_category='musician')
        self.withdrawal_request = WithdrawalRequest.objects.create(
            creator=self.creator_user,
            amount=100.00,
            account_number='0966445333',
        )
        self.base_url = self.live_server_url
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testuser')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='signin']")
        login_button.click()

    @ override_settings(DEBUG=True)
    def test_approve_withdraw_modal_cancel_btn(self):
        url = f'{self.base_url}/approve_withdrawals/'
        self.BROWSER.get(url)

        self.assertIn('Pending Withdrawals', self.BROWSER.title)
        header_text = self.BROWSER.find_element(By.TAG_NAME, 'h2').text
        self.assertIn('Approve Withdrawal Requests', header_text)

        # User clicks the approve button
        self.BROWSER.find_element(By.CLASS_NAME, 'approve-request').click()

        # Confirmation modal opens
        modal = self.wait_for(element_id='confirmationModal')
        self.BROWSER.find_element(By.ID, 'cancel').click()


class RejectWithdrawalTest(FunctionalTest):
    @ override_settings(DEBUG=True)
    def setUp(self):
        super().setUp()
        # Create a creator user and a withdrawal request
        self.user1 = get_user_model().objects.create_user(
            username='testuser', email='te89st@bot.io', password='testpassword', is_staff=True)
        self.user2 = get_user_model().objects.create_user(
            username='testcreator', email='te34st@bot.io', password='testpassword')
        self.creator_user = CreatorProfile.objects.create(
            user=self.user2, patron_title='testpatron1', about='test', creator_category='musician')
        self.withdrawal_request = WithdrawalRequest.objects.create(
            creator=self.creator_user,
            amount=100.00,
            account_number='0966445333',
        )
        self.base_url = self.live_server_url
        # login user
        self.BROWSER.get(f'{self.base_url}/accounts/login/')
        username_field = self.BROWSER.find_element(By.ID, 'id_username')
        password_field = self.BROWSER.find_element(By.ID, 'id_password')
        username_field.send_keys('testuser')
        password_field.send_keys('testpassword')
        login_button = self.BROWSER.find_element(
            By.CSS_SELECTOR, "input[type='submit'][value='signin']")
        login_button.click()

    @ override_settings(DEBUG=True)
    def test_reject_withdraw_modal_cnacel_btn(self):
        url = f'{self.base_url}/approve_withdrawals/'
        self.BROWSER.get(url)

        self.assertIn('Pending Withdrawals', self.BROWSER.title)
        header_text = self.BROWSER.find_element(By.TAG_NAME, 'h2').text
        self.assertIn('Approve Withdrawal Requests', header_text)

        # User clicks the approve button
        self.BROWSER.find_element(By.CLASS_NAME, 'reject-request').click()
        modal = self.wait_for(element_id='confirmationModal')
        self.BROWSER.find_element(By.ID, 'cancel').click()
