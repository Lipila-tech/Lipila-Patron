# coding: utf-8

"""
    Payments V1

    To facilitate the capability for consumers to make a payment or refund to service providers.

    The version of the OpenAPI document: v1.0
    Contact: developer-support@mtn.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from openapi_client.models.loyalty_balances import LoyaltyBalances
from openapi_client.models.payment_response_links import PaymentResponseLinks
from openapi_client.models.reverse_transaction_history_data import ReverseTransactionHistoryData
from typing import Optional, Set
from typing_extensions import Self

class ReverseTransactionHistory(BaseModel):
    """
    ReverseTransactionHistory
    """ # noqa: E501
    status_code: Optional[StrictStr] = Field(default=None, alias="statusCode")
    status_message: Optional[StrictStr] = Field(default=None, alias="statusMessage")
    transaction_id: Optional[StrictStr] = Field(default=None, description="API generated Id to include for tracing requests", alias="transactionId")
    correlator_id: Optional[StrictStr] = Field(default=None, alias="correlatorId")
    sequence_no: Optional[StrictStr] = Field(default=None, description="A unique id for tracing all requests", alias="sequenceNo")
    data: Optional[ReverseTransactionHistoryData] = None
    loyalty_information: Optional[LoyaltyBalances] = Field(default=None, alias="loyaltyInformation")
    links: Optional[PaymentResponseLinks] = Field(default=None, alias="_links")
    __properties: ClassVar[List[str]] = ["statusCode", "statusMessage", "transactionId", "correlatorId", "sequenceNo", "data", "loyaltyInformation", "_links"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of ReverseTransactionHistory from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of data
        if self.data:
            _dict['data'] = self.data.to_dict()
        # override the default output from pydantic by calling `to_dict()` of loyalty_information
        if self.loyalty_information:
            _dict['loyaltyInformation'] = self.loyalty_information.to_dict()
        # override the default output from pydantic by calling `to_dict()` of links
        if self.links:
            _dict['_links'] = self.links.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ReverseTransactionHistory from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "statusCode": obj.get("statusCode"),
            "statusMessage": obj.get("statusMessage"),
            "transactionId": obj.get("transactionId"),
            "correlatorId": obj.get("correlatorId"),
            "sequenceNo": obj.get("sequenceNo"),
            "data": ReverseTransactionHistoryData.from_dict(obj["data"]) if obj.get("data") is not None else None,
            "loyaltyInformation": LoyaltyBalances.from_dict(obj["loyaltyInformation"]) if obj.get("loyaltyInformation") is not None else None,
            "_links": PaymentResponseLinks.from_dict(obj["_links"]) if obj.get("_links") is not None else None
        })
        return _obj

