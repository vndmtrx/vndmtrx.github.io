#!/usr/bin/env python3
"""Linter deterministico para posts do blog vndmtrx.github.io.

Valida as 16 invariantes rigidas do Jekyll ([ERRO]) e aponta heuristicas
consultivas de ritmo e anti-slop ([AVISO]). Stdlib pura, zero dependencias.

Uso:
    python3 .agents/skills/blog-posts/scripts/lint_post.py <arquivo.md> [--strict] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

VALID_CATEGORIES = {"Tutoriais", "Artigos", "Ensaios", "Crônicas"}
REQUIRED_FM_KEYS = {"layout", "title", "subtitle", "author", "date", "permalink", "category", "tags"}
ALLOWED_LIQUID_TAGS = {"include", "raw", "endraw"}

# Ranges comuns de emojis (evita falsos positivos com acentuacao latina ou simbolos matematicos)
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]"
)

UNICODE_ARROWS_RE = re.compile(r"[→←➔↔⇒⇐➜➝➞➡⬅]")
CALLOUT_START_RE = re.compile(r"^\s*>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", re.IGNORECASE)
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$")
FOOTNOTE_REF_RE = re.compile(r"\[\^([^\]]+)\]")
INTERNAL_LINK_RE = re.compile(r"\[[^\]]*\]\((?:https?://vndmtrx\.github\.io)?(/posts/[^)]+)\)")
LIQUID_TAG_RE = re.compile(r"\{%\s*([a-zA-Z0-9_-]+)\b[^%]*%\}|\{\{[^}]+\}\}")
INLINE_CODE_RE = re.compile(r"`[^`]+`")

# Heuristicas anti-slop ([AVISO])
BANNED_PATTERNS: List[Tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bprecisão cirúrgica\b", re.IGNORECASE), 'jargao pomposo ("precisao cirurgica")'),
    (re.compile(r"\bcirúrgic[oa]s?\b", re.IGNORECASE), 'jargao pomposo ("cirurgico/a")'),
    (re.compile(r"\bmagistral(?:mente)?\b", re.IGNORECASE), 'jargao pomposo ("magistral")'),
    (re.compile(r"\bimpecáve(?:l|is)\b", re.IGNORECASE), 'jargao pomposo ("impecavel")'),
    (re.compile(r"\beloquente(?:s|mente)?\b", re.IGNORECASE), 'jargao pomposo ("eloquente")'),
    (re.compile(r"\blapidar\b", re.IGNORECASE), 'jargao pomposo ("lapidar")'),
    (re.compile(r"\brobust[oa]s?\b", re.IGNORECASE), 'possivel uso vazio de "robusto"'),
    (re.compile(r"\bilusão reconfortante\b", re.IGNORECASE), 'cliche de LLM ("ilusao reconfortante")'),
    (re.compile(r"\bbala de prata\b", re.IGNORECASE), 'cliche de LLM ("bala de prata")'),
    (re.compile(r"\bneste post(?:,)? vamos\b", re.IGNORECASE), 'abertura cliche ("Neste post vamos...")'),
    (re.compile(r"\bvale ressaltar\b", re.IGNORECASE), 'cliche de LLM ("Vale ressaltar...")'),
    (re.compile(r"\bdecisão crucial\b", re.IGNORECASE), 'cliche de LLM ("decisao crucial")'),
    (re.compile(r"\banomalia bizarra\b", re.IGNORECASE), 'dupla redundante ("anomalia bizarra")'),
    (re.compile(r"\banarquia caótica\b", re.IGNORECASE), 'dupla redundante ("anarquia caotica")'),
    (re.compile(r"\bprova cabal\b", re.IGNORECASE), 'dupla redundante ("prova cabal")'),
    (re.compile(r"\barma destrutiva\b", re.IGNORECASE), 'dupla redundante ("arma destrutiva")'),
    (
        re.compile(r"(?<!-)\bamerican[oa]s?\b", re.IGNORECASE),
        'gentilico dos EUA: prefira "estadunidense" ou "dos EUA"',
    ),
]

BUREAUCRATIC_OPENERS_RE = re.compile(
    r"^(?:Além disso|Nesse sentido|Nesse contexto|Dessa forma|Por outro lado|Em suma|Portanto)\b",
    re.IGNORECASE,
)

MENTE_WORD_RE = re.compile(r"\b([a-záàâãéêíóôõúç]{5,}mente)\b", re.IGNORECASE)
MENTE_NON_ADVERBS = {
    "semente", "clemente", "demente", "dormente", "tormente", "fermente",
    "comente", "aumente", "alimente", "experimente", "implemente", "documente",
    "argumente", "lamente", "fomente", "fragmente", "sedimente", "movimente",
    "pavimente", "orçamente", "regimente", "complemente", "suplemente",
    "instrumente", "arrebente", "acrescente", "apresente", "represente",
    "frequente", "consequente", "subsequente", "permanente", "pertinente",
    "iminente", "eminente", "proeminente", "continente", "abstinete",
}

BINARY_CONTRAST_RE = re.compile(
    r"\bnão\s+(?:é|era|foi|são|eram|foram|morreu|nasce|nasceu|está|estava|vem|veio|funciona|serve|se trata)\b"
    r"[^.!?]{3,110}[.;]\s+"
    r"(?:(?:Ele|Ela|Eles|Elas|Isso|Isto|Mas)\s+)?"
    r"(?:é|era|foi|são|eram|foram|morreu|nasce|nasceu|está|estava|vem|veio|funciona|serve|trata-se)\b",
    re.IGNORECASE,
)

CLIFFHANGER_RE = re.compile(
    r"(?:Guarde esse ponto\.|E isso muda tudo\.|E não para por aí\.|Simples assim\.)",
    re.IGNORECASE,
)

SYMMETRIC_LIST_ITEM_RE = re.compile(r"^\s*[-*]\s+\*\*[^*]{2,60}\*\*\s*:?\s+(.+)$")

ENCYCLOPEDIC_OPEN_RE = re.compile(
    r"^(?:O|A|Os|As)\s+[A-Za-zÀ-ÿ0-9_.-]{2,30}\s+é\s+um(?:a)?\s+"
    r"(?:sistema|ferramenta|protocolo|framework|biblioteca|conceito|serviço|componente|"
    r"mecanismo|padrão|linguagem|tecnologia|plataforma|processo|método|software|utilitário)\b"
)


@dataclass
class Issue:
    severity: str  # "ERRO" | "AVISO"
    line: int
    rule: str
    message: str


def strip_inline_code(text: str) -> str:
    return INLINE_CODE_RE.sub("", text)


def parse_front_matter(lines: List[str]) -> Tuple[Optional[Dict[str, object]], int, List[Issue]]:
    """Extrai front matter YAML basico sem depender de PyYAML."""
    issues: List[Issue] = []
    if not lines or lines[0].strip() != "---":
        issues.append(Issue("ERRO", 1, "front-matter", "Front matter YAML ausente na linha 1."))
        return None, 0, issues

    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx == -1:
        issues.append(Issue("ERRO", 1, "front-matter", "Front matter YAML nao fechado com '---'."))
        return None, 0, issues

    fm: Dict[str, object] = {}
    current_key: Optional[str] = None
    for idx in range(1, end_idx):
        raw = lines[idx]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Item de lista YAML pertencente a current_key
        if re.match(r"^\s+-\s+", raw) and current_key is not None:
            item = re.sub(r"^\s+-\s+", "", raw).strip().strip('"').strip("'")
            existing = fm.get(current_key)
            if isinstance(existing, list):
                existing.append(item)
            else:
                fm[current_key] = [item]
            continue

        m = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        # Remove comentario inline fora de aspas
        if not (val.startswith('"') or val.startswith("'")):
            val = re.sub(r"\s+#.*$", "", val).strip()
        current_key = key

        if val == "":
            fm[key] = []
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            items = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()] if inner else []
            fm[key] = items
        elif val.lower() in ("true", "false"):
            fm[key] = val.lower() == "true"
        else:
            fm[key] = val.strip('"').strip("'")

    return fm, end_idx + 1, issues


def validate_front_matter(fm: Dict[str, object]) -> List[Issue]:
    issues: List[Issue] = []
    missing = sorted(REQUIRED_FM_KEYS - set(fm.keys()))
    if missing:
        issues.append(Issue("ERRO", 1, "front-matter", f"Campos obrigatorios ausentes: {', '.join(missing)}."))

    if fm.get("layout") and fm.get("layout") != "post":
        issues.append(Issue("ERRO", 1, "front-matter", f"layout esperado 'post', encontrado '{fm.get('layout')}'."))

    if "author" in fm and not isinstance(fm["author"], list):
        issues.append(Issue("ERRO", 1, "front-matter", "Campo 'author' deve ser lista YAML (ex.: - \"Eduardo N. S. R.\")."))

    cat = fm.get("category")
    if cat is not None and cat not in VALID_CATEGORIES:
        issues.append(
            Issue(
                "ERRO",
                1,
                "categoria",
                f"Categoria invalida '{cat}'. Use: {', '.join(sorted(VALID_CATEGORIES))}.",
            )
        )

    tags = fm.get("tags")
    if isinstance(tags, list):
        if not (2 <= len(tags) <= 6):
            issues.append(Issue("ERRO", 1, "tags", f"Use entre 2 e 6 tags (encontradas: {len(tags)})."))
        if isinstance(cat, str):
            for t in tags:
                if t.lower() == cat.lower():
                    issues.append(Issue("ERRO", 1, "tags", f"Tag '{t}' e identica a category '{cat}'."))
    elif "tags" in fm:
        issues.append(Issue("ERRO", 1, "tags", "Campo 'tags' deve ser uma lista YAML."))

    return issues


def lint_mermaid_block(block_lines: List[Tuple[int, str]]) -> List[Issue]:
    issues: List[Issue] = []
    in_subgraph = False
    subgraph_start = 0
    subgraph_nodes = set()

    for lineno, line in block_lines:
        if EMOJI_RE.search(line):
            issues.append(Issue("ERRO", lineno, "mermaid-emoji", "Emoji encontrado dentro de bloco Mermaid."))
        if "──>" in line or "──" in line:
            issues.append(Issue("ERRO", lineno, "mermaid-seta", "Seta tipografica em Mermaid; use ASCII ('-->' ou '==>')."))

        stripped = line.strip()
        if stripped.startswith("subgraph "):
            in_subgraph = True
            subgraph_start = lineno
            subgraph_nodes = set()
            continue
        if in_subgraph and stripped == "end":
            if len(subgraph_nodes) == 1:
                issues.append(
                    Issue(
                        "ERRO",
                        subgraph_start,
                        "mermaid-subgraph",
                        "subgraph envolve apenas 1 no; use subgraph apenas para agrupar 2+ nos.",
                    )
                )
            in_subgraph = False
            continue
        if in_subgraph and stripped and not stripped.startswith(("direction ", "class ", "style ", "%%")):
            # Captura identificadores de nos definidos ou conectados
            for node_id in re.findall(r"\b([A-Za-z][A-Za-z0-9_]*)\s*(?:\[|\(|\{|-->|==>|--|-\.-)", stripped):
                if node_id not in {"subgraph", "end", "class", "style", "direction"}:
                    subgraph_nodes.add(node_id)

    return issues


def lint_post(path: Path) -> List[Issue]:
    raw_bytes = path.read_bytes()
    issues: List[Issue] = []

    if b"\r\n" in raw_bytes:
        issues.append(Issue("ERRO", 1, "line-endings", "Arquivo usa CRLF (\\r\\n); converta para LF (\\n)."))

    text = raw_bytes.decode("utf-8", errors="replace").replace("\r\n", "\n")
    lines = text.split("\n")

    fm, body_start, fm_issues = parse_front_matter(lines)
    issues.extend(fm_issues)
    if fm is not None:
        issues.extend(validate_front_matter(fm))

    has_math = bool(fm and fm.get("math") is True)
    has_mermaid_fm = bool(fm and fm.get("mermaid") is True)
    found_mermaid_block = False

    in_fence = False
    fence_char = ""
    fence_len = 0
    fence_lang = ""
    mermaid_buf: List[Tuple[int, str]] = []

    in_raw = False
    in_callout = False
    in_references_section = False
    seen_first_prose_para = False
    in_first_prose_para = False
    just_saw_h2 = False

    footnote_refs: Dict[str, List[int]] = {}
    footnote_defs: Dict[str, int] = {}

    # Para analises de blocos/paragrafos e listas
    prose_paragraphs: List[Tuple[int, str, bool]] = []  # (start_line, text, breaks_run)
    cur_para_lines: List[str] = []
    cur_para_start = 0
    para_break_pending = True

    sym_list_run: List[Tuple[int, int]] = []  # (lineno, content_len)

    def flush_paragraph() -> None:
        nonlocal cur_para_lines, cur_para_start, seen_first_prose_para, in_first_prose_para
        nonlocal para_break_pending, just_saw_h2
        if not cur_para_lines:
            return
        joined = " ".join(x.strip() for x in cur_para_lines).strip()
        if joined:
            if not seen_first_prose_para:
                seen_first_prose_para = True
                in_first_prose_para = False
            prose_paragraphs.append((cur_para_start, joined, para_break_pending))
            para_break_pending = False

            # Checagem de abertura enciclopedica logo apos ##
            if just_saw_h2 and ENCYCLOPEDIC_OPEN_RE.search(joined):
                issues.append(
                    Issue(
                        "AVISO",
                        cur_para_start,
                        "in-media-res",
                        "Possivel abertura enciclopedica apos '##'; prefira abrir direto no problema ou tese.",
                    )
                )
            just_saw_h2 = False

            # Checagem de dois $ soltos no mesmo paragrafo quando math: true
            if has_math:
                clean = strip_inline_code(joined)
                # Remove $$...$$ de display math
                clean = re.sub(r"\$\$[^$]+\$\$", "", clean)
                # Detecta valores monetarios com $ sem escape (US$, R$, $100)
                money_dollars = re.findall(r"(?<!\\)(?:US\$|R\$|\$\s?\d)", clean)
                if len(money_dollars) >= 2:
                    issues.append(
                        Issue(
                            "ERRO",
                            cur_para_start,
                            "katex-dollar",
                            "Dois '$' monetarios/soltos no mesmo paragrafo com math: true; escape '\\$' ou escreva por extenso.",
                        )
                    )
        cur_para_lines = []
        cur_para_start = 0

    def flush_sym_list() -> None:
        nonlocal sym_list_run
        if len(sym_list_run) >= 3:
            lengths = [ln for _, ln in sym_list_run]
            min_l, max_l = min(lengths), max(lengths)
            if min_l > 0 and (max_l / min_l) <= 1.8:
                start_l = sym_list_run[0][0]
                end_l = sym_list_run[-1][0]
                issues.append(
                    Issue(
                        "AVISO",
                        start_l,
                        "lista-simetrica",
                        f"Lista simetrica (L{start_l}-L{end_l}, {len(sym_list_run)} itens '- **Negrito:**' de tamanho parecido); varie pesos ou dissolva em prosa.",
                    )
                )
        sym_list_run = []

    for idx in range(body_start, len(lines)):
        lineno = idx + 1
        line = lines[idx]
        stripped = line.strip()

        # Controle de blocos {% raw %} / {% endraw %} (inclusive dentro de code blocks)
        raw_opened_here = "{% raw %}" in line or "{%- raw -%}" in line
        raw_closed_here = "{% endraw %}" in line or "{%- endraw -%}" in line

        # Checagem de Liquid desprotegido (Jekyll processa Liquid mesmo dentro de code blocks!)
        if not in_raw and not raw_opened_here:
            for lm in LIQUID_TAG_RE.finditer(line):
                tag_name = lm.group(1)
                if tag_name is None or tag_name not in ALLOWED_LIQUID_TAGS:
                    issues.append(
                        Issue(
                            "ERRO",
                            lineno,
                            "liquid-raw",
                            f"Sintaxe Liquid '{lm.group(0)[:30]}' fora de '{{% raw %}}'; proteja pontualmente se for codigo.",
                        )
                    )

        if raw_opened_here and not raw_closed_here:
            in_raw = True
        elif raw_closed_here:
            in_raw = False

        # Controle de code fences
        fm_match = FENCE_RE.match(line)
        if fm_match:
            f_str = fm_match.group(2)
            f_rest = fm_match.group(3).strip()
            if not in_fence:
                flush_paragraph()
                flush_sym_list()
                para_break_pending = True
                in_callout = False
                in_fence = True
                fence_char = f_str[0]
                fence_len = len(f_str)
                fence_lang = f_rest.split()[0].lower() if f_rest else ""
                if fence_lang == "mermaid":
                    found_mermaid_block = True
                    mermaid_buf = []
                continue
            elif f_str[0] == fence_char and len(f_str) >= fence_len and not f_rest:
                if fence_lang == "mermaid":
                    issues.extend(lint_mermaid_block(mermaid_buf))
                    mermaid_buf = []
                in_fence = False
                fence_char = ""
                fence_len = 0
                fence_lang = ""
                continue

        if in_fence:
            if fence_lang == "mermaid":
                mermaid_buf.append((lineno, line))
            continue

        # Linha vazia fecha paragrafo, callout e lista
        if not stripped:
            flush_paragraph()
            flush_sym_list()
            in_callout = False
            continue

        # Divisor horizontal no corpo
        if stripped in ("---", "***", "___"):
            flush_paragraph()
            flush_sym_list()
            para_break_pending = True
            if stripped == "---":
                issues.append(Issue("ERRO", lineno, "sem-divisor", "Divisor '---' proibido no corpo do post."))
            continue

        # Includes Liquid isolados (ex.: toc.html)
        if stripped.startswith("{%") and stripped.endswith("%}"):
            flush_paragraph()
            flush_sym_list()
            para_break_pending = True
            continue

        # Tags HTML de bloco (<details>, </details>, <summary>, etc.)
        if stripped.startswith("<") and stripped.endswith(">"):
            flush_paragraph()
            flush_sym_list()
            para_break_pending = True
            continue

        # Tabelas Markdown (checa invariantes de texto e coleta footnotes, sem contar como paragrafo)
        if stripped.startswith("|"):
            flush_paragraph()
            flush_sym_list()
            para_break_pending = True
            clean_tbl = strip_inline_code(line)
            if "\u2014" in clean_tbl:
                issues.append(Issue("ERRO", lineno, "sem-travessao", "Travessao longo (U+2014) proibido em tabela."))
            if UNICODE_ARROWS_RE.search(clean_tbl):
                issues.append(Issue("ERRO", lineno, "setas-ascii", "Seta Unicode em tabela; use ASCII ('->', '<-', '=>')."))
            if EMOJI_RE.search(clean_tbl):
                issues.append(Issue("ERRO", lineno, "sem-emoji-prosa", "Emoji solto em tabela; permitido apenas dentro de callouts."))
            for ilm in INTERNAL_LINK_RE.finditer(clean_tbl):
                issues.append(
                    Issue(
                        "ERRO",
                        lineno,
                        "link-interno",
                        f"Link interno hardcoded '{ilm.group(1)}'; use '{{% include post-ref.html slug=\"...\" %}}'.",
                    )
                )
            for ref_m in FOOTNOTE_REF_RE.finditer(clean_tbl):
                footnote_refs.setdefault(ref_m.group(1), []).append(lineno)
            continue

        # Callouts / Blockquotes
        if CALLOUT_START_RE.match(line):
            flush_paragraph()
            flush_sym_list()
            para_break_pending = True
            in_callout = True
            if FOOTNOTE_REF_RE.search(strip_inline_code(line)):
                issues.append(Issue("ERRO", lineno, "callout-footnote", "Footnote [^n] proibido dentro de callout."))
            continue
        if stripped.startswith(">"):
            flush_paragraph()
            flush_sym_list()
            para_break_pending = True
            clean_q = strip_inline_code(line)
            if in_callout and FOOTNOTE_REF_RE.search(clean_q):
                issues.append(Issue("ERRO", lineno, "callout-footnote", "Footnote [^n] proibido dentro de callout."))
            elif not in_callout:
                for ref_m in FOOTNOTE_REF_RE.finditer(clean_q):
                    footnote_refs.setdefault(ref_m.group(1), []).append(lineno)
            if "\u2014" in clean_q:
                issues.append(Issue("ERRO", lineno, "sem-travessao", "Travessao longo (U+2014) proibido."))
            if UNICODE_ARROWS_RE.search(clean_q):
                issues.append(Issue("ERRO", lineno, "setas-ascii", "Seta Unicode em prosa; use ASCII ('->', '<-', '=>')."))
            continue
        else:
            in_callout = False

        # Definicao de footnote
        fn_def = FOOTNOTE_DEF_RE.match(stripped)
        if fn_def:
            flush_paragraph()
            flush_sym_list()
            para_break_pending = True
            fn_id = fn_def.group(1)
            fn_body = fn_def.group(2)
            footnote_defs[fn_id] = lineno
            if not in_references_section:
                issues.append(
                    Issue(
                        "ERRO",
                        lineno,
                        "footnote-secao",
                        f"Definicao [^{fn_id}] fora da secao '## Referências'.",
                    )
                )
            # Checa parenteses nao encodados dentro da URL de ([Link](url))
            if re.search(r"\]\(https?://[^)\s]*\([^)]*\)", fn_body):
                issues.append(
                    Issue(
                        "ERRO",
                        lineno,
                        "url-parenteses",
                        f"URL em [^{fn_id}] contem parenteses literais; encode como %28/%29.",
                    )
                )
            continue

        # Cabecalhos
        h_match = HEADING_RE.match(line)
        if h_match:
            flush_paragraph()
            flush_sym_list()
            para_break_pending = True
            hashes, title_text = h_match.group(1), h_match.group(2)
            level = len(hashes)
            if level == 1:
                issues.append(Issue("ERRO", lineno, "sem-h1", "H1 ('#') proibido no corpo do post; comece em '##'."))
            if "`" in title_text:
                issues.append(Issue("ERRO", lineno, "titulo-limpo", f"Backtick/codigo inline proibido em cabecalho: '{title_text}'."))
            if re.search(r"\[[^\]]+\]\([^)]+\)", title_text):
                issues.append(Issue("ERRO", lineno, "titulo-limpo", f"Link Markdown proibido em cabecalho: '{title_text}'."))
            if FOOTNOTE_REF_RE.search(title_text):
                issues.append(Issue("ERRO", lineno, "titulo-limpo", f"Footnote proibido em cabecalho: '{title_text}'."))
            if "\u2014" in title_text:
                issues.append(Issue("ERRO", lineno, "sem-travessao", "Travessao longo (U+2014) proibido em cabecalho."))
            if EMOJI_RE.search(title_text):
                issues.append(Issue("ERRO", lineno, "sem-emoji-prosa", "Emoji proibido em cabecalho."))

            in_references_section = level == 2 and title_text.strip().lower().startswith("referência")
            just_saw_h2 = level == 2 and not in_references_section and title_text.strip().lower() != "exercícios"
            continue

        # Checagens comuns de linha de prosa/lista (fora de codigo inline)
        clean_line = strip_inline_code(line)

        if "\u2014" in clean_line:
            issues.append(Issue("ERRO", lineno, "sem-travessao", "Travessao longo (U+2014) proibido; use virgula, parenteses ou dois-pontos."))
        if UNICODE_ARROWS_RE.search(clean_line):
            issues.append(Issue("ERRO", lineno, "setas-ascii", "Seta Unicode em prosa; use ASCII ('->', '<-', '=>')."))
        if EMOJI_RE.search(clean_line):
            issues.append(Issue("ERRO", lineno, "sem-emoji-prosa", "Emoji solto em prosa; permitido apenas dentro de callouts."))
        for ilm in INTERNAL_LINK_RE.finditer(clean_line):
            issues.append(
                Issue(
                    "ERRO",
                    lineno,
                    "link-interno",
                    f"Link interno hardcoded '{ilm.group(1)}'; use '{{% include post-ref.html slug=\"...\" %}}'.",
                )
            )
        for ref_m in FOOTNOTE_REF_RE.finditer(clean_line):
            fn_id = ref_m.group(1)
            footnote_refs.setdefault(fn_id, []).append(lineno)

        # Itens de lista
        if re.match(r"^\s*(?:[-*+]|\d+\.)\s+", line):
            flush_paragraph()
            para_break_pending = True
            just_saw_h2 = False
            sym_m = SYMMETRIC_LIST_ITEM_RE.match(line)
            if sym_m:
                sym_list_run.append((lineno, len(sym_m.group(1).strip())))
            else:
                flush_sym_list()
            # Aplica vocabulario banido em itens de lista tambem
            for pat, desc in BANNED_PATTERNS:
                if pat.search(clean_line):
                    issues.append(Issue("AVISO", lineno, "antipadrao-lexical", f"Detectado {desc}."))
            continue
        else:
            flush_sym_list()

        # Linha de paragrafo de prosa
        if not cur_para_lines:
            cur_para_start = lineno
            if not seen_first_prose_para:
                in_first_prose_para = True

        if in_first_prose_para and FOOTNOTE_REF_RE.search(clean_line):
            issues.append(
                Issue(
                    "ERRO",
                    lineno,
                    "primeiro-paragrafo-footnote",
                    "Footnote [^n] proibido no primeiro paragrafo (polui o excerpt da Home).",
                )
            )

        cur_para_lines.append(line)

    # Flush final
    flush_paragraph()
    flush_sym_list()

    # Mermaid vs front matter
    if found_mermaid_block and not has_mermaid_fm:
        issues.append(Issue("ERRO", 1, "mermaid-front-matter", "Bloco Mermaid encontrado sem 'mermaid: true' no front matter."))

    # Consistencia de footnotes
    for fn_id, ref_lines in footnote_refs.items():
        if fn_id not in footnote_defs:
            issues.append(Issue("ERRO", ref_lines[0], "footnote-orfao", f"Referencia [^{fn_id}] sem definicao em '## Referências'."))
    for fn_id, def_line in footnote_defs.items():
        if fn_id not in footnote_refs:
            issues.append(Issue("ERRO", def_line, "footnote-nao-usado", f"Definicao [^{fn_id}] nao e referenciada no texto."))

    # --- Heuristicas sobre paragrafos de prosa ([AVISO]) ---
    binary_contrast_hits: List[Tuple[int, str]] = []

    for start_line, para, _ in prose_paragraphs:
        clean_para = strip_inline_code(para)
        # Ignora legendas curtas em italico (*Comando para...*)
        if clean_para.startswith("*") and clean_para.endswith("*") and len(clean_para) < 160:
            continue

        # Vocabulario banido
        for pat, desc in BANNED_PATTERNS:
            if pat.search(clean_para):
                issues.append(Issue("AVISO", start_line, "antipadrao-lexical", f"Detectado {desc}."))

        # Abertura burocratica
        bm = BUREAUCRATIC_OPENERS_RE.match(clean_para)
        if bm:
            issues.append(
                Issue(
                    "AVISO",
                    start_line,
                    "conectivo-burocratico",
                    f'Paragrafo aberto com muleta de transicao ("{bm.group(0)}"); prefira justaposicao direta ou transicao seca.',
                )
            )

        # Densidade de adverbios em -mente
        mente_hits = [
            w for w in MENTE_WORD_RE.findall(clean_para)
            if w.lower() not in MENTE_NON_ADVERBS
        ]
        if len(mente_hits) >= 2:
            issues.append(
                Issue(
                    "AVISO",
                    start_line,
                    "adverbios-mente",
                    f"Alta densidade de adverbios em -mente ({len(mente_hits)} no paragrafo: {', '.join(mente_hits[:4])}).",
                )
            )

        # Contraste binario (coleta todos; so avisa se >= 2 no post)
        for bcm in BINARY_CONTRAST_RE.finditer(clean_para):
            binary_contrast_hits.append((start_line, bcm.group(0)[:70]))

        # Micro-cliffhangers dramaticos
        cm = CLIFFHANGER_RE.search(clean_para)
        if cm:
            issues.append(
                Issue(
                    "AVISO",
                    start_line,
                    "cliffhanger-ia",
                    f'Micro-cliffhanger dramatico detectado ("{cm.group(0)}"); avalie cortar ou integrar a prosa.',
                )
            )

    if len(binary_contrast_hits) >= 2:
        for hit_line, snippet in binary_contrast_hits:
            issues.append(
                Issue(
                    "AVISO",
                    hit_line,
                    "contraste-binario",
                    f'Contraste binario repetido ({len(binary_contrast_hits)}x no post): "{snippet}...".',
                )
            )

    # Monotonia visual e abertura repetida em paragrafos consecutivos
    runs: List[List[Tuple[int, str]]] = []
    cur_run: List[Tuple[int, str]] = []
    for start_line, para, breaks in prose_paragraphs:
        if para.startswith("*") and para.endswith("*") and len(para) < 160:
            if cur_run:
                runs.append(cur_run)
                cur_run = []
            continue
        if breaks and cur_run:
            runs.append(cur_run)
            cur_run = []
        cur_run.append((start_line, para))
    if cur_run:
        runs.append(cur_run)

    for run in runs:
        # Janela deslizante de 3 paragrafos consecutivos com extensao visual parecida
        i = 0
        while i <= len(run) - 3:
            window = run[i : i + 3]
            lens = [len(p) for _, p in window]
            avg = sum(lens) / 3.0
            if 180 <= avg <= 650 and all(abs(l - avg) / avg <= 0.22 for l in lens):
                issues.append(
                    Issue(
                        "AVISO",
                        window[0][0],
                        "monotonia-visual",
                        f"3 paragrafos seguidos com extensao visual quase identica (L{window[0][0]}, L{window[1][0]}, L{window[2][0]}: {lens} chars); crie contraste visual.",
                    )
                )
                i += 3
            else:
                i += 1

        # 3 paragrafos seguidos iniciando com a mesma palavra
        j = 0
        while j <= len(run) - 3:
            first_words = [re.findall(r"[A-Za-zÀ-ÿ]+", p)[:1] for _, p in run[j : j + 3]]
            words = [w[0].lower() if w else "" for w in first_words]
            if words[0] and words[0] == words[1] == words[2]:
                issues.append(
                    Issue(
                        "AVISO",
                        run[j][0],
                        "abertura-repetida",
                        f'3 paragrafos seguidos abertos com "{words[0]}" (L{run[j][0]}, L{run[j+1][0]}, L{run[j+2][0]}); quebre a ordem direta.',
                    )
                )
                j += 3
            else:
                j += 1

    issues.sort(key=lambda x: (0 if x.severity == "ERRO" else 1, x.line, x.rule))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida posts do blog vndmtrx.github.io.")
    parser.add_argument("post", type=Path, help="Caminho para o arquivo Markdown do post.")
    parser.add_argument("--strict", action="store_true", help="Retorna exit code 1 tambem se houver [AVISO].")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Imprime relatorio em JSON.")
    args = parser.parse_args()

    if not args.post.is_file():
        print(f"[ERRO] Arquivo nao encontrado: {args.post}", file=sys.stderr)
        return 2

    issues = lint_post(args.post)
    errors = [i for i in issues if i.severity == "ERRO"]
    warnings = [i for i in issues if i.severity == "AVISO"]

    if args.as_json:
        print(
            json.dumps(
                {
                    "file": str(args.post),
                    "errors": len(errors),
                    "warnings": len(warnings),
                    "issues": [asdict(i) for i in issues],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"=== {args.post} | {len(errors)} ERRO(s), {len(warnings)} AVISO(s) ===")
        for item in issues:
            print(f"[{item.severity}] L{item.line} ({item.rule}): {item.message}")
        if not issues:
            print("OK: nenhuma invariante violada e nenhum alerta anti-slop.")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
