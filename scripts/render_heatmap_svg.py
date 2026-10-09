import json
from datetime import datetime, timedelta

INPUT_FILE = "data/contributions.json"
OUTPUT_FILE = "contrib-heatmap.svg"


# ============================================================
# CONFIGURAÇÕES
# ============================================================

USERNAME = "KpyBara"

WIDTH = 900
HEIGHT = 280

CELL_SIZE = 11
CELL_GAP = 4

GRID_X = 45
GRID_Y = 55

# Paleta Cyberpunk / Afterlife
PALETTE = [
    "#15151C",  # 0 - sem contribuição
    "#3A0A24",  # 1
    "#78083C",  # 2
    "#C5004F",  # 3
    "#FF0055",  # 4
    "#FF6BA8",  # 5
]


# ============================================================
# CARREGAR DADOS
# ============================================================


def load_data():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        return json.load(file)


# ============================================================
# ORGANIZAR CONTRIBUIÇÕES
# ============================================================


def build_grid(contributions):

    dates = {}

    for item in contributions:

        date = item["date"]
        level = int(item["level"])

        dates[date] = level

    if not dates:
        raise RuntimeError("Nenhuma contribuição encontrada.")

    parsed_dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

    first_date = min(parsed_dates)

    # Volta para o domingo da primeira semana.
    start_date = first_date.replace(hour=0, minute=0, second=0, microsecond=0)

    # Python: Monday=0 ... Sunday=6
    weekday = start_date.weekday()

    start_date -= timedelta(days=(weekday + 1) % 7)

    grid = []

    for week in range(53):

        column = []

        for day in range(7):

            current = start_date + timedelta(weeks=week, days=day)

            date_string = current.strftime("%Y-%m-%d")

            level = dates.get(date_string, 0)

            column.append((date_string, level))

        grid.append(column)

    return grid


# ============================================================
# ESTATÍSTICAS
# ============================================================


def calculate_stats(data):

    contributions = data["contributions"]

    active_days = sum(1 for item in contributions if item["level"] > 0)

    highest_level = max((item["level"] for item in contributions), default=0)

    return active_days, highest_level


# ============================================================
# SVG
# ============================================================


