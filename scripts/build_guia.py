#!/usr/bin/env python3
"""Converte GUIA.md + guias/*.md numa página HTML publicável.

Uso: python3 scripts/build_guia.py [saida.html]

Conversor escrito à mão para não adicionar dependência ao repo — cobre exatamente
o subconjunto de markdown que os guias usam.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Ordem de leitura sugerida, não alfabética.
TOPICS = [
    ("numeros-e-ceticismo", "Números e Ceticismo", "⚠️", "leia antes de tudo"),
    ("agencia-ia", "Agência de IA", "🤖", "o caminho mais rápido para caixa"),
    ("saas-produto", "SaaS e Produto Digital", "💻", "recorrência com IA"),
    ("low-ticket", "Low Ticket e Tráfego Pago", "🎯", "adquirir cliente pagando"),
    ("negocio-solo", "Negócio Solo", "🧠", "Hormozi e mentalidade"),
    ("copy-e-criativo", "Copy e Criativo", "✍️", "o que vende"),
    ("ecommerce", "E-commerce", "📦", "o experimento honesto"),
]


def inline(text):
    out = []
    for i, chunk in enumerate(re.split(r"(`[^`]+`)", text)):
        if i % 2:
            out.append(f"<code>{html.escape(chunk[1:-1])}</code>")
            continue
        c = html.escape(chunk)
        c = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: _link(m), c)
        c = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", c)
        c = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", c)
        out.append(c)
    return "".join(out)


def _link(m):
    """Links entre guias viram âncoras internas; o resto fica como está."""
    label, href = m.group(1), m.group(2)
    stem = re.sub(r"^(guias/)?", "", href).replace(".md", "").split("#")[0]
    if stem in dict((t[0], t) for t in TOPICS):
        return f'<a href="#t-{stem}">{label}</a>'
    if href.endswith(".md") or href.startswith("references/"):
        return label  # caminho de repo: não é clicável na web
    return f'<a href="{href}">{label}</a>'


def slug(prefix, text):
    s = re.sub(r"[^\w\s-]", "", re.sub(r"<[^>]+>", "", text)).strip().lower()
    return f"{prefix}-{re.sub(r'[\s_]+', '-', s)}"


def render_table(rows):
    def cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]

    head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
    out = ['<div class="scroll"><table><thead><tr>']
    out += [f"<th>{inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def render_list(items):
    checklist = any(re.match(r"\[[ x]\]\s", t) for _, t in items)
    out = [f'<ul{" class=\"check\"" if checklist else ""}>']
    depth = 0
    for ind, text in items:
        want = 1 if ind >= 2 else 0
        while depth < want:
            out.append("<ul>")
            depth += 1
        while depth > want:
            out.append("</ul>")
            depth -= 1
        m = re.match(r"\[([ x])\]\s+(.*)", text)
        out.append(
            f"<li><span></span>{inline(m.group(2))}</li>" if m else f"<li>{inline(text)}</li>"
        )
    out.append("</ul>" * (depth + 1))
    return "".join(out)


def convert(md, prefix, base_level=0):
    """base_level desloca os títulos (h1 do guia vira h2 da página)."""
    lines = md.split("\n")
    body, subs = [], []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            body.append(
                f'<div class="scroll"><pre><code>{html.escape(chr(10).join(block))}</code></pre></div>'
            )
            continue

        if re.fullmatch(r"-{3,}", stripped):
            body.append("<hr>")
            i += 1
            continue

        m = re.match(r"(#{1,4})\s+(.*)", stripped)
        if m:
            lvl, text = min(len(m.group(1)) + base_level, 6), m.group(2)
            sid = slug(prefix, text)
            if lvl == 3:
                label = text.split(" — ")[0].strip()
                subs.append((sid, label))
            body.append(f'<h{lvl} id="{sid}">{inline(text)}</h{lvl}>')
            i += 1
            continue

        if stripped.startswith(">"):
            quotes = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quotes.append(lines[i].strip().lstrip(">").strip())
                i += 1
            if len(quotes) > 1 and not quotes[1].startswith("*"):
                quotes = [" ".join(quotes)]
            inner = "".join(f"<p>{inline(q)}</p>" for q in quotes if q)
            body.append(f"<blockquote>{inner}</blockquote>")
            continue

        if stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            body.append(render_table(rows))
            continue

        if re.match(r"[-*\d]\.?\s", stripped) and re.match(r"[-*]\s|\d+\.\s", stripped):
            ordered = bool(re.match(r"\d+\.\s", stripped))
            items = []
            while i < len(lines):
                cur = lines[i]
                if re.match(r"\s*([-*]\s|\d+\.\s)", cur):
                    ind = len(cur) - len(cur.lstrip())
                    items.append((ind, re.sub(r"^\s*([-*]|\d+\.)\s+", "", cur).strip()))
                    i += 1
                elif cur.strip() and not re.match(r"\s*[|>#`]", cur) and items:
                    ind, prev = items[-1]
                    items[-1] = (ind, prev + " " + cur.strip())
                    i += 1
                else:
                    break
            rendered = render_list(items)
            if ordered:
                rendered = rendered.replace("<ul>", "<ol>").replace("</ul>", "</ol>")
            body.append(rendered)
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
            r"\s*([-*]\s|\d+\.\s|[|>#]|```|-{3,}$)", lines[i]
        ):
            para.append(lines[i].strip())
            i += 1
        body.append(f"<p>{inline(' '.join(para))}</p>")

    return "".join(body), subs


CSS = """
:root{
  --ground:#F5F6F4; --surface:#FFFFFF; --surface-2:#EDEFEB;
  --ink:#14201C; --ink-soft:#4A5551; --ink-faint:#78837D;
  --rule:#DDE0DA; --accent:#0F5C4A; --accent-soft:#E4EFEA;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#101512; --surface:#171E1A; --surface-2:#1E2723;
    --ink:#E6EAE6; --ink-soft:#9AA8A1; --ink-faint:#75837C;
    --rule:#2A342F; --accent:#4FBF9B; --accent-soft:#1B2C26;
  }
}
:root[data-theme="dark"]{
  --ground:#101512; --surface:#171E1A; --surface-2:#1E2723;
  --ink:#E6EAE6; --ink-soft:#9AA8A1; --ink-faint:#75837C;
  --rule:#2A342F; --accent:#4FBF9B; --accent-soft:#1B2C26;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--serif); font-size:17px; line-height:1.68;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1220px;margin:0 auto;padding:0 24px;display:flex;gap:52px;align-items:flex-start}
main{flex:1;min-width:0;max-width:70ch;padding:52px 0 120px}

nav{
  position:sticky; top:0; width:228px; flex:none;
  padding:60px 0 40px; font-family:var(--mono); font-size:11px;
  max-height:100vh; overflow-y:auto;
}
nav p{
  margin:0 0 12px; text-transform:uppercase; letter-spacing:.14em;
  color:var(--ink-faint); font-size:9.5px;
}
nav a{
  display:block; padding:6px 0 6px 11px; border-left:2px solid var(--rule);
  color:var(--ink-soft); text-decoration:none; line-height:1.35;
}
nav a:hover{border-left-color:var(--accent);color:var(--accent)}
nav a b{display:block;font-weight:600;color:var(--ink);letter-spacing:.01em}
nav a span{display:block;color:var(--ink-faint);font-size:9.5px;margin-top:1px}
nav .sub{padding-left:22px;border-left-color:transparent;font-size:10px}
nav .sub:hover{border-left-color:var(--rule)}
@media(max-width:960px){nav{display:none}.wrap{gap:0}main{max-width:none;padding-top:36px}}

h1,h2,h3,h4,h5{font-family:var(--sans);text-wrap:balance;line-height:1.18;letter-spacing:-.02em}
h1{font-size:clamp(30px,5vw,44px);font-weight:750;margin:0 0 6px}
h2{
  font-size:clamp(23px,3.4vw,31px); font-weight:750; margin:0 0 8px;
  padding-top:26px;
}
h3{font-size:19px;font-weight:700;margin:46px 0 14px;padding-top:18px;border-top:1px solid var(--rule)}
h4{font-size:16px;font-weight:680;margin:30px 0 10px}
h5{font-size:14px;font-weight:680;margin:24px 0 8px;color:var(--ink-soft)}

.topic{margin:80px 0 0;padding-top:30px;border-top:2px solid var(--ink)}
.topic .kicker{
  font-family:var(--mono);font-size:10px;text-transform:uppercase;
  letter-spacing:.17em;color:var(--accent);margin:0 0 10px;
}

p{margin:0 0 17px}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px}
strong{font-weight:640}
hr{border:0;height:1px;background:var(--rule);margin:40px 0}

