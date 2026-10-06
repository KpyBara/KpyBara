from PIL import Image

INPUT_FILE = "source-prepped.png"
OUTPUT_FILE = "kpybara-ascii.svg"

WIDTH = 520
HEIGHT = 520

CHARS = "@%#*+=-:. "

PINK = "#FF0055"
PINK_LIGHT = "#FF6BA8"
CYAN = "#00F0FF"
BG = "#050509"


def pixel_to_char(value):
    index = int(value / 256 * len(CHARS))

    index = min(index, len(CHARS) - 1)

    return CHARS[index]


def generate_ascii(image):

    image = image.resize((80, 40))

    pixels = image.load()

    lines = []

    for y in range(image.height):

        line = ""

        for x in range(image.width):

            value = pixels[x, y]

            character = pixel_to_char(value)

            line += character

        lines.append(line)

    return lines


def generate_svg(lines):

    svg = f"""<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

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
            stop-color="#12050D"/>

    </linearGradient>

    <filter
        id="glow"
        x="-100%"
        y="-100%"
        width="300%"
        height="300%">

        <feGaussianBlur
            stdDeviation="1.8"
            result="blur"/>

        <feMerge>

            <feMergeNode
                in="blur"/>

            <feMergeNode
                in="SourceGraphic"/>

        </feMerge>

    </filter>

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
            stroke-opacity="0.04"/>

    </pattern>

    <style>

        .ascii {{
            font-family:
                "Courier New",
                monospace;

            font-size: 5px;

            font-weight: bold;

            letter-spacing: 1px;

            fill: {PINK};

            opacity: 0;

            animation:
                boot
                2s
                ease-out
                forwards;

            filter: url(#glow);
        }}

        @keyframes boot {{

            0% {{
                opacity: 0;
                transform:
                    translateY(20px);
            }}

            30% {{
                opacity: 0.3;
            }}

            70% {{
                opacity: 0.8;
            }}

            100% {{
                opacity: 1;
                transform:
                    translateY(0);
            }}

        }}

        .cursor {{
            animation:
                blink
                0.8s
                infinite;
        }}

        @keyframes blink {{

            0% {{
                opacity: 1;
            }}

            50% {{
                opacity: 0;
            }}

            100% {{
                opacity: 1;
            }}

        }}

    </style>

</defs>

<rect
    width="100%"
    height="100%"
    rx="12"
    fill="url(#background)"/>

<rect
    x="1"
    y="1"
    width="{WIDTH - 2}"
    height="{HEIGHT - 2}"
    rx="12"
    fill="none"
    stroke="{PINK}"
    stroke-opacity="0.5"/>

<rect
    width="100%"
    height="100%"
    fill="url(#scanlines)"/>

<text
    x="25"
    y="30"
    fill="{PINK}"
    font-family="monospace"
    font-size="12"
    font-weight="bold">

    KPYBARA // VISUAL_IDENTITY

</text>

<text
    x="{WIDTH - 25}"
    y="30"
    text-anchor="end"
    fill="{CYAN}"
    font-family="monospace"
    font-size="8">

    IMAGE_MATRIX

</text>

<line
    x1="25"
    y1="42"
    x2="{WIDTH - 25}"
    y2="42"
    stroke="{PINK}"
    stroke-opacity="0.3"/>

<g class="ascii">
"""

    start_x = 42
    start_y = 75
    line_height = 9

    for index, line in enumerate(lines):

        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        y = start_y + index * line_height

        svg += f"""
<text
    x="{start_x}"
    y="{y}">
    {safe_line}
</text>
"""

    svg += f"""
</g>

<text
    x="25"
    y="495"
    fill="{PINK_LIGHT}"
    font-family="monospace"
    font-size="8">

    &gt; IDENTITY_MATRIX_LOADED

</text>

<text
    x="{WIDTH - 25}"
    y="495"
    text-anchor="end"
    fill="#444"
    font-family="monospace"
    font-size="8">

    AFTERLIFE_NET

</text>

<text
    x="{WIDTH - 25}"
    y="465"
    text-anchor="end"
    fill="{PINK}"
    font-family="monospace"
    font-size="10"
    class="cursor">

    █

</text>

</svg>
"""

    return svg


def main():

    print("[+] GENERATING ASCII IDENTITY...")

    image = Image.open(INPUT_FILE).convert("L")

    lines = generate_ascii(image)

    svg = generate_svg(lines)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        file.write(svg)

    print(f"[+] SVG CREATED: " f"{OUTPUT_FILE}")

    print("[+] IDENTITY MATRIX ONLINE.")


if __name__ == "__main__":
    main()
