# -*- coding: utf-8 -*-
import sys
import math
import os
from datetime import date, timedelta

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QSlider, QLabel, QPushButton, QSizePolicy,
    QDialog, QCalendarWidget, QDialogButtonBox, QDateEdit, QFormLayout,
    QSpinBox, QComboBox, QGroupBox,
)
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF, QDate, Signal, QSettings, QThread
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont,
    QRadialGradient, QLinearGradient, QPainterPath,
)
from PySide6.QtWidgets import QStyle, QStyleOptionSlider

# ---------------------------------------------------------------------------
# Planet catalogue
# J2000 reference epoch: 2000-01-01
# mean_lon: mean ecliptic longitude at J2000 (degrees)
# ---------------------------------------------------------------------------
J2000 = date(2000, 1, 1)

PLANETS = [
    dict(name="Mercury", period=87.969,   au=0.39, color=QColor(180, 180, 185), size=5,  mean_lon=252.25,
         spin_days=58.646,   radius_km=2440,   orbital_speed_km_s=47.4),
    dict(name="Venus",   period=224.701,  au=0.72, color=QColor(240, 190,  80), size=7,  mean_lon=181.98,
         spin_days=-243.025, radius_km=6052,   orbital_speed_km_s=35.0),
    dict(name="Earth",   period=365.256,  au=1.00, color=QColor( 60, 140, 220), size=8,  mean_lon=100.46,
         spin_days=0.9973,   radius_km=6371,   orbital_speed_km_s=29.8),
    dict(name="Mars",    period=686.971,  au=1.52, color=QColor(200,  70,  50), size=6,  mean_lon=355.45,
         spin_days=1.026,    radius_km=3390,   orbital_speed_km_s=24.1),
    dict(name="Jupiter", period=4332.59,  au=5.20, color=QColor(210, 145, 100), size=16, mean_lon= 34.40,
         spin_days=0.4135,   radius_km=69911,  orbital_speed_km_s=13.1),
    dict(name="Saturn",  period=10759.2,  au=9.58, color=QColor(210, 178, 110), size=13, mean_lon= 49.94,
         spin_days=0.4440,   radius_km=58232,  orbital_speed_km_s=9.7),
    dict(name="Uranus",  period=30688.5,  au=19.2, color=QColor(130, 210, 230), size=11, mean_lon=313.23,
         spin_days=-0.7183,  radius_km=25362,  orbital_speed_km_s=6.8),
    dict(name="Neptune", period=60182.0,  au=30.1, color=QColor( 60,  80, 200), size=10, mean_lon=304.88,
         spin_days=0.6713,   radius_km=24622,  orbital_speed_km_s=5.4),
]

DATE_MIN = date(2000,  1,  1)
DATE_MAX = date(2050, 12, 31)
TOTAL_DAYS = (DATE_MAX - DATE_MIN).days

# ---------------------------------------------------------------------------
# Moon catalogue  (dist_fac = orbit radius as a multiple of the planet's half-size;
#                  au      = real orbital semi-major axis in AU)
# ---------------------------------------------------------------------------
MOONS = {
    "Earth": [
        dict(name="Moon",     period=27.322,  dist_fac= 8.0, au=0.002570, size=2.5, color=QColor(180,180,180), mean_lon=  0),
    ],
    "Mars": [
        dict(name="Phobos",   period= 0.319,  dist_fac= 5.0, au=0.000063, size=1.5, color=QColor(160,140,120), mean_lon=  0),
        dict(name="Deimos",   period= 1.263,  dist_fac= 8.5, au=0.000157, size=1.5, color=QColor(150,130,110), mean_lon=120),
    ],
    "Jupiter": [
        dict(name="Io",       period= 1.769,  dist_fac= 5.5, au=0.002819, size=2.0, color=QColor(220,180, 80), mean_lon=  0),
        dict(name="Europa",   period= 3.551,  dist_fac= 7.5, au=0.004486, size=1.8, color=QColor(200,190,170), mean_lon= 90),
        dict(name="Ganymede", period= 7.155,  dist_fac=10.5, au=0.007155, size=2.5, color=QColor(160,150,130), mean_lon=180),
        dict(name="Callisto", period=16.690,  dist_fac=14.5, au=0.012588, size=2.2, color=QColor(120,110,100), mean_lon=270),
    ],
    "Saturn": [
        dict(name="Enceladus",period= 1.370,  dist_fac= 6.5, au=0.001592, size=1.5, color=QColor(230,230,240), mean_lon=  0),
        dict(name="Tethys",   period= 1.888,  dist_fac= 8.5, au=0.001971, size=1.8, color=QColor(210,210,220), mean_lon= 72),
        dict(name="Dione",    period= 2.737,  dist_fac=11.0, au=0.002524, size=1.8, color=QColor(200,200,210), mean_lon=144),
        dict(name="Rhea",     period= 4.518,  dist_fac=13.5, au=0.003524, size=2.0, color=QColor(190,185,180), mean_lon=216),
        dict(name="Titan",    period=15.950,  dist_fac=19.0, au=0.008169, size=2.8, color=QColor(210,170, 90), mean_lon=288),
    ],
    "Uranus": [
        dict(name="Miranda",  period= 1.414,  dist_fac= 5.0, au=0.000865, size=1.5, color=QColor(170,200,210), mean_lon=  0),
        dict(name="Ariel",    period= 2.520,  dist_fac= 7.0, au=0.001277, size=1.8, color=QColor(160,195,210), mean_lon= 90),
        dict(name="Umbriel",  period= 4.144,  dist_fac= 9.5, au=0.001779, size=1.8, color=QColor(110,120,130), mean_lon=180),
        dict(name="Titania",  period= 8.706,  dist_fac=12.5, au=0.002915, size=2.0, color=QColor(150,170,180), mean_lon=270),
        dict(name="Oberon",   period=13.460,  dist_fac=15.5, au=0.003902, size=2.0, color=QColor(140,150,160), mean_lon= 45),
    ],
    "Neptune": [
        dict(name="Triton",   period= 5.877,  dist_fac= 8.5, au=0.002372, size=2.2, color=QColor(170,190,220), mean_lon=  0),
    ],
}

# ---------------------------------------------------------------------------
# Zodiac signs – starting ecliptic longitude = index * 30°  (Aries = 0°)
# ---------------------------------------------------------------------------
ZODIAC = [
    dict(name="Aries",       symbol="\u2648", color=QColor(220,  80,  80)),
    dict(name="Taurus",      symbol="\u2649", color=QColor(100, 180,  80)),
    dict(name="Gemini",      symbol="\u264a", color=QColor(220, 200,  60)),
    dict(name="Cancer",      symbol="\u264b", color=QColor( 80, 160, 200)),
    dict(name="Leo",         symbol="\u264c", color=QColor(230, 140,  40)),
    dict(name="Virgo",       symbol="\u264d", color=QColor(160, 100, 200)),
    dict(name="Libra",       symbol="\u264e", color=QColor( 80, 200, 180)),
    dict(name="Scorpio",     symbol="\u264f", color=QColor(180,  40,  60)),
    dict(name="Sagittarius", symbol="\u2650", color=QColor(200, 120,  60)),
    dict(name="Capricorn",   symbol="\u2651", color=QColor( 80, 120, 160)),
    dict(name="Aquarius",    symbol="\u2652", color=QColor( 60, 180, 220)),
    dict(name="Pisces",      symbol="\u2653", color=QColor(140,  80, 200)),
]

# ---------------------------------------------------------------------------
# Translations
# ---------------------------------------------------------------------------
STRINGS = {
    "en": {
        "title":         "Solar System Visualization",
        "play":          "\u25b6  Play",
        "pause":         "\u23f8  Pause",
        "now":           "\u23f1 Now",
        "pick_date":     "\U0001f4c5 Pick Date",
        "zoom":          "Zoom:",
        "zodiac":        "\u2648 Zodiac",
        "even":          "\u2261 Even",
        "settings":      "\u2699 Settings",
        "align_label":   "Align:",
        "align_tip":     "Jump to previous / next date where 3+ planets align within 15\u00b0",
        "settings_title": "Settings",
        "lang_label":    "Language:",
        "zfont_label":   "Zodiac font size:",
        "range_group":   "Time Slider Range",
        "start_date":    "Start date:",
        "end_date":      "End date:",
        "ok":            "OK",
        "cancel":        "Cancel",
        "zodiac_names": ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"],
    },
    "uk": {
        "title":         "\u0421\u043e\u043d\u044f\u0447\u043d\u0430 \u0441\u0438\u0441\u0442\u0435\u043c\u0430",
        "play":          "\u25b6  \u0413\u0440\u0430\u0442\u0438",
        "pause":         "\u23f8  \u041f\u0430\u0443\u0437\u0430",
        "now":           "\u23f1 \u0417\u0430\u0440\u0430\u0437",
        "pick_date":     "\U0001f4c5 \u0414\u0430\u0442\u0430",
        "zoom":          "\u041c\u0430\u0441\u0448\u0442\u0430\u0431:",
        "zodiac":        "\u2648 \u0417\u043e\u0434\u0456\u0430\u043a",
        "even":          "\u2261 \u0420\u0456\u0432\u043d\u043e",
        "settings":      "\u2699 \u041d\u0430\u043b\u0430\u0448\u0442\u0443\u0432\u0430\u043d\u043d\u044f",
        "align_label":   "\u0420\u0456\u0432\u043d\u044f\u043d\u043d\u044f:",
        "align_tip":     "\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u0434\u043e \u043f\u043e\u043f\u0435\u0440\u0435\u0434\u043d\u044c\u043e\u0433\u043e / \u043d\u0430\u0441\u0442\u0443\u043f\u043d\u043e\u0433\u043e \u0437\u0456\u0431\u0440\u0430\u043d\u043d\u044f \u043f\u043b\u0430\u043d\u0435\u0442 (3+ \u043f\u043b\u0430\u043d\u0435\u0442\u0438 \u0432 15\u00b0)",
        "settings_title": "\u041d\u0430\u043b\u0430\u0448\u0442\u0443\u0432\u0430\u043d\u043d\u044f",
        "lang_label":    "\u041c\u043e\u0432\u0430:",
        "zfont_label":   "\u0420\u043e\u0437\u043c\u0456\u0440 \u0448\u0440\u0438\u0444\u0442\u0443 \u0437\u043e\u0434\u0456\u0430\u043a\u0443:",
        "range_group":   "\u0414\u0456\u0430\u043f\u0430\u0437\u043e\u043d \u0447\u0430\u0441\u0443",
        "start_date":    "\u041f\u043e\u0447\u0430\u0442\u043e\u043a:",
        "end_date":      "\u041a\u0456\u043d\u0435\u0446\u044c:",
        "ok":            "OK",
        "cancel":        "\u0421\u043a\u0430\u0441\u0443\u0432\u0430\u0442\u0438",
        "zodiac_names":  ["\u041e\u0432\u0435\u043d","\u0422\u0435\u043b\u0435\u0446\u044c",
                          "\u0411\u043b\u0438\u0437\u043d\u044e\u043a\u0438","\u0420\u0430\u043a",
                          "\u041b\u0435\u0432","\u0414\u0456\u0432\u0430",
                          "\u0422\u0435\u0440\u0435\u0437\u0438","\u0421\u043a\u043e\u0440\u043f\u0456\u043e\u043d",
                          "\u0421\u0442\u0440\u0456\u043b\u0435\u0446\u044c","\u041a\u043e\u0437\u0435\u0440\u0456\u0433",
                          "\u0412\u043e\u0434\u043e\u043b\u0456\u0439","\u0420\u0438\u0431\u0438"],
    },
}


