"""
Tests the mtn momo API
"""
from django.test import TestCase, Client
from api.momo.mtn import Collections, Disbursement
from api.utils import generate_reference_id
from lipila.utils import check_payment_status


class MTNBaseTestCase(TestCase):
    """ Tests inheritance """

    def setUp(self):
        self.ref = generate_reference_id()
        self.col_mtn = Collections()
        self.dis_mtn = Disbursement()

    def test_collections_inheritance(self):
        self.assertTrue(self.col_mtn.x_target_environment, 'sandbox')
        self.assertTrue(len(self.col_mtn.subscription_col_key), 32)
        self.assertEqual(self.col_mtn.content_type, 'application/json')
       
    def test_disbursement_inheritance(self):
        self.assertTrue(self.dis_mtn.x_target_environment, 'sandbox')
        self.assertTrue(len(self.dis_mtn.subscription_dis_key), 32)
        self.assertEqual(self.dis_mtn.content_type, 'application/json')
       

    def test_sandbox_provisioning_collection(self):
        self.assertEqual(self.col_mtn.api_key, '')
        self.assertEqual(self.col_mtn.api_token, 'Bearer ')
        ref_id = self.col_mtn.provision_sandbox(
            self.col_mtn.subscription_col_key, self.ref)
        self.assertEqual(ref_id.status_code, 201)  # 3 assert methods success
        self.assertNotEqual(ref_id, '')
        self.assertNotEqual(ref_id, 'Bearer ')
        token = self.col_mtn.create_api_token(
            self.col_mtn.subscription_col_key, 'collection', self.ref)
        self.assertEqual(token.status_code, 200)

    def test_sandbox_provisioning_disbursement(self):
        self.assertEqual(self.dis_mtn.api_key, '')
        self.assertEqual(self.dis_mtn.api_token, 'Bearer ')
        ref_id = self.dis_mtn.provision_sandbox(
            self.dis_mtn.subscription_dis_key, self.ref)
        self.assertEqual(ref_id.status_code, 201)  # 3 assert methods success
        self.assertNotEqual(ref_id, '')
        self.assertNotEqual(ref_id, 'Bearer ')
        token = self.dis_mtn.create_api_token(
            self.dis_mtn.subscription_dis_key, 'disbursement', self.ref)
        self.assertEqual(token.status_code, 200)


class MTNCollectionsTestCase(TestCase):
    """Test MTN Collections methods"""
    
    def setUp(self):
        # Create a first momo collection user instance
        self.momo1 = Collections()
        self.ref = generate_reference_id()
        self.api_user = self.momo1.create_api_user(
            self.momo1.subscription_col_key, self.ref)
        self.api_key = self.momo1.create_api_key(
            self.momo1.subscription_col_key, self.ref)
        self.api_token = self.momo1.create_api_token(
            self.momo1.subscription_col_key, 'collection', self.ref)

    def test_x_reference_id(self):
        """ Test the x_reference id creation"""
        self.assertEqual(type(self.ref), str)

    def test_api_user(self):
        """ Test Sandbox user creation"""
        self.assertEqual(self.api_user.status_code, 201)

    def test_api_key(self):
        """Tesk Api key creation"""
        self.assertEqual(self.api_key.status_code, 201)

    def test_api_token(self):
        """ Test API access token creation"""
        self.assertEqual(self.api_token.status_code, 200)

    def test_request_to_pay_accepted(self):
        """Returns 202 accepted status"""
        momo2 = Collections()
        ref = generate_reference_id()
        api_user = momo2.create_api_user(
            momo2.subscription_col_key, ref)
        api_key = momo2.create_api_key(
            momo2.subscription_col_key, ref)
        api_token = momo2.create_api_token(
            momo2.subscription_col_key, 'collection', ref)
        payment = self.momo1.request_to_pay('2456', '0969620939', ref)
        self.assertEqual(payment.status_code, 202)
        self.assertEqual(payment.data['message'], 'pending')
        # duplicate request to pay
        payment = self.momo1.request_to_pay('56', '0969610939', ref)
        self.assertEqual(payment.status_code, 409)
        self.assertEqual(payment.data['reason'], 'Conflict user exists')
        # new collection object request
        payment = momo2.request_to_pay('56', '0969610939', self.ref)
        self.assertEqual(payment.status_code, 202)
        self.assertEqual(payment.data['message'], 'pending')       

    def test_request_to_pay_bad_request(self):
        """Returns 400 Bad Request status"""
        with self.assertRaises(ValueError) as rtp:
            self.momo1.request_to_pay('6', '0969620939', 'myrefre')
        self.assertEqual(str(
            rtp.exception), 'Amount must be greater than 10 and payer must be 10 digits long.')

        with self.assertRaises(ValueError) as rtp:
            payment = self.momo1.request_to_pay('2456', '9620939', 'myrefre')
        self.assertEqual(str(
            rtp.exception), 'Amount must be greater than 10 and payer must be 10 digits long.')
        # reference should not have spaces
        with self.assertRaises(ValueError) as rtp:
            payment = self.momo1.request_to_pay(
                '2456', '9620939545', 'my refre')
        self.assertEqual(str(rtp.exception),
                         "Reference should not contain spaces.")

    def test_get_payment_status_completed(self):
        """Returns a 200 OK status"""
        payment = self.momo1.request_to_pay('2456', '0969620939', self.ref)
        get_payment_status = self.momo1.get_payment_status(self.ref)
        # assert completed successfully ok
        self.assertEqual(get_payment_status.status_code, 200)

    def test_get_payment_status_bad_request(self):
        """Returns a 400 Bad Request status"""
        get_payment_status = self.momo1.get_payment_status(
            '8647749439037hhfkgsdhfkla67e839')
        # assert completed successfully with error
        self.assertEqual(get_payment_status.data['reason'], 'Bad Request')
        self.assertEqual(get_payment_status.status_code, 400)

    def test_get_payment_status_404(self):
        """Returns a 404 user not found status code"""
        momo2 = Collections()
        get_payment_status = self.momo1.get_payment_status(
            self.ref)
        self.assertEqual(get_payment_status.status_code, 404)
        self.assertEqual(get_payment_status.data['reason'], 'Not Found')

    def test_validate_collection_account_holder(self):
        """validate collections account"""
        check_account_status = self.momo1.validate_account_holder(
            self.momo1.subscription_col_key, 'msisdn', '0965766634', 'collection')
        self.assertEqual(check_account_status.status_code,
                         200)  # assert successful

    def test_raise_value_errors(self):
        """ Test the length of PartyId"""
        self.assertRaises(ValueError,
                          self.momo1.request_to_pay,
                          '36654', '096962', '56797356')
        self.assertRaises(ValueError,
                          self.momo1.request_to_pay,
                          '36654', '0969620978895774', '56797356')
        self.assertRaises(ValueError,
                          self.momo1.request_to_pay,
                          '5', '0969620978', '56797356')

    def test_raise_type_errors(self):
        """Test the type of paramateres"""
        self.assertRaises(TypeError,
                          self.momo1.request_to_pay,
                          12345, '0969620939', '56797356')
        self.assertRaises(TypeError,
                          self.momo1.request_to_pay,
                          '12345', 969620939, '56797356')
        self.assertRaises(TypeError,
                          self.momo1.request_to_pay,
                          '12345', '0969620939', 56797356)


