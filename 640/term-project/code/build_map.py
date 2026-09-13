"""
The Second Rent -- build the standalone interactive choropleth (Medium 02).

Emits one self-contained HTML file: inline SVG geometry, inline data, inline
fonts, no network calls. Hover a county for a tooltip, click to pin it, toggle
the age band, or switch to the compare view.

    python code/build_map.py  ->  mediums/secondrent_map.html

David Jorgensen | DSC 640 Term Project
"""

import base64
import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.affinity import scale, translate

sys.path.insert(0, str(Path(__file__).resolve().parent))
import secondrent as sr  # noqa: E402

OUT = sr.ROOT / "mediums" / "secondrent_map.html"
AGES = {"infant": "MCInfant", "toddler": "MCToddler", "preschool": "MCPreschool"}
YEARS = list(range(2008, 2019))

# ------------------------------------------------------------------ geometry


def composite_geometry():
    """CONUS in Albers with Alaska and Hawaii scaled and tucked in beneath."""
    counties = gpd.read_file(f"zip://{sr.GEO / 'cb_2018_us_county_20m.zip'}")
    states = gpd.read_file(f"zip://{sr.GEO / 'cb_2018_us_state_20m.zip'}")
    counties["GEOID"] = counties["GEOID"].astype(str).str.zfill(5)

    def part(gdf, fips, epsg):
        sub = gdf[gdf["STATEFP"].isin(fips)].to_crs(epsg=epsg).copy()
        return sub

    lower48 = [f"{i:02d}" for i in range(1, 57) if f"{i:02d}" not in ("02", "15")]
    c_main, s_main = part(counties, lower48, 5070), part(states, lower48, 5070)
    minx, miny, maxx, maxy = s_main.total_bounds

    def place(gdf, factor, at_x, at_y):
        """Scale a projected inset and drop its lower-left corner at (at_x, at_y)."""
        geom = gdf.geometry
        origin = (geom.total_bounds[0], geom.total_bounds[1])
        geom = geom.apply(lambda g: scale(g, factor, factor, origin=origin))
        bx, by = geom.total_bounds[0], geom.total_bounds[1]
        out = gdf.copy()
        out.geometry = geom.apply(lambda g: translate(g, at_x - bx, at_y - by))
        return out

    ak_x, ak_y = minx - 90_000, miny - 300_000
    hi_x, hi_y = minx + 1_150_000, miny - 330_000
    c_ak = place(part(counties, ["02"], 3338), 0.36, ak_x, ak_y)
    s_ak = place(part(states, ["02"], 3338), 0.36, ak_x, ak_y)
    c_hi = place(part(counties, ["15"], 26962), 1.0, hi_x, hi_y)
    s_hi = place(part(states, ["15"], 26962), 1.0, hi_x, hi_y)

    # The insets have been scaled and moved, so the result is a composite layout
    # rather than any real projection. Drop the CRS before merging.
    parts = [c_main, c_ak, c_hi, s_main, s_ak, s_hi]
    parts = [g.set_crs(None, allow_override=True) for g in parts]
    allc = gpd.GeoDataFrame(pd.concat(parts[:3], ignore_index=True), geometry="geometry")
    alls = gpd.GeoDataFrame(pd.concat(parts[3:], ignore_index=True), geometry="geometry")
    # 20m boundaries carry more vertices than a 1,000px map can resolve.
    allc.geometry = allc.geometry.simplify(1500, preserve_topology=True)
    alls.geometry = alls.geometry.simplify(1500, preserve_topology=True)
    return allc, alls


def to_paths(gdf, minx, maxy, k):
    """Turn projected geometry into SVG path data in a y-down pixel space."""

    def ring(coords):
        pts = [f"{(x - minx) * k:.1f},{(maxy - y) * k:.1f}" for x, y in coords]
        return "M" + "L".join(pts) + "Z"

    out = []
    for geom in gdf.geometry:
        if geom is None or geom.is_empty:
            out.append("")
            continue
        polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
        d = "".join(ring(p.exterior.coords) for p in polys)
        out.append(d)
    return out


# ---------------------------------------------------------------------- data