# ---------------------------------------------------------------------------
# Alignment detection  – days within a range where 3+ planets fit in <=15°
# ---------------------------------------------------------------------------
ALIGN_THRESHOLD = 15.0   # degrees
ALIGN_COOLDOWN  = 7      # minimum days between separate events

def _count_alignment(d: date, threshold: float = ALIGN_THRESHOLD) -> int:
    """Return max number of planets simultaneously within a threshold-degree arc."""
    angles = sorted(planet_angle_deg(p, d) for p in PLANETS)
    n = len(angles)
    ext = angles + [a + 360.0 for a in angles]
    best = 0
    for i in range(n):
        j = i
        while j < i + n and ext[j] - ext[i] <= threshold:
            j += 1
        best = max(best, j - i)
    return best


def _mark_color(count: int) -> QColor:
    """Map planet-count to a cold→warm colour.  3=blue … 8=red."""
    t = max(0.0, min(1.0, (count - 3) / 5.0))
    if t < 0.33:
        s = t / 0.33
        r, g, b = int(30), int(80 + s * 140), int(255 - s * 175)
    elif t < 0.67:
        s = (t - 0.33) / 0.34
        r, g, b = int(30 + s * 210), 220, int(80 - s * 50)
    else:
        s = (t - 0.67) / 0.33
        r, g, b = 255, int(220 - s * 170), 30
    return QColor(r, g, b, 220)


def compute_alignments(d_min: date, d_max: date, min_planets: int = 3) -> list:
    """Return sorted list of (day-offset, count) tuples where alignments occur."""
    marks = []
    total = (d_max - d_min).days
    cooldown = 0
    for offset in range(0, total + 1):
        if cooldown > 0:
            cooldown -= 1
            continue
        d = d_min + timedelta(days=offset)
        cnt = _count_alignment(d)
        if cnt >= min_planets:
            marks.append((offset, cnt))
            cooldown = ALIGN_COOLDOWN
    return marks


def days_since_j2000(d: date) -> float:
    return (d - J2000).days


# Solar-term kinds: 0=cross-quarter, 1=equinox, 2=solstice
_SOLAR_TERM_TARGETS = [
    (0,   1), (45,  0), (90,  2), (135, 0),
    (180, 1), (225, 0), (270, 2), (315, 0),
]
_ST_SYMBOLS = {
    0: ("\u25c6", QColor(180, 120, 255, 220)),   # cross-quarter ◆ purple
    1: ("\u2295", QColor( 80, 210, 160, 220)),   # equinox  ⊕ green
    2: ("\u2600", QColor(255, 210,  60, 220)),   # solstice ☀ yellow
}


def compute_solar_terms(d_min: date, d_max: date) -> list:
    """Return (float_day_offset, kind) for the 8 solar terms in the date range.
    The fractional part of the offset encodes the sub-day time (hours/minutes)."""
    earth = next(p for p in PLANETS if p["name"] == "Earth")
    results = []
    total = (d_max - d_min).days
    prev = None
    for i in range(total + 2):
        d = d_min + timedelta(days=i)
        lon = (planet_angle_deg(earth, d) + 180.0) % 360.0
        if prev is not None:
            step = (lon - prev) % 360.0
            if 0 < step < 5:           # sane forward step
                for target, kind in _SOLAR_TERM_TARGETS:
                    gap = (target - prev) % 360.0
                    if gap < step:
                        frac = gap / step if step > 0 else 0.0
                        results.append((max(0.0, i - 1 + frac), kind))
        prev = lon
    return results


def planet_angle_deg(planet: dict, d: date) -> float:
    days = days_since_j2000(d)
    return (planet["mean_lon"] + 360.0 * days / planet["period"]) % 360.0


def _lon_diff(a: float, b: float) -> float:
    """Signed angular difference b - a, normalised to (-180, 180]."""
    d = (b - a) % 360.0
    return d - 360.0 if d > 180.0 else d


def compute_moon_phase_angle(d: date) -> float:
    """Return geocentric Moon phase angle in degrees.
    0° = New Moon, 90° = First Quarter, 180° = Full Moon, 270° = Last Quarter."""
    days = days_since_j2000(d)
    moon = MOONS["Earth"][0]
    moon_lon = (moon["mean_lon"] + 360.0 * days / moon["period"]) % 360.0
    earth = next(p for p in PLANETS if p["name"] == "Earth")
    earth_lon = planet_angle_deg(earth, d)
    # Geocentric direction to the Sun
    sun_geo = (earth_lon + 180.0) % 360.0
    return (moon_lon - sun_geo) % 360.0


MOON_PHASE_SYMBOLS = ["\U0001f311","\U0001f312","\U0001f313","\U0001f314",
                       "\U0001f315","\U0001f316","\U0001f317","\U0001f318"]
MOON_PHASE_NAMES_EN = ["New Moon","Waxing Crescent","First Quarter","Waxing Gibbous",
                        "Full Moon","Waning Gibbous","Last Quarter","Waning Crescent"]


def moon_phase_info(d: date) -> tuple:
    """Return (symbol, name, illumination_pct) for the given date."""
    angle = compute_moon_phase_angle(d)
    idx = int((angle + 22.5) / 45.0) % 8
    illum = round((1 - math.cos(math.radians(angle))) / 2 * 100)
    return MOON_PHASE_SYMBOLS[idx], MOON_PHASE_NAMES_EN[idx], illum


