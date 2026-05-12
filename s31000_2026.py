# Numer albumu: s31000
# Data: 2026-05-12
# Opis programu:
# Program generuje losową sekwencję DNA, zapisuje ją w formacie FASTA,
# wstawia imię użytkownika w losowym miejscu oraz wypisuje statystyki sekwencji.
# Dodatkowo użytkownik może ustawić procentowy rozkład nukleotydów A, C, G, T.
# Program posiada także tryb batch mode, czyli generowanie wielu sekwencji
# i zapis ich do jednego pliku multi-FASTA.

import random


def generate_sequence(length: int) -> str:
    """
    Zwraca losową sekwencję DNA o zadanej długości.
    Sekwencja składa się wyłącznie ze znaków A, C, G, T.
    Przy tej wersji funkcja używa domyślnego, równego rozkładu nukleotydów.
    """
    nucleotides = ["A", "C", "G", "T"]
    sequence = ""

    for _ in range(length):
        sequence += random.choice(nucleotides)

    return sequence


def generate_sequence_with_distribution(length: int, distribution: dict) -> str:
    """
    Zwraca losową sekwencję DNA o zadanej długości,
    uwzględniając procentowy rozkład nukleotydów podany przez użytkownika.

    Przykład:
    A = 30%, C = 20%, G = 20%, T = 30%.
    """
    nucleotides = ["A", "C", "G", "T"]

    weights = [
        distribution["A"],
        distribution["C"],
        distribution["G"],
        distribution["T"]
    ]

    sequence = ""

    for _ in range(length):
        nucleotide = random.choices(nucleotides, weights=weights, k=1)[0]
        sequence += nucleotide

    return sequence


def get_nucleotide_distribution() -> dict:
    """
    Pobiera od użytkownika procentowy udział nukleotydów A, C, G, T.
    Sprawdza, czy wszystkie wartości są poprawne oraz czy ich suma wynosi 100%.
    """
    while True:
        print()
        print("Podaj procentowy udział nukleotydów.")
        print("Suma wartości dla A, C, G i T musi wynosić dokładnie 100.")

        try:
            percent_a = float(input("Podaj procent A: "))
            percent_c = float(input("Podaj procent C: "))
            percent_g = float(input("Podaj procent G: "))
            percent_t = float(input("Podaj procent T: "))

            if percent_a < 0 or percent_c < 0 or percent_g < 0 or percent_t < 0:
                print("Błąd: procenty nie mogą być ujemne.")
                continue

            total = percent_a + percent_c + percent_g + percent_t

            if total == 100:
                return {
                    "A": percent_a,
                    "C": percent_c,
                    "G": percent_g,
                    "T": percent_t
                }
            else:
                print(f"Błąd: suma procentów wynosi {total}, a powinna wynosić 100.")

        except ValueError:
            print("Błąd: podane wartości muszą być liczbami.")


def calculate_stats(sequence: str) -> dict:
    """
    Zwraca słownik ze statystykami sekwencji.
    Klucze: "A", "C", "G", "T" oraz "GC".
    Wartości są procentami zaokrąglonymi do dwóch miejsc po przecinku.
    """
    length = len(sequence)

    count_a = sequence.count("A")
    count_c = sequence.count("C")
    count_g = sequence.count("G")
    count_t = sequence.count("T")

    stats = {
        "A": round((count_a / length) * 100, 2),
        "C": round((count_c / length) * 100, 2),
        "G": round((count_g / length) * 100, 2),
        "T": round((count_t / length) * 100, 2),
        "GC": round(((count_g + count_c) / length) * 100, 2)
    }

    return stats


def insert_name(sequence: str, name: str) -> str:
    """
    Wstawia imię użytkownika w losową pozycję sekwencji.
    Imię jest zapisane małymi literami, aby odróżnić je od nukleotydów.
    """
    position = random.randint(0, len(sequence))
    name_lower = name.lower()

    sequence_with_name = sequence[:position] + name_lower + sequence[position:]

    return sequence_with_name


def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    """
    Zwraca sformatowany rekord FASTA jako string.
    Nagłówek zaczyna się od znaku >.
    Sekwencja jest łamana na linie o szerokości 80 znaków.
    """
    if description == "":
        header = f">{seq_id}"
    else:
        header = f">{seq_id} {description}"

    lines = [header]

    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i + line_width])

    return "\n".join(lines)


