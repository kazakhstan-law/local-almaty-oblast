"""Проверка 3 — оформление: якоря статей и пунктов на месте, нумерация не сбита, нет хвостовых пробелов."""
import re
import sys

from changed import added_lines, at_base, changed_files

ANCHOR = re.compile(r'<a id="[^"]+"></a>')
POINT = re.compile(r"^(\d+(?:-\d+)?)\. ")


def main():
    bad = 0
    for f in changed_files():
        if not f.endswith(".md"):
            continue
        before, after = at_base(f), open(f, encoding="utf-8").read()
        a0, a1 = ANCHOR.findall(before), ANCHOR.findall(after)
        if a0 != a1:
            bad += 1
            print(f"✗ {f}: набор якорей изменился ({len(a0)} → {len(a1)})")
        p0 = [m.group(1) for l in before.split("\n") if (m := POINT.match(l))]
        p1 = [m.group(1) for l in after.split("\n") if (m := POINT.match(l))]
        if p0 != p1:
            bad += 1
            print(f"✗ {f}: нумерация пунктов изменилась")
        for l in added_lines(f):
            if l != l.rstrip() or "\t" in l:
                bad += 1
                print(f"✗ {f}: хвостовой пробел или табуляция: {l[:60]!r}")
        if not after.endswith("\n"):
            bad += 1
            print(f"✗ {f}: нет перевода строки в конце файла")
        print(f"✓ {f}: якоря {len(a1)}, пунктов {len(p1)}, оформление в порядке" if not bad else "")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
