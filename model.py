from dataclasses import dataclass, field
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


@dataclass
class IdentifiedPatient:
    patient: Patient
    medications: list[Medication] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.patient.name

    @property
    def cpf(self) -> str:
        return self.patient.cpf

    @property
    def context(self) -> str:
        if not self.medications:
            return f"Patient: {self.name}\nNo active medications."

        context = f"Patient: {self.name}\n\nActive medications:\n"

        for med in self.medications:
            context += f"\n- {med.name} ({med.dosage})"
            context += f"\n  Frequency: {med.frequency}"
            if med.notes:
                context += f"\n  Instructions: {med.notes}"
            context += "\n"

        return context
