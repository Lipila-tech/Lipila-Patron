# coding: utf-8

"""
    Payments V1

    To facilitate the capability for consumers to make a payment or refund to service providers.

    The version of the OpenAPI document: v1.0
    Contact: developer-support@mtn.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.feecheck_request import FeecheckRequest

class TestFeecheckRequest(unittest.TestCase):
    """FeecheckRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> FeecheckRequest:
        """Test FeecheckRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `FeecheckRequest`
        """
        model = FeecheckRequest()
        if include_optional:
            return FeecheckRequest(
                correlator_id = 'c5f80cb8-dc8b-11ea-87d0-0242ac130003',
                payment_date = '2020-08-12T11:04:53.668Z',
                name = 'Manual Boost for RWC',
                calling_system = 'AYOBA',
                transaction_type = 'FeeCheck',
                target_system = 'ECW',
                callback_url = 'https://api.mtn.com/v1/callback',
                quote_id = '9223372036854775807',
                channel = 'AIRTIME',
                description = 'Manual Boost for RW',
                authorization_code = '',
                fee_bearer = 'Payer',
                amount = openapi_client.models.fee_money_type.FeeMoneyType(
                    amount = 50.0, 
                    units = 'SWZ', ),
                tax_amount = openapi_client.models.fee_money_type.FeeMoneyType(
                    amount = 50.0, 
                    units = 'SWZ', ),
                total_amount = openapi_client.models.fee_money_type.FeeMoneyType(
                    amount = 50.0, 
                    units = 'SWZ', ),
                payer = openapi_client.models.payer.Payer(
                    payer_id_type = 'MSISDN', 
                    payer_id = '233364654737', 
                    payer_note = 'Manual Boost for RWC', 
                    payer_name = '', 
                    payer_email = '', 
                    payer_ref = '233364654737', 
                    payer_surname = 'Orimoloye', 
                    include_payer_charges = False, ),
                payee = [
                    openapi_client.models.payee.Payee(
                        amount = openapi_client.models.money_type.MoneyType(
                            amount = 50.0, 
                            units = 'XOF', ), 
                        tax_amount = openapi_client.models.money_type.MoneyType(
                            amount = 50.0, 
                            units = 'XOF', ), 
                        total_amount = , 
                        payee_id_type = 'USER', 
                        payee_id = 'AYO.DEPOSIT', 
                        payee_note = 'Manual Boost for RWC', 
                        payee_name = '', )
                    ],
                payment_method = openapi_client.models.payment_method.PaymentMethod(
                    name = 'Manual Boost for RWC', 
                    description = 'Manual Boost for RWC', 
                    valid_from = '2021-07-21T17:32:28Z', 
                    valid_to = '2021-07-21T17:32:28Z', 
                    type = 'BankCard', 
                    details = openapi_client.models.payment_method_type_details.PaymentMethodTypeDetails(
                        bank_card = openapi_client.models.bank_card.BankCard(
                            brand = 'Visa', 
                            card_number = 'xxxx xxxx xxx xxx', 
                            expiration_date = '2021-07-21T17:32:28Z', 
                            cvv = '123', 
                            last_four_digits = '1234', 
                            name_on_card = 'Bruce Wayne', 
                            bank = 'Bank of Gotham', 
                            pin = '123', ), 
                        tokenized_card = openapi_client.models.tokenized_card.TokenizedCard(
                            brand = '', 
                            last_four_digits = '', 
                            token_type = '', 
                            token = '', 
                            issuer = '', ), 
                        bank_account_debit = openapi_client.models.bank_account_debit.BankAccountDebit(
                            account_number = '', 
                            account_number_type = '', 
                            bic = '', 
                            owner = '', 
                            bank = '', ), 
                        bank_account_transfer = openapi_client.models.bank_account_transfer.BankAccountTransfer(
                            account_number = '', 
                            account_number_type = '', 
                            bic = '', 
                            owner = '', 
                            bank = '', ), 
                        account = openapi_client.models.account.Account(
                            id = '', 
                            name = '', 
                            description = '', ), 
                        loyalty_account = openapi_client.models.loyalty_account.LoyaltyAccount(
                            id = '', 
                            name = '', 
                            description = '', ), 
                        bucket = openapi_client.models.bucket.Bucket(
                            id = '', 
                            name = '', 
                            description = '', ), 
                        voucher = openapi_client.models.voucher.Voucher(
                            code = '', 
                            description = '', 
                            value = '', 
                            expiration_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            campaign = '', ), 
                        digital_wallet = openapi_client.models.digital_wallet.DigitalWallet(
                            service = 'MoMo', 
                            wallet_id = '233364654737', 
                            wallet_uri = 'https://paypal.me/johndoe', ), 
                        invoice = openapi_client.models.invoice_method.InvoiceMethod(
                            id = '86rer4478878t991', 
                            frequency = 'on_call', 
                            start_date = '2021-03-20', 
                            end_date = '2021-09-20', 
                            retry_on_fail = True, 
                            deactivate_on_fail = 'true', 
                            callback_url = 'https://merchant-application-url/webhook-endpoint', 
                            retry_run = '1-5', 
                            retry_frequency = 'once', ), ), ),
                status = 'Pending',
                status_date = '2020-08-12T11:04:53.668Z',
                additional_information = [
                    openapi_client.models.additional_information.AdditionalInformation(
                        name = 'BundleName', 
                        description = 'Voice_1111', )
                    ],
                segment = 'subscriber'
            )
        else:
            return FeecheckRequest(
                correlator_id = 'c5f80cb8-dc8b-11ea-87d0-0242ac130003',
                transaction_type = 'FeeCheck',
                callback_url = 'https://api.mtn.com/v1/callback',
                total_amount = openapi_client.models.fee_money_type.FeeMoneyType(
                    amount = 50.0, 
                    units = 'SWZ', ),
                payment_method = openapi_client.models.payment_method.PaymentMethod(
                    name = 'Manual Boost for RWC', 
                    description = 'Manual Boost for RWC', 
                    valid_from = '2021-07-21T17:32:28Z', 
                    valid_to = '2021-07-21T17:32:28Z', 
                    type = 'BankCard', 
                    details = openapi_client.models.payment_method_type_details.PaymentMethodTypeDetails(
                        bank_card = openapi_client.models.bank_card.BankCard(
                            brand = 'Visa', 
                            card_number = 'xxxx xxxx xxx xxx', 
                            expiration_date = '2021-07-21T17:32:28Z', 
                            cvv = '123', 
                            last_four_digits = '1234', 
                            name_on_card = 'Bruce Wayne', 
                            bank = 'Bank of Gotham', 
                            pin = '123', ), 
                        tokenized_card = openapi_client.models.tokenized_card.TokenizedCard(
                            brand = '', 
                            last_four_digits = '', 
                            token_type = '', 
                            token = '', 
                            issuer = '', ), 
                        bank_account_debit = openapi_client.models.bank_account_debit.BankAccountDebit(
                            account_number = '', 
                            account_number_type = '', 
                            bic = '', 
                            owner = '', 
                            bank = '', ), 
                        bank_account_transfer = openapi_client.models.bank_account_transfer.BankAccountTransfer(
                            account_number = '', 
                            account_number_type = '', 
                            bic = '', 
                            owner = '', 
                            bank = '', ), 
                        account = openapi_client.models.account.Account(
                            id = '', 
                            name = '', 
                            description = '', ), 
                        loyalty_account = openapi_client.models.loyalty_account.LoyaltyAccount(
                            id = '', 
                            name = '', 
                            description = '', ), 
                        bucket = openapi_client.models.bucket.Bucket(
                            id = '', 
                            name = '', 
                            description = '', ), 
                        voucher = openapi_client.models.voucher.Voucher(
                            code = '', 
                            description = '', 
                            value = '', 
                            expiration_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            campaign = '', ), 
                        digital_wallet = openapi_client.models.digital_wallet.DigitalWallet(
                            service = 'MoMo', 
                            wallet_id = '233364654737', 
                            wallet_uri = 'https://paypal.me/johndoe', ), 
                        invoice = openapi_client.models.invoice_method.InvoiceMethod(
                            id = '86rer4478878t991', 
                            frequency = 'on_call', 
                            start_date = '2021-03-20', 
                            end_date = '2021-09-20', 
                            retry_on_fail = True, 
                            deactivate_on_fail = 'true', 
                            callback_url = 'https://merchant-application-url/webhook-endpoint', 
                            retry_run = '1-5', 
                            retry_frequency = 'once', ), ), ),
        )
        """

    def testFeecheckRequest(self):
        """Test FeecheckRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()