def build_data(df):
    """Per-county attributes for every age band, plus the reference series."""
    d18 = df[df.StudyYear == 2018].copy()
    idx = np.interp(YEARS, [2008, 2018], [sr.CPI[2008], sr.CPI[2018]])
    deflator = pd.Series(sr.CPI[2018] / idx, index=YEARS)

    counties, refs = {}, {"national": {}, "states": {}}

    for age, col in AGES.items():
        d18[f"b_{age}"] = d18[col] * sr.WEEKS / d18["MHI"] * 100
        d18[f"r_{age}"] = d18.groupby("State_Abbreviation")[f"b_{age}"].rank(
            ascending=False, method="min"
        )
        nat = df.dropna(subset=[col]).groupby("StudyYear")[col].median() * deflator
        refs["national"][age] = [round(nat.get(y, float("nan")), 1) for y in YEARS]
        for st, grp in df.dropna(subset=[col]).groupby("State_Abbreviation"):
            s = grp.groupby("StudyYear")[col].median() * deflator
            refs["states"].setdefault(st, {})[age] = [
                None if pd.isna(s.get(y)) else round(s.get(y), 1) for y in YEARS
            ]

    counted = {
        age: d18.dropna(subset=[f"b_{age}"]).groupby("State_Abbreviation").size().to_dict()
        for age in AGES
    }

    series = {}
    for age, col in AGES.items():
        piv = df.pivot_table(index="County_FIPS_Code", columns="StudyYear", values=col)
        piv = piv.reindex(columns=YEARS)
        for y in YEARS:
            piv[y] = piv[y] * deflator[y]
        series[age] = piv.round(0)

    for _, r in d18.iterrows():
        fips = r["County_FIPS_Code"]
        rec = {
            "n": r["County_Name"],
            "s": r["State_Abbreviation"],
            "S": r["State_Name"],
            "i": None if pd.isna(r["MHI"]) else int(r["MHI"]),
            "b": {},
            "p": {},
            "k": {},
            "t": {},
        }
        for age, col in AGES.items():
            b, price, rank = r[f"b_{age}"], r[col], r[f"r_{age}"]
            rec["b"][age] = None if pd.isna(b) else round(float(b), 1)
            rec["p"][age] = None if pd.isna(price) else round(float(price))
            rec["k"][age] = (
                None if pd.isna(rank) else [int(rank), int(counted[age].get(r["State_Abbreviation"], 0))]
            )
            row = series[age].loc[fips] if fips in series[age].index else None
            rec["t"][age] = (
                None if row is None
                else [None if pd.isna(v) else int(v) for v in row.tolist()]
            )
        counties[fips] = rec

    return counties, refs


# ---------------------------------------------------------------------- html


def font_face(name, weight, filename):
    raw = (sr.FONTS / filename).read_bytes()
    b64 = base64.b64encode(raw).decode()
    kind = "woff2" if filename.endswith(".woff2") else "truetype"
    return (
        f'@font-face{{font-family:"{name}";font-weight:{weight};font-display:swap;'
        f'src:url(data:font/{kind};base64,{b64}) format("{kind}");}}'
    )


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Second Rent &mdash; Childcare burden by county</title>
<style>
__FONTS__
:root{
  --ink:#163a48; --mid:#5c8a9b; --muted:#93b3bd; --pale:#c3d4da; --wash:#e9eef1;
  --paper:#faf9f7; --panel:#f4f2f0; --rule:#d9dedd; --accent:#bf5a3f; --nodata:#eef0ee;
}
*{box-sizing:border-box;margin:0;padding:0}
body{
  background:var(--paper); color:var(--ink);
  font-family:"Source Sans 3",system-ui,sans-serif; font-size:15px; line-height:1.5;
  padding:28px 26px 40px;
}
.wrap{max-width:1240px;margin:0 auto}
.kicker{font-size:11px;letter-spacing:.19em;text-transform:uppercase;color:var(--accent);
        font-weight:700}
h1{font-family:"Merriweather",Georgia,serif;font-weight:700;font-size:30px;line-height:1.15;
   margin-top:8px;letter-spacing:-.01em}
.deck{color:var(--mid);margin-top:8px;max-width:62ch}
.bar{display:flex;flex-wrap:wrap;gap:22px;align-items:flex-end;justify-content:space-between;
     border-bottom:1px solid var(--rule);padding-bottom:14px;margin:20px 0 18px}
