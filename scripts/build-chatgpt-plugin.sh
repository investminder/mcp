#!/usr/bin/env bash
#
# Construit l'archive du plugin ChatGPT Investminder.
#
# Usage : scripts/build-chatgpt-plugin.sh [dossier-de-sortie]
#   dossier-de-sortie : par défaut ./dist
#
# Produit dist/investminder-chatgpt-plugin-<version>.zip contenant :
#   plugin.json, mcp.json, assets/ (fichiers référencés par le manifeste),
#   README.md et LICENSE.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT/dist}"

FILES=(plugin.json mcp.json README.md LICENSE)
DIRS=(assets)

die() { echo "Erreur : $*" >&2; exit 1; }

command -v zip >/dev/null || die "la commande 'zip' est introuvable."
command -v python3 >/dev/null || die "python3 est requis pour valider les JSON."

cd "$ROOT"

# 1. Présence des fichiers attendus
for f in "${FILES[@]}"; do [[ -f "$f" ]] || die "fichier manquant : $f"; done
for d in "${DIRS[@]}"; do [[ -d "$d" ]] || die "dossier manquant : $d"; done

# 2. JSON valides
for f in plugin.json mcp.json; do
  python3 -m json.tool "$f" >/dev/null || die "$f n'est pas un JSON valide."
done

# 3. Chemins relatifs référencés par plugin.json (ex. ./assets/im-icon.svg)
missing=$(python3 - <<'PY'
import json, os
def walk(v):
    if isinstance(v, dict):
        for x in v.values(): yield from walk(x)
    elif isinstance(v, list):
        for x in v: yield from walk(x)
    elif isinstance(v, str) and v.startswith("./"):
        yield v
for p in sorted(set(walk(json.load(open("plugin.json"))))):
    if not os.path.isfile(p):
        print(p)
PY
)
[[ -z "$missing" ]] || die "fichiers référencés introuvables :"$'\n'"$missing"

# 4. Version et nom de l'archive
VERSION=$(python3 -c 'import json; print(json.load(open("plugin.json"))["version"])')
NAME=$(python3 -c 'import json; print(json.load(open("plugin.json"))["name"])')
ARCHIVE="$OUT_DIR/${NAME}-chatgpt-plugin-${VERSION}.zip"

# 5. Avertissement si des modifications ne sont pas commitées
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if [[ -n "$(git status --porcelain -- "${FILES[@]}" "${DIRS[@]}")" ]]; then
    echo "Attention : modifications non commitées dans les fichiers du plugin." >&2
  fi
fi

# 6. Construction de l'archive (sans fichiers système macOS)
mkdir -p "$OUT_DIR"
rm -f "$ARCHIVE"
zip -r -X -q "$ARCHIVE" "${FILES[@]}" "${DIRS[@]}" \
  -x '*.DS_Store' -x '__MACOSX/*' -x '*/._*'

echo "Archive créée : $ARCHIVE"
unzip -l "$ARCHIVE"
