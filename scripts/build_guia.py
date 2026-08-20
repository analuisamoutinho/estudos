#!/usr/bin/env python3
"""Converte GUIA.md na página HTML publicável.

Uso: python3 scripts/build_guia.py [saida.html]

Escrito à mão em vez de usar uma lib de markdown para não adicionar dependência
ao repo — cobre exatamente o subconjunto de markdown que o GUIA.md usa.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "GUIA.md"


def inline(text):
    """Formatação inline: código, negrito, itálico, links."""
    out = []
    for i, chunk in enumerate(re.split(r"(`[^`]+`)", text)):
        if i % 2:
            out.append(f"<code>{html.escape(chunk[1:-1])}</code>")
            continue
        c = html.escape(chunk)
        c = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', c)
        c = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", c)
        c = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", c)
        out.append(c)
    return "".join(out)


def slug(text):
    s = re.sub(r"[^\w\s-]", "", re.sub(r"<[^>]+>", "", text)).strip().lower()
    return re.sub(r"[\s_]+", "-", s)


def render_table(rows):
    """rows: linhas cruas de uma tabela markdown (inclui a linha separadora)."""
    def cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]

    head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
    out = ['<div class="scroll"><table><thead><tr>']
    out += [f"<th>{inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        out += [f"<td>{inline(c)}</td>" for c in row]
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def render_list(items):
    """items: [(indent, texto)] — suporta um nível de aninhamento e checkboxes."""
    checklist = any(re.match(r"\[[ x]\]\s", t) for _, t in items)
    cls = ' class="check"' if checklist else ""
    out = [f"<ul{cls}>"]
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
        if m:
            out.append(f"<li><span></span>{inline(m.group(2))}</li>")
        else:
            out.append(f"<li>{inline(text)}</li>")
    out.append("</ul>" * (depth + 1))
    return "".join(out)


def convert(md):
    lines = md.split("\n")
    body, toc = [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

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
            lvl, text = len(m.group(1)), m.group(2)
            sid = slug(text)
            if lvl == 2:
                label, _, rest = text.partition(" — ")
                toc.append((sid, label.strip(), rest.strip()))
            body.append(f'<h{lvl} id="{sid}">{inline(text)}</h{lvl}>')
            i += 1
            continue

        if stripped.startswith(">"):
            quotes = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quotes.append(lines[i].strip().lstrip(">").strip())
                i += 1
            # Uma nota longa (linhas que continuam a frase) vira parágrafo único;
            # citações curtas consecutivas viram linhas separadas.
            if len(quotes) > 1 and not quotes[1].startswith(("*", "**")):
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

        if re.match(r"[-*]\s", stripped):
            items = []
            while i < len(lines):
                cur = lines[i]
                if re.match(r"\s*[-*]\s", cur):
                    ind = len(cur) - len(cur.lstrip())
                    items.append((ind, re.sub(r"^\s*[-*]\s+", "", cur).strip()))
                    i += 1
                elif cur.strip() and not re.match(r"\s*[|>#`]", cur) and items:
                    ind, prev = items[-1]
                    items[-1] = (ind, prev + " " + cur.strip())
                    i += 1
                else:
                    break
            body.append(render_list(items))
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
            r"\s*([-*]\s|[|>#]|```|-{3,}$)", lines[i]
        ):
            para.append(lines[i].strip())
            i += 1
        body.append(f"<p>{inline(' '.join(para))}</p>")

    return "".join(body), toc


CSS = """
:root{
  --ground:#F5F6F4; --surface:#FFFFFF; --surface-2:#EDEFEB;
  --ink:#14201C; --ink-soft:#4A5551; --ink-faint:#78837D;
  --rule:#DDE0DA; --accent:#0F5C4A; --accent-soft:#E4EFEA; --signal:#A8401C;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#101512; --surface:#171E1A; --surface-2:#1E2723;
    --ink:#E6EAE6; --ink-soft:#9AA8A1; --ink-faint:#75837C;
    --rule:#2A342F; --accent:#4FBF9B; --accent-soft:#1B2C26; --signal:#E8894F;
  }
}
:root[data-theme="dark"]{
  --ground:#101512; --surface:#171E1A; --surface-2:#1E2723;
  --ink:#E6EAE6; --ink-soft:#9AA8A1; --ink-faint:#75837C;
  --rule:#2A342F; --accent:#4FBF9B; --accent-soft:#1B2C26; --signal:#E8894F;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--serif); font-size:17px; line-height:1.68;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px;display:flex;gap:56px;align-items:flex-start}
main{flex:1;min-width:0;max-width:70ch;padding:56px 0 120px}

/* ---- índice lateral ---- */
nav{
  position:sticky; top:0; width:212px; flex:none;
  padding:64px 0 40px; font-family:var(--mono); font-size:11px;
  max-height:100vh; overflow-y:auto;
}
nav p{
  margin:0 0 14px; text-transform:uppercase; letter-spacing:.14em;
  color:var(--ink-faint); font-size:10px;
}
nav a{
  display:block; padding:5px 0 5px 11px; margin-left:-1px;
  border-left:2px solid var(--rule); color:var(--ink-soft);
  text-decoration:none; line-height:1.4;
}
nav a:hover{border-left-color:var(--accent);color:var(--accent);background:none}
nav a b{display:block;font-weight:600;color:var(--ink);letter-spacing:.02em}
nav a span{display:block;color:var(--ink-faint);font-size:10px;margin-top:1px}
@media(max-width:940px){nav{display:none}.wrap{gap:0}main{max-width:none;padding-top:40px}}

/* ---- títulos ---- */
h1,h2,h3,h4{font-family:var(--sans);text-wrap:balance;line-height:1.18;letter-spacing:-.02em}
h1{font-size:clamp(30px,5vw,44px);font-weight:750;margin:0 0 6px}
h2{
  font-size:clamp(21px,3vw,27px); font-weight:700; margin:76px 0 20px;
  padding-top:22px; border-top:2px solid var(--ink);
}
h3{font-size:18px;font-weight:680;margin:42px 0 12px}
h4{font-size:15px;font-weight:680;margin:28px 0 10px;color:var(--ink-soft)}
h2:first-of-type{margin-top:44px}

p{margin:0 0 17px}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px}
strong{font-weight:640}
hr{border:0;height:1px;background:var(--rule);margin:44px 0}