.group{display:flex;gap:0}
.group button{
  font:inherit;font-size:13px;font-weight:600;color:var(--mid);background:var(--paper);
  border:1px solid var(--rule);padding:6px 15px;cursor:pointer;margin-left:-1px;
}
.group button:first-child{margin-left:0}
.group button[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.group.warm button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent)}
.grouplab{font-size:10.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--mid);
          font-weight:700;margin-bottom:6px}

.app{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:24px;align-items:start}
@media (max-width:980px){.app{grid-template-columns:minmax(0,1fr)}}
.view{display:none}
.view.on{display:block}

svg{display:block;width:100%;height:auto;overflow:visible}
#map path.county{stroke:#ffffff;stroke-width:.4;cursor:pointer}
#map path.county:hover{stroke:var(--ink);stroke-width:1.1}
#map path.state{fill:none;stroke:#ffffff;stroke-width:1.1;pointer-events:none}
#map path.pinned{stroke:var(--accent);stroke-width:2.2;pointer-events:none;fill:none}

.legend{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin-top:10px;font-size:12px;
        color:var(--mid)}
.legend .steps{display:flex}
.legend .steps span{display:flex;flex-direction:column;align-items:flex-start;font-size:11px}
.legend .steps i{display:block;width:56px;height:11px}
.caption{font-size:12.5px;color:var(--mid);border-top:1px solid var(--rule);margin-top:12px;
         padding-top:8px}
.caption b{color:var(--ink);font-weight:600}

.rail{background:var(--panel);padding:16px 16px 18px;position:sticky;top:20px}
.rail h2{font-size:10.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--mid);
         font-weight:700;margin-bottom:6px}
.cname{font-family:"Merriweather",Georgia,serif;font-weight:700;font-size:19px;line-height:1.15}
.cstate{font-size:11px;letter-spacing:.12em;color:var(--mid);font-weight:600;margin-top:2px}
.big{font-family:"Merriweather",Georgia,serif;font-weight:700;font-size:40px;line-height:1;
     color:var(--accent);margin-top:10px}
.sub{font-size:12.5px;color:var(--mid);margin-top:4px}
.chip{display:inline-block;margin-top:10px;padding:4px 9px;border:1px solid var(--accent);
      color:var(--accent);font-size:12px;font-weight:600}
.railrule{border:0;border-top:1px solid var(--rule);margin:15px 0 12px}
.hintbox{margin-top:12px;padding:9px 11px;background:var(--paper);border:1px solid var(--rule);
         font-size:12px;color:var(--mid)}
.hintbox b{color:var(--ink);font-weight:600}

#tip{
  position:fixed;pointer-events:none;opacity:0;transition:opacity .08s;z-index:9;
  background:var(--ink);color:var(--paper);padding:7px 10px;font-size:12.5px;line-height:1.35;
  max-width:220px;
}
#tip b{font-weight:700}
#tip .v{color:#e9c3b6;font-weight:700}

footer{border-top:1px solid var(--rule);margin-top:26px;padding-top:10px;font-size:11.5px;
       color:var(--mid);line-height:1.45}
