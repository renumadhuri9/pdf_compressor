import os
import subprocess

# Compression presets
PRESETS = {
    "1": ("120", "High Quality (Least Compression)"),
    "2": ("100", "Balanced Quality (Recommended)"),
    "3": ("80", "Strong Compression")
}


def compress_pdf(input_pdf, output_pdf, resolution):
    """
    Compress PDF using Ghostscript.
    """

    gs_exe = r"D:\Program Files\gs10.07.1\bin\gswin64c.exe"

    gs_command = [
        gs_exe,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",

        # Image compression settings
        "-dDownsampleColorImages=true",
        "-dColorImageDownsampleType=/Bicubic",
        f"-dColorImageResolution={resolution}",

        "-dDownsampleGrayImages=true",
        "-dGrayImageDownsampleType=/Bicubic",
        f"-dGrayImageResolution={resolution}",

        "-dDownsampleMonoImages=true",
        "-dMonoImageDownsampleType=/Subsample",
        "-dMonoImageResolution=300",

        # JPEG quality (0-100)
        "-dJPEGQ=65",

        f"-sOutputFile={output_pdf}",
        input_pdf
    ]

    try:
        subprocess.run(gs_command, check=True)

        print("\n✓ Compression completed successfully.")
        print(f"\nCompressed file saved as:\n{output_pdf}")

        original_size = os.path.getsize(input_pdf) / 1024
        compressed_size = os.path.getsize(output_pdf) / 1024

        print(f"\nOriginal Size   : {original_size:.2f} KB")
        print(f"Compressed Size : {compressed_size:.2f} KB")

        reduction = (
            (original_size - compressed_size) / original_size
        ) * 100

        print(f"Reduction       : {reduction:.2f}%")

        if compressed_size <= 500:
            print("\n✓ File is below 500 KB.")
        else:
            print("\n⚠ File is still above 500 KB.")
            print("Try option 3 for stronger compression.")

    except FileNotFoundError:
        print("\nGhostscript executable not found.")
        print("Check the Ghostscript installation path.")

    except subprocess.CalledProcessError as e:
        print("\nAn error occurred during compression.")
        print(e)


def main():

    print("\n========== PDF COMPRESSOR ==========\n")

    input_pdf = input(
        "Enter full path of PDF: "
    ).strip().strip('"')

    if not os.path.exists(input_pdf):
        print("\nFile does not exist.")
        return

    print("\nChoose Compression Level:\n")

    for key, (_, desc) in PRESETS.items():
        print(f"{key}. {desc}")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice not in PRESETS:
        print("\nInvalid choice.")
        return

    resolution, description = PRESETS[choice]

    directory = os.path.dirname(input_pdf)
    filename = os.path.splitext(
        os.path.basename(input_pdf)
    )[0]

    output_pdf = os.path.join(
        directory,
        f"{filename}_compressed.pdf"
    )

    print(f"\nUsing: {description}")

    compress_pdf(input_pdf, output_pdf, resolution)


if __name__ == "__main__":
    main()