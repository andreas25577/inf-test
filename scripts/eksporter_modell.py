"""Leser LinkML-skjemaet og skriver en forenklet JSON-beskrivelse av modellen
som nettsiden bruker til fanen «Modell»."""

import json
import sys

from linkml_runtime.utils.schemaview import SchemaView

skjema_fil, ut_fil = sys.argv[1], sys.argv[2]
sv = SchemaView(skjema_fil)

klasser = []
for navn in sv.all_classes():
    c = sv.get_class(navn)
    felter = []
    for slot in sv.class_induced_slots(navn):
        felter.append({
            "navn": slot.name,
            "type": slot.range or "string",
            "paakrevd": bool(slot.required),
            "flere": bool(slot.multivalued),
            "beskrivelse": slot.description or "",
            "erKlasse": slot.range in sv.all_classes(),
            "erEnum": slot.range in sv.all_enums(),
        })
    klasser.append({
        "navn": navn,
        "uri": c.class_uri or "",
        "beskrivelse": c.description or "",
        "felter": felter,
    })

enums = []
for navn in sv.all_enums():
    e = sv.get_enum(navn)
    enums.append({
        "navn": navn,
        "beskrivelse": e.description or "",
        "verdier": [
            {"navn": k, "beskrivelse": v.description or ""}
            for k, v in (e.permissible_values or {}).items()
        ],
    })

s = sv.schema
modell = {
    "navn": s.name,
    "tittel": s.title or s.name,
    "beskrivelse": s.description or "",
    "versjon": s.version or "",
    "klasser": klasser,
    "enums": enums,
}

with open(ut_fil, "w", encoding="utf-8") as f:
    json.dump(modell, f, ensure_ascii=False, indent=2)
