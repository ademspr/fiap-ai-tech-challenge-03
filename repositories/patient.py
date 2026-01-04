from model import Patient


class PatientRepository:
    def __init__(self, connection):
        self._connection = connection

    def get_by_cpf(self, cpf: str) -> Patient | None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, cpf, name, birth_date, phone, email, created_at
                FROM patients
                WHERE cpf = %s;
                """,
                (cpf,),
            )
            result = cursor.fetchone()

            if result is None:
                return None

            return Patient(
                id=result["id"],
                cpf=result["cpf"],
                name=result["name"],
                birth_date=result["birth_date"],
                phone=result["phone"],
                email=result["email"],
                created_at=result["created_at"],
            )
