from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Patient:
    id: int
    cpf: str
    name: str
    birth_date: date
    phone: str | None = None
    email: str | None = None
    created_at: datetime | None = None


@dataclass
class Medication:
    id: int
    patient_id: int
    name: str
    dosage: str
    frequency: str
    start_date: date
    end_date: date | None = None
    notes: str | None = None
    created_at: datetime | None = None

