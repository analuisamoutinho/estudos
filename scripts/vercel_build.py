#!/usr/bin/env python3
"""Build completo, chamado pelo Vercel a cada deploy (ver vercel.json).

Regenera docs/*.html a partir de GUIA.md + guias/*.md. Isto é o que permite
editar conteúdo (por um CMS, ou direto no GitHub) sem rodar nada localmente:
o Vercel executa este script no próprio deploy.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_guia
import build_landing
import build_single
from build_guia import ROOT, TOPICS


def main():
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)

    sys.argv = ["build_guia.py", str(docs / "tudo.html")]
    build_guia.main()

    sys.argv = ["build_landing.py", str(docs / "index.html")]
    build_landing.main()

    for stem, *_ in TOPICS:
        sys.argv = ["build_single.py", stem, str(docs / f"{stem}.html")]
        build_single.main()

    print(f"\nvercel_build: {len(TOPICS)} tópicos gerados em {docs}")


if __name__ == "__main__":
    main()
