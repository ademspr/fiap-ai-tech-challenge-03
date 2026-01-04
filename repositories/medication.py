from model import Medication


class MedicationRepository:
    def __init__(self, connection):
        self._connection = connection

    def get_active_by_patient_id(self, patient_id: int) -> list[Medication]:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, patient_id, name, dosage, frequency,
                       start_date, end_date, notes, created_at
                FROM medications
                WHERE patient_id = %s
                  AND (end_date IS NULL OR end_date >= CURRENT_DATE)
                ORDER BY name;
                """,
                (patient_id,),
            )

            return [
                Medication(
                    id=row["id"],
                    patient_id=row["patient_id"],
                    name=row["name"],
                    dosage=row["dosage"],
                    frequency=row["frequency"],
                    start_date=row["start_date"],
                    end_date=row["end_date"],
                    notes=row["notes"],
                    created_at=row["created_at"],
                )
                for row in cursor.fetchall()
            ]
