# convert_md.py
import markdown
import sys

# Lit le contenu Markdown depuis l'entrée standard (stdin)
md_content = sys.stdin.read()

# Convertit le Markdown en HTML
html_content = markdown.markdown(md_content)

# Affiche le HTML sur la sortie standard (stdout)
print(html_content)
