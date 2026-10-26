"""Request and response schemas for the API."""
from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    type: str = Field(..., pattern="^(pemasukan|pengeluaran)$")
    amount: float = Field(..., gt=0)
    note: str = Field(..., min_length=2)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    category: str | None = None


class CategorizeRequest(BaseModel):
    note: str = Field(..., min_length=2)
    type: str = Field(..., pattern="^(pemasukan|pengeluaran)$")
