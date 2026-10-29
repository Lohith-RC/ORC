"""
assemble_final_tex.py
---------------------
Assembles the complete, clean vtu_final_report.tex with NO duplicates.
"""

import os

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
TEX_FILE = os.path.join(DOCS_DIR, "vtu_final_report.tex")

# Import the text variables
from expand_vtu_report_full import generate_latex
from build_full_chapters import ch1_text
from build_ch2_ch3 import ch2_text, ch3_text
from build_ch4_ch5 import ch4_text, ch5_text
from build_ch6_ch7 import ch6_text, ch7_text
from build_ch8_ch9_refs import ch8_text, ch9_text, refs_annex_text

print("Assembling clean vtu_final_report.tex...")

full_content = (
    generate_latex() + "\n\n" +
    ch1_text + "\n\n" +
    ch2_text + "\n\n" +
    ch3_text + "\n\n" +
    ch4_text + "\n\n" +
    ch5_text + "\n\n" +
    ch6_text + "\n\n" +
    ch7_text + "\n\n" +
    ch8_text + "\n\n" +
    ch9_text + "\n\n" +
    refs_annex_text
)

with open(TEX_FILE, 'w', encoding='utf-8') as f:
    f.write(full_content)

print(f"SUCCESS! Assembled clean vtu_final_report.tex ({len(full_content)} chars, {len(full_content.splitlines())} lines)")
