"""Проверка 2 — соответствие между языками: правка в rus.md требует правки в kaz.md того же акта, и наоборот."""
import sys

from changed import changed_files


def main():
    files = set(changed_files())
    bad = 0
    for f in sorted(files):
        for a, b in (("rus.md", "kaz.md"), ("kaz.md", "rus.md")):
            if f.endswith("/" + a):
                other = f[: -len(a)] + b
                if other not in files:
                    bad += 1
                    print(f"✗ {f} изменён, {other} — нет")
                else:
                    print(f"✓ {f} и {other} изменены вместе")
    if not bad:
        print("Оба языка изменены вместе.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