ul,ol{margin:0 0 18px;padding-left:22px}
li{margin-bottom:7px}
li::marker{color:var(--ink-faint)}
ul ul,ol ol,ul ol,ol ul{margin:7px 0 0}
ul.check{list-style:none;padding-left:0}
ul.check li{position:relative;padding-left:29px}
ul.check li span{
  position:absolute;left:0;top:.36em;width:15px;height:15px;
  border:1.5px solid var(--ink-faint);border-radius:3px;
}

blockquote{
  margin:22px 0;padding:15px 20px;background:var(--surface);
  border-left:3px solid var(--accent);border-radius:0 4px 4px 0;
}
blockquote p{margin:0 0 9px;font-size:16px;color:var(--ink-soft)}
blockquote p:last-child{margin:0}
blockquote em{color:var(--ink);font-style:italic}

.scroll{overflow-x:auto;margin:24px 0;-webkit-overflow-scrolling:touch}
table{
  border-collapse:collapse;width:100%;font-family:var(--sans);
  font-size:13.5px;line-height:1.5;font-variant-numeric:tabular-nums;
}
th{
  text-align:left;font-family:var(--mono);font-size:10px;font-weight:600;
  text-transform:uppercase;letter-spacing:.1em;color:var(--ink-faint);
  padding:0 14px 9px 0;border-bottom:1.5px solid var(--ink);white-space:nowrap;
}
td{padding:11px 14px 11px 0;border-bottom:1px solid var(--rule);vertical-align:top}
tr:last-child td{border-bottom:0}
td:first-child{color:var(--ink);font-weight:550}
table code{font-size:12px}