def generate_svg(data, grid):

    active_days, highest_level = calculate_stats(data)

    updated_at = data.get("updated_at", "UNKNOWN")

    svg = []

    svg.append(f"""<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

    <!-- Fundo -->
    <linearGradient
        id="background"
        x1="0"
        y1="0"
        x2="1"
        y2="1">

        <stop
            offset="0%"
            stop-color="#050509"/>

        <stop
            offset="100%"
            stop-color="#0D0710"/>

    </linearGradient>


    <!-- Brilho rosa -->
    <filter
        id="neonGlow"
        x="-100%"
        y="-100%"
        width="300%"
        height="300%">

        <feGaussianBlur
            stdDeviation="2.5"
            result="blur"/>

        <feMerge>

            <feMergeNode
                in="blur"/>

            <feMergeNode
                in="SourceGraphic"/>

        </feMerge>

    </filter>


    <!-- Scanlines -->
    <pattern
        id="scanlines"
        width="4"
        height="4"
        patternUnits="userSpaceOnUse">

        <line
            x1="0"
            y1="0"
            x2="4"
            y2="0"
            stroke="#FF0055"
            stroke-opacity="0.04"
            stroke-width="1"/>

    </pattern>


    <!-- Animação -->
    <style>

        .cell {{
            opacity: 0;
            transform-box: fill-box;
            transform-origin: center;

            animation:
                boot 0.45s
                ease-out
                forwards;
        }}

        @keyframes boot {{

            0% {{
                opacity: 0;

                transform:
                    translate(
                        -10px,
                        -10px
                    )
                    scale(0.3);
            }}

            60% {{
                opacity: 1;

                transform:
                    translate(
                        2px,
                        2px
                    )
                    scale(1.15);
            }}

            100% {{
                opacity: 1;

                transform:
                    translate(0, 0)
                    scale(1);
            }}

        }}

    </style>

</defs>


<!-- ===================================================== -->
<!-- FUNDO -->
<!-- ===================================================== -->

<rect
    width="100%"
    height="100%"
    rx="12"
    fill="url(#background)"/>


<!-- Borda -->

<rect
    x="1"
    y="1"
    width="{WIDTH - 2}"
    height="{HEIGHT - 2}"
    rx="12"
    fill="none"
    stroke="#FF0055"
    stroke-opacity="0.45"
    stroke-width="1"/>


<!-- Scanlines -->

<rect
    width="100%"
    height="100%"
    fill="url(#scanlines)"
    pointer-events="none"/>


<!-- ===================================================== -->
<!-- CABEÇALHO -->
<!-- ===================================================== -->

<text
    x="45"
    y="27"
    fill="#FF0055"
    font-family="monospace"
    font-size="13"
    font-weight="bold">

    KPYBARA // CONTRIBUTION_NETWORK

</text>


<text
    x="855"
    y="27"
    text-anchor="end"
    fill="#555"
    font-family="monospace"
    font-size="10">

    STATUS: ONLINE

</text>


<!-- Linha de terminal -->

<line
    x1="45"
    y1="36"
    x2="855"
    y2="36"
    stroke="#FF0055"
    stroke-opacity="0.25"/>


<!-- ===================================================== -->
<!-- GRID -->
<!-- ===================================================== -->
""")

    # ========================================================
    # CÉLULAS
    # ========================================================

    animation_index = 0

    for week_index, week in enumerate(grid):

        for day_index, (date, level) in enumerate(week):

            x = GRID_X + week_index * (CELL_SIZE + CELL_GAP)

            y = GRID_Y + day_index * (CELL_SIZE + CELL_GAP)

            color = PALETTE[min(level, len(PALETTE) - 1)]

            delay = week_index * 0.025 + day_index * 0.035

            svg.append(f"""
<rect
    class="cell"
    x="{x}"
    y="{y}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="2"
    fill="{color}"
    style="animation-delay:{delay:.3f}s"
    data-date="{date}"
    data-level="{level}"/>
""")

            animation_index += 1

    # --------------------------------------------------------
    # LEGENDA
    # --------------------------------------------------------

    legend_x = 45
    legend_y = 225

    svg.append(f"""
<!-- LEGENDA -->

<text
    x="{legend_x}"
    y="{legend_y}"
    fill="#666"
    font-family="monospace"
    font-size="9">

    LESS

</text>
""")

    for index, color in enumerate(PALETTE):

        x = legend_x + 34 + index * 17

        svg.append(f"""
<rect
    x="{x}"
    y="{legend_y - 9}"
    width="11"
    height="11"
    rx="2"
    fill="{color}"/>
""")

    more_x = legend_x + 34 + len(PALETTE) * 17

    svg.append(f"""
<text
    x="{more_x}"
    y="{legend_y}"
    fill="#666"
    font-family="monospace"
    font-size="9">

    MORE

</text>
""")

    # --------------------------------------------------------
    # ESTATÍSTICAS
    # --------------------------------------------------------

    svg.append(f"""
<!-- ESTATÍSTICAS -->

<text
    x="855"
    y="180"
    text-anchor="end"
    fill="#FF0055"
    font-family="monospace"
    font-size="12"
    font-weight="bold">

    {active_days} ACTIVE DAYS

</text>


<text
    x="855"
    y="198"
    text-anchor="end"
    fill="#777"
    font-family="monospace"
    font-size="9">

    PEAK LEVEL: {highest_level}

</text>


<!-- STATUS -->

<circle
    cx="48"
    cy="220"
    r="3"
    fill="#FF0055"
    filter="url(#neonGlow)"/>


<text
    x="58"
    y="224"
    fill="#FF0055"
    font-family="monospace"
    font-size="9">

    CONNECTION ESTABLISHED

</text>


<text
    x="855"
    y="224"
    text-anchor="end"
    fill="#333"
    font-family="monospace"
    font-size="8">

    UPDATED: {updated_at[:10]}

</text>


</svg>
""")

    return "".join(svg)


# ============================================================
# MAIN
# ============================================================


def main():

    print("[+] RENDERING CYBERPUNK CONTRIBUTION NETWORK...")

    data = load_data()

    grid = build_grid(data["contributions"])

    svg = generate_svg(data, grid)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        file.write(svg)

    print(f"[+] SVG CREATED: {OUTPUT_FILE}")

    print("[+] CYBERPUNK NETWORK ONLINE.")


if __name__ == "__main__":
    main()
