import json
import os
import re
import sys

src = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/re/dbh/out")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

names = {
    "ENG": "English", "FRE": "French", "GER": "German", "ITA": "Italian", "SPA": "Spanish", "MEX": "Spanish (LatAm)",
    "POR": "Portuguese", "BRA": "Portuguese (Brazil)", "DUT": "Dutch", "DAN": "Danish", "NOR": "Norwegian",
    "SWE": "Swedish", "FIN": "Finnish", "POL": "Polish", "CZE": "Czech", "HUN": "Hungarian", "RUS": "Russian",
    "TUR": "Turkish", "GRE": "Greek", "CRO": "Croatian", "ARA": "Arabic", "JPN": "Japanese", "JAP": "Japanese (alt)",
    "KOR": "Korean", "CHI": "Chinese (Traditional)", "SCH": "Chinese (Simplified)",
}


def unesc(s):
    return s.replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")


os.makedirs(out, exist_ok=True)
langs = []
for f in sorted(os.listdir(src)):
    if not f.endswith(".tsv"):
        continue
    code = f[:-4]
    if not re.fullmatch(r"[A-Z]{3}", code):
        continue
    rows = []
    with open(os.path.join(src, f), encoding="utf-8") as h:
        for line in h:
            p = line.rstrip("\n").split("\t")
            if len(p) < 6:
                continue
            rows.append([p[1], p[2], p[5], unesc(p[4])])
    with open(os.path.join(out, code + ".json"), "w", encoding="utf-8") as w:
        json.dump(rows, w, ensure_ascii=False, separators=(",", ":"))
    langs.append({"code": code, "name": names.get(code, code), "rows": len(rows)})
    print(code, len(rows))

langs.sort(key=lambda l: (l["code"] != "ENG", l["name"]))
with open(os.path.join(out, "index.json"), "w", encoding="utf-8") as w:
    json.dump(langs, w, ensure_ascii=False)
