import ply.lex as lex
from django.template.loader import render_to_string
from django.utils.html import escape


tokens = (
    "ANSWER",
    "IMAGE",
    "TEXT",
    "SPACE",
)


def t_ANSWER(t):
    r"(\#[0-9]+)"
    t.value = f"<a href='{t.value}'>{t.value}</a>"
    return t


def t_IMAGE(t):
    r"\%"
    return t


def t_TEXT(t):
    r'\S+\S*'
    t.value = escape(t.value)
    return t


def t_SPACE(t):
    r'\s'
    return t


def t_error(t):
    print(f"Illegal character {t.value[0]}")
    return t


lexer = lex.lex()


def parse_content(content: str, files) -> str:
    lexer.input(content)
    s = ""
    while True:
        token = lexer.token()
        if not token:
            break
        if token.type == "IMAGE":
            try:
                token.value = render_to_string(
                    "components/displayable_file.html",
                    context={"file": files.pop()},
                )
            except IndexError:
                pass
        s += token.value
    return s