# ---------------------------------------------------------------------------
# Solar-system canvas
# ---------------------------------------------------------------------------
class SolarSystemWidget(QWidget):
    AU_SCALE = 22          # pixels per AU at default zoom
    planetSelected = Signal(str)   # emits planet name, or "" when deselected

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_date = date.today()
        self.zoom = 1.0
        self.show_zodiac = True
        self.even_mode = False
        self.zodiac_font_scale = 1.0
        self.planet_scale = 1.0
        self._zodiac_names = STRINGS["en"]["zodiac_names"]
        self.geo_mode = False
        self.show_zodiac_sectors = False
        self.show_trail = False
        # --- new state ---
        self.selected_planet: str | None = None   # name of selected planet
        self.show_info_panel = False
        self._planet_screen_pos: dict = {}        # name -> (sx, sy, r)
        self.trail_date_min: date = DATE_MIN
        self.trail_date_max: date = DATE_MAX
        self._time_suffix: str = ""    # optional HH:MM appended to date label on solar terms
        self.setMinimumSize(900, 900)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("background-color: #06060f;")

    def set_date(self, d: date):
        self.current_date = d
        self.update()

    def set_zoom(self, factor: float):
        self.zoom = factor
        self.update()

    def set_show_zodiac(self, visible: bool):
        self.show_zodiac = visible
        self.update()

    def set_even_mode(self, enabled: bool):
        self.even_mode = enabled
        self.update()

    def set_zodiac_font_scale(self, scale: float):
        self.zodiac_font_scale = scale
        self.update()

    def set_zodiac_names(self, names: list):
        self._zodiac_names = names
        self.update()

    def set_planet_scale(self, scale: float):
        self.planet_scale = scale
        self.update()

    def set_geo_mode(self, enabled: bool):
        self.geo_mode = enabled
        self.update()

    def set_show_trail(self, enabled: bool):
        self.show_trail = enabled
        self.update()

    def set_show_zodiac_sectors(self, enabled: bool):
        self.show_zodiac_sectors = enabled
        self.update()

    def set_trail_range(self, d_min: date, d_max: date):
        self.trail_date_min = d_min
        self.trail_date_max = d_max
        self.update()

    def set_time_suffix(self, s: str):
        """Set an optional time string (e.g. '14:32') appended to the date label."""
        self._time_suffix = s
        self.update()

    def set_selected_planet(self, name: str | None):
        self.selected_planet = name or None
        self.update()

    def set_show_info_panel(self, visible: bool):
        self.show_info_panel = visible
        self.update()

    # ------------------------------------------------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.position() if hasattr(event, 'position') else event.pos()
            mx, my = pos.x(), pos.y()
            best, best_dist = None, float('inf')
            for name, (sx, sy, sr) in self._planet_screen_pos.items():
                dist = math.hypot(mx - sx, my - sy)
                hit_r = max(sr * 2.2, 14)
                if dist <= hit_r and dist < best_dist:
                    best_dist = dist
                    best = name
            # Toggle off if clicking the already-selected planet
            new_sel = None if best == self.selected_planet else best
            if new_sel != self.selected_planet:
                self.selected_planet = new_sel
                self.planetSelected.emit(new_sel or "")
                self.update()
        super().mousePressEvent(event)

    # ------------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2

        # Background starfield (deterministic)
        self._draw_stars(painter, w, h)

        # Scale: use max_au=38 so all orbits sit inside the zodiac band
        max_au = 38.0
        scale = min(w, h) / 2.0 / max_au * 0.92 * self.zoom

        n = len(PLANETS)
        half_canvas = min(w, h) / 2.0
        zodiac_inner = half_canvas * 0.80
        even_step = zodiac_inner / (n + 1)

        # Zodiac ring and sector wedges only shown in geocentric mode
        painter.save()
        painter.translate(cx, cy)
        if self.show_zodiac_sectors and self.geo_mode:
            self._draw_zodiac_sectors(painter, w, h)
        if self.show_zodiac and self.geo_mode:
            self._draw_zodiac(painter, w, h)
        painter.restore()

        # Compute Earth's heliocentric pixel position for geocentric offset
        earth_planet = next(p for p in PLANETS if p["name"] == "Earth")
        earth_idx = PLANETS.index(earth_planet)
        if self.even_mode:
            earth_orbit_r = even_step * (earth_idx + 1)
        else:
            earth_orbit_r = earth_planet["au"] * scale
        earth_angle = math.radians(planet_angle_deg(earth_planet, self.current_date))
        earth_hx = earth_orbit_r * math.cos(earth_angle)
        earth_hy = -earth_orbit_r * math.sin(earth_angle)

        # Translate for planets: geocentric (Earth at centre) or heliocentric (Sun)
        if self.geo_mode:
            _tx, _ty = cx - earth_hx, cy - earth_hy
        else:
            _tx, _ty = cx, cy
        painter.translate(_tx, _ty)

        # Geocentric trails (drawn first so they sit behind planets)
        if self.show_trail and self.geo_mode:
            self._draw_trails(painter, scale, earth_hx, earth_hy, even_step)

        # Sun glow (heliocentric origin; in geo mode it orbits Earth naturally)
        self._draw_sun(painter, scale, even_step)

        # Orbits + planets
        self._planet_screen_pos.clear()
        for idx, planet in enumerate(PLANETS):
            if self.even_mode:
                orbit_r = even_step * (idx + 1)
            else:
                orbit_r = planet["au"] * scale
            # In helio mode show orbit ring; when a planet is selected show only its orbit
            if not self.geo_mode:
                if self.selected_planet is None or planet["name"] == self.selected_planet:
                    self._draw_orbit(painter, orbit_r)

            angle_rad = math.radians(planet_angle_deg(planet, self.current_date))
            px = orbit_r * math.cos(angle_rad)
            py = -orbit_r * math.sin(angle_rad)

            # Track screen position for mouse hit-testing
            pr = planet["size"] / 2.0 * self.planet_scale
            self._planet_screen_pos[planet["name"]] = (_tx + px, _ty + py, pr)

            self._draw_planet(painter, planet, px, py, scale)

        # Date label + overlays (undo translate first)
        painter.resetTransform()
        self._draw_date_label(painter, w, h)
        self._draw_moon_phase_overlay(painter, w, h)
        if self.show_info_panel and self.selected_planet:
            self._draw_info_panel(painter, w, h)

        painter.end()

    # ------------------------------------------------------------------
    def _draw_trails(self, painter, scale, earth_hx, earth_hy, even_step=0.0):
        """Draw geocentric path trails + retrograde station markers."""
        STEP = 5        # sample every N days
        HALF = 550      # ±days from current date

        earth_planet = next(p for p in PLANETS if p["name"] == "Earth")
        earth_idx    = PLANETS.index(earth_planet)
        cur_abs = (self.current_date - DATE_MIN).days

        # Real-AU Earth radius (needed for retrograde lon detection always)
        r_au_e = earth_planet["au"] * scale

        # No trails at all when no planet is selected
        if not self.selected_planet:
            return

        # Clamp sampling window to the timeline slider range
        range_lo = (self.trail_date_min - DATE_MIN).days
        range_hi = (self.trail_date_max - DATE_MIN).days

        for planet in PLANETS:
            if planet["name"] == "Earth":
                continue
            if planet["name"] != self.selected_planet:
                continue

            p_idx = PLANETS.index(planet)
            color = planet["color"]

            # Visual radii must match how planets are drawn so trail aligns
            r_vis_p = (even_step * (p_idx    + 1)) if self.even_mode else (planet["au"]       * scale)
            r_vis_e = (even_step * (earth_idx + 1)) if self.even_mode else (earth_planet["au"] * scale)
            # Real-AU planet radius for accurate retrograde (lon) detection
            r_au_p  = planet["au"] * scale

            pts = []    # (tx, ty, day_abs)
            lons = []   # geocentric ecliptic longitude at each sample

            lo = max(range_lo, cur_abs - HALF)
            hi = min(range_hi, cur_abs + HALF)
            # Snap lo to the STEP grid so sample positions are frame-stable
            lo = (lo // STEP) * STEP

            for day_abs in range(lo, hi + 1, STEP):
                d = DATE_MIN + timedelta(days=day_abs)

                ang_p = math.radians(planet_angle_deg(planet,       d))
                ang_e = math.radians(planet_angle_deg(earth_planet, d))

                # Visual position (mode-aware) → painter trail coords
                px_vis = r_vis_p * math.cos(ang_p)
                py_vis = -r_vis_p * math.sin(ang_p)
                ex_vis = r_vis_e * math.cos(ang_e)
                ey_vis = -r_vis_e * math.sin(ang_e)
                tx = px_vis - ex_vis + earth_hx
                ty = py_vis - ey_vis + earth_hy

                # Geocentric longitude from true AU positions (retrograde detection)
                gx =  (r_au_p * math.cos(ang_p) - r_au_e * math.cos(ang_e))
                gy = -(- r_au_p * math.sin(ang_p) + r_au_e * math.sin(ang_e))
                lon = math.degrees(math.atan2(gy, gx)) % 360.0

                pts.append((tx, ty, day_abs))
                lons.append(lon)

            if len(pts) < 3:
                continue

            n = len(pts)

            # ── Draw trail polyline, past faded / future brighter ──────
            pen = QPen()
            pen.setWidthF(1.2)
            pen.setCapStyle(Qt.RoundCap)
            for i in range(n - 1):
                x0, y0, d0 = pts[i]
                x1, y1, d1 = pts[i + 1]
                alpha = 50 if d0 < cur_abs else 100
                pen.setColor(QColor(color.red(), color.green(), color.blue(), alpha))
                painter.setPen(pen)
                painter.drawLine(QPointF(x0, y0), QPointF(x1, y1))

            # ── Detect retrograde station points ───────────────────────
            # Use a 2-step window to reduce noise from angular wrap
            stations = []
            for i in range(1, n - 1):
                d_prev = _lon_diff(lons[i - 1], lons[i])
                d_next = _lon_diff(lons[i],     lons[i + 1])
                if d_prev > 0.05 and d_next < -0.05:
                    stations.append((pts[i][0], pts[i][1], pts[i][2], "retro"))
                elif d_prev < -0.05 and d_next > 0.05:
                    stations.append((pts[i][0], pts[i][1], pts[i][2], "direct"))

            # ── Draw station markers with label ────────────────────────
            font = QFont("Segoe UI", 7, QFont.Bold)
            painter.setFont(font)
            for sx, sy, sd, stype in stations:
                if stype == "retro":
                    dot_c  = QColor(255,  90,  50, 230)   # orange-red = begin retrograde
                    lbl_c  = QColor(255, 160, 120, 220)
                    lbl    = "R"
                else:
                    dot_c  = QColor( 60, 210, 170, 230)   # cyan-green = end retrograde
                    lbl_c  = QColor(120, 230, 200, 220)
                    lbl    = "D"
                painter.setBrush(QBrush(dot_c))
                painter.setPen(QPen(QColor(255, 255, 255, 140), 0.8))
                painter.drawEllipse(QPointF(sx, sy), 4.5, 4.5)
                painter.setPen(QPen(lbl_c))
                painter.drawText(QPointF(sx + 6, sy + 4), lbl)

    # ------------------------------------------------------------------
    def _draw_zodiac_sectors(self, painter, w, h):
        """Full-radius translucent pie wedges + thin radial boundary lines."""
        half = min(w, h) / 2.0
        outer_r = half * 0.975
        rect = QRectF(-outer_r, -outer_r, outer_r * 2, outer_r * 2)
        for i, sign in enumerate(ZODIAC):
            start = float(i * 30)
            color = sign["color"]
            alpha = 22 if i % 2 == 0 else 13
            fill = QColor(color.red(), color.green(), color.blue(), alpha)
            path = QPainterPath()
            path.moveTo(0.0, 0.0)
            path.arcTo(rect, start, 30.0)
            path.closeSubpath()
            painter.setBrush(QBrush(fill))
            painter.setPen(Qt.NoPen)
            painter.drawPath(path)
        # Radial boundary lines
        pen = QPen(QColor(255, 255, 255, 25))
        pen.setWidthF(0.8)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        for i in range(12):
            angle = math.radians(i * 30)
            painter.drawLine(QPointF(0.0, 0.0),
                             QPointF(outer_r * math.cos(angle),
                                     -outer_r * math.sin(angle)))

    def _draw_zodiac(self, painter, w, h):
        half    = min(w, h) / 2.0
        outer_r = half * 0.975
        inner_r = half * 0.80           # wider band for bigger text
        label_r = (outer_r + inner_r) / 2.0
        band_h  = outer_r - inner_r     # available band height in pixels

        rect_out = QRectF(-outer_r, -outer_r, outer_r * 2, outer_r * 2)
        rect_in  = QRectF(-inner_r, -inner_r, inner_r * 2, inner_r * 2)

        for i, sign in enumerate(ZODIAC):
            start = float(i * 30)
            end   = start + 30.0
            color = sign["color"]
            fill  = QColor(color.red(), color.green(), color.blue(), 30 if i % 2 == 0 else 20)

            # Annular sector
            path = QPainterPath()
            path.moveTo(inner_r * math.cos(math.radians(start)),
                        -inner_r * math.sin(math.radians(start)))
            path.lineTo(outer_r * math.cos(math.radians(start)),
                        -outer_r * math.sin(math.radians(start)))
            path.arcTo(rect_out, start, 30.0)
            path.lineTo(inner_r * math.cos(math.radians(end)),
                        -inner_r * math.sin(math.radians(end)))
            path.arcTo(rect_in, end, -30.0)
            path.closeSubpath()

            painter.setBrush(QBrush(fill))
            painter.setPen(Qt.NoPen)
            painter.drawPath(path)

            # Sector boundary line
            pen = QPen(QColor(color.red(), color.green(), color.blue(), 70))
            pen.setWidthF(1.0)
            painter.setPen(pen)
            painter.drawLine(
                QPointF(inner_r * math.cos(math.radians(start)),
                        -inner_r * math.sin(math.radians(start))),
                QPointF(outer_r * math.cos(math.radians(start)),
                        -outer_r * math.sin(math.radians(start)))
            )

            # Labels: big symbol glyph + name below
            mid = start + 15.0
            lx  = label_r * math.cos(math.radians(mid))
            ly  = -label_r * math.sin(math.radians(mid))
            painter.save()
            painter.translate(lx, ly)
            painter.rotate(-mid)

            sym_h  = min(band_h * 0.52, 16) * self.zodiac_font_scale
            name_h = min(band_h * 0.32, 11) * self.zodiac_font_scale
            half_w = 30

            # Symbol  (Segoe UI Symbol gives correct zodiac glyphs on Windows)
            sym_font = QFont("Segoe UI Symbol", 0)
            sym_font.setPixelSize(max(10, int(sym_h)))
            painter.setFont(sym_font)
            painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 230)))
            painter.drawText(QRectF(-half_w, -sym_h - 1, half_w * 2, sym_h + 2),
                             Qt.AlignCenter, sign["symbol"])

            # Name
            name_font = QFont("Segoe UI", 0)
            name_font.setPixelSize(max(7, int(name_h)))
            painter.setFont(name_font)
            painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), 170)))
            lname = self._zodiac_names[i] if i < len(self._zodiac_names) else sign["name"]
            painter.drawText(QRectF(-half_w, 1, half_w * 2, name_h + 2),
                             Qt.AlignCenter, lname)
            painter.restore()

    # ------------------------------------------------------------------
    def _draw_stars(self, painter, w, h):
        import random
        rng = random.Random(42)
        for _ in range(250):
            sx = rng.randint(0, w)
            sy = rng.randint(0, h)
            r = rng.random()
            alpha = int(r * 70 + 20)   # darker stars
            size = r * 1.6
            painter.setPen(QPen(QColor(200, 210, 255, alpha)))
            painter.drawEllipse(QPointF(sx, sy), size, size)

    def _draw_sun(self, painter, scale, even_step=0.0):
        # In even mode use a fraction of even_step so the sun stays smaller
        # than the nearest orbit ring.  In real mode scale proportionally with
        # zoom (no hard upper cap so it shrinks correctly on zoom-out).
        if self.even_mode and even_step > 0:
            sun_r = even_step * 0.38          # ~38 % of the innermost even gap
        else:
            sun_r = max(6.0, scale * 0.12)    # real mode: ~12% of 1 AU, scales with zoom
        glow_rs = [sun_r * 3.8, sun_r * 2.8, sun_r * 2.0, sun_r * 1.4]
        alphas  = [18, 35, 60, 120]
        for radius, alpha in zip(glow_rs, alphas):
            grad = QRadialGradient(QPointF(0, 0), radius)
            grad.setColorAt(0.0, QColor(255, 230, 100, alpha))
            grad.setColorAt(1.0, QColor(255, 150,  50,  0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(0, 0), radius, radius)

        # Sun disk
        offset = sun_r * 0.25
        grad = QRadialGradient(QPointF(-offset, -offset), sun_r * 1.1)
        grad.setColorAt(0.0, QColor(255, 255, 200))
        grad.setColorAt(0.6, QColor(255, 200,  80))
        grad.setColorAt(1.0, QColor(230, 130,  30))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(0, 0), sun_r, sun_r)

    def _draw_orbit(self, painter, r):
        pen = QPen(QColor(255, 255, 255, 30))
        pen.setWidth(1)
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(0, 0), r, r)

    def _draw_planet(self, painter, planet, px, py, scale):
        color: QColor = planet["color"]
        r = planet["size"] / 2.0 * self.planet_scale

        # Selection highlight ring
        if self.selected_planet == planet["name"]:
            ring_pen = QPen(QColor(255, 255, 120, 200))
            ring_pen.setWidthF(2.0)
            painter.setPen(ring_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(px, py), r + 5, r + 5)

        # Planet glow
        glow_r = r * 2.5
        grad = QRadialGradient(QPointF(px, py), glow_r)
        glow_color = QColor(color)
        glow_color.setAlpha(60)
        grad.setColorAt(0.0, glow_color)
        grad.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(px, py), glow_r, glow_r)

        # Planet disk with subtle gradient
        disk_grad = QRadialGradient(QPointF(px - r * 0.3, py - r * 0.3), r * 1.2)
        lighter = color.lighter(150)
        disk_grad.setColorAt(0.0, lighter)
        disk_grad.setColorAt(1.0, color.darker(130))
        painter.setBrush(QBrush(disk_grad))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(px, py), r, r)

        # Saturn rings
        if planet["name"] == "Saturn":
            self._draw_saturn_rings(painter, px, py, r)

        # Moons
        self._draw_moons(painter, planet, px, py)

        # Label
        font = QFont("Segoe UI", 7)
        painter.setFont(font)
        painter.setPen(QPen(color.lighter(160)))
        painter.drawText(QPointF(px + r + 3, py - r), planet["name"])

    def _draw_moons(self, painter, planet, px, py):
        p_moons = MOONS.get(planet["name"], [])
        if not p_moons:
            return
        planet_r = planet["size"] / 2.0
        days = days_since_j2000(self.current_date)

        # In geocentric mode Earth's Moon gets a larger radius + bigger disk
        geo_earth = self.geo_mode and planet["name"] == "Earth"
        moon_orbit_mult = 2.2 if geo_earth else 1.0
        moon_size_mult  = 3.5 if geo_earth else 1.0

        if self.even_mode:
            # Visual spacing: proportional to dist_fac
            for moon in p_moons:
                orbit_r = planet_r * moon["dist_fac"] * moon_orbit_mult
                self._draw_single_moon(painter, moon, px, py, orbit_r, days, moon_size_mult)
        else:
            # Real-proportions mode: scale so outermost moon sits at planet_r * 6,
            # others proportional by actual AU. Minimum planet_r * 2 so tiny inner
            # moons (Phobos etc.) stay visible.
            max_au = max(m["au"] for m in p_moons)
            for moon in p_moons:
                orbit_r = max(planet_r * 2.0, planet_r * 6.0 * moon["au"] / max_au) * moon_orbit_mult
                self._draw_single_moon(painter, moon, px, py, orbit_r, days, moon_size_mult)

    def _draw_single_moon(self, painter, moon, px, py, orbit_r, days, size_mult=1.0):
        # faint orbit ring
        pen = QPen(QColor(255, 255, 255, 20))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(px, py), orbit_r, orbit_r)
        # moon position
        ang = math.radians((moon["mean_lon"] + 360.0 * days / moon["period"]) % 360.0)
        mx = px + orbit_r * math.cos(ang)
        my = py - orbit_r * math.sin(ang)
        mr = moon["size"] / 2.0 * size_mult
        # glow
        ggrad = QRadialGradient(QPointF(mx, my), mr * 2.2)
        gc = QColor(moon["color"]); gc.setAlpha(50)
        ggrad.setColorAt(0.0, gc)
        ggrad.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(ggrad))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(mx, my), mr * 2.2, mr * 2.2)
        # disk
        painter.setBrush(QBrush(moon["color"]))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(mx, my), mr, mr)

    def _draw_saturn_rings(self, painter, px, py, r):
        pen = QPen(QColor(210, 190, 140, 160))
        for ring_r, width in [(r * 1.7, 2), (r * 2.1, 1.5), (r * 2.5, 1)]:
            pen.setWidthF(width)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(px, py), ring_r, ring_r * 0.35)

    def _draw_date_label(self, painter, w, h):
        text = self.current_date.strftime("%B %d, %Y")
        if self._time_suffix:
            text += f"  {self._time_suffix}"
        font = QFont("Segoe UI", 13, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor(200, 220, 255, 210)))
        painter.drawText(QRectF(10, h - 34, w - 20, 28), Qt.AlignLeft, text)

    # ------------------------------------------------------------------
    def _draw_moon_phase_overlay(self, painter, w, h):
        """Draw a large moon phase display in the top-left corner."""
        sym, name, illum = moon_phase_info(self.current_date)
        angle = compute_moon_phase_angle(self.current_date)

        pad    = 12
        disk_r = 34
        box_w  = 170
        box_h  = disk_r * 2 + 52
        bx, by = pad, pad

        # Panel background
        painter.setBrush(QBrush(QColor(8, 15, 38, 200)))
        painter.setPen(QPen(QColor(100, 140, 200, 120), 1.0))
        painter.drawRoundedRect(QRectF(bx, by, box_w, box_h), 8, 8)

        # Moon disk centre
        mcx = bx + disk_r + pad
        mcy = by + disk_r + pad

        # Dark base
        painter.setBrush(QBrush(QColor(30, 32, 45)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(mcx, mcy), disk_r, disk_r)

        # ──────────────────────────────────────────────────────────────
        # Lit-region path using a two-cubic Bezier terminator.
        # Convention (Northern-hemisphere view, top = north):
        #   angle   0 = New Moon       (right lit side zero)
        #   angle  90 = First Quarter  (right half lit)
        #   angle 180 = Full Moon
        #   angle 270 = Last Quarter   (left half lit)
        #
        # The terminator is a half-ellipse with:
        #   horizontal semi-axis = cos(angle) * disk_r   (signed)
        #   vertical   semi-axis = disk_r
        # For waxing (0-180) the outer limb is the RIGHT semicircle.
        # For waning (180-360) the outer limb is the LEFT semicircle,
        # and we negate cos so the terminator moves the correct direction.
        # ──────────────────────────────────────────────────────────────
        disk_rect = QRectF(mcx - disk_r, mcy - disk_r, disk_r * 2, disk_r * 2)
        disk_full = QPainterPath()
        disk_full.addEllipse(QPointF(mcx, mcy), disk_r, disk_r)

        K = 0.5523   # Bezier circle approximation constant
        phase_rad = math.radians(angle)
        lit = QPainterPath()

        if angle < 0.5 or angle > 359.5:
            pass   # New Moon: nothing lit
        elif abs(angle - 180.0) < 0.5:
            lit.addEllipse(QPointF(mcx, mcy), disk_r, disk_r)   # Full Moon
        elif angle < 180.0:   # Waxing
            tx = math.cos(phase_rad) * disk_r   # +disk_r (crescent) → -disk_r (gibbous)
            lit.moveTo(mcx, mcy - disk_r)                 # TOP
            lit.arcTo(disk_rect, 90, -180)                # right limb CW → BOTTOM
            # Bezier terminator: BOTTOM → mid → TOP
            lit.cubicTo(mcx + K * tx,  mcy + disk_r,
                        mcx + tx,      mcy + K * disk_r,
                        mcx + tx,      mcy)
            lit.cubicTo(mcx + tx,      mcy - K * disk_r,
                        mcx + K * tx,  mcy - disk_r,
                        mcx,           mcy - disk_r)
            lit.closeSubpath()
        else:              # Waning (180 < angle < 360)
            tx = -math.cos(phase_rad) * disk_r  # moves right as angle → 360
            lit.moveTo(mcx, mcy - disk_r)                 # TOP
            lit.arcTo(disk_rect, 90, 180)                 # left limb CCW → BOTTOM
            # Bezier terminator: BOTTOM → mid → TOP
            lit.cubicTo(mcx + K * tx,  mcy + disk_r,
                        mcx + tx,      mcy + K * disk_r,
                        mcx + tx,      mcy)
            lit.cubicTo(mcx + tx,      mcy - K * disk_r,
                        mcx + K * tx,  mcy - disk_r,
                        mcx,           mcy - disk_r)
            lit.closeSubpath()

        final_path = lit.intersected(disk_full)
        moon_grad = QRadialGradient(QPointF(mcx - disk_r * 0.25, mcy - disk_r * 0.25), disk_r * 1.3)
        moon_grad.setColorAt(0.0, QColor(240, 240, 220))
        moon_grad.setColorAt(1.0, QColor(180, 180, 160))
        painter.setBrush(QBrush(moon_grad))
        painter.setPen(Qt.NoPen)
        painter.drawPath(final_path)

        # Rim
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(180, 180, 160, 80), 0.8))
        painter.drawEllipse(QPointF(mcx, mcy), disk_r, disk_r)

        # Phase name
        name_font = QFont("Segoe UI", 10, QFont.Bold)
        painter.setFont(name_font)
        painter.setPen(QPen(QColor(210, 230, 255, 230)))
        tx = bx + disk_r * 2 + pad * 2
        tw = box_w - disk_r * 2 - pad * 3
        painter.drawText(QRectF(tx, by + pad, tw, 20),
                         Qt.AlignLeft | Qt.AlignVCenter, name)
        # Illumination %
        pct_font = QFont("Segoe UI", 9)
        painter.setFont(pct_font)
        painter.setPen(QPen(QColor(150, 190, 240, 200)))
        painter.drawText(QRectF(tx, by + pad + 22, tw, 18),
                         Qt.AlignLeft | Qt.AlignVCenter, f"Illuminated: {illum}%")
        # Small bar
        bar_y = by + pad + 44
        bar_x = tx
        bar_w = min(tw, 80)
        bar_h2 = 6
        painter.setBrush(QBrush(QColor(30, 40, 70)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(bar_x, bar_y, bar_w, bar_h2), 3, 3)
        painter.setBrush(QBrush(QColor(200, 220, 255, 200)))
        painter.drawRoundedRect(QRectF(bar_x, bar_y, bar_w * illum / 100, bar_h2), 3, 3)

    def _draw_info_panel(self, painter, w, h):
        """Overlay panel on the left side showing selected planet data."""
        planet = next((p for p in PLANETS if p["name"] == self.selected_planet), None)
        if planet is None:
            return

        # Compute distance to Earth
        earth_data = next(p for p in PLANETS if p["name"] == "Earth")
        if planet["name"] == "Earth":
            dist_str = "—"
        else:
            ang_e = math.radians(planet_angle_deg(earth_data, self.current_date))
            ang_p = math.radians(planet_angle_deg(planet, self.current_date))
            ex = earth_data["au"] * math.cos(ang_e)
            ey = earth_data["au"] * math.sin(ang_e)
            px2 = planet["au"] * math.cos(ang_p)
            py2 = planet["au"] * math.sin(ang_p)
            dist_au = math.hypot(px2 - ex, py2 - ey)
            dist_km = dist_au * 149_597_870.7
            if dist_km >= 1_000_000:
                dist_str = f"{dist_km / 1_000_000:.2f} M km"
            else:
                dist_str = f"{dist_km:,.0f} km"

        pad    = 14
        line_h = 26
        title_h = 30
        lines = [
            ("Orbital period",  f"{planet['period']:.1f} days"),
            ("Radius",          f"{planet['radius_km']:,} km"),
            ("Orbital speed",   f"{planet['orbital_speed_km_s']:.1f} km/s"),
            ("Rotation period", (
                f"{abs(planet['spin_days']):.3f} d (retro)"
                if planet['spin_days'] < 0
                else f"{planet['spin_days']:.3f} d")),
            ("Distance (Sun)",  f"{planet['au']:.2f} AU"),
            ("Distance (Earth)", dist_str),
        ]

        panel_w = 268
        panel_h = pad * 2 + title_h + len(lines) * line_h + 4
        # Position below moon-phase box (top-left) with a gap
        moon_box_bottom = 12 + 34 * 2 + 52 + 8   # by(12) + box_h(120) + gap(8)
        px0 = 12
        py0 = moon_box_bottom

        # Background
        bg = QColor(10, 18, 40, 215)
        border = QColor(planet["color"].red(), planet["color"].green(), planet["color"].blue(), 180)
        painter.setBrush(QBrush(bg))
        painter.setPen(QPen(border, 1.5))
        painter.drawRoundedRect(QRectF(px0, py0, panel_w, panel_h), 8, 8)

        # Title
        title_font = QFont("Segoe UI", 14, QFont.Bold)
        painter.setFont(title_font)
        painter.setPen(QPen(planet["color"].lighter(180)))
        painter.drawText(QRectF(px0 + pad, py0 + pad - 2, panel_w - pad * 2, title_h),
                         Qt.AlignLeft | Qt.AlignVCenter, planet["name"])

        # Separator line
        sep_y = py0 + pad + title_h
        painter.setPen(QPen(QColor(border.red(), border.green(), border.blue(), 80), 1.0))
        painter.drawLine(QPointF(px0 + pad, sep_y), QPointF(px0 + panel_w - pad, sep_y))

        # Data rows
        lbl_font = QFont("Segoe UI", 10)
        val_font = QFont("Segoe UI", 10, QFont.Bold)
        lbl_w = 118
        for i, (lbl, val) in enumerate(lines):
            row_y = sep_y + 4 + i * line_h
            painter.setFont(lbl_font)
            painter.setPen(QPen(QColor(140, 170, 210, 210)))
            painter.drawText(QRectF(px0 + pad, row_y, lbl_w, line_h),
                             Qt.AlignLeft | Qt.AlignVCenter, lbl + ":")
            painter.setFont(val_font)
            painter.setPen(QPen(QColor(220, 235, 255, 240)))
            painter.drawText(QRectF(px0 + pad + lbl_w, row_y, panel_w - pad * 2 - lbl_w, line_h),
                             Qt.AlignLeft | Qt.AlignVCenter, val)


# ---------------------------------------------------------------------------
# Clickable label – emits doubleClicked on double-click
# ---------------------------------------------------------------------------
class _ClickableLabel(QLabel):
    doubleClicked = Signal()

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)


