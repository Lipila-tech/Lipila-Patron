"""Defines classes and methods that interact with the MTN momo api"""
import requests
import json
from django.conf import settings
from rest_framework.response import Response
from api.utils import (
    generate_transaction_id, basic_auth, 
    is_payment_details_valid, is_deposit_details_valid
    )


class MTNBase():
    """Base class for the mtn api"""

    def __init__(self):
        self.x_target_environment = settings.MTN_TARGET_ENV
        self.content_type = 'application/json'
        self.api_key = ''
        self.api_token = 'Bearer '

    def create_api_user(self, subscription_key: str, transaction_id) -> Response:
        """
        Used to create an API user in the mtn sandbox.

        Args:
            subscription_key(str): MTN developer provided key
            which provides access to the (collections or disbursement) api.

        Returns:
            HTTP Response
        """
        url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"

        payload = json.dumps({
            "providerCallbackHost": "{}".format(settings.CALLBACK_URL_MTN)
        })
        headers = {
            'X-Reference-Id': transaction_id,
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': self.content_type
        }
        try:
            response = requests.request(
                'POST', url, headers=headers, data=payload)
            if response.status_code == 201:
                return response
            elif response.status_code == 400:
                raise ValueError(" Bad request when creating api user")
            elif response.status_code == 409:
                raise ValueError("Conflict user exists")
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)

    def create_api_key(self, subscription_key: str, transaction_id) -> Response:
        """
        Used to create an API key for an API user in the sandbox target environment.

        Args:
            subscription_key(str): MTN developer provided key
            which provides access to the (collections or disbursement) api.

        Returns:
            HTTP Response
        """
        url = f"https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{transaction_id}/apikey"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 201:
                key = response.json()
                self.api_key = self.api_key + key['apiKey']
                return response
            elif response.status_code == 400:
                raise ValueError("Bad request when creating api key")
            elif response.status_code == 404:
                raise ValueError("Not found")
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)

    def provision_sandbox(self, subscription_key: str, transaction_id:str):
        """ creates the api user and api token
        """
        try:
            api_user = self.create_api_user(subscription_key, transaction_id)
            api_key = self.create_api_key(subscription_key, transaction_id)

            if api_user.status_code == 201 and api_key.status_code == 201:
                return api_user
            else:
                raise ValueError("Failed")
        except ValueError:
            return Response(status=api_user.status_code)

    def create_api_token(self, subscription_key: str, endpoint: str, transaction_id)->Response:
        """
        This operation is used to create an access token to the mtn api which can then
        be used to authorize and authenticate towards the other end-points
        of the API.

        Args:
            subscription_key(str): MTN developer provided key
            which provides access to the (collections or disbursement) api.

        Returns:
            HTTP Response
        """
        url = f"https://sandbox.momodeveloper.mtn.com/{endpoint}/token/"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Authorization': basic_auth(transaction_id, self.api_key)
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                token = response.json()
                self.api_token = self.api_token + token['access_token']
                return response
            elif response.status_code == 401:
                raise ValueError("Unauthorized")
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)

    def validate_account_holder(
            self, subscription_key: str,
            accountHolderIdType: str,
            accountHolderId: str,
            endpoint: str
    ):
        """
        Checks if a user account is registered with mtn momo.
        Args:
        subscription_key(str): MTN developer provided key
            which provides access to the (collections or disbursement) api.
        accountHlderIdType(str): The type of account, can be msisdn or email
        accountHolderId(str): The mobile number or email address to validate.
        endpoint(str): The api endpoint either collection or disbursement

        Returns:
            HTTP Reponse.
        """
        url = f"https://sandbox.momodeveloper.mtn.com/{endpoint}/v1_0/accountholder/{accountHolderIdType}/{accountHolderId}/active"
        headers = {
            'X-Target-Environment': self.x_target_environment,
            'Authorization': self.api_token,
            'Ocp-Apim-Subscription-Key': subscription_key,
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise ValueError("Bad request when validating account holder")
            else:
                return response
        except Exception as e:
            return Response(status=response.status_code)


class Collections(MTNBase):
    """
    This class provisions the MTN sandbox collections endpoints.
    """

    def __init__(self):
        super().__init__()
        self.subscription_col_key = settings.MTN_COLLECTIONS_KEY

    def request_to_pay(self, amount: str, payer: str, transaction_id: str) -> Response:
        """
        This method queries the MTN momo request to pay endpoint.

        Args:
            amount(str): The amount to collect from the payer.
            payer(str): The mtn momo registered mobile number.
            transaction_id(str): Unique str formated uuid number to that identitifies the tr
                        transaction.

        Returns:
            A HTTP Response.
        """
        is_valid = is_payment_details_valid(amount, payer, transaction_id)
        
        if is_valid:
            """ Query the Collections API"""
            try:
                url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
                payload = json.dumps({
                    "amount": amount,
                    "currency": 'EUR',
                    "externalId": 'lipilaPatron',
                    "payer": {
                        "partyIdType": "MSISDN",
                        "partyId": payer
                    },
                    "payerMessage": f"send money to {payer}",
                    "payeeNote": "Lipila gateway"
                })
                headers = {
                    'X-Reference-Id': transaction_id,
                    'Ocp-Apim-Subscription-Key': self.subscription_col_key,
                    'X-Target-Environment': self.x_target_environment,
                    'Authorization': self.api_token,
                    'Content-Type': self.content_type
                }
                response = requests.post(url, headers=headers, data=payload)
                if response.status_code == 202:
                    return Response(status=202, data={'message': 'pending'})
                elif response.status_code == 400:
                    return Response(status=400, data={'reason': 'Bad Request to pay'})
                elif response.status_code == 409:
                    return Response(status=409, data={'reason': 'Conflict user exists'})
                elif response.status_code == 500:
                    return Response(status=500, data={'reason': 'mtn server error'})
            except Exception as e:
                return Response(status=500, data={'reason': 'mtn server error'})

    def get_payment_status(self, transaction_id) -> Response:
        """
         Queries the mtn api to get the transaction status.

        Args:
            referenceid(str): The id that was used to make the payment.

        Returns:
            A HTTP response.
        """

        url = f"https://sandbox.momodeveloper.mtn.com/collection/v2_0/payment/{transaction_id}"
        headers = {
            'X-Target-Environment': self.x_target_environment,
            'Ocp-Apim-Subscription-Key': self.subscription_col_key,
            'Authorization': self.api_token
        }
        try:
            response = requests.get(url, headers=headers, data={})
            if response.status_code == 200:
                return response
            elif response.status_code == 400:
                return Response(status=400, data={'reason': 'Bad Request get payment status'})
            elif response.status_code == 404:
                return Response(status=404, data={'reason': 'Not Found'})
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)