footer b{color:var(--ink);font-weight:600}
</style>
</head>
<body>
<div class="wrap">

  <span class="kicker">The Second Rent &middot; Medium 02</span>
  <h1>Childcare burden by county</h1>
  <p class="deck">Center-based childcare priced as a share of local median household income, 2018.
    The federal government calls care affordable at 7%. Hover any county for its number, click to
    pin it, and switch the age band to watch the premium move.</p>

  <div class="bar">
    <div>
      <div class="grouplab">Child&rsquo;s age</div>
      <div class="group warm" id="ages">
        <button data-age="infant" aria-pressed="true">Infant</button>
        <button data-age="toddler" aria-pressed="false">Toddler</button>
        <button data-age="preschool" aria-pressed="false">Preschool</button>
      </div>
    </div>
    <div>
      <div class="grouplab">View</div>
      <div class="group" id="views">
        <button data-view="map" aria-pressed="true">Map view</button>
        <button data-view="compare" aria-pressed="false">Compare view</button>
      </div>
    </div>
  </div>

  <div class="app">
    <div>
      <div class="view on" id="view-map">
        <svg id="map" viewBox="0 0 __W__ __H__" role="img"
             aria-label="Choropleth of childcare burden by United States county">
          <g id="counties"></g>
          <g id="states">__STATES__</g>
          <path id="pin" class="pinned"></path>
          <text x="14" y="__AKY__" font-size="13" fill="#5c8a9b" font-weight="600">ALASKA</text>
          <text x="__HIX__" y="__HIY__" font-size="13" fill="#5c8a9b" font-weight="600">HAWAII</text>
        </svg>
        <div class="legend">
          <div class="steps" id="legend"></div>
          <span><i style="display:inline-block;width:22px;height:11px;background:var(--nodata);
            border:1px solid var(--rule);vertical-align:-1px"></i> not reported</span>
        </div>
        <p class="caption"><b>The map is the interface.</b> Every shaded county spends more than
          the 7% standard. Blank counties did not publish a price that year, which is not the same
          as being cheap.</p>
      </div>

      <div class="view" id="view-compare">
        <svg id="scatter" viewBox="0 0 720 520" role="img"
             aria-label="County median income against annualized childcare price"></svg>
        <p class="caption"><b>Cheap is not the same as affordable.</b> Each dot is a county; the
          diagonals are fixed shares of income. A county above the 15% line is unaffordable
          whatever its sticker price. The pinned county keeps its ring in both views.</p>
      </div>
    </div>

    <aside class="rail">
      <h2>Selected county</h2>
      <div class="cname" id="cname">Suffolk County</div>
      <div class="cstate" id="cstate">MASSACHUSETTS</div>
      <div class="big" id="cburden">32.2%</div>
      <div class="sub" id="csub">of median household income goes to center-based infant care</div>
      <div class="chip" id="crank">Rank 1 of 14 counties</div>

      <hr class="railrule">
      <h2 id="trendlab">Real price, 2008&ndash;2018</h2>
      <svg id="trend" viewBox="0 0 300 190" role="img"
           aria-label="Real price trend for the selected county"></svg>
      <div class="sub" id="tsub"></div>

      <div class="hintbox"><b>Why three lines?</b> A single county trend answers &ldquo;is it
        rising?&rdquo; Adding the state and national medians answers what a legislator asks next:
        rising compared with what?</div>
    </aside>
  </div>

  <footer>
    <b>Source:</b> U.S. Department of Labor, Women&rsquo;s Bureau, National Database of Childcare
    Prices, 2008&ndash;2018. <b>Method:</b> full-time weekly prices annualized &times;52; trends
    deflated to constant 2018 dollars with CPI-U annual averages; burden = annualized price
    &divide; county median household income. The ratio describes a county, not an individual
    household, and no values are imputed. Prepared by David Jorgensen, DSC 640 Term Project.
  </footer>
</div>

<div id="tip"></div>

<script>
const DATA = __DATA__;
const REFS = __REFS__;
const PATHS = __PATHS__;
const YEARS = __YEARS__;
const RAMP = __RAMP__;
const CUTS = [10, 13, 16, 19, 21];
const LABELS = __BINLABELS__;
const NODATA = "#eef0ee";
const ACCENT = "#bf5a3f";
const AGE_WORD = {infant: "infant", toddler: "toddler", preschool: "preschool"};

let age = "infant";
let pinned = "25025";

const $ = (s) => document.querySelector(s);
const shade = (v) => {
  if (v === null || v === undefined) return NODATA;
  for (let i = 0; i < CUTS.length; i++) if (v < CUTS[i]) return RAMP[i];
  return RAMP[5];
};

/* ---------------------------------------------------------------- map */
const gCounties = $("#counties");
for (const fips in PATHS) {
  const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
  p.setAttribute("d", PATHS[fips]);
  p.setAttribute("class", "county");
  p.dataset.fips = fips;
  gCounties.appendChild(p);
}

const legend = $("#legend");
RAMP.forEach((c, i) => {
  const s = document.createElement("span");
  s.innerHTML = '<i style="background:' + c + '"></i>' + LABELS[i];
  legend.appendChild(s);
});

function paintMap() {
  for (const p of gCounties.children) {
    const rec = DATA[p.dataset.fips];
    p.setAttribute("fill", shade(rec ? rec.b[age] : null));
  }
  const pin = $("#pin");
  pin.setAttribute("d", PATHS[pinned] || "");
}

