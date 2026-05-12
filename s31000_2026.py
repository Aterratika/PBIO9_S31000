# Numer albumu: s31000
# Data: 2026-05-12
# Opis programu:
# Program generuje losową sekwencję DNA, zapisuje ją w formacie FASTA,
# wstawia imię użytkownika w losowym miejscu oraz wypisuje statystyki sekwencji.
# Dodatkowo użytkownik może ustawić procentowy rozkład nukleotydów A, C, G, T.

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


def save_to_file(filename: str, content: str) -> None:
    """
    Zapisuje podany tekst do pliku.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def main():
    """
    Główna funkcja programu.
    Pobiera dane od użytkownika, generuje sekwencję,
    zapisuje plik FASTA i wypisuje statystyki.
    """
    length = validate_positive_int("Podaj długość sekwencji: ")

    seq_id = validate_sequence_id("Podaj ID sekwencji: ")

    description = input("Podaj opis sekwencji: ")

    name = input("Podaj imię: ")

    distribution = get_nucleotide_distribution()

    dna_sequence = generate_sequence_with_distribution(length, distribution)

    stats = calculate_stats(dna_sequence)

    sequence_with_name = insert_name(dna_sequence, name)

    fasta_content = format_fasta(seq_id, description, sequence_with_name)

    filename = f"{seq_id}.fasta"

    save_to_file(filename, fasta_content)

    print()
    print(f"Sekwencja zapisana do pliku: {filename}")
    print()
    print("Zadany rozkład nukleotydów:")
    print(f"  A: {distribution['A']:.2f}%")
    print(f"  C: {distribution['C']:.2f}%")
    print(f"  G: {distribution['G']:.2f}%")
    print(f"  T: {distribution['T']:.2f}%")
    print()
    print(f"Statystyki wygenerowanej sekwencji (n={length}):")
    print(f"  A: {stats['A']:.2f}%")
    print(f"  C: {stats['C']:.2f}%")
    print(f"  G: {stats['G']:.2f}%")
    print(f"  T: {stats['T']:.2f}%")
    print(f"  GC-content: {stats['GC']:.2f}%")


if __name__ == "__main__":
    main()