def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """
    Pobiera od użytkownika liczbę całkowitą z podanego zakresu.
    W przypadku błędu ponownie prosi o podanie wartości.
    """
    while True:
        user_input = input(prompt)

        try:
            value = int(user_input)

            if min_val <= value <= max_val:
                return value
            else:
                print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")

        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")


def validate_sequence_id(prompt: str) -> str:
    """
    Pobiera od użytkownika ID sekwencji.
    ID nie może być puste i nie może zawierać białych znaków.
    """
    while True:
        seq_id = input(prompt)

        if seq_id == "":
            print("Błąd: ID sekwencji nie może być puste.")
        elif any(char.isspace() for char in seq_id):
            print("Błąd: ID sekwencji nie może zawierać białych znaków.")
        else:
            return seq_id


def create_batch_id(base_id: str, number: int) -> str:
    """
    Tworzy unikalne ID dla sekwencji w trybie batch.
    Przykład: Seq + 1 -> Seq_001.
    """
    return f"{base_id}_{number:03d}"


def generate_batch_fasta(batch_count: int,
                         length: int,
                         base_id: str,
                         description: str,
                         name: str,
                         distribution: dict) -> tuple:
    """
    Generuje wiele sekwencji DNA i zwraca zawartość pliku multi-FASTA
    oraz listę statystyk dla każdej sekwencji.

    Każda sekwencja ma unikalne ID, np. Seq_001, Seq_002.
    """
    fasta_records = []
    all_stats = []

    for i in range(1, batch_count + 1):
        current_id = create_batch_id(base_id, i)

        dna_sequence = generate_sequence_with_distribution(length, distribution)

        stats = calculate_stats(dna_sequence)

        sequence_with_name = insert_name(dna_sequence, name)

        fasta_record = format_fasta(current_id, description, sequence_with_name)

        fasta_records.append(fasta_record)

        all_stats.append({
            "id": current_id,
            "stats": stats
        })

    multi_fasta_content = "\n\n".join(fasta_records)

    return multi_fasta_content, all_stats


def save_to_file(filename: str, content: str) -> None:
    """
    Zapisuje podany tekst do pliku.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def main():
    """
    Główna funkcja programu.
    Pobiera dane od użytkownika, generuje jedną lub wiele sekwencji,
    zapisuje plik FASTA i wypisuje statystyki.
    """
    length = validate_positive_int("Podaj długość sekwencji: ")

    seq_id = validate_sequence_id("Podaj bazowe ID sekwencji: ")

    description = input("Podaj opis sekwencji: ")

    name = input("Podaj imię: ")

    distribution = get_nucleotide_distribution()

    batch_count = validate_positive_int(
        "Podaj liczbę sekwencji do wygenerowania: ",
        min_val=1,
        max_val=1000
    )

    fasta_content, all_stats = generate_batch_fasta(
        batch_count,
        length,
        seq_id,
        description,
        name,
        distribution
    )

    filename = f"{seq_id}.fasta"

    save_to_file(filename, fasta_content)

    print()
    print(f"Sekwencje zapisane do pliku: {filename}")
    print()
    print("Zadany rozkład nukleotydów:")
    print(f"  A: {distribution['A']:.2f}%")
    print(f"  C: {distribution['C']:.2f}%")
    print(f"  G: {distribution['G']:.2f}%")
    print(f"  T: {distribution['T']:.2f}%")

    print()
    print(f"Wygenerowano liczbę sekwencji: {batch_count}")
    print(f"Długość każdej sekwencji biologicznej: {length}")

    print()
    print("Statystyki wygenerowanych sekwencji:")

    for item in all_stats:
        current_id = item["id"]
        stats = item["stats"]

        print()
        print(f"Sekwencja: {current_id}")
        print(f"  A: {stats['A']:.2f}%")
        print(f"  C: {stats['C']:.2f}%")
        print(f"  G: {stats['G']:.2f}%")
        print(f"  T: {stats['T']:.2f}%")
        print(f"  GC-content: {stats['GC']:.2f}%")


if __name__ == "__main__":
    main()