code{
  font-family:var(--mono);font-size:.86em;background:var(--surface-2);
  padding:.14em .38em;border-radius:3px;
}
pre{
  margin:0;background:var(--surface);border:1px solid var(--rule);
  border-radius:5px;padding:17px 19px;overflow-x:auto;
}
pre code{background:none;padding:0;font-size:12.5px;line-height:1.72;color:var(--ink-soft)}

header{padding:60px 0 8px;border-bottom:2px solid var(--ink)}
.eyebrow{
  font-family:var(--mono);font-size:10.5px;text-transform:uppercase;
  letter-spacing:.19em;color:var(--accent);margin:0 0 15px;
}
.lede{font-size:19px;color:var(--ink-soft);margin:16px 0 26px;max-width:60ch}
.stats{display:flex;flex-wrap:wrap;margin:0 0 28px;border-top:1px solid var(--rule)}
.stat{padding:14px 28px 14px 0;margin-right:28px;border-right:1px solid var(--rule)}
.stat:last-child{border-right:0;margin-right:0}
.stat b{
  display:block;font-family:var(--sans);font-size:25px;font-weight:730;
  letter-spacing:-.02em;font-variant-numeric:tabular-nums;line-height:1.1;
}
.stat span{
  display:block;font-family:var(--mono);font-size:9.5px;text-transform:uppercase;
  letter-spacing:.13em;color:var(--ink-faint);margin-top:4px;
}
footer{
  margin-top:70px;padding-top:22px;border-top:1px solid var(--rule);
  font-family:var(--mono);font-size:11px;color:var(--ink-faint);line-height:1.7;
}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
"""


def main():
    hub = (ROOT / "GUIA.md").read_text(encoding="utf-8")
    # O hub vira o sumário: fica só o bloco "Por onde começar" em diante.
    tail = hub.split("## Por onde começar", 1)[1]
    intro, _ = convert("## Por onde começar" + tail, "hub", base_level=0)

    sections, nav = [], []
    for stem, title, emoji, tag in TOPICS:
        md = (ROOT / "guias" / f"{stem}.md").read_text(encoding="utf-8")
        md = md.split("\n", 1)[1]  # descarta o h1 do arquivo
        body, subs = convert(md, stem, base_level=1)
        sections.append(
            f'<section class="topic" id="t-{stem}">'
            f'<p class="kicker">{emoji} {html.escape(tag)}</p>'
            f'<h2>{html.escape(title)}</h2>{body}</section>'
        )
        nav.append(
            f'<a href="#t-{stem}"><b>{html.escape(title)}</b>'
            f'<span>{html.escape(tag)}</span></a>'
            + "".join(f'<a class="sub" href="#{sid}">{html.escape(lbl)}</a>' for sid, lbl in subs[:7])
        )

    out = f"""<title>Central de Estudos</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{CSS}</style>
<div class="wrap">
<nav><p>Tópicos</p><a href="#topo"><b>Por onde começar</b></a>{"".join(nav)}</nav>
<main>
<header id="topo">
  <p class="eyebrow">Biblioteca de transcrições · Síntese operacional</p>
  <h1>Central de Estudos</h1>
  <p class="lede">Agência de IA, SaaS, low ticket, negócio solo, copy e e-commerce —
  destilados da leitura integral de 168 transcrições de YouTube.</p>
  <div class="stats">
    <div class="stat"><b>168</b><span>vídeos lidos</span></div>
    <div class="stat"><b>30+</b><span>canais</span></div>
    <div class="stat"><b>6</b><span>grandes tópicos</span></div>
    <div class="stat"><b>12</b><span>números sem lastro</span></div>
  </div>
</header>
{intro}
{"".join(sections)}
<footer>
  Gerado de <code>GUIA.md</code> + <code>guias/*.md</code>. Cada afirmação é rastreável ao vídeo
  e timestamp em <code>references/youtube/</code>.<br>
  Transcrições automáticas — números e nomes de ferramentas podem conter erros.
</footer>
</main>
</div>
"""
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "GUIA.html"
    dest.write_text(out, encoding="utf-8")
    print(f"{dest}  ({len(out):,} bytes, {len(TOPICS)} tópicos)")


if __name__ == "__main__":
    main()
