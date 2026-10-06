import json

INPUT_FILE = "data/profile_info.json"
OUTPUT_FILE = "info-card.svg"

WIDTH = 490
HEIGHT = 390


# ============================================================
# CORES — AFTERLIFE / CYBERPUNK
# ============================================================

BG = "#050509"
PANEL = "#0D0710"

PINK = "#FF0055"
PINK_LIGHT = "#FF6BA8"
CYAN = "#00F0FF"

WHITE = "#EAEAEA"
GRAY = "#777777"
DARK_GRAY = "#33333A"


# ============================================================
# CARREGAR PERFIL
# ============================================================


def load_profile():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        return json.load(file)


# ============================================================
# ESCAPAR TEXTO PARA SVG
# ============================================================


def escape_svg(text):

    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


# ============================================================
# GERAR SVG
# ============================================================


def generate_svg(profile):

    focus = profile.get("focus", [])

    stack = profile.get("stack", [])

    os_list = profile.get("os", [])

    focus_text = " / ".join(focus)
    stack_text = " / ".join(stack)
    os_text = " / ".join(os_list)

    svg = f"""<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

    <!-- Fundo -->
    <linearGradient
        id="panel"
        x1="0"
        y1="0"
        x2="1"
        y2="1">

        <stop
            offset="0%"
            stop-color="{PANEL}"/>

        <stop
            offset="100%"
            stop-color="{BG}"/>

    </linearGradient>


    <!-- Brilho Neon -->
    <filter
        id="glow"
        x="-100%"
        y="-100%"
        width="300%"
        height="300%">

        <feGaussianBlur
            stdDeviation="2"
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
            stroke="{PINK}"
            stroke-opacity="0.035"
            stroke-width="1"/>

    </pattern>


    <!-- Animação -->
    <style>

        .line {{
            opacity: 0;
            animation:
                bootLine
                0.4s
                ease-out
                forwards;
        }}

        @keyframes bootLine {{

            0% {{
                opacity: 0;
                transform:
                    translateX(-12px);
            }}

            70% {{
                opacity: 1;
                transform:
                    translateX(2px);
            }}

            100% {{
                opacity: 1;
                transform:
                    translateX(0);
            }}

        }}

    </style>

</defs>


<!-- ===================================================== -->
<!-- PAINEL -->
<!-- ===================================================== -->

<rect
    x="1"
    y="1"
    width="{WIDTH - 2}"
    height="{HEIGHT - 2}"
    rx="10"
    fill="url(#panel)"
    stroke="{PINK}"
    stroke-opacity="0.45"
    stroke-width="1"/>


<rect
    width="100%"
    height="100%"
    rx="10"
    fill="url(#scanlines)"/>


<!-- ===================================================== -->
<!-- CABEÇALHO -->
<!-- ===================================================== -->

<text
    x="25"
    y="32"
    fill="{PINK}"
    font-family="monospace"
    font-size="14"
    font-weight="bold">

    KPYBARA@AFTERLIFE

</text>


<text
    x="{WIDTH - 25}"
    y="32"
    text-anchor="end"
    fill="{GRAY}"
    font-family="monospace"
    font-size="9">

    NET://PROFILE

</text>


<line
    x1="25"
    y1="45"
    x2="{WIDTH - 25}"
    y2="45"
    stroke="{PINK}"
    stroke-opacity="0.3"/>


<!-- ===================================================== -->
<!-- IDENTIDADE -->
<!-- ===================================================== -->

<g class="line" style="animation-delay:0.15s">

    <text
        x="25"
        y="75"
        fill="{CYAN}"
        font-family="monospace"
        font-size="11">

        IDENTITY

    </text>


    <text
        x="25"
        y="98"
        fill="{WHITE}"
        font-family="monospace"
        font-size="18"
        font-weight="bold">

        {escape_svg(profile.get("name", "UNKNOWN"))}

    </text>


    <text
        x="25"
        y="118"
        fill="{PINK_LIGHT}"
        font-family="monospace"
        font-size="10">

        @{escape_svg(profile.get("username", "UNKNOWN"))}

    </text>

</g>


<!-- ===================================================== -->
<!-- STATUS -->
<!-- ===================================================== -->

<g class="line" style="animation-delay:0.30s">

    <circle
        cx="28"
        cy="146"
        r="4"
        fill="{PINK}"
        filter="url(#glow)"/>


    <text
        x="40"
        y="150"
        fill="{PINK}"
        font-family="monospace"
        font-size="10"
        font-weight="bold">

        SYSTEM: {escape_svg(profile.get("status", "ONLINE"))}

    </text>

</g>


<!-- ===================================================== -->
<!-- DADOS -->
<!-- ===================================================== -->

<g class="line" style="animation-delay:0.45s">

    <text
        x="25"
        y="180"
        fill="{GRAY}"
        font-family="monospace"
        font-size="9">

        ROLE

    </text>


    <text
        x="140"
        y="180"
        fill="{WHITE}"
        font-family="monospace"
        font-size="10">

        {escape_svg(profile.get("role", "UNKNOWN"))}

    </text>

</g>


<g class="line" style="animation-delay:0.55s">

    <text
        x="25"
        y="202"
        fill="{GRAY}"
        font-family="monospace"
        font-size="9">

        EDUCATION

    </text>


    <text
        x="140"
        y="202"
        fill="{WHITE}"
        font-family="monospace"
        font-size="10">

        {escape_svg(profile.get("education", "UNKNOWN"))}

    </text>

</g>


<g class="line" style="animation-delay:0.65s">

    <text
        x="25"
        y="224"
        fill="{GRAY}"
        font-family="monospace"
        font-size="9">

        LOCATION

    </text>


    <text
        x="140"
        y="224"
        fill="{WHITE}"
        font-family="monospace"
        font-size="10">

        {escape_svg(profile.get("location", "UNKNOWN"))}

    </text>

</g>


<g class="line" style="animation-delay:0.75s">

    <text
        x="25"
        y="246"
        fill="{GRAY}"
        font-family="monospace"
        font-size="9">

        EDITOR

    </text>


    <text
        x="140"
        y="246"
        fill="{CYAN}"
        font-family="monospace"
        font-size="10">

        {escape_svg(profile.get("editor", "UNKNOWN"))}

    </text>

</g>


<!-- ===================================================== -->
<!-- STACK -->
<!-- ===================================================== -->

<g class="line" style="animation-delay:0.90s">

    <text
        x="25"
        y="278"
        fill="{CYAN}"
        font-family="monospace"
        font-size="10">

        STACK

    </text>


    <text
        x="25"
        y="299"
        fill="{WHITE}"
        font-family="monospace"
        font-size="9">

        {escape_svg(stack_text)}

    </text>

</g>


<!-- ===================================================== -->
<!-- FOCUS -->
<!-- ===================================================== -->

<g class="line" style="animation-delay:1.05s">

    <text
        x="25"
        y="328"
        fill="{CYAN}"
        font-family="monospace"
        font-size="10">

        CURRENT_FOCUS

    </text>


    <text
        x="25"
        y="348"
        fill="{PINK_LIGHT}"
        font-family="monospace"
        font-size="9">

        {escape_svg(focus_text)}

    </text>

</g>


<!-- ===================================================== -->
<!-- FOOTER -->
<!-- ===================================================== -->

<text
    x="{WIDTH - 25}"
    y="375"
    text-anchor="end"
    fill="{DARK_GRAY}"
    font-family="monospace"
    font-size="8">

    CONNECTION: ENCRYPTED // AFTERLIFE_NET

</text>


</svg>
"""

    return svg


# ============================================================
# MAIN
# ============================================================


def main():

    print("[+] BUILDING KPYBARA INFO CARD...")

    profile = load_profile()

    svg = generate_svg(profile)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        file.write(svg)

    print(f"[+] SVG CREATED: {OUTPUT_FILE}")

    print("[+] PROFILE CARD ONLINE.")


if __name__ == "__main__":
    main()
