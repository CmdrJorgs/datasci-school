#!/usr/bin/env bash
# Render each medium to PDF with headless Chrome, then bundle the package.
# David Jorgensen | DSC 640 Term Project
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$HERE/../build"
mkdir -p "$OUT"

render () {          # render <html-basename> <pdf-basename>
  google-chrome \
    --headless=new \
    --disable-gpu \
    --no-sandbox \
    --run-all-compositor-stages-before-draw \
    --virtual-time-budget=12000 \
    --no-pdf-header-footer \
    --print-to-pdf="$OUT/$2" \
    "file://$HERE/$1" 2>/dev/null
  echo "  $2"
}

echo "rendering mediums"
render medium00_cover.html        00_cover.pdf
render medium01_infographic.html  medium01_infographic.pdf
render medium02_map.html          medium02_map.pdf
render medium03_brief.html        medium03_brief.pdf

pdfunite "$OUT/00_cover.pdf" \
         "$OUT/medium01_infographic.pdf" \
         "$OUT/medium02_map.pdf" \
         "$OUT/medium03_brief.pdf" \
         "$OUT/Jorgensen_DSC640_TheSecondRent_Mediums.pdf"
echo "  Jorgensen_DSC640_TheSecondRent_Mediums.pdf"