/* ---- listas ---- */
ul{margin:0 0 18px;padding-left:20px}
li{margin-bottom:7px}
li::marker{color:var(--ink-faint)}
ul ul{margin:7px 0 0}
ul.check{list-style:none;padding-left:0}
ul.check li{position:relative;padding-left:29px;margin-bottom:9px}
ul.check li span{
  position:absolute;left:0;top:.36em;width:15px;height:15px;
  border:1.5px solid var(--ink-faint);border-radius:3px;
}

/* ---- citações ---- */
blockquote{
  margin:22px 0; padding:15px 20px; background:var(--surface);
  border-left:3px solid var(--accent); border-radius:0 4px 4px 0;
}
blockquote p{margin:0 0 9px;font-size:16px;color:var(--ink-soft)}
blockquote p:last-child{margin:0}
blockquote em{color:var(--ink);font-style:italic}

/* ---- tabelas ---- */
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

/* ---- código ---- */
code{
  font-family:var(--mono);font-size:.86em;background:var(--surface-2);
  padding:.14em .38em;border-radius:3px;
}
pre{
  margin:0;background:var(--surface);border:1px solid var(--rule);
  border-radius:5px;padding:17px 19px;overflow-x:auto;
}
pre code{background:none;padding:0;font-size:12.5px;line-height:1.72;color:var(--ink-soft)}

/* ---- cabeçalho ---- */
header{padding:64px 0 8px;border-bottom:2px solid var(--ink);margin-bottom:8px}
.eyebrow{
  font-family:var(--mono);font-size:10.5px;text-transform:uppercase;
  letter-spacing:.19em;color:var(--accent);margin:0 0 15px;
}
.lede{font-size:19px;color:var(--ink-soft);margin:16px 0 26px;max-width:60ch}
.stats{display:flex;flex-wrap:wrap;gap:0;margin:0 0 30px;border-top:1px solid var(--rule)}
.stat{padding:14px 30px 14px 0;margin-right:30px;border-right:1px solid var(--rule)}
.stat:last-child{border-right:0}
.stat b{
  display:block;font-family:var(--sans);font-size:25px;font-weight:730;
  letter-spacing:-.02em;font-variant-numeric:tabular-nums;line-height:1.1;
}
.stat span{
  display:block;font-family:var(--mono);font-size:9.5px;text-transform:uppercase;
  letter-spacing:.13em;color:var(--ink-faint);margin-top:4px;
}
footer{
  margin-top:64px;padding-top:22px;border-top:1px solid var(--rule);
  font-family:var(--mono);font-size:11px;color:var(--ink-faint);line-height:1.7;
}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
"""


def main():
    md = SRC.read_text(encoding="utf-8")
    lines = md.split("\n")

    # O cabeçalho é montado à mão; o corpo começa no primeiro <hr>.
    cut = next(i for i, l in enumerate(lines) if re.fullmatch(r"-{3,}", l.strip()))
    body, toc = convert("\n".join(lines[cut + 1:]))

    nav = "".join(
        f'<a href="#{sid}"><b>{html.escape(label)}</b><span>{html.escape(rest)}</span></a>'
        for sid, label, rest in toc
    )

    out = f"""<title>Manual do Low Ticket</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{CSS}</style>
<div class="wrap">
<nav><p>Índice</p>{nav}</nav>
<main>
<header>
  <p class="eyebrow">Central de Estudos · Síntese</p>
  <h1>Manual do Low Ticket</h1>
  <p class="lede">O método consolidado, os números de referência e as divergências
  entre os professores — destilado da leitura integral de 149 transcrições.</p>
  <div class="stats">
    <div class="stat"><b>149</b><span>vídeos lidos</span></div>
    <div class="stat"><b>13</b><span>canais</span></div>
    <div class="stat"><b>11</b><span>princípios de consenso</span></div>
    <div class="stat"><b>6</b><span>divergências reais</span></div>
  </div>
</header>
{body}
<footer>
  Gerado a partir de <code>references/youtube/</code>. Cada afirmação é rastreável
  ao vídeo e timestamp de origem.<br>
  Transcrições automáticas — números e nomes de ferramentas podem conter erros.
</footer>
</main>
</div>
"""
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "GUIA.html"
    dest.write_text(out, encoding="utf-8")
    print(f"{dest}  ({len(out):,} bytes, {len(toc)} seções)")


if __name__ == "__main__":
    main()
