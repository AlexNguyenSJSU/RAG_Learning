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

class SentimentAnalysisRequest(BaseModel):
    """Information about a sentiment analysis request."""
    sentiment: str = Field(
        ...,
        description="The sentiment of the text"
    )
    aggressiveness: int = Field(
        ...,
        description="How aggressive the text is on a scale from 1 to 10"
    )
    language: str = Field(
        ...,
        description="The language the text is written in"
    )