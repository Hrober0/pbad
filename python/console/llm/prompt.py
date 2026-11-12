INSTRUCTION = """\
Jesteś asystentem, który na podstawie pytania użytkownika buduje zapytanie SQL
dla bazy PostgreSQL 18 z rozszerzeniem PostGIS 3.6.

Wygeneruj jedno zapytanie SELECT odpowiadające na pytanie użytkownika.
Jeśli pytanie nie może zostać wyrażone jako zapytanie SQL, zwróć pusty
ciąg w polu sql i wyjaśnij przyczynę w polu explanation.

Wynik zapytania ma odpowiadać dokładnie na pytanie.

Poniżej znajdziesz dodatkowe informacje o bazie danych, które mogą pomóc
w zbudowaniu zapytania.

{context}"""

RESPONSE_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "sql": {
            "type": "string",
            "description": "Samo zapytanie SELECT, bez markdown i bez komentarzy.",
        },
        "explanation": {
            "type": "string",
            "description": (
                "Krótkie wyjaśnienie po polsku najważniejszych decyzji podjętych "
                "przy tworzeniu zapytania, w szczególności przyjętych założeń, "
                "interpretacji niejednoznaczności i wyborów, które nie wynikają "
                "bezpośrednio z pytania. Jeśli nie ma nic istotnego do wyjaśnienia, "
                "zwróć pusty ciąg."
            ),
        },
    },
    "required": ["sql", "explanation"],
    "additionalProperties": False,
}


def build_system(context: str) -> str:
    return INSTRUCTION.format(context=context)
