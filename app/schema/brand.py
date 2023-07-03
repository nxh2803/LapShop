from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BrandBase(BaseModel):
    brand_id: str

class BrandResponse(BrandBase):
    brand_name: str
    brand_description: str
    
class BrandListResponse(BaseModel):
    brand_id: str
    brand_name: str
    brand_description: str