class Disbursement(MTNBase):
    """
    This class provisions the MTN sandbox disbursements endpoints.
    """

    def __init__(self):
        super().__init__()
        self.subscription_dis_key = settings.MTN_DISBURSEMENT_KEY

    def deposit(self, amount: str, payee: str, transaction_id: str) -> Response:
        """
        This method queries the MTN momo deposit endpoint.

        Args:
            amount(str): The amount to send to the payer.
            payee(str): The mtn momo registered mobile number.
            transaction_id(str): Unique str formated uuid number to that identitifies the tr
                        transaction.

        Returns:
            A HTTP Response.
        """
        try:
            is_valid = is_deposit_details_valid(amount, payee, transaction_id)
        except (ValueError, TypeError):
            return Response(status=400, data={'reason': 'Bad Request deposit'})
        
        if is_valid:
            """ deposit funds to multiple users"""
            try:
                url = "https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/deposit"
                payload = json.dumps({
                    "amount": amount,
                    "currency": 'EUR',
                    "externalId": transaction_id,
                    "payee": {
                        "partyIdType": "MSISDN",
                        "partyId": payee
                    },
                    "payerMessage": f"send money to {payee}",
                    "payeeNote": "Lipila gateway"
                })
                headers = {
                    'X-Reference-Id': transaction_id,
                    'Ocp-Apim-Subscription-Key': self.subscription_dis_key,
                    'X-Target-Environment': self.x_target_environment,
                    'Authorization': self.api_token,
                    'Content-Type': self.content_type
                }
                response = requests.post(url, headers=headers, data=payload)
                if response.status_code == 202:
                    return response
                elif response.status_code == 400:
                    return Response(status=400, data={'reason': 'Bad Request deposit'})
                elif response.status_code == 409:
                    return Response(status=409, data={'reason': 'Conflict user exists'})
                elif response.status_code == 500:
                    return Response(status=500, data={'reason': 'mtn server error'})
            except Exception as e:
                return Response(status=500, data={'reason': 'mtn server error'})

    def get_transaction_status(self, transaction: str, referenceid: str) -> Response:
        """
        Queries the mtn api to get the transaction status.

        Args:
            transaction(str): The type of transactions (deposit, transfer, refund)
            referenceid(str): The id that was used to make the deposit.

        Returns:
            A HTTP response.
        """
        url = f"https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/{transaction}/{referenceid}"
        headers = {
            'X-Target-Environment': self.x_target_environment,
            'Ocp-Apim-Subscription-Key': self.subscription_dis_key,
            'Authorization': self.api_token
        }
        try:
            response = requests.get(url, headers=headers, data={})
            if response.status_code == 200:
                return response
            elif response.status_code == 400:
                return Response(status=400, data={'reason': ' get trans status'})
            elif response.status_code == 404:
                return Response(status=404, data={'reason': 'Not Found'})
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)

    def get_account_balance(self) -> Response:
        """ 
        Queries the mtn api for account balance.
        Returns:
            HTTP Response.
        """
        url = f"https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/account/balance"
        headers = {
            'X-Target-Environment': self.x_target_environment,
            'Ocp-Apim-Subscription-Key': self.subscription_dis_key,
            'Authorization': self.api_token
        }
        try:
            response = requests.get(url, headers=headers, data={})
            if response.status_code == 200:
                """ 
                    {
                        "availableBalance": "string",
                        "currency": "string"
                    }
                """
                return response
            elif response.status_code == 400:
                return Response(status=400, data={'reason': 'Bad Request get acount balance'})
            elif response.status_code == 404:
                return Response(status=404, data={'reason': 'Not Found'})
            elif response.status_code == 500:
                raise ValueError("Mtn Server error")
        except ValueError:
            return Response(status=response.status_code)