# ---------------------------------------------------------------------------
# Slider subclass: double-click signal + alignment mark painting
# ---------------------------------------------------------------------------
_MONTH_ABBR = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]


class _RangeSlider(QSlider):
    doubleClicked = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._marks: list = []
        self._show_marks: bool = True
        self._date_min: "date | None" = None
        self._solar_terms: list = []   # list of (offset, kind)

    def set_marks(self, marks: list):
        self._marks = marks
        self.update()

    def set_show_marks(self, visible: bool):
        self._show_marks = visible
        self.update()

    def set_date_range(self, d_min: "date"):
        self._date_min = d_min
        self.update()

    def set_solar_terms(self, terms: list):
        self._solar_terms = terms
        self.update()

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        total = self.maximum() - self.minimum()
        if total <= 0:
            return
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        groove = self.style().subControlRect(
            QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        gx = groove.x()
        gw = groove.width()
        gy = groove.center().y()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # ── Year / month tick marks with labels ──────────────────────
        if self._date_min is not None:
            from datetime import date as _date
            d_min = self._date_min
            d_max = d_min + timedelta(days=total)
            n_months = (d_max.year - d_min.year) * 12 + d_max.month - d_min.month
            # Decide label density: every month, every quarter, or every year
            show_all_months  = n_months <= 48
            show_qtr_months  = n_months <= 120
            yr_font  = QFont("Segoe UI", 7, QFont.Bold)
            mo_font  = QFont("Segoe UI", 6)
            yr, mo = d_min.year, 1
            while True:
                tick_d = _date(yr, mo, 1)
                if tick_d > d_max:
                    break
                if tick_d >= d_min:
                    offset = (tick_d - d_min).days
                    x = int(gx + offset / total * gw)
                    if mo == 1:
                        # Tall year tick + year label above
                        painter.setPen(QPen(QColor(160, 200, 255, 200), 1.2))
                        painter.drawLine(x, gy - 10, x, gy + 10)
                        painter.setFont(yr_font)
                        painter.setPen(QPen(QColor(160, 200, 255, 220)))
                        painter.drawText(x - 14, gy - 12, str(yr))
                    else:
                        # Month tick
                        show_lbl = show_all_months or (show_qtr_months and mo in (4, 7, 10))
                        painter.setPen(QPen(QColor(100, 140, 200, 130), 0.8))
                        painter.drawLine(x, gy - 5, x, gy + 5)
                        if show_lbl:
                            painter.setFont(mo_font)
                            painter.setPen(QPen(QColor(120, 160, 210, 180)))
                            lbl = _MONTH_ABBR[mo - 1]
                            painter.drawText(x - 8, gy + 16, lbl)
                mo += 1
                if mo > 12:
                    mo = 1
                    yr += 1

        # ── Solar-term ticks ──────────────────────────────────────────
        if self._solar_terms:
            st_font = QFont("Segoe UI Symbol", 6)
            painter.setFont(st_font)
            for offset, kind in self._solar_terms:
                frac = offset / total
                if not (0 <= frac <= 1):
                    continue
                x = int(gx + frac * gw)
                sym, col = _ST_SYMBOLS[kind]
                tick_h = 8 if kind == 0 else 11
                painter.setPen(QPen(col, 1.2))
                painter.drawLine(x, gy - tick_h, x, gy + tick_h)
                painter.setPen(QPen(col))
                painter.drawText(x - 4, gy - tick_h - 1, sym)

        # ── Alignment marks ───────────────────────────────────────────
        if self._marks and self._show_marks:
            pen = QPen()
            pen.setWidthF(1.5)
            for offset, cnt in self._marks:
                frac = (offset - self.minimum()) / total
                x = int(gx + frac * gw)
                pen.setColor(_mark_color(cnt))
                painter.setPen(pen)
                painter.drawLine(x, gy - 6, x, gy + 6)
        painter.end()


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar System Visualization")
        self.resize(960, 1000)
        self.setStyleSheet("""
            QMainWindow { background: #06060f; }
            QWidget     { background: #06060f; color: #c8d8f0; }
            QLabel      { color: #a0c0e8; font-family: 'Segoe UI'; font-size: 10pt; }
            QPushButton {
                background: #1a2a4a; color: #90c0e8;
                border: 1px solid #2a4a7a; border-radius: 6px;
                padding: 2px 6px; font-size: 10pt;
            }
            QPushButton:hover   { background: #253a60; }
            QPushButton:pressed { background: #0e1a30; }
            QPushButton:checked { background: #1a4a2a; border: 1px solid #2a8a4a; color: #60e880; }
            QSlider::groove:horizontal {
                height: 6px; background: #1a2a4a; border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4a8ad0; border: 1px solid #6aaaf0;
                width: 16px; height: 16px; margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #2a5a9a; border-radius: 3px;
            }
        """)

        self._animation_timer = QTimer(self)
        self._animation_timer.setInterval(40)          # ~25 fps
        self._animation_timer.timeout.connect(self._advance_day)
        self._anim_step = 1                            # days per tick (fixed 1d)
        today = date.today()
        self._slider_min = today
        self._slider_max = date(today.year + 3, today.month, today.day)
        self._lang = "en"
        self._zodiac_font_scale = 1.0
        self._alignment_marks: list = []
        self._min_align_planets: int = 3
        self._solar_term_data: list = []      # list of (float_offset, kind)
        self._current_float_offset: float = 0.0

        self._build_ui()
        self._set_current_date(date.today())
        self._load_settings()

    # ------------------------------------------------------------------
    def _icon_btn(self, icon: str, tip: str, w: int = 34, checkable: bool = False) -> QPushButton:
        """Create a compact icon-only push button."""
        btn = QPushButton(icon)
        btn.setFixedSize(w, 30)
        btn.setToolTip(tip)
        btn.setCheckable(checkable)
        btn.setFont(QFont("Segoe UI Symbol", 11))
        return btn

    def showEvent(self, event):
        super().showEvent(event)
        try:
            import ctypes
            hwnd = int(self.winId())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

    # ------------------------------------------------------------------
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(6)

        # ── Canvas ──────────────────────────────────────────────────────
        self.canvas = SolarSystemWidget()
        self.canvas.set_trail_range(self._slider_min, self._slider_max)
        root.addWidget(self.canvas, stretch=1)

        # ── Slider row ──────────────────────────────────────────────────
        slider_row = QHBoxLayout()
        slider_row.setSpacing(8)

        self.lbl_min = _ClickableLabel(self._slider_min.strftime("%Y-%m-%d"))
        self.lbl_min.setFixedWidth(82)
        self.lbl_min.setCursor(Qt.PointingHandCursor)
        self.lbl_min.setToolTip("Double-click to change range start")
        self.lbl_min.doubleClicked.connect(lambda: self._open_range_dialog("min"))
        slider_row.addWidget(self.lbl_min)

        self.slider = _RangeSlider(Qt.Horizontal)
        self.slider.setRange(0, (self._slider_max - self._slider_min).days)
        self.slider.set_date_range(self._slider_min)
        self._solar_term_data = compute_solar_terms(self._slider_min, self._slider_max)
        self.slider.set_solar_terms(self._solar_term_data)
        self.slider.setFixedHeight(42)
        self.slider.valueChanged.connect(self._slider_moved)
        self.slider.setToolTip("Drag to change date")

        btn_prev_st = self._icon_btn("\u2190", "Jump to previous solar term (equinox / solstice)", w=26)
        btn_prev_st.clicked.connect(self._jump_prev_solar_term)
        slider_row.addWidget(btn_prev_st)
        slider_row.addWidget(self.slider, stretch=1)
        btn_next_st = self._icon_btn("\u2192", "Jump to next solar term (equinox / solstice)", w=26)
        btn_next_st.clicked.connect(self._jump_next_solar_term)
        slider_row.addWidget(btn_next_st)

        self.lbl_max = _ClickableLabel(self._slider_max.strftime("%Y-%m-%d"))
        self.lbl_max.setFixedWidth(82)
        self.lbl_max.setCursor(Qt.PointingHandCursor)
        self.lbl_max.setToolTip("Double-click to change range end")
        self.lbl_max.doubleClicked.connect(lambda: self._open_range_dialog("max"))
        slider_row.addWidget(self.lbl_max)

        root.addLayout(slider_row)

        # ── Toolbar row (all buttons + inline sliders) ──────────────────
        toolbar = QHBoxLayout()
        toolbar.setSpacing(4)

        # Play / Pause
        self.btn_play = self._icon_btn("\u25b6", self._tr("play"), w=34)
        self.btn_play.clicked.connect(self._toggle_play)
        toolbar.addWidget(self.btn_play)

        # Now
        btn_now = self._icon_btn("\u29bf", "Jump to today")
        btn_now.setObjectName("btn_now")
        btn_now.clicked.connect(lambda: self._set_current_date(date.today()))
        toolbar.addWidget(btn_now)

        # Pick Date
        btn_cal = self._icon_btn("\u25a6", self._tr("pick_date"))
        btn_cal.setObjectName("btn_cal")
        btn_cal.clicked.connect(self._open_calendar)
        toolbar.addWidget(btn_cal)

        # Settings
        btn_settings = self._icon_btn("\u2699", self._tr("settings"))
        btn_settings.setObjectName("btn_settings")
        btn_settings.clicked.connect(self._open_settings)
        toolbar.addWidget(btn_settings)

        toolbar.addSpacing(10)

        # Zoom label + slider + value
        self._zoom_lbl_widget = QLabel(self._tr("zoom"))
        self._zoom_lbl_widget.setObjectName("lbl_zoom_text")
        toolbar.addWidget(self._zoom_lbl_widget)
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(100, 2500)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(150)
        self.zoom_slider.setToolTip("Zoom")
        self.zoom_slider.valueChanged.connect(self._zoom_changed)
        toolbar.addWidget(self.zoom_slider)
        self.lbl_zoom = QLabel("1.00\u00d7")
        self.lbl_zoom.setFixedWidth(44)
        toolbar.addWidget(self.lbl_zoom)

        toolbar.addSpacing(8)

        # Zodiac toggle
        self.btn_zodiac = self._icon_btn("\u2648", "Toggle zodiac sectors", checkable=True)
        self.btn_zodiac.setChecked(True)
        self.btn_zodiac.toggled.connect(self._toggle_zodiac)
        toolbar.addWidget(self.btn_zodiac)

        # Even mode toggle
        self.btn_even = self._icon_btn("\u2261", "Equal orbit spacing", checkable=True)
        self.btn_even.toggled.connect(self._toggle_even)
        toolbar.addWidget(self.btn_even)

        # Geocentric mode toggle  (♁ = Earth symbol U+2641)
        self.btn_geo = self._icon_btn("\u2641", "Earth-centric view", checkable=True)
        self.btn_geo.toggled.connect(self._toggle_geo)
        toolbar.addWidget(self.btn_geo)

        # Zodiac sector wedges toggle  (☸ = wheel/dharma U+2638)
        self.btn_sectors = self._icon_btn("\u2638", "Show zodiac sector wedges", checkable=True)
        self.btn_sectors.toggled.connect(self._toggle_zodiac_sectors)
        toolbar.addWidget(self.btn_sectors)

        # Geocentric trail + retrograde stations toggle  (⇌ = double arrows)
        self.btn_trail = self._icon_btn("\u21cc", "Show geocentric trails & retrograde stations (geo mode)", checkable=True)
        self.btn_trail.toggled.connect(self._toggle_trail)
        toolbar.addWidget(self.btn_trail)

        # Planet info panel toggle  (ⓘ = circled i)
        self.btn_info = self._icon_btn("\u24d8", "Show info panel for selected planet", w=34, checkable=True)
        self.btn_info.toggled.connect(self._toggle_info_panel)
        toolbar.addWidget(self.btn_info)

        toolbar.addSpacing(8)

        # Alignment nav
        self.lbl_align = QLabel(self._tr("align_label"))
        self.lbl_align.setObjectName("lbl_align")
        toolbar.addWidget(self.lbl_align)
        self.btn_prev_align = self._icon_btn("\u25c4", self._tr("align_tip"), w=30)
        self.btn_prev_align.clicked.connect(self._jump_prev_align)
        toolbar.addWidget(self.btn_prev_align)
        self.lbl_align_count = QLabel("0")
        self.lbl_align_count.setFixedWidth(28)
        self.lbl_align_count.setAlignment(Qt.AlignCenter)
        self.lbl_align_count.setToolTip("Number of alignment events in range")
        toolbar.addWidget(self.lbl_align_count)
        self.btn_next_align = self._icon_btn("\u25ba", self._tr("align_tip"), w=30)
        self.btn_next_align.clicked.connect(self._jump_next_align)
        toolbar.addWidget(self.btn_next_align)

        # Marks toggle
        self.btn_marks = self._icon_btn("\u25cf", "Toggle alignment marks", w=30, checkable=True)
        self.btn_marks.setChecked(True)
        self.btn_marks.toggled.connect(self._toggle_marks)
        toolbar.addWidget(self.btn_marks)

        toolbar.addSpacing(8)

        # Planet scale label + slider + value
        lbl_p = QLabel("\u2295")
        lbl_p.setFont(QFont("Segoe UI Symbol", 11))
        lbl_p.setToolTip("Planet size scale")
        toolbar.addWidget(lbl_p)
        self.planet_slider = QSlider(Qt.Horizontal)
        self.planet_slider.setRange(25, 400)
        self.planet_slider.setValue(100)
        self.planet_slider.setFixedWidth(110)
        self.planet_slider.setToolTip("Scale planet sizes")
        self.planet_slider.valueChanged.connect(self._planet_scale_changed)
        toolbar.addWidget(self.planet_slider)
        self.lbl_planet_scale = QLabel("1.00\u00d7")
        self.lbl_planet_scale.setFixedWidth(44)
        toolbar.addWidget(self.lbl_planet_scale)

        toolbar.addStretch()
        root.addLayout(toolbar)

        # Connect planet selection signal
        self.canvas.planetSelected.connect(self._on_planet_selected)

    # ------------------------------------------------------------------
    def _set_current_date(self, d: date):
        d = max(self._slider_min, min(self._slider_max, d))
        self._current_date = d
        days_offset = (d - self._slider_min).days
        self._current_float_offset = float(days_offset)
        self.slider.blockSignals(True)
        self.slider.setValue(days_offset)
        self.slider.blockSignals(False)
        self.canvas.set_time_suffix("")
        self.canvas.set_date(d)
        self._update_moon_phase_btn(d)

    def _slider_moved(self, value: int):
        d = self._slider_min + timedelta(days=value)
        self._current_date = d
        self._current_float_offset = float(value)
        self.canvas.set_time_suffix("")
        self.canvas.set_date(d)
        self._update_moon_phase_btn(d)

    def _update_moon_phase_btn(self, d: date):
        pass  # Moon phase is now rendered directly on the canvas

    def _on_planet_selected(self, name: str):
        # Info panel shows automatically if btn_info is checked
        pass  # canvas already updated via set_selected_planet via signal

    # ── Solar-term navigation ──────────────────────────────────────────
    def _jump_prev_solar_term(self):
        cur = self._current_float_offset - 0.01
        best = None
        for offset, kind in self._solar_term_data:
            if offset < cur and (best is None or offset > best[0]):
                best = (offset, kind)
        if best is not None:
            self._go_to_solar_term(*best)

    def _jump_next_solar_term(self):
        cur = self._current_float_offset + 0.01
        best = None
        for offset, kind in self._solar_term_data:
            if offset > cur and (best is None or offset < best[0]):
                best = (offset, kind)
        if best is not None:
            self._go_to_solar_term(*best)

    def _go_to_solar_term(self, offset: float, kind: int):
        """Move to a solar term given its float day-offset from slider_min."""
        day = int(offset)
        frac = offset - day
        total_minutes = round(frac * 24 * 60)
        hours, minutes = divmod(total_minutes, 60)
        d = self._slider_min + timedelta(days=day)
        self._current_float_offset = offset
        self._current_date = d
        self.slider.blockSignals(True)
        self.slider.setValue(day)
        self.slider.blockSignals(False)
        sym_char = _ST_SYMBOLS[kind][0]
        self.canvas.set_time_suffix(f"{sym_char} {hours:02d}:{minutes:02d}")
        self.canvas.set_date(d)
        self._update_moon_phase_btn(d)

    def _toggle_play(self):
        if self._animation_timer.isActive():
            self._animation_timer.stop()
            self.btn_play.setText("\u25b6")
        else:
            self._animation_timer.start()
            self.btn_play.setText("\u23f8")

    def _set_speed(self, days: int):
        self._anim_step = days

    def _advance_day(self):
        total = (self._slider_max - self._slider_min).days
        new_val = self.slider.value() + self._anim_step
        if new_val > total:
            new_val = 0
        self.slider.setValue(new_val)

    # ------------------------------------------------------------------
    def _set_slider_range(self, new_min: date, new_max: date):
        self._slider_min = new_min
        self._slider_max = new_max
        total = (new_max - new_min).days
        cur_offset = max(0, min(total, (self._current_date - new_min).days))
        self.slider.blockSignals(True)
        self.slider.setRange(0, total)
        self.slider.set_date_range(new_min)
        self.slider.setValue(cur_offset)
        self.slider.blockSignals(False)
        self.lbl_min.setText(new_min.strftime("%Y-%m-%d"))
        self.lbl_max.setText(new_max.strftime("%Y-%m-%d"))
        self.canvas.set_date(new_min + timedelta(days=cur_offset))
        self.canvas.set_trail_range(new_min, new_max)
        self._solar_term_data = compute_solar_terms(new_min, new_max)
        self.slider.set_solar_terms(self._solar_term_data)
        self._recompute_alignments()

    def _open_range_dialog(self, side: str = ""):
        dlg = QDialog(self)
        dlg.setWindowTitle("Set Slider Range")
        dlg.setStyleSheet(self.styleSheet())
        vbox = QVBoxLayout(dlg)
        form = QFormLayout()
        de_min = QDateEdit(QDate(self._slider_min.year, self._slider_min.month, self._slider_min.day))
        de_max = QDateEdit(QDate(self._slider_max.year, self._slider_max.month, self._slider_max.day))
        for de in (de_min, de_max):
            de.setCalendarPopup(True)
            de.setDisplayFormat("yyyy-MM-dd")
            de.setMinimumWidth(130)
        form.addRow("Start date:", de_min)
        form.addRow("End date:",   de_max)
        vbox.addLayout(form)
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        vbox.addWidget(btns)
        # Focus the relevant field
        if side == "min":
            de_min.setFocus()
        elif side == "max":
            de_max.setFocus()
        if dlg.exec() == QDialog.Accepted:
            qmin, qmax = de_min.date(), de_max.date()
            new_min = date(qmin.year(), qmin.month(), qmin.day())
            new_max = date(qmax.year(), qmax.month(), qmax.day())
            if new_max > new_min:
                self._set_slider_range(new_min, new_max)
                self._save_settings()

    # ------------------------------------------------------------------
    # Internationalisation
    # ------------------------------------------------------------------
    def _tr(self, key: str) -> str:
        return STRINGS.get(self._lang, STRINGS["en"]).get(key, key)

    def _apply_language(self):
        self.setWindowTitle(self._tr("title"))
        # Update tooltip text for icon buttons
        for obj_name, key in [
            ("btn_now",      "now"),
            ("btn_cal",      "pick_date"),
            ("btn_settings", "settings"),
        ]:
            btn = self.findChild(QPushButton, obj_name)
            if btn:
                btn.setToolTip(self._tr(key))
        for obj_name, key in [("lbl_align", "align_label")]:
            lbl = self.findChild(QLabel, obj_name)
            if lbl:
                lbl.setText(self._tr(key))
        is_play = not self._animation_timer.isActive()
        self.btn_play.setText("\u25b6" if is_play else "\u23f8")
        self.btn_zodiac.setToolTip(self._tr("zodiac"))
        self.btn_even.setToolTip(self._tr("even"))
        # Update zoom label
        lbl = self.findChild(QLabel, "lbl_zoom_text")
        if lbl:
            lbl.setText(self._tr("zoom"))
        # Update zodiac names on canvas
        self.canvas.set_zodiac_names(self._tr("zodiac_names"))

    # ------------------------------------------------------------------
    # Settings dialog
    # ------------------------------------------------------------------
    def _open_settings(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(self._tr("settings_title"))
        dlg.setStyleSheet(self.styleSheet())
        dlg.setMinimumWidth(340)
        vbox = QVBoxLayout(dlg)

        form = QFormLayout()
        form.setSpacing(10)

        # Language
        cmb_lang = QComboBox()
        cmb_lang.addItem("English", "en")
        cmb_lang.addItem("\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430", "uk")
        cur_idx = cmb_lang.findData(self._lang)
        if cur_idx >= 0:
            cmb_lang.setCurrentIndex(cur_idx)
        form.addRow(self._tr("lang_label"), cmb_lang)

        # Zodiac font size  (50 – 200 %)
        spn_font = QSpinBox()
        spn_font.setRange(50, 200)
        spn_font.setSuffix(" %")
        spn_font.setValue(int(self._zodiac_font_scale * 100))
        form.addRow(self._tr("zfont_label"), spn_font)

        # Min aligned planets for marks (3 – 8)
        spn_min_align = QSpinBox()
        spn_min_align.setRange(3, 8)
        spn_min_align.setValue(self._min_align_planets)
        spn_min_align.setToolTip("Minimum number of planets in alignment to show a mark")
        form.addRow("Min planets (marks):", spn_min_align)

        vbox.addLayout(form)

        # Time slider range group
        grp = QGroupBox(self._tr("range_group"))
        grp.setStyleSheet("QGroupBox { color: #80a0c0; font-size: 9pt; }")
        gform = QFormLayout(grp)
        de_min = QDateEdit(QDate(self._slider_min.year,
                                 self._slider_min.month,
                                 self._slider_min.day))
        de_max = QDateEdit(QDate(self._slider_max.year,
                                 self._slider_max.month,
                                 self._slider_max.day))
        for de in (de_min, de_max):
            de.setCalendarPopup(True)
            de.setDisplayFormat("yyyy-MM-dd")
            de.setMinimumWidth(140)
        gform.addRow(self._tr("start_date"), de_min)
        gform.addRow(self._tr("end_date"),   de_max)
        vbox.addWidget(grp)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        vbox.addWidget(btns)

        if dlg.exec() != QDialog.Accepted:
            return

        # Apply language
        new_lang = cmb_lang.currentData()
        if new_lang != self._lang:
            self._lang = new_lang
            self._apply_language()

        # Apply zodiac font
        new_scale = spn_font.value() / 100.0
        if new_scale != self._zodiac_font_scale:
            self._zodiac_font_scale = new_scale
            self.canvas.set_zodiac_font_scale(new_scale)

        # Apply min aligned planets
        new_min_align = spn_min_align.value()
        if new_min_align != self._min_align_planets:
            self._min_align_planets = new_min_align
            self._recompute_alignments()

        # Apply date range
        qmin, qmax = de_min.date(), de_max.date()
        new_min = date(qmin.year(), qmin.month(), qmin.day())
        new_max = date(qmax.year(), qmax.month(), qmax.day())
        if new_max > new_min and (new_min != self._slider_min or new_max != self._slider_max):
            self._set_slider_range(new_min, new_max)

        self._save_settings()

    # ------------------------------------------------------------------
    # Alignment marks
    # ------------------------------------------------------------------
    def _recompute_alignments(self):
        self._alignment_marks = compute_alignments(
            self._slider_min, self._slider_max, self._min_align_planets)
        self.slider.set_marks(self._alignment_marks)
        self.lbl_align_count.setText(str(len(self._alignment_marks)))

    def _jump_prev_align(self):
        cur = self.slider.value()
        prev = [m[0] for m in self._alignment_marks if m[0] < cur]
        if prev:
            self.slider.setValue(prev[-1])

    def _jump_next_align(self):
        cur = self.slider.value()
        nxt = [m[0] for m in self._alignment_marks if m[0] > cur]
        if nxt:
            self.slider.setValue(nxt[0])

    # ------------------------------------------------------------------
    def _toggle_zodiac(self, checked: bool):
        self.canvas.set_show_zodiac(checked)
        self._save_settings()

    def _toggle_even(self, checked: bool):
        self.canvas.set_even_mode(checked)
        self._zoom_lbl_widget.setVisible(not checked)
        self.zoom_slider.setVisible(not checked)
        self.lbl_zoom.setVisible(not checked)
        self._save_settings()

    def _toggle_geo(self, checked: bool):
        self.canvas.set_geo_mode(checked)
        self._save_settings()

    def _toggle_zodiac_sectors(self, checked: bool):
        self.canvas.set_show_zodiac_sectors(checked)
        self._save_settings()

    def _toggle_trail(self, checked: bool):
        self.canvas.set_show_trail(checked)
        self._save_settings()

    def _toggle_info_panel(self, checked: bool):
        self.canvas.set_show_info_panel(checked)
        self._save_settings()

    def _toggle_marks(self, checked: bool):
        self.slider.set_show_marks(checked)
        self._save_settings()

    def _planet_scale_changed(self, value: int):
        scale = value / 100.0
        self.lbl_planet_scale.setText(f"{scale:.2f}\u00d7")
        self.canvas.set_planet_scale(scale)
        self._save_settings()

    def _zoom_changed(self, value: int):
        factor = value / 100.0
        self.lbl_zoom.setText(f"{factor:.2f}×")
        self.canvas.set_zoom(factor)
        self._save_settings()

    # ------------------------------------------------------------------
    # Settings path: INI file next to the script for reliable cross-OS saves
    @staticmethod
    def _settings() -> QSettings:
        ini = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.ini")
        return QSettings(ini, QSettings.IniFormat)

    def _save_settings(self):
        s = self._settings()
        s.setValue("zoom",              self.zoom_slider.value())
        s.setValue("show_zodiac",       self.btn_zodiac.isChecked())
        s.setValue("even_mode",         self.btn_even.isChecked())
        s.setValue("slider_min",        self._slider_min.isoformat())
        s.setValue("slider_max",        self._slider_max.isoformat())
        s.setValue("language",          self._lang)
        s.setValue("zodiac_font_scale",  int(self._zodiac_font_scale * 100))
        s.setValue("show_marks",        self.btn_marks.isChecked())
        s.setValue("planet_scale",      self.planet_slider.value())
        s.setValue("min_align_planets", self._min_align_planets)
        s.setValue("geo_mode",          self.btn_geo.isChecked())
        s.setValue("zodiac_sectors",    self.btn_sectors.isChecked())
        s.setValue("show_trail",        self.btn_trail.isChecked())
        s.setValue("show_info_panel",   self.btn_info.isChecked())
        s.sync()

    def _load_settings(self):
        # Block all interactive-widget signals so that mid-load state changes
        # (e.g. btn_even going False→True) don't trigger _save_settings() and
        # overwrite the INI with partially-default values before we finish loading.
        _blocked = [
            self.btn_zodiac, self.btn_even, self.btn_geo, self.btn_sectors,
            self.btn_trail, self.btn_info, self.btn_marks, self.zoom_slider, self.planet_slider,
        ]
        for w in _blocked:
            w.blockSignals(True)
        try:
            self._do_load_settings()
        finally:
            for w in _blocked:
                w.blockSignals(False)
            # Manually propagate every loaded state to canvas/widgets
            # (signals were blocked, so handlers never fired during load)
            self._zoom_changed(self.zoom_slider.value())
            self._planet_scale_changed(self.planet_slider.value())
            self.canvas.set_show_zodiac(self.btn_zodiac.isChecked())
            self.canvas.set_even_mode(self.btn_even.isChecked())
            self.canvas.set_geo_mode(self.btn_geo.isChecked())
            self.canvas.set_show_zodiac_sectors(self.btn_sectors.isChecked())
            self.canvas.set_show_trail(self.btn_trail.isChecked())
            self.canvas.set_show_info_panel(self.btn_info.isChecked())
            self.slider.set_show_marks(self.btn_marks.isChecked())
            # Zoom row visibility depends on even mode
            even_on = self.btn_even.isChecked()
            self._zoom_lbl_widget.setVisible(not even_on)
            self.zoom_slider.setVisible(not even_on)
            self.lbl_zoom.setVisible(not even_on)
            # Refresh moon phase display with loaded date
            self._update_moon_phase_btn(self._current_date)
            # One clean save so the file is up to date
            self._save_settings()

    def _do_load_settings(self):
        s = self._settings()
        try:
            zoom = int(s.value("zoom", 100))
            self.zoom_slider.setValue(zoom)
        except (TypeError, ValueError):
            pass
        zodiac = s.value("show_zodiac", True)
        # QSettings stores bools as strings on some platforms
        if isinstance(zodiac, str):
            zodiac = zodiac.lower() not in ("false", "0", "")
        self.btn_zodiac.setChecked(bool(zodiac))
        even = s.value("even_mode", False)
        if isinstance(even, str):
            even = even.lower() not in ("false", "0", "")
        self.btn_even.setChecked(bool(even))
        # Language
        lang = s.value("language", "en")
        if lang in STRINGS:
            self._lang = lang
            self._apply_language()
        # Zodiac font scale
        try:
            zfs = int(s.value("zodiac_font_scale", 100))
            self._zodiac_font_scale = zfs / 100.0
            self.canvas.set_zodiac_font_scale(self._zodiac_font_scale)
        except (TypeError, ValueError):
            pass
        # Show marks
        show_marks = s.value("show_marks", True)
        if isinstance(show_marks, str):
            show_marks = show_marks.lower() not in ("false", "0", "")
        self.btn_marks.setChecked(bool(show_marks))
        # Planet scale
        try:
            ps = int(s.value("planet_scale", 100))
            self.planet_slider.setValue(ps)
        except (TypeError, ValueError):
            pass
        try:
            raw_min = s.value("slider_min", None)
            raw_max = s.value("slider_max", None)
            if raw_min and raw_max:
                new_min = date.fromisoformat(raw_min)
                new_max = date.fromisoformat(raw_max)
                if new_max > new_min:
                    self._set_slider_range(new_min, new_max)
        except (TypeError, ValueError):
            pass
        # Min aligned planets
        try:
            map_val = int(s.value("min_align_planets", 3))
            if 3 <= map_val <= 8:
                self._min_align_planets = map_val
        except (TypeError, ValueError):
            pass
        # Geo mode
        geo = s.value("geo_mode", False)
        if isinstance(geo, str):
            geo = geo.lower() not in ("false", "0", "")
        self.btn_geo.setChecked(bool(geo))
        # Zodiac sectors
        sectors = s.value("zodiac_sectors", False)
        if isinstance(sectors, str):
            sectors = sectors.lower() not in ("false", "0", "")
        self.btn_sectors.setChecked(bool(sectors))
        # Trail
        trail = s.value("show_trail", False)
        if isinstance(trail, str):
            trail = trail.lower() not in ("false", "0", "")
        self.btn_trail.setChecked(bool(trail))
        # Info panel
        info_panel = s.value("show_info_panel", False)
        if isinstance(info_panel, str):
            info_panel = info_panel.lower() not in ("false", "0", "")
        self.btn_info.setChecked(bool(info_panel))
        # Compute alignment marks for initial range
        self._recompute_alignments()

    def closeEvent(self, event):
        self._save_settings()
        super().closeEvent(event)

    def _open_calendar(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Pick a Date")
        dlg.setStyleSheet(self.styleSheet() + """
            QCalendarWidget QAbstractItemView {
                color: #c8d8f0; background: #0d1a30;
                selection-background-color: #2a5a9a;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #0d1a30;
            }
            QCalendarWidget QToolButton {
                color: #90c0e8; background: #1a2a4a;
                border: 1px solid #2a4a7a; border-radius: 4px;
            }
            QCalendarWidget QSpinBox {
                color: #90c0e8; background: #1a2a4a;
                border: 1px solid #2a4a7a;
            }
        """)
        vbox = QVBoxLayout(dlg)
        cal = QCalendarWidget()
        cal.setMinimumDate(QDate(DATE_MIN.year, DATE_MIN.month, DATE_MIN.day))
        cal.setMaximumDate(QDate(DATE_MAX.year, DATE_MAX.month, DATE_MAX.day))
        # pre-select current simulation date
        cd = self._current_date
        cal.setSelectedDate(QDate(cd.year, cd.month, cd.day))
        vbox.addWidget(cal)
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        vbox.addWidget(btns)
        if dlg.exec() == QDialog.Accepted:
            qd = cal.selectedDate()
            self._set_current_date(date(qd.year(), qd.month(), qd.day()))


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Solar System")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