/* ------------------------------------------------------------ tooltip */
const tip = $("#tip");
gCounties.addEventListener("mousemove", (e) => {
  const t = e.target.closest("path.county");
  if (!t) return;
  const rec = DATA[t.dataset.fips];
  if (!rec) return;
  const v = rec.b[age];
  tip.innerHTML = "<b>" + rec.n + ", " + rec.s + "</b><br>" +
    (v === null
      ? "no published price"
      : '<span class="v">' + v.toFixed(1) + "%</span> of median income &middot; $" +
        rec.p[age] + "/wk");
  tip.style.opacity = 1;
  const pad = 14;
  let x = e.clientX + pad, y = e.clientY + pad;
  if (x + 230 > window.innerWidth) x = e.clientX - 230;
  tip.style.left = x + "px";
  tip.style.top = y + "px";
});
gCounties.addEventListener("mouseleave", () => (tip.style.opacity = 0));
gCounties.addEventListener("click", (e) => {
  const t = e.target.closest("path.county");
  if (t && DATA[t.dataset.fips]) { pinned = t.dataset.fips; render(); }
});

/* --------------------------------------------------------------- rail */
function renderRail() {
  const rec = DATA[pinned];
  $("#cname").textContent = rec.n;
  $("#cstate").textContent = rec.S.toUpperCase();
  const v = rec.b[age];
  $("#cburden").textContent = v === null ? "n/a" : v.toFixed(1) + "%";
  $("#csub").textContent =
    "of median household income goes to center-based " + AGE_WORD[age] + " care";
  const k = rec.k[age];
  $("#crank").textContent = k
    ? "Rank " + k[0] + " of " + k[1] + " counties in " + rec.s
    : "not ranked — no published price";
  $("#trendlab").innerHTML = "Real price, 2008–2018";
}

/* -------------------------------------------------------------- trend */
function renderTrend() {
  const rec = DATA[pinned];
  const svg = $("#trend");
  const W = 300, H = 190, L = 40, R = 96, T = 10, B = 26;
  const county = rec.t[age] || [];
  const state = (REFS.states[rec.s] || {})[age] || [];
  const nat = REFS.national[age] || [];
  const all = [].concat(county, state, nat).filter((v) => v !== null && v !== undefined);
  if (!all.length) { svg.innerHTML = ""; $("#tsub").textContent = ""; return; }
  const lo = Math.floor(Math.min.apply(null, all) / 50) * 50;
  const hi = Math.ceil(Math.max.apply(null, all) / 50) * 50;
  const x = (i) => L + (i / (YEARS.length - 1)) * (W - L - R);
  const y = (v) => H - B - ((v - lo) / (hi - lo || 1)) * (H - T - B);

  const line = (vals, color, w) => {
    let d = "", pen = false;
    vals.forEach((v, i) => {
      if (v === null || v === undefined) { pen = false; return; }
      d += (pen ? "L" : "M") + x(i).toFixed(1) + "," + y(v).toFixed(1);
      pen = true;
    });
    return d ? '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="' + w +
      '" stroke-linecap="round" stroke-linejoin="round"/>' : "";
  };
  const last = (vals) => { for (let i = vals.length - 1; i >= 0; i--)
    if (vals[i] !== null && vals[i] !== undefined) return [i, vals[i]]; return null; };
  const tag = (vals, color, text, weight) => {
    const p = last(vals);
    if (!p) return "";
    return '<circle cx="' + x(p[0]).toFixed(1) + '" cy="' + y(p[1]).toFixed(1) +
      '" r="3" fill="' + color + '"/>' +
      '<text x="' + (x(p[0]) + 7).toFixed(1) + '" y="' + (y(p[1]) + 3).toFixed(1) +
      '" font-size="10" fill="' + color + '" font-weight="' + weight + '">' + text + "</text>";
  };

  let g = "";
  [lo, Math.round((lo + hi) / 2), hi].forEach((v) => {
    g += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y(v).toFixed(1) + '" y2="' +
      y(v).toFixed(1) + '" stroke="#d9dedd" stroke-width="1"/>' +
      '<text x="' + (L - 6) + '" y="' + (y(v) + 3.5).toFixed(1) +
      '" font-size="10" fill="#5c8a9b" text-anchor="end">$' + v + "</text>";
  });
  [0, 5, 10].forEach((i) => {
    g += '<text x="' + x(i).toFixed(1) + '" y="' + (H - 8) +
      '" font-size="10" fill="#5c8a9b" text-anchor="middle">' + YEARS[i] + "</text>";
  });

  g += line(nat, "#93b3bd", 2) + line(state, "#2f6d82", 2) + line(county, ACCENT, 2.6);
  g += tag(nat, "#93b3bd", "national", 400);
  g += tag(state, "#2f6d82", rec.s + " median", 400);
  g += tag(county, ACCENT, "this county", 700);
  svg.innerHTML = g;

  const a = county.find((v) => v !== null && v !== undefined);
  const b = last(county);
  $("#tsub").textContent = a && b
    ? "$" + a + " → $" + b[1] + " a week in constant 2018 dollars, " +
      (b[1] >= a ? "+" : "") + (((b[1] / a) - 1) * 100).toFixed(1) + "% in real terms."
    : "";
}

