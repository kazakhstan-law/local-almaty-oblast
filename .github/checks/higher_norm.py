"""ПРОТОТИП. Проверка 1 — вышестоящая норма.

Изменённая строка регламента маслихата, которая регулирует известный вопрос, сверяется
с формулировкой закона «О местном государственном управлении и самоуправлении» (акт 7966)
из репозитория kazakhstan-law/codes. Таблица правил — ручная и короткая: это прототип,
который показывает форму проверки, а не её покрытие.
"""
import re
import sys
import urllib.request

from changed import added_lines, changed_files

LAW = ("https://raw.githubusercontent.com/kazakhstan-law/codes/main/"
       "03-laws/2001/0123-o-mestnom-gosudarstvennom-upravlenii-i-samoupravlenii-v-respubli-7966/rus.md")
VOTE = re.compile(r"(двумя третями|большинством) голосов(?: не менее двух третей)? от [^,.;]*?депутатов")
RULES = [  # (тема в тексте регламента, якорь статьи закона, признак нужного пункта закона)
    ("недовери", "st24", "выразить недоверие акиму"),
]


def law_phrase(text, anchor, marker):
    body = text.split(f'<a id="{anchor}"></a>', 1)[1]
    body = body.split("<a id=", 1)[0]
    for line in body.split("\n"):
        if marker in line and not line.startswith("#"):
            m = VOTE.search(line)
            if m:
                return line.strip(), m.group(0)
    return None, None


def main():
    files = [f for f in changed_files() if f.startswith("08-local-decisions/") and f.endswith("/rus.md")]
    if not files:
        print("Изменённых регламентов нет — проверять нечего.")
        return 0
    law = urllib.request.urlopen(LAW, timeout=30).read().decode()
    bad = 0
    for f in files:
        for line in added_lines(f):
            for topic, anchor, marker in RULES:
                if topic not in line:
                    continue
                m = VOTE.search(line)
                if not m:
                    continue
                law_line, need = law_phrase(law, anchor, marker)
                print(f"{f}\n  регламент: «{m.group(0)}»\n  закон, ст. {anchor[2:]}: «{need}»")
                if m.group(0) != need:
                    bad += 1
                    print("  ✗ расходится с вышестоящей нормой\n  закон: " + law_line[:200])
                else:
                    print("  ✓ совпадает с законом")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
