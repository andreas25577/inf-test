# LinkML-katalog

Et lite testprosjekt for å prøve [LinkML](https://linkml.io). Det har en datamodell for en
datakatalog i data.norge-stil (datasett, distribusjoner, begreper og organisasjoner),
noen eksempeldata og en nettside som viser dataene. Nettsiden publiseres automatisk
på GitHub Pages.

## Hva ligger hvor

| Fil | Hva det er |
| --- | --- |
| `src/schema/katalog.yaml` | Datamodellen. Det er denne du endrer når modellen skal endres. |
| `data/katalog.yaml` | Eksempeldataene. De må følge modellen. |
| `site/index.html` | Nettsiden som viser dataene og modellen. |
| `scripts/bygg.sh` | Validerer dataene og bygger siden til mappen `_site/`. |
| `scripts/eksporter_modell.py` | Lager en forenklet modellbeskrivelse som siden bruker. |
| `.github/workflows/pages.yml` | Kjører bygget på GitHub og publiserer siden. |

## Slik legger du det på GitHub

1. Lag et nytt, tomt repo på GitHub. Ikke huk av for README eller .gitignore.
2. Gå til mappen i en terminal og kjør:
   ```bash
   git init
   git add .
   git commit -m "Første versjon"
   git branch -M main
   git remote add origin https://github.com/BRUKERNAVN/REPONAVN.git
   git push -u origin main
   ```
   Har du GitHub Desktop, kan du i stedet velge **File → Add local repository** og publisere derfra.
3. Gå til **Settings → Pages** i repoet. Under **Source** velger du **GitHub Actions**.
4. Gå til fanen **Actions** og vent til jobben er grønn. Er den allerede ferdig, trykker du på
   den og velger **Re-run all jobs**.
5. Siden ligger på `https://BRUKERNAVN.github.io/REPONAVN/`.

Hvis repoet er privat, krever GitHub Pages et betalt abonnement. Med gratiskonto må repoet være offentlig.

## Slik jobber du videre

Endre `src/schema/katalog.yaml` eller `data/katalog.yaml` og push. GitHub validerer dataene
mot modellen. Hvis dataene ikke stemmer, blir jobben rød og siden blir ikke oppdatert.
Feilmeldingen står i loggen under **Actions**.

Du kan redigere filene direkte på github.com (blyantikonet) hvis du ikke vil jobbe lokalt.

## Kjøre lokalt (valgfritt)

Krever Python 3.10–3.12.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./scripts/bygg.sh
python -m http.server -d _site 8000
```

Åpne så http://localhost:8000. På Windows kjører du `bygg.sh` i Git Bash.

Nyttige LinkML-kommandoer:

```bash
# Valider dataene
linkml-validate -s src/schema/katalog.yaml -C Katalog data/katalog.yaml

# Sjekk skjemaet for vanlige feil og mangler
linkml-lint src/schema/katalog.yaml

# Konverter dataene til andre formater
linkml-convert -s src/schema/katalog.yaml -C Katalog -t json data/katalog.yaml
linkml-convert -s src/schema/katalog.yaml -C Katalog -t ttl  data/katalog.yaml
```

## Ting å prøve

- Legg til et nytt datasett eller begrep i `data/katalog.yaml`.
- Legg inn en feil med vilje, f.eks. `tilgangsniva: hemmelig`, og se at valideringen stopper den.
- Legg til et nytt felt i modellen, f.eks. `kontaktpunkt` på `Datasett`.
- Legg til en ny klasse, f.eks. `Informasjonsmodell`, og koble den til datasett.