/* ------------------------------------------------------------ scatter */
function renderScatter() {
  const svg = $("#scatter");
  const W = 720, H = 520, L = 66, R = 92, T = 18, B = 48;
  const xmax = 160000, ymax = 30000;
  const x = (v) => L + (v / xmax) * (W - L - R);
  const y = (v) => H - B - (v / ymax) * (H - T - B);

  let g = "";
  for (let v = 25000; v <= 150000; v += 25000) {
    g += '<line x1="' + x(v).toFixed(1) + '" x2="' + x(v).toFixed(1) + '" y1="' + T +
      '" y2="' + (H - B) + '" stroke="#e9eef1" stroke-width="1"/>' +
      '<text x="' + x(v).toFixed(1) + '" y="' + (H - B + 16) +
      '" font-size="11" fill="#5c8a9b" text-anchor="middle">$' + (v / 1000) + "k</text>";
  }
  for (let v = 5000; v <= 30000; v += 5000) {
    g += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y(v).toFixed(1) + '" y2="' +
      y(v).toFixed(1) + '" stroke="#e9eef1" stroke-width="1"/>' +
      '<text x="' + (L - 8) + '" y="' + (y(v) + 4).toFixed(1) +
      '" font-size="11" fill="#5c8a9b" text-anchor="end">$' + (v / 1000) + "k</text>";
  }

  let dots = "", ring = "";
  for (const fips in DATA) {
    const r = DATA[fips];
    if (r.i === null || r.p[age] === null) continue;
    const px = x(r.i), py = y(r.p[age] * 52);
    if (px > W - R || py < T) continue;
    dots += '<circle cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="2.4" fill="' +
      shade(r.b[age]) + '" fill-opacity=".75"/>';
    if (fips === pinned) {
      ring = '<circle cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) +
        '" r="7" fill="none" stroke="' + ACCENT + '" stroke-width="2.2"/>' +
        '<text x="' + (px + 12).toFixed(1) + '" y="' + (py - 8).toFixed(1) +
        '" font-size="12" font-weight="700" fill="' + ACCENT + '">' + r.n + ", " + r.s + "</text>";
    }
  }

  let iso = "";
  [[7, ACCENT, 2.2, "7% of income"], [15, "#2f6d82", 1.5, "15% of income"],
   [25, "#5c8a9b", 1.5, "25% of income"]].forEach(([share, color, w, text]) => {
    const xEnd = Math.min(xmax, (ymax * 100) / share);
    iso += '<line x1="' + x(0) + '" y1="' + y(0) + '" x2="' + x(xEnd).toFixed(1) + '" y2="' +
      y((xEnd * share) / 100).toFixed(1) + '" stroke="' + color + '" stroke-width="' + w +
      (share === 7 ? '"' : '" stroke-dasharray="6 4"') + "/>";
    iso += '<text x="' + (x(xEnd) + 6).toFixed(1) + '" y="' +
      (y((xEnd * share) / 100) + 4).toFixed(1) + '" font-size="11.5" fill="' + color +
      '" font-weight="' + (share === 7 ? 700 : 400) + '">' + text + "</text>";
  });

  g += dots + iso + ring;
  g += '<text x="' + ((L + W - R) / 2) + '" y="' + (H - 10) +
    '" font-size="12" fill="#163a48" text-anchor="middle">Median household income, 2018</text>';
  g += '<text transform="translate(16,' + ((T + H - B) / 2) +
    ') rotate(-90)" font-size="12" fill="#163a48" text-anchor="middle">Annualized ' +
    AGE_WORD[age] + " care</text>";
  svg.innerHTML = g;
}

