from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReceiptData(BaseModel):
    receipt_number: str
    receipt_date: str
    brand: str
    encoded_receipt_file: str
    receipt_client: str
    brand_model: str
    response_id: Optional[UUID] = None


class ReceiptApproverResponseCreate(BaseModel):
    ocr_raw: Dict
    processed: Dict
    client: str
    receipt_classifier_response: Dict


class ReceiptApproverResponseSchema(BaseModel):
    id: Optional[UUID]
    receipt_number: str
    receipt_date: str
    brand: str
    receipt_type: Optional[dict]
    validation_result: dict
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_with_custom_fields(cls, orm_obj):
        """
        This custom class method will handle the conversion of SQLAlchemy fields
        to Pydantic model fields where names do not match.
        """
        # Manually mapping fields
        return cls(
            id=orm_obj.id,
            receipt_number=orm_obj.user_input_data.get(
                "receipt_number"
            ),  # Extract from JSON
            receipt_date=orm_obj.user_input_data.get(
                "receipt_date"
            ),  # Extract from JSON
            brand=orm_obj.user_input_data.get("brand"),  # Extract from JSON
            receipt_type=orm_obj.receipt_classifier_response,  # Maps directly
            validation_result=orm_obj.processed,  # Maps directly
            last_updated=orm_obj.last_updated,
        )
