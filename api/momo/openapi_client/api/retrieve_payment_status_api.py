# coding: utf-8

"""
    Payments V1

    To facilitate the capability for consumers to make a payment or refund to service providers.

    The version of the OpenAPI document: v1.0
    Contact: developer-support@mtn.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from pydantic import Field, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Optional, Union
from typing_extensions import Annotated
from openapi_client.models.payment_transaction_status_response import PaymentTransactionStatusResponse

from openapi_client.api_client import ApiClient, RequestSerialized
from openapi_client.api_response import ApiResponse
from openapi_client.rest import RESTResponseType


class RetrievePaymentStatusApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def get_payment_transaction_status(
        self,
        correlator_id: Annotated[StrictStr, Field(description="Unique identifier in the client for the payment in case it is needed to correlate, could also be a reference id generated when making the request")],
        transaction_id: Annotated[Optional[StrictStr], Field(description="Client generated Id to include for tracing requests.")] = None,
        x_authorization: Annotated[Optional[StrictStr], Field(description="Encrypted ECW credentials")] = None,
        amount: Optional[Union[StrictFloat, StrictInt]] = None,
        target_system: Annotated[Optional[StrictStr], Field(description="target system expected to fulful the service")] = None,
        payment_type: Annotated[Optional[StrictStr], Field(description="Type of the transaction")] = None,
        customer_id: Annotated[Optional[StrictStr], Field(description="This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN")] = None,
        description: Annotated[Optional[StrictStr], Field(description="can be a payer note, a merchant identifier ie. merchantId etc.")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> PaymentTransactionStatusResponse:
        """Provides the status of a Payment Transaction to service providers.

        Provides the status of a Payment Transaction to service providers.

        :param correlator_id: Unique identifier in the client for the payment in case it is needed to correlate, could also be a reference id generated when making the request (required)
        :type correlator_id: str
        :param transaction_id: Client generated Id to include for tracing requests.
        :type transaction_id: str
        :param x_authorization: Encrypted ECW credentials
        :type x_authorization: str
        :param amount:
        :type amount: float
        :param target_system: target system expected to fulful the service
        :type target_system: str
        :param payment_type: Type of the transaction
        :type payment_type: str
        :param customer_id: This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN
        :type customer_id: str
        :param description: can be a payer note, a merchant identifier ie. merchantId etc.
        :type description: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_payment_transaction_status_serialize(
            correlator_id=correlator_id,
            transaction_id=transaction_id,
            x_authorization=x_authorization,
            amount=amount,
            target_system=target_system,
            payment_type=payment_type,
            customer_id=customer_id,
            description=description,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "PaymentTransactionStatusResponse",
            '400': "Error",
            '401': "Error",
            '403': "Error",
            '404': "Error",
            '405': "Error",
            '500': "Error",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def get_payment_transaction_status_with_http_info(
        self,
        correlator_id: Annotated[StrictStr, Field(description="Unique identifier in the client for the payment in case it is needed to correlate, could also be a reference id generated when making the request")],
        transaction_id: Annotated[Optional[StrictStr], Field(description="Client generated Id to include for tracing requests.")] = None,
        x_authorization: Annotated[Optional[StrictStr], Field(description="Encrypted ECW credentials")] = None,
        amount: Optional[Union[StrictFloat, StrictInt]] = None,
        target_system: Annotated[Optional[StrictStr], Field(description="target system expected to fulful the service")] = None,
        payment_type: Annotated[Optional[StrictStr], Field(description="Type of the transaction")] = None,
        customer_id: Annotated[Optional[StrictStr], Field(description="This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN")] = None,
        description: Annotated[Optional[StrictStr], Field(description="can be a payer note, a merchant identifier ie. merchantId etc.")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[PaymentTransactionStatusResponse]:
        """Provides the status of a Payment Transaction to service providers.

        Provides the status of a Payment Transaction to service providers.

        :param correlator_id: Unique identifier in the client for the payment in case it is needed to correlate, could also be a reference id generated when making the request (required)
        :type correlator_id: str
        :param transaction_id: Client generated Id to include for tracing requests.
        :type transaction_id: str
        :param x_authorization: Encrypted ECW credentials
        :type x_authorization: str
        :param amount:
        :type amount: float
        :param target_system: target system expected to fulful the service
        :type target_system: str
        :param payment_type: Type of the transaction
        :type payment_type: str
        :param customer_id: This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN
        :type customer_id: str
        :param description: can be a payer note, a merchant identifier ie. merchantId etc.
        :type description: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_payment_transaction_status_serialize(
            correlator_id=correlator_id,
            transaction_id=transaction_id,
            x_authorization=x_authorization,
            amount=amount,
            target_system=target_system,
            payment_type=payment_type,
            customer_id=customer_id,
            description=description,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "PaymentTransactionStatusResponse",
            '400': "Error",
            '401': "Error",
            '403': "Error",
            '404': "Error",
            '405': "Error",
            '500': "Error",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def get_payment_transaction_status_without_preload_content(
        self,
        correlator_id: Annotated[StrictStr, Field(description="Unique identifier in the client for the payment in case it is needed to correlate, could also be a reference id generated when making the request")],
        transaction_id: Annotated[Optional[StrictStr], Field(description="Client generated Id to include for tracing requests.")] = None,
        x_authorization: Annotated[Optional[StrictStr], Field(description="Encrypted ECW credentials")] = None,
        amount: Optional[Union[StrictFloat, StrictInt]] = None,
        target_system: Annotated[Optional[StrictStr], Field(description="target system expected to fulful the service")] = None,
        payment_type: Annotated[Optional[StrictStr], Field(description="Type of the transaction")] = None,
        customer_id: Annotated[Optional[StrictStr], Field(description="This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN")] = None,
        description: Annotated[Optional[StrictStr], Field(description="can be a payer note, a merchant identifier ie. merchantId etc.")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Provides the status of a Payment Transaction to service providers.

        Provides the status of a Payment Transaction to service providers.

        :param correlator_id: Unique identifier in the client for the payment in case it is needed to correlate, could also be a reference id generated when making the request (required)
        :type correlator_id: str
        :param transaction_id: Client generated Id to include for tracing requests.
        :type transaction_id: str
        :param x_authorization: Encrypted ECW credentials
        :type x_authorization: str
        :param amount:
        :type amount: float
        :param target_system: target system expected to fulful the service
        :type target_system: str
        :param payment_type: Type of the transaction
        :type payment_type: str
        :param customer_id: This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN
        :type customer_id: str
        :param description: can be a payer note, a merchant identifier ie. merchantId etc.
        :type description: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_payment_transaction_status_serialize(
            correlator_id=correlator_id,
            transaction_id=transaction_id,
            x_authorization=x_authorization,
            amount=amount,
            target_system=target_system,
            payment_type=payment_type,
            customer_id=customer_id,
            description=description,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "PaymentTransactionStatusResponse",
            '400': "Error",
            '401': "Error",
            '403': "Error",
            '404': "Error",
            '405': "Error",
            '500': "Error",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _get_payment_transaction_status_serialize(
        self,
        correlator_id,
        transaction_id,
        x_authorization,
        amount,
        target_system,
        payment_type,
        customer_id,
        description,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if correlator_id is not None:
            _path_params['correlatorId'] = correlator_id
        # process the query parameters
        if amount is not None:
            
            _query_params.append(('amount', amount))
            
        if target_system is not None:
            
            _query_params.append(('targetSystem', target_system))
            
        if payment_type is not None:
            
            _query_params.append(('paymentType', payment_type))
            
        if customer_id is not None:
            
            _query_params.append(('customerId', customer_id))
            
        if description is not None:
            
            _query_params.append(('description', description))
            
        # process the header parameters
        if transaction_id is not None:
            _header_params['transactionId'] = transaction_id
        if x_authorization is not None:
            _header_params['X-Authorization'] = x_authorization
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
            'OAuth2'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/payments/{correlatorId}/transactionStatus',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )

