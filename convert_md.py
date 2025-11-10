#!/usr/bin/env python3
# convert_md.py
# Convertit du Markdown en HTML via stdin/stdout
# Usage: cat fichier.md | python convert_md.py > fichier.html
#        python convert_md.py -i input.md -o output.html

import argparse
import sys
from pathlib import Path
import markdown
from markdown.extensions import Extension  # noqa: F401

# Extensions recommandées (tu peux en ajouter/supprimer)
DEFAULT_EXTENSIONS = [
    "extra",  # inclut tables, footnotes, abbr, def_list, etc.
    "toc",  # génération de table des matières
    "nl2br",  # convertit les sauts de ligne en <br>
    "sane_lists",  # corrige le comportement des listes
    "smarty",  # typographie intelligente (guillemets, tirets…)
    "codehilite",  # coloration syntaxique des blocs de code
    "fenced_code",  # blocs de code avec ```
]


def md_to_html(md_text: str, extensions=DEFAULT_EXTENSIONS) -> str:
    """Convertit une chaîne Markdown en HTML."""
    return markdown.markdown(
        md_text,
        extensions=extensions,
        output_format="html5",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Convertit du Markdown en HTML (stdin/stdout ou fichiers)"
    )
    parser.add_argument("-i", "--input", type=Path, help="Fichier Markdown en entrée")
    parser.add_argument("-o", "--output", type=Path, help="Fichier HTML en sortie")
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        default=DEFAULT_EXTENSIONS,
        help="Extensions Markdown à activer",
    )
    parser.add_argument(
        "--no-default-extensions",
        action="store_true",
        help="Désactive les extensions par défaut",
    )

    args = parser.parse_args()

    # Lecture du contenu Markdown
    if args.input:
        try:
            md_content = args.input.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Erreur : fichier introuvable → {args.input}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Erreur de lecture du fichier : {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Lecture depuis stdin (avec encodage correct)
        md_content = sys.stdin.read()

    # Gestion des extensions
    exts = args.extensions
    if args.no_default_extensions:
        exts = args.extensions or []

    # Conversion
    try:
        html_content = md_to_html(md_content, extensions=exts)
    except Exception as e:
        print(f"Erreur lors de la conversion Markdown → HTML : {e}", file=sys.stderr)
        sys.exit(1)

    # Écriture du résultat
    if args.output:
        try:
            args.output.write_text(html_content, encoding="utf-8")
        except Exception as e:
            print(f"Erreur d'écriture du fichier : {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Sortie stdout en UTF-8
        print(html_content)

    # Optionnel : ajouter un doctype HTML complet
    if not args.input and not args.output:
        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>Markdown → HTML</title>
</head>
<body>
{html_content}
</body>
</html>"""
        print(full_html)


if __name__ == "__main__":
    main()
