#!/usr/bin/env bash
# Validerer dataene og bygger nettsiden i mappen _site/.
# Brukes både lokalt og av GitHub Actions.
set -euo pipefail

SKJEMA=src/schema/katalog.yaml
DATA=data/katalog.yaml
UT=_site

echo "1/5 Validerer data mot skjemaet"
linkml-validate -s "$SKJEMA" -C Katalog "$DATA"

echo "2/5 Kopierer nettsiden"
rm -rf "$UT"
mkdir -p "$UT/data" "$UT/artefakter"
cp site/* "$UT/"

echo "3/5 Konverterer data til JSON"
linkml-convert -s "$SKJEMA" -C Katalog -t json -o "$UT/data/katalog.json" "$DATA"

echo "4/5 Lager modellbeskrivelse og diagram"
python scripts/eksporter_modell.py "$SKJEMA" "$UT/data/modell.json"
gen-erdiagram "$SKJEMA" | sed '/^```/d' > "$UT/data/diagram.mmd"

echo "5/5 Genererer artefakter fra skjemaet"
gen-json-schema "$SKJEMA" > "$UT/artefakter/katalog.schema.json"
gen-shacl "$SKJEMA" > "$UT/artefakter/katalog.shacl.ttl"
gen-owl "$SKJEMA" > "$UT/artefakter/katalog.owl.ttl"
linkml-convert -s "$SKJEMA" -C Katalog -t ttl -o "$UT/artefakter/katalog-data.ttl" "$DATA"
cp "$SKJEMA" "$UT/artefakter/katalog.yaml"

echo "Ferdig. Siden ligger i $UT/"
