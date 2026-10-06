from pathlib import Path

from PIL import Image, ImageOps

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "source-photo.jpg"
OUTPUT_FILE = PROJECT_ROOT / "source-prepped.png"

WIDTH = 120
HEIGHT = 120


def main():
    print("[+] ACCESSING VISUAL INPUT...")
    print(f"[+] SOURCE: {INPUT_FILE}")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Foto não encontrada: {INPUT_FILE}")

    image = Image.open(INPUT_FILE)

    print(f"[+] ORIGINAL SIZE: " f"{image.width}x{image.height}")

    image = ImageOps.exif_transpose(image)

    image = ImageOps.fit(
        image, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS, centering=(0.5, 0.45)
    )

    image = image.convert("L")

    image.save(OUTPUT_FILE, "PNG")

    print(f"[+] PREPROCESSED IMAGE: " f"{OUTPUT_FILE}")

    print("[+] VISUAL MATRIX READY.")


if __name__ == "__main__":
    main()
