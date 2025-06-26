from pydantic import BaseModel, Field
from typing import Optional, List

class KeyDataExtractionRequest(BaseModel):
    """Information about an extracted person."""
    name: Optional[str] = Field(
        default="cannot-extract", description="Name of the person"
    )
    middlename: Optional[str] = Field(
        default="cannot-extract", description="Middle name of the person"
    )
    lastname: Optional[str] = Field(
        default="cannot-extract", description="Last name of the person"
    )
    country: Optional[str] = Field(
        default="cannot-extract", description="Country of the person"
    )

class ExtractedPeople(BaseModel):
    people: List[KeyDataExtractionRequest]