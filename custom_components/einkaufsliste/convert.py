"""⚖️ Fremde Maße beim Rezept-Import umrechnen (amerikanische / englische Rezepte).

„1 cup flour“ -> „125 g flour“, „2 oz cheese“ -> „57 g cheese“, „1 lb beef“ -> „454 g beef“,
„2 tbsp sugar“ -> „2 EL sugar“, „350 °F“ -> „175 °C“.

Eine Tasse (cup) wiegt je nach Zutat unterschiedlich viel – für die häufigsten Zutaten
gibt es deshalb eigene Werte, alles andere wird als Flüssigkeit (240 ml) gerechnet.
"""

from __future__ import annotations

import math
import re

from .quantity import NUM1, _value

# Gramm pro Tasse (cup) – Stichwort im Zutaten-Namen (englisch und deutsch)
_CUP_GRAMS: tuple[tuple[tuple[str, ...], int], ...] = (
    (("brown sugar", "brauner zucker", "rohrzucker"), 220),
    (("powdered sugar", "icing sugar", "confectioners", "puderzucker"), 120),
    (("sugar", "zucker"), 200),
    (("flour", "mehl"), 125),
    (("butter",), 227),
    (("rice", "reis"), 185),
    (("oats", "oatmeal", "haferflocken"), 90),
    (("cocoa", "kakao"), 100),
    (("nuts", "almonds", "walnuts", "nüsse", "mandeln"), 140),
    (("cheese", "käse", "parmesan", "cheddar", "mozzarella"), 100),
    (("honey", "honig", "syrup", "sirup"), 340),
    (("chocolate chips", "schokostückchen", "schokotropfen"), 170),
    (("breadcrumbs", "semmelbrösel", "paniermehl"), 110),
)
_ML_PER_CUP = 240

# Schreibweise -> (Art, Faktor)
_UNITS: dict[str, tuple[str, float]] = {}
for _words, _kind, _factor in (
    (("cup", "cups", "c."), "cup", 1),
    (("tablespoon", "tablespoons", "tbsp", "tbsps", "tbs", "tbl"), "EL", 1),
    (("teaspoon", "teaspoons", "tsp", "tsps"), "TL", 1),
    (("ounce", "ounces", "oz"), "g", 28.35),
    (("pound", "pounds", "lb", "lbs"), "g", 453.6),
    (("fl oz", "fl. oz", "fl.oz", "fluid ounce", "fluid ounces"), "ml", 29.57),
    (("pint", "pints", "pt"), "ml", 473),
    (("quart", "quarts", "qt"), "ml", 946),
    (("gallon", "gallons", "gal"), "ml", 3785),
    (("stick", "sticks"), "g", 113),  # 1 Stück Butter (USA) = 113 g
):
    for _w in _words:
        _UNITS[_w] = (_kind, _factor)

_UNIT_RX = "|".join(sorted((re.escape(u) for u in _UNITS), key=len, reverse=True))
_LINE = re.compile(rf"^(?P<num>{NUM1}(?:\s*(?:-|–|to)\s*{NUM1})?)\s*(?P<unit>{_UNIT_RX})(?=\s|$)\s*(?:of\s+)?(?P<rest>.*)$", re.IGNORECASE)
_TEMP = re.compile(r"(?P<f>\d{3})\s*(?:°\s*F|degrees?\s*F(?:ahrenheit)?|F\b)", re.IGNORECASE)


def _round(value: float) -> str:
    """Schöne Zahlen: 57 g, 125 g, 454 g; ab 1000 auf 10 gerundet."""
    if value >= 1000:
        value = round(value / 10) * 10
    elif value >= 50:
        value = round(value / 5) * 5
    else:
        value = round(value)
    return str(int(max(value, 1)))


def _amount(num_text: str) -> float | None:
    parts = re.split(r"\s*(?:-|–|to)\s*", num_text.strip())
    vals = [_value(p) for p in parts if p]
    if not vals or any(v is None for v in vals):
        return None
    return max(vals)  # bei „2-3 cups“ lieber etwas mehr kaufen


def _cup_grams(rest: str) -> int | None:
    low = rest.lower()
    for words, grams in _CUP_GRAMS:
        if any(w in low for w in words):
            return grams
    return None


def convert_line(line: str) -> str:
    """Eine Zutaten-Zeile mit fremder Einheit umrechnen – alles andere bleibt, wie es ist."""
    m = _LINE.match(line.strip())
    if not m:
        return line
    kind, factor = _UNITS[m.group("unit").lower()]
    rest = m.group("rest").strip()
    if kind in ("EL", "TL"):  # Löffel bleiben Löffel, nur deutsch geschrieben
        return f"{m.group('num').strip()} {kind} {rest}".strip()
    amount = _amount(m.group("num"))
    if amount is None:
        return line
    if kind == "cup":
        grams = _cup_grams(rest)
        if grams:
            return f"{_round(amount * grams)} g {rest}".strip()
        return f"{_round(amount * _ML_PER_CUP)} ml {rest}".strip()
    return f"{_round(amount * factor)} {kind} {rest}".strip()


def convert_temps(text: str) -> str:
    """°F -> °C im Zubereitungstext: „350 °F“ -> „175 °C“ (auf 5 Grad gerundet)."""
    def repl(m: re.Match) -> str:
        c = (int(m.group("f")) - 32) * 5 / 9
        return f"{int(5 * math.floor(c / 5 + 0.5))} °C"
    return _TEMP.sub(repl, text)
