#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
raw=${1:-"$script_dir/capture-brute-7680x4320.png"}
sheet=${2:-"$script_dir/../.cache/golden-sheet/golden_sheet.png"}
case_dir=${3:-"$script_dir/../.cache/golden-sheet/cases"}
game_dir=${THEEND_CODE_ROOT:-"$script_dir/../../TheEnd"}
font="$game_dir/TheEnd.Client/Content/Fonts/JetBrainsMono-Light.ttf"

export LC_NUMERIC=C

if ! command -v magick >/dev/null 2>&1; then
    echo "ImageMagick 7 is required (missing 'magick' command)." >&2
    exit 1
fi
if ! command -v awk >/dev/null 2>&1; then
    echo "A POSIX awk implementation is required." >&2
    exit 1
fi

if [[ ! -f "$raw" ]]; then
    echo "Missing raw capture: $raw" >&2
    exit 1
fi
if [[ ! -f "$font" ]]; then
    echo "Missing repository font: $font" >&2
    exit 1
fi

dimensions=$(magick identify -quiet -format '%[width]x%[height]' "$raw")
if [[ "$dimensions" != "7680x4320" ]]; then
    echo "Expected a 7680x4320 capture, found $dimensions" >&2
    exit 1
fi

# The render target uses 4x supersampling at a 12 px camera cell: exactly 48 pixels
# per world cell. The origin follows from CenterOn(122,171), not from a fitted crop.
pixels_per_cell=48
origin_x=-2016
origin_y=-6048
crop_side=672
tile_side=480
raw_width=7680
raw_height=4320

cases=(
    '01|mur droit H|58|135'
    '02|mur droit V|88|135'
    '03|L|118|135'
    '04|T|148|135'
    '05|croix|178|135'
    '06|diagonale /|58|153'
    '07|diagonale \\|88|153'
    '08|V déclaré|118|153'
    '09|zigzag non déclaré|148|153'
    '10|porte mur droit|178|153'
    '11|cercle déclaré|58.5|171.5'
    '12|cercle déchiré|88.5|171.5'
    '13|cercle non déclaré|118.5|171.5'
    '14|porte entre croisements|148|171'
    '15|croix + porte|178|171'
    '16|porte diagonale|58|189'
    '17|deux salles|88|189'
    '18|croix sur masse|118|189'
    '19|porte entre blocs (V)|148|189'
    '20|couloir dans la masse|178.5|189.5'
    '21|petite croix sur masse|58|207'
    '22|pont + porte entre blocs (H)|88.5|207'
    '23|logement + mur + porte|118|206.5'
    '24|porte serrée entre blocs|148|207'
    '25|porte sur cercle déclaré|178.5|207.5'
)

work_dir=$(mktemp -d "${TMPDIR:-/tmp}/theend-golden-sheet.XXXXXX")
trap 'rm -rf -- "$work_dir"' EXIT

tile_paths=()
for entry in "${cases[@]}"; do
    IFS='|' read -r id label center_x center_y <<< "$entry"
    left=$(awk -v c="$center_x" -v p="$pixels_per_cell" -v o="$origin_x" -v s="$crop_side" \
        'BEGIN { printf "%.0f", c * p + o - s / 2 }')
    top=$(awk -v c="$center_y" -v p="$pixels_per_cell" -v o="$origin_y" -v s="$crop_side" \
        'BEGIN { printf "%.0f", c * p + o - s / 2 }')
    if ((left < 0 || top < 0 || left + crop_side > raw_width || top + crop_side > raw_height)); then
        echo "Case $id falls outside the raw capture: ${crop_side}x${crop_side}+${left}+${top}" >&2
        exit 1
    fi

    case_output="$work_dir/${id}.png"
    tile_output="$work_dir/${id}-tile.png"

    magick "$raw" \
        -crop "${crop_side}x${crop_side}+${left}+${top}" +repage \
        -strip \
        "$case_output"

    magick "$case_output" \
        -resize "${tile_side}x${tile_side}" \
        -background '#080d16' -gravity north -splice 0x32 \
        -gravity northwest -font "$font" -pointsize 18 \
        -fill '#dae4f0' -annotate +8+6 "$id  $label" \
        -strip \
        "$tile_output"
    tile_paths+=("$tile_output")
done

staged_sheet="$work_dir/golden_sheet.png"
magick montage "${tile_paths[@]}" \
    -tile 5x5 -geometry +4+4 -background '#080d16' -strip "$staged_sheet"

# Publish only after every crop and the complete montage have been built successfully.
mkdir -p -- "$case_dir" "$(dirname -- "$sheet")"
for entry in "${cases[@]}"; do
    IFS='|' read -r id _ <<< "$entry"
    mv -f -- "$work_dir/${id}.png" "$case_dir/${id}.png"
done
mv -f -- "$staged_sheet" "$sheet"

echo "Built $sheet from $raw"