class MTNDisbursementTestCase(TestCase):
    """Test MTN Disbursement methods"""

    def setUp(self):
        self.momo1 = Disbursement()
        self.ref = generate_reference_id()
        self.api_user = self.momo1.create_api_user(
            self.momo1.subscription_dis_key, self.ref)
        self.api_key = self.momo1.create_api_key(
            self.momo1.subscription_dis_key, self.ref)
        self.api_token = self.momo1.create_api_token(
            self.momo1.subscription_dis_key, 'disbursement', self.ref)
        self.deposit = self.momo1.deposit('3665', '0969620939', self.ref)

    def test_api_user(self):
        """ Test Sandbox user creation"""
        self.assertEqual(self.api_user.status_code, 201)

    def test_api_key(self):
        """Tesk Api key creaStion"""
        self.assertEqual(self.api_key.status_code, 201)

    def test_api_token(self):
        """ Test API access token creation"""
        self.assertEqual(self.api_token.status_code, 200)

    def test_validate_disbursement_account_holder(self):
        """validate disbursement account"""
        check_account_status = self.momo1.validate_account_holder(
            self.momo1.subscription_dis_key, 'msisdn', '0966776644', 'disbursement')
        self.assertEqual(check_account_status.status_code,
                         200)  # assert successful

    def test_deposit_accepted(self):
        """Test the deposit method"""
        self.assertEqual(self.deposit.status_code,
                         202)  # assert successful accepted

    def test_get_deposit_status_completed(self):
        """Test get transfer status method"""
        get_deposit_status = self.momo1.get_transaction_status(
            'deposit', self.ref)  # check the payment status
        # assert completed successfully
        self.assertEqual(get_deposit_status.status_code, 200)

    def test_raise_value_errors(self):
        """ Test the length of PartyId"""
        self.assertRaises(ValueError,
                          self.momo1.deposit,
                          '36654', '096962', '56797356')
        self.assertRaises(ValueError,
                          self.momo1.deposit,
                          '36654', '0969620978895774', '56797356')
        self.assertRaises(ValueError,
                          self.momo1.deposit,
                          '5', '0969620978', '56797356')

    def test_raise_type_errors(self):
        """Test the type of paramateres"""
        self.assertRaises(TypeError,
                          self.momo1.deposit,
                          12345, '0969620939', '56797356')
        self.assertRaises(TypeError,
                          self.momo1.deposit,
                          '12345', 969620939, '56797356')
        self.assertRaises(TypeError,
                          self.momo1.deposit,
                          '12345', '0969620939', 56797356)
