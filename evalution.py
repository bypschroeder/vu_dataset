import os
from collections import Counter
import statistics
from smpl.import_smpl import get_random_gender, get_random_height, get_random_weight
from _helpers.scene import get_random_blend_file


def main():
    iterations = 5000
    file_path = os.path.abspath("clothing/models/t-shirt")

    genders = []
    heights_m = []
    heights_f = []
    weights_m = []
    weights_f = []
    sizes = []

    for _ in range(iterations):
        gender = get_random_gender()
        height = get_random_height(gender)
        weight = get_random_weight(height, gender)
        size = get_random_blend_file(os.path.join(file_path, gender))

        genders.append(gender)
        sizes.append(os.path.basename(size))

        if gender == "male":
            heights_m.append(height)
            weights_m.append(weight)
        else:
            heights_f.append(height)
            weights_f.append(weight)

    print("\n=== AUSWERTUNG ===")

    # Geschlechterverteilung
    gender_count = Counter(genders)
    print("\nGeschlechterverteilung:")
    print(
        f"Männlich: {gender_count['male']} ({gender_count['male']/iterations*100:.1f}%)"
    )
    print(
        f"Weiblich: {gender_count['female']} ({gender_count['female']/iterations*100:.1f}%)"
    )

    # Größenstatistik
    print("\nGrößenstatistik für Männer:")
    if heights_m:  # Prüfen, ob es männliche Daten gibt
        print(f"Minimale Größe: {min(heights_m)} cm")
        print(f"Maximale Größe: {max(heights_m)} cm")
        print(f"Durchschnittliche Größe: {statistics.mean(heights_m):.1f} cm")
    else:
        print("Keine männlichen Daten vorhanden.")

    print("\nGrößenstatistik für Frauen:")
    if heights_f:  # Prüfen, ob es weibliche Daten gibt
        print(f"Minimale Größe: {min(heights_f)} cm")
        print(f"Maximale Größe: {max(heights_f)} cm")
        print(f"Durchschnittliche Größe: {statistics.mean(heights_f):.1f} cm")
    else:
        print("Keine weiblichen Daten vorhanden.")

    # Gewichtsstatistik
    print("\nGewichtsstatistik für Männer:")
    if weights_m:  # Prüfen, ob es männliche Daten gibt
        print(f"Minimales Gewicht: {min(weights_m):.1f} kg")
        print(f"Maximales Gewicht: {max(weights_m):.1f} kg")
        print(f"Durchschnittliches Gewicht: {statistics.mean(weights_m):.1f} kg")
    else:
        print("Keine männlichen Daten vorhanden.")

    print("\nGewichtsstatistik für Frauen:")
    if weights_f:  # Prüfen, ob es weibliche Daten gibt
        print(f"Minimales Gewicht: {min(weights_f):.1f} kg")
        print(f"Maximales Gewicht: {max(weights_f):.1f} kg")
        print(f"Durchschnittliches Gewicht: {statistics.mean(weights_f):.1f} kg")
    else:
        print("Keine weiblichen Daten vorhanden.")

    # Kleidungsgrößenverteilung
    sizes_counter = Counter(sizes)
    print("\nVerteilung der Kleidungsgrößen:")
    for size, count in sizes_counter.most_common():
        print(f"{size}: {count} ({count/iterations*100:.1f}%)")


if __name__ == "__main__":
    main()
