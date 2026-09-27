#!/usr/bin/env python3
"""Add/maintain Players and Countries sheets in the operational tennis workbook."""

from pathlib import Path
import hashlib
import json
import re
import unicodedata
import pycountry
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

PATH = Path("LSC_Tennis_Update_System.xlsx")
if not PATH.exists():
    raise SystemExit("Workbook missing; run create_tennis_workbook.py first.")

wb = load_workbook(PATH)

green = "3E8B68"
white = "FFFFFF"
header_fill = PatternFill("solid", fgColor=green)

if "Countries" in wb.sheetnames:
    del wb["Countries"]
ws_countries = wb.create_sheet("Countries", 4)
ws_countries.append(["Country", "ISO3", "ISO2", "Flag"])
country_rows = []
for country in sorted(pycountry.countries, key=lambda c: c.name):
    alpha2 = country.alpha_2
    flag = "".join(chr(127397 + ord(ch)) for ch in alpha2)
    country_rows.append([country.name, country.alpha_3, alpha2, flag])
for row in country_rows:
    ws_countries.append(row)

if "Players" not in wb.sheetnames:
    ws_players = wb.create_sheet("Players", 3)
    ws_players.append(["Player", "Country", "Country Code", "Flag Override", "Notes"])
    ws_players.append(["Jannik Sinner", "Italy", "ITA", "", "Current men's baseline holder."])
    ws_players.append(["Elena Rybakina", "Kazakhstan", "KAZ", "", "Current women's baseline holder."])
else:
    ws_players = wb["Players"]

for ws in (ws_players, ws_countries):
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = Font(bold=True, color=white)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"

for col, width in {"A":26, "B":26, "C":15, "D":18, "E":55}.items():
    ws_players.column_dimensions[col].width = width
for col, width in {"A":34, "B":12, "C":10, "D":10}.items():
    ws_countries.column_dimensions[col].width = width

ws_players.data_validations.dataValidation = []
dv_country = DataValidation(
    type="list",
    formula1="Countries!$A$2:$A$" + str(len(country_rows)+1),
    allow_blank=True,
)
ws_players.add_data_validation(dv_country)
dv_country.add("B2:B1000")

ws_readme = wb["README"]
note = "Player representation / flags"
existing = [ws_readme.cell(r, 1).value for r in range(1, ws_readme.max_row + 1)]
if note not in existing:
    insert_at = 6
    ws_readme.insert_rows(insert_at, amount=2)
    ws_readme.cell(insert_at, 1, note)
    ws_readme.cell(insert_at, 1).font = Font(bold=True, color="7FBEA1")
    ws_readme.cell(insert_at + 1, 1,
        "Players contains one row per player. Choose a Country from the Countries lookup. "
        "The builder derives the Unicode flag automatically. Use Flag Override only for "
        "historical/special representations where a modern flag would be misleading."
    )
    ws_readme.cell(insert_at + 1, 1).alignment = Alignment(wrap_text=True, vertical="top")

# Canonical player identity extension.
def _identity_key(name):
    s = unicodedata.normalize("NFKC", str(name)).strip().casefold()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def _player_id(name):
    return "TP-" + hashlib.sha256(_identity_key(name).encode("utf-8")).hexdigest()[:12].upper()

headers = [c.value for c in ws_players[1]]
if "Player ID (auto)" not in headers:
    id_col = ws_players.max_column + 1
    ws_players.cell(1, id_col, "Player ID (auto)")
else:
    id_col = headers.index("Player ID (auto)") + 1
country_col = headers.index("Country") + 1
code_col = headers.index("Country Code") + 1
code_lookup = {row[0]: row[1] for row in country_rows}
for r in range(2, ws_players.max_row + 1):
    name = ws_players.cell(r, 1).value
    if not name:
        continue
    if not ws_players.cell(r, id_col).value:
        ws_players.cell(r, id_col, _player_id(name))
    country = ws_players.cell(r, country_col).value
    if country and not ws_players.cell(r, code_col).value and country in code_lookup:
        ws_players.cell(r, code_col, code_lookup[country])
ws_players.cell(1, id_col).fill = header_fill
ws_players.cell(1, id_col).font = Font(bold=True, color=white)
ws_players.cell(1, id_col).alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws_players.column_dimensions[ws_players.cell(1, id_col).column_letter].width = 20

if "Aliases" in wb.sheetnames:
    del wb["Aliases"]
ws_aliases = wb.create_sheet("Aliases", 4)
ws_aliases.append(["Alias", "Canonical Player", "Lineage scope"])
alias_path = Path("data/tennis-player-aliases.json")
if alias_path.exists():
    alias_data = json.loads(alias_path.read_text(encoding="utf-8"))
    for scope, mapping in alias_data.get("scopes", {}).items():
        for alias, canonical in sorted(mapping.items()):
            ws_aliases.append([alias, canonical, scope])
for cell in ws_aliases[1]:
    cell.fill = header_fill
    cell.font = Font(bold=True, color=white)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws_aliases.freeze_panes = "A2"
ws_aliases.column_dimensions["A"].width = 30
ws_aliases.column_dimensions["B"].width = 30
ws_aliases.column_dimensions["C"].width = 14

ws_readme["A6"] = "Player identity / representation"
ws_readme["A7"] = (
    "For a new player, enter Player + Country. Leave Country Code and Player ID blank: "
    "the workflow fills them automatically. Approved historical name variants are resolved "
    "through the Aliases sheet. Use Flag Override only when needed."
)
ws_readme["A7"].alignment = Alignment(wrap_text=True, vertical="top")

wb.save(PATH)
print("Players/Countries lookup ready.")