/* -------------------------------------------------------------- wiring */
function render() { paintMap(); renderRail(); renderTrend(); renderScatter(); }

document.getElementById("ages").addEventListener("click", (e) => {
  const b = e.target.closest("button");
  if (!b) return;
  age = b.dataset.age;
  for (const x of e.currentTarget.children)
    x.setAttribute("aria-pressed", String(x === b));
  render();
});
document.getElementById("views").addEventListener("click", (e) => {
  const b = e.target.closest("button");
  if (!b) return;
  for (const x of e.currentTarget.children)
    x.setAttribute("aria-pressed", String(x === b));
  $("#view-map").classList.toggle("on", b.dataset.view === "map");
  $("#view-compare").classList.toggle("on", b.dataset.view === "compare");
});

// Deep links: #compare opens the comparison view, #c25025 pins a county by FIPS,
// and #toddler or #preschool selects an age band.
(function () {
  const h = location.hash.slice(1);
  const m = h.match(/c(\d{5})/);
  if (m && DATA[m[1]]) pinned = m[1];
  const a = h.match(/infant|toddler|preschool/);
  if (a) {
    age = a[0];
    for (const x of document.getElementById("ages").children)
      x.setAttribute("aria-pressed", String(x.dataset.age === age));
  }
  if (/compare/.test(h)) {
    for (const x of document.getElementById("views").children)
      x.setAttribute("aria-pressed", String(x.dataset.view === "compare"));
    $("#view-map").classList.remove("on");
    $("#view-compare").classList.add("on");
  }
})();

render();
</script>
</body>
</html>
"""


def main():
    df = sr.load()
    counties, states = composite_geometry()

    minx, miny, maxx, maxy = counties.total_bounds
    k = 1000.0 / (maxx - minx)
    width, height = 1000.0, (maxy - miny) * k

    counties["d"] = to_paths(counties, minx, maxy, k)
    states["d"] = to_paths(states, minx, maxy, k)

    data, refs = build_data(df)
    paths = {r["GEOID"]: r["d"] for _, r in counties.iterrows() if r["d"]}

    ak = counties[counties["STATEFP"] == "02"]
    hi = counties[counties["STATEFP"] == "15"]
    ak_y = (maxy - ak.total_bounds[3]) * k + 12
    hi_x = (hi.total_bounds[0] - minx) * k
    hi_y = (maxy - hi.total_bounds[3]) * k - 6

    fonts = "".join(
        [
            font_face("Merriweather", 400, "Merriweather-400.woff2"),
            font_face("Merriweather", 700, "Merriweather-700.ttf"),
            font_face("Source Sans 3", 400, "SourceSans3-400.woff2"),
            font_face("Source Sans 3", 600, "SourceSans3-600.ttf"),
            font_face("Source Sans 3", 700, "SourceSans3-700.ttf"),
        ]
    )

    html = (
        TEMPLATE.replace("__FONTS__", fonts)
        .replace("__W__", f"{width:.0f}")
        .replace("__H__", f"{height:.0f}")
        .replace("__AKY__", f"{ak_y:.0f}")
        .replace("__HIX__", f"{hi_x:.0f}")
        .replace("__HIY__", f"{hi_y:.0f}")
        .replace(
            "__STATES__",
            "".join(f'<path class="state" d="{d}"/>' for d in states["d"] if d),
        )
        .replace("__PATHS__", json.dumps(paths, separators=(",", ":")))
        .replace("__DATA__", json.dumps(data, separators=(",", ":")))
        .replace("__REFS__", json.dumps(refs, separators=(",", ":")))
        .replace("__YEARS__", json.dumps(YEARS))
        .replace("__RAMP__", json.dumps(sr.RAMP))
        .replace("__BINLABELS__", json.dumps(sr.BIN_LABELS))
    )
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(sr.ROOT)}  ({len(html) / 1e6:.2f} MB, "
          f"{len(paths)} counties)")


if __name__ == "__main__":
    main()
