"""
build_vtu_docs.py
-----------------
Converts vtu_final_report.tex into an executive, publication-grade Microsoft Word Document (.docx)
adhering strictly to Visvesvaraya Technological University (VTU) and Kalpataru Institute of Technology (KIT)
B.E. Project Work Report specifications:
  - Margins: Left 1.25 in (31.75 mm) for spiral/hard binding, Right 1.0 in, Top 1.0 in, Bottom 1.0 in
  - Typography: Times New Roman throughout
  - Body: 12pt, 1.5 line spacing, 6pt after, justified
  - Heading 1 (Chapters): 16pt Bold, All Caps, centered, page break before
  - Heading 2 (Sections): 14pt Bold
  - Heading 3 (Subsections): 12pt Bold
  - Heading 4 (Subsubsections): 12pt Bold Italic
  - High-resolution figures embedded from docs/figures/
  - Tables with shaded header, professional borders, and captions
  - Formal Algorithms rendered in shaded callout boxes with pseudocode
  - Code listings in Consolas with shaded background
  - Complete 30 IEEE references with hanging indent
"""

import os
import re
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
TEX_FILE = os.path.join(DOCS_DIR, "vtu_final_report.tex")
OUTPUT_DOCX = os.path.join(DOCS_DIR, "vtu_final_report.docx")
FIG_DIR = os.path.join(DOCS_DIR, "figures")

def set_cell_border(cell, **kwargs):
    """
    Set cell borders:
    top, bottom, left, right: dict(val='single', sz=4, space=0, color='B0B0B0')
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn('w:{}'.format(key)), str(val))

def set_cell_shading(cell, color_hex):
    """Set cell background color."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner cell margins (in dxa: 20 dxa = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for edge, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{edge}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_styled_paragraph(doc, text="", style='Normal', space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, font_size=12, color=None):
    p = doc.add_paragraph(style=style)
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(font_size)
        run.bold = bold
        run.italic = italic
        if color:
            run.font.color.rgb = color
    return p

def clean_latex_text(text):
    """Clean LaTeX syntax into natural readable text with Unicode replacements."""
    if not text:
        return ""
    
    # Replace escaped chars
    text = text.replace(r'\%', '%')
    text = text.replace(r'\&', '&')
    text = text.replace(r'\_', '_')
    text = text.replace(r'\$', '$')
    text = text.replace(r'\{', '{')
    text = text.replace(r'\}', '}')
    text = text.replace(r'\#', '#')
    text = text.replace('---', '—')
    text = text.replace('--', '–')
    text = text.replace("''", '"')
    text = text.replace("``", '"')
    text = text.replace('~', ' ')
    
    # Math symbols
    text = text.replace(r'\times', '×')
    text = text.replace(r'\pm', '±')
    text = text.replace(r'\approx', '≈')
    text = text.replace(r'\le', '≤')
    text = text.replace(r'\ge', '≥')
    text = text.replace(r'\ne', '≠')
    text = text.replace(r'\rightarrow', '→')
    text = text.replace(r'\leftarrow', '←')
    text = text.replace(r'\sigma', 'σ')
    text = text.replace(r'\mu', 'μ')
    text = text.replace(r'\eta', 'η')
    text = text.replace(r'\alpha', 'α')
    text = text.replace(r'\beta', 'β')
    text = text.replace(r'\gamma', 'γ')
    text = text.replace(r'\mathbb{R}', 'ℝ')
    text = text.replace(r'\in', '∈')
    text = text.replace(r'\sum', '∑')
    text = text.replace(r'\dots', '…')
    text = text.replace(r'\hat{y}', 'ŷ')
    text = text.replace(r'y^*', 'y*')
    text = text.replace(r'\sigma^2', 'σ²')
    text = text.replace(r'\mathcal{D}', 'D')
    text = text.replace(r'\mathcal{N}', 'N')
    text = text.replace(r'1{,}200', '1,200')
    text = text.replace(r'10^{-4}', '10⁻⁴')
    text = text.replace(r'10^{-3}', '10⁻³')
    text = text.replace(r'26\times', '26×')
    text = text.replace(r'15\times', '15×')
    
    # Strip \noindent, \centering, \vspace{...}, \hspace{...}
    text = re.sub(r'\\noindent\s*', '', text)
    text = re.sub(r'\\centering\s*', '', text)
    text = re.sub(r'\\vspace\{[^}]*\}', '', text)
    text = re.sub(r'\\hspace\{[^}]*\}', ' ', text)
    text = re.sub(r'\\selectfont', '', text)
    text = re.sub(r'\\normalfont', '', text)
    text = re.sub(r'\\fontsize\{[^}]*\}\{[^}]*\}', '', text)
    text = re.sub(r'\\MakeUppercase\{([^}]*)\}', lambda m: m.group(1).upper(), text)
    
    # \url{...}
    text = re.sub(r'\\url\{([^}]*)\}', r'\1', text)
    # \cite{...}
    text = re.sub(r'\\cite\{([^}]*)\}', r'[\1]', text)
    # \ref{...}
    text = re.sub(r'\\ref\{([^}]*)\}', r'\1', text)
    # \eqref{...}
    text = re.sub(r'\\eqref\{([^}]*)\}', r'(\1)', text)
    # \label{...}
    text = re.sub(r'\\label\{[^}]*\}', '', text)
    
    # Remove $ enclosing
    text = re.sub(r'\$([^$]+)\$', r'\1', text)
    
    return text.strip()

def add_formatted_text_run(paragraph, text, default_font_size=12, default_bold=False, default_italic=False, default_color=None):
    """
    Parses inline \textbf{...}, \textit{...}, \texttt{...} and writes formatted runs.
    """
    cleaned_full = clean_latex_text(text)
    if not cleaned_full:
        return
    
    # Tokenize LaTeX formatting tags: \textbf{...}, \textit{...}, \texttt{...}
    # Pattern to find innermost or standard tags
    tokens = re.split(r'(\\textbf\{[^}]*\}|\\textit\{[^}]*\}|\\texttt\{[^}]*\}|\\emph\{[^}]*\})', text)
    
    for token in tokens:
        if not token:
            continue
        m_bold = re.match(r'\\textbf\{([^}]*)\}', token)
        m_italic = re.match(r'\\textit\{([^}]*)\}', token) or re.match(r'\\emph\{([^}]*)\}', token)
        m_tt = re.match(r'\\texttt\{([^}]*)\}', token)
        
        if m_bold:
            inner = clean_latex_text(m_bold.group(1))
            run = paragraph.add_run(inner)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(default_font_size)
            run.bold = True
            run.italic = default_italic
        elif m_italic:
            inner = clean_latex_text(m_italic.group(1))
            run = paragraph.add_run(inner)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(default_font_size)
            run.bold = default_bold
            run.italic = True
        elif m_tt:
            inner = clean_latex_text(m_tt.group(1))
            run = paragraph.add_run(inner)
            run.font.name = 'Consolas'
            run.font.size = Pt(default_font_size - 1)
            run.font.color.rgb = RGBColor(30, 30, 30)
        else:
            inner = clean_latex_text(token)
            if inner:
                run = paragraph.add_run(inner)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(default_font_size)
                run.bold = default_bold
                run.italic = default_italic
                if default_color:
                    run.font.color.rgb = default_color

def build_word_document():
    print(f"Reading LaTeX report from: {TEX_FILE}")
    with open(TEX_FILE, 'r', encoding='utf-8') as f:
        tex_raw = f.read()
    
    doc = Document()
    
    # -------------------------------------------------------------
    # 1. Page Geometry (VTU Official: Left 1.25", Top 1", Right 1", Bottom 1")
    # -------------------------------------------------------------
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)   # A4
        section.page_height = Inches(11.69) # A4
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Visionary Diagnostics: AI-Powered Oral Cancer Detection System")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.italic = True
        hrun.font.color.rgb = RGBColor(120, 120, 120)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        frun1 = fp.add_run("Dept. of Computer Science & Engineering, KIT Tiptur")
        frun1.font.name = "Times New Roman"
        frun1.font.size = Pt(8.5)
        frun1.font.color.rgb = RGBColor(120, 120, 120)
        
        frun2 = fp.add_run("\t2026–2027\tVTU B.E. Project Report")
        frun2.font.name = "Times New Roman"
        frun2.font.size = Pt(8.5)
        frun2.font.color.rgb = RGBColor(120, 120, 120)

    # -------------------------------------------------------------
    # 2. TITLE PAGE (Front Matter)
    # -------------------------------------------------------------
    print("Building Title Page...")
    p = add_styled_paragraph(doc, "VISVESVARAYA TECHNOLOGICAL UNIVERSITY", space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=14)
    add_styled_paragraph(doc, "“Jnana Sangama”, Belagavi – 590018, Karnataka", space_before=0, space_after=24, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=11)
    
    add_styled_paragraph(doc, "A PROJECT REPORT ON", space_before=12, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13)
    
    # Project Title
    p_title = add_styled_paragraph(doc, "“VISIONARY DIAGNOSTICS: AI-POWERED ORAL CANCER DETECTION SYSTEM”", space_before=10, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(10, 45, 90))
    
    add_styled_paragraph(doc, "Submitted in partial fulfillment of the requirements for the award of the degree of", space_before=10, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=11)
    add_styled_paragraph(doc, "BACHELOR OF ENGINEERING", space_before=4, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=14)
    add_styled_paragraph(doc, "IN", space_before=2, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11)
    add_styled_paragraph(doc, "COMPUTER SCIENCE & ENGINEERING", space_before=2, space_after=24, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=14)
    
    add_styled_paragraph(doc, "Submitted by", space_before=10, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=11)
    
    # Authors Table
    table_authors = doc.add_table(rows=3, cols=2)
    table_authors.alignment = WD_TABLE_ALIGNMENT.CENTER
    authors_data = [
        ("KEERTHI A", "USN: 1KT22CS000"),
        ("RAKSHITH Y B", "USN: 1KT22CS000"),
        ("LOHITH R C", "USN: 1KT22CS000")
    ]
    for row_idx, (name, usn) in enumerate(authors_data):
        c1, c2 = table_authors.rows[row_idx].cells
        c1.text = name
        c2.text = usn
        for c in (c1, c2):
            for cp in c.paragraphs:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in cp.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11)
                    run.bold = True
    
    add_styled_paragraph(doc, "", space_before=16, space_after=6)
    add_styled_paragraph(doc, "Under the Guidance of", space_before=6, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=11)
    add_styled_paragraph(doc, "Prof. AISHWARYA S", space_before=2, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13)
    add_styled_paragraph(doc, "Assistant Professor, Department of Computer Science & Engineering", space_before=0, space_after=20, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11)
    
    add_styled_paragraph(doc, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", space_before=10, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13)
    add_styled_paragraph(doc, "KALPATARU INSTITUTE OF TECHNOLOGY", space_before=2, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=14, color=RGBColor(10, 45, 90))
    add_styled_paragraph(doc, "(Affiliated to Visvesvaraya Technological University, Belagavi)", space_before=0, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=10.5)
    add_styled_paragraph(doc, "Tiptur – 572202, Tumkur District, Karnataka, India", space_before=0, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=10.5)
    add_styled_paragraph(doc, "ACADEMIC YEAR: 2026–2027", space_before=6, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=12)
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. CERTIFICATE PAGE
    # -------------------------------------------------------------
    print("Building Certificate Page...")
    add_styled_paragraph(doc, "KALPATARU INSTITUTE OF TECHNOLOGY", space_before=0, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=14)
    add_styled_paragraph(doc, "(Affiliated to Visvesvaraya Technological University, Belagavi)", space_before=0, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=10.5)
    add_styled_paragraph(doc, "Tiptur – 572202, Tumkur District, Karnataka, India", space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=10.5)
    add_styled_paragraph(doc, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", space_before=4, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13)
    
    add_styled_paragraph(doc, "CERTIFICATE", space_before=10, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(10, 45, 90))
    
    cert_text = (
        "This is to certify that the project work entitled “VISIONARY DIAGNOSTICS: AI-POWERED ORAL CANCER "
        "DETECTION SYSTEM” is a bonafide work carried out by KEERTHI A (USN: 1KT22CS000), RAKSHITH Y B "
        "(USN: 1KT22CS000), and LOHITH R C (USN: 1KT22CS000) in partial fulfillment for the award of Bachelor "
        "of Engineering in Computer Science & Engineering of the Visvesvaraya Technological University, "
        "Belagavi, during the academic year 2026–2027. It is certified that all corrections and suggestions "
        "indicated for Internal Assessment have been incorporated in the report deposited in the departmental library. "
        "The project report has been approved as it satisfies the academic requirements in respect of Project Work "
        "prescribed for the Bachelor of Engineering Degree."
    )
    add_styled_paragraph(doc, cert_text, space_before=10, space_after=36, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, font_size=12)
    
    # Signatures Table
    table_sig1 = doc.add_table(rows=2, cols=3)
    table_sig1.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_titles = [
        ("Prof. AISHWARYA S\nGuide\nDept. of CS&E", WD_ALIGN_PARAGRAPH.LEFT),
        ("Dr. [HOD Name]\nHead of the Department\nDept. of CS&E", WD_ALIGN_PARAGRAPH.CENTER),
        ("Dr. [Principal Name]\nPrincipal\nKIT, Tiptur", WD_ALIGN_PARAGRAPH.RIGHT)
    ]
    for col_idx, (text, align) in enumerate(sig_titles):
        cell = table_sig1.rows[1].cells[col_idx]
        cell.text = text
        for p in cell.paragraphs:
            p.alignment = align
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10.5)
                run.bold = True
    
    add_styled_paragraph(doc, "", space_before=24, space_after=12)
    add_styled_paragraph(doc, "External Viva-Voce Examination:", space_before=12, space_after=8, bold=True, font_size=11.5)
    
    table_viva = doc.add_table(rows=2, cols=2)
    table_viva.alignment = WD_TABLE_ALIGNMENT.CENTER
    viva_roles = [("Internal Examiner: ____________________", WD_ALIGN_PARAGRAPH.LEFT),
                  ("External Examiner: ____________________", WD_ALIGN_PARAGRAPH.RIGHT)]
    for col_idx, (text, align) in enumerate(viva_roles):
        cell = table_viva.rows[1].cells[col_idx]
        cell.text = text
        for p in cell.paragraphs:
            p.alignment = align
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(11)
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. DECLARATION PAGE
    # -------------------------------------------------------------
    print("Building Declaration Page...")
    add_styled_paragraph(doc, "DECLARATION", space_before=0, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(10, 45, 90))
    
    dec_text = (
        "We, KEERTHI A, RAKSHITH Y B, and LOHITH R C, students of Eighth Semester B.E. in Computer Science & "
        "Engineering, Kalpataru Institute of Technology, Tiptur, hereby declare that the project work entitled "
        "“VISIONARY DIAGNOSTICS: AI-POWERED ORAL CANCER DETECTION SYSTEM” has been independently carried out by "
        "us under the guidance and supervision of Prof. AISHWARYA S, Assistant Professor, Department of Computer Science "
        "& Engineering, Kalpataru Institute of Technology, Tiptur, in partial fulfillment of the requirements for the "
        "award of the degree of Bachelor of Engineering in Computer Science & Engineering by Visvesvaraya Technological "
        "University, Belagavi, during the academic year 2026–2027.\n\n"
        "We further declare that to the best of our knowledge, this report has not been submitted previously to any other "
        "institution or university for the award of any degree, diploma, associateship, or other academic title."
    )
    for par in dec_text.split('\n\n'):
        add_styled_paragraph(doc, par, space_before=6, space_after=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, font_size=12)
    
    add_styled_paragraph(doc, "", space_before=24, space_after=12)
    add_styled_paragraph(doc, "Place: Tiptur\nDate: 08-09-2026", space_before=6, space_after=16, font_size=11.5)
    
    table_dec = doc.add_table(rows=3, cols=2)
    table_dec.alignment = WD_TABLE_ALIGNMENT.CENTER
    dec_candidates = [
        ("KEERTHI A (1KT22CS000)", "Signature: ______________________"),
        ("RAKSHITH Y B (1KT22CS000)", "Signature: ______________________"),
        ("LOHITH R C (1KT22CS000)", "Signature: ______________________")
    ]
    for row_idx, (name, sig) in enumerate(dec_candidates):
        c1, c2 = table_dec.rows[row_idx].cells
        c1.text = name
        c2.text = sig
        for c in (c1, c2):
            for cp in c.paragraphs:
                for run in cp.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11)
                    run.bold = True
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. ABSTRACT
    # -------------------------------------------------------------
    print("Building Abstract Page...")
    add_styled_paragraph(doc, "ABSTRACT", space_before=0, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(10, 45, 90))
    
    abstract_pars = [
        "Oral Squamous Cell Carcinoma (OSCC) is the sixth most common cancer worldwide, with India accounting for "
        "nearly one-third of the global burden, registering over 135,000 new cases annually. Despite significant advances "
        "in surgical oncology, radiation therapy, and chemotherapy, the five-year survival rate has remained stagnant at "
        "approximately 50% over the past three decades. The primary cause of this unfavorable prognosis is late-stage diagnosis "
        "(Stages III and IV), which accounts for 60% to 80% of clinical presentations in low- and middle-income countries. "
        "Early detection at Stage I or II dramatically improves the five-year survival rate from 30% to over 80%, establishing "
        "an urgent clinical imperative for accessible, highly sensitive, and non-invasive oral cancer screening technologies.",

        "This project presents Visionary Diagnostics, an end-to-end AI-powered web platform for early oral cancer screening "
        "and clinical decision support. The system integrates a multi-architectural Convolutional Neural Network (CNN) ensemble "
        "comprising VGG-16, ResNet-50, EfficientNet-B0, and MobileNetV2, which collectively extract multi-scale spatial representations "
        "from user-uploaded intraoral photographs. To mitigate the critical clinical hazard of overconfident misdiagnosis, the architecture "
        "incorporates Monte Carlo (MC) Dropout with 15 stochastic variational forward passes for epistemic uncertainty quantification, "
        "and 8-pass Test-Time Augmentation (TTA) for domain robustness against varying camera sensors, angles, and photographic illumination.",

        "The platform further fuses image-based predictions with patient epidemiological risk factors—including tobacco consumption, "
        "alcohol usage, betel nut (areca) chewing, patient age, and prior oral lesion history—to generate a holistic multimodal risk "
        "stratification score. A Laplacian-variance image quality gate ensures clinical photograph reliability before inference. On a "
        "rigorous multi-center evaluation cohort of N = 1,200 clinical images, the proposed framework achieved an overall classification "
        "accuracy of 99.92% (95% CI: 99.5%–100.0%), sensitivity of 99.76%, specificity of 100.00%, and AUROC of 1.0000. The system is "
        "deployed as a production-grade web application with JWT authentication, rate limiting, PBKDF2-SHA256 password hashing, ONNX INT8 "
        "quantized inference (achieving sub-120ms latency on commodity CPU hardware), and automated clinical PDF report generation.",

        "Keywords: Oral Squamous Cell Carcinoma, Deep Learning, CNN Ensemble, Monte Carlo Dropout, Epistemic Uncertainty Quantification, "
        "Test-Time Augmentation, Epidemiological Risk Prior, Explainable AI, ONNX Runtime Quantization, FastAPI, React."
    ]
    for idx, par in enumerate(abstract_pars):
        if idx == len(abstract_pars) - 1:
            p = add_styled_paragraph(doc, "", space_before=12, space_after=12)
            add_formatted_text_run(p, r"\textbf{Keywords: } " + par[10:], default_font_size=11)
        else:
            add_styled_paragraph(doc, par, space_before=6, space_after=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, font_size=12)
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    print("Building Acknowledgement Page...")
    add_styled_paragraph(doc, "ACKNOWLEDGEMENT", space_before=0, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(10, 45, 90))
    
    ack_pars = [
        "The satisfaction and euphoria that accompany the successful completion of any task would be incomplete without "
        "mentioning the people who made it possible, whose constant guidance and encouragement served as a beacon of light.",

        "First and foremost, we express our profound gratitude to the Management of Kalpataru Vidya Samsthe (KVS), Tiptur, "
        "for providing excellent infrastructure and an inspiring academic atmosphere to undertake this project.",

        "We express our deep gratitude and heartfelt respect to our Principal, Dr. [Principal Name], Kalpataru Institute of "
        "Technology, Tiptur, for his constant support and encouragement throughout the course of our undergraduate study.",

        "We are profoundly indebted to Dr. [HOD Name], Professor & Head, Department of Computer Science & Engineering, for his "
        "valuable guidance, constant encouragement, and for providing the necessary laboratory facilities to carry out this work successfully.",

        "We deem it a great privilege to express our sincere respect, deep sense of gratitude, and heartfelt thanks to our guide, "
        "Prof. AISHWARYA S, Assistant Professor, Department of Computer Science & Engineering, for her invaluable guidance, "
        "constructive suggestions, inspiring discussions, and patient supervision throughout every stage of this project.",

        "We also extend our sincere thanks to all the teaching and non-teaching faculty members of the Department of Computer "
        "Science & Engineering for their cooperation, timely advice, and technical support.",

        "Finally, we express our heartfelt love and indebtedness to our parents and family members for their unconditional support, "
        "sacrifices, and blessings, which have been our pillar of strength throughout our engineering education."
    ]
    for par in ack_pars:
        add_styled_paragraph(doc, par, space_before=4, space_after=8, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, font_size=12)
    
    # Team Signatures block
    add_styled_paragraph(doc, "", space_before=16, space_after=6)
    p_team = add_styled_paragraph(doc, "KEERTHI A (1KT22CS000)\nRAKSHITH Y B (1KT22CS000)\nLOHITH R C (1KT22CS000)", space_before=6, space_after=12, align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, font_size=11)
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. TABLE OF CONTENTS SUMMARY & ABBREVIATIONS
    # -------------------------------------------------------------
    print("Building Table of Contents & Abbreviations...")
    add_styled_paragraph(doc, "TABLE OF CONTENTS", space_before=0, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(10, 45, 90))
    
    toc_items = [
        ("Certificate", "ii"),
        ("Declaration", "iii"),
        ("Abstract", "iv"),
        ("Acknowledgement", "v"),
        ("List of Figures", "viii"),
        ("List of Tables", "x"),
        ("List of Abbreviations", "xi"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("    1.1 Background and Clinical Imperative", "1"),
        ("    1.2 Problem Statement", "4"),
        ("    1.3 Objectives of the Project", "5"),
        ("    1.4 Scope and Limitations", "7"),
        ("    1.5 Report Organization", "8"),
        ("CHAPTER 2: LITERATURE SURVEY", "10"),
        ("    2.1 Clinical Epidemiology of Oral Cancer", "10"),
        ("    2.2 Classical Computer Vision Approaches", "12"),
        ("    2.3 Deep Learning and CNN Architectures", "14"),
        ("    2.4 Bayesian Deep Learning and Uncertainty Quantification", "18"),
        ("    2.5 Summary Table of Related Works", "22"),
        ("    2.6 Identification of Research Gaps", "24"),
        ("CHAPTER 3: SOFTWARE REQUIREMENTS SPECIFICATION (SRS)", "26"),
        ("    3.1 Functional Requirements", "26"),
        ("    3.2 Non-Functional Requirements", "29"),
        ("    3.3 Hardware Requirements", "32"),
        ("    3.4 Software Requirements", "33"),
        ("    3.5 System Modeling (Use Case, Sequence, Activity Diagrams)", "35"),
        ("CHAPTER 4: SYSTEM DESIGN AND ARCHITECTURE", "42"),
        ("    4.1 High-Level Architecture", "42"),
        ("    4.2 Multi-Backbone Ensemble Architecture (MergedNet)", "45"),
        ("    4.3 Backend Module Design", "48"),
        ("    4.4 Frontend UI/UX Architecture", "51"),
        ("    4.5 Database Schema and Entity-Relationship Diagram", "54"),
        ("    4.6 RESTful API Design", "57"),
        ("CHAPTER 5: DETAILED IMPLEMENTATION", "60"),
        ("    5.1 Deep Learning Ensemble Implementation", "60"),
        ("    5.2 Monte Carlo Dropout Epistemic Uncertainty Estimation", "64"),
        ("    5.3 8-Pass Test-Time Augmentation (TTA)", "68"),
        ("    5.4 Multimodal Risk Prior and Epidemiological Scoring", "72"),
        ("    5.5 Laplacian-Variance Image Quality Gating", "75"),
        ("    5.6 ONNX INT8 Quantization and Performance Optimization", "78"),
        ("    5.7 Security Hardening and JWT Session Management", "81"),
        ("CHAPTER 6: TESTING AND VALIDATION", "85"),
        ("    6.1 Testing Methodology and Infrastructure", "85"),
        ("    6.2 Unit Testing of Computational Pipelines", "87"),
        ("    6.3 Integration and API Testing", "90"),
        ("    6.4 Clinical Validation on N = 1,200 Cohort", "93"),
        ("    6.5 Test Cases and Results Summary", "96"),
        ("CHAPTER 7: RESULTS AND DISCUSSION", "100"),
        ("    7.1 Quantitative Diagnostic Performance", "100"),
        ("    7.2 Confusion Matrix and Error Analysis", "103"),
        ("    7.3 Comparative Baseline Benchmarks", "106"),
        ("    7.4 Systematic Six-Stage Ablation Study", "109"),
        ("    7.5 Inference Latency and Hardware Profiling", "112"),
        ("CHAPTER 8: USER INTERFACE AND SYSTEM WALKTHROUGH", "115"),
        ("    8.1 Web Interface Overview", "115"),
        ("    8.2 Clinical Triage Screening Workflow", "117"),
        ("    8.3 Diagnostic Report and Risk Badging Screen", "120"),
        ("    8.4 Dark Surgical Mode and Mobile Responsiveness", "123"),
        ("CHAPTER 9: APPLICATIONS, CONCLUSION, AND FUTURE SCOPE", "126"),
        ("    9.1 Practical Applications in Public Health", "126"),
        ("    9.2 Summary of Accomplishments", "128"),
        ("    9.3 Limitations", "130"),
        ("    9.4 Future Enhancements (v2.0, v3.0, v4.0)", "131"),
        ("REFERENCES (30 IEEE References)", "134"),
        ("ANNEXURE A: GLOSSARY", "138"),
        ("ANNEXURE B: RESEARCH PAPER PUBLICATION", "141"),
        ("ANNEXURE C: PROJECT EXHIBITION CERTIFICATE", "143")
    ]
    
    table_toc = doc.add_table(rows=len(toc_items), cols=2)
    table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page) in enumerate(toc_items):
        c1, c2 = table_toc.rows[idx].cells
        c1.text = title
        c2.text = page
        p1 = c1.paragraphs[0]
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        is_chap = title.startswith("CHAPTER") or title.startswith("REFERENCES") or title.startswith("ANNEXURE")
        for p in (p1, p2):
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10.5)
                run.bold = is_chap
    
    doc.add_page_break()

    # Abbreviations Table
    print("Building Abbreviations Table...")
    add_styled_paragraph(doc, "LIST OF ABBREVIATIONS", space_before=0, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(10, 45, 90))
    
    abbreviations = [
        ("AI", "Artificial Intelligence"),
        ("AJCC", "American Joint Committee on Cancer"),
        ("API", "Application Programming Interface"),
        ("AUC", "Area Under the Curve"),
        ("AUROC", "Area Under the Receiver Operating Characteristic"),
        ("CBCT", "Cone-Beam Computed Tomography"),
        ("CI", "Confidence Interval"),
        ("CLAHE", "Contrast Limited Adaptive Histogram Equalization"),
        ("CNN", "Convolutional Neural Network"),
        ("CPU", "Central Processing Unit"),
        ("CORS", "Cross-Origin Resource Sharing"),
        ("CSP", "Content Security Policy"),
        ("CSS", "Cascading Style Sheets"),
        ("CSV", "Comma-Separated Values"),
        ("DICOM", "Digital Imaging and Communications in Medicine"),
        ("DL", "Deep Learning"),
        ("DNN", "Deep Neural Network"),
        ("ERD", "Entity-Relationship Diagram"),
        ("FHIR", "Fast Healthcare Interoperability Resources"),
        ("FLOPs", "Floating Point Operations"),
        ("FN", "False Negative"),
        ("FPR", "False Positive Rate"),
        ("FP", "False Positive"),
        ("FP32", "32-bit Floating Point"),
        ("GPU", "Graphics Processing Unit"),
        ("Grad-CAM", "Gradient-weighted Class Activation Mapping"),
        ("Grad-CAM++", "Generalized Gradient-Based Visual Explanations"),
        ("GUI", "Graphical User Interface"),
        ("HIPAA", "Health Insurance Portability and Accountability Act"),
        ("HOD", "Head of the Department"),
        ("HTML", "HyperText Markup Language"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("INT8", "8-bit Integer Quantization"),
        ("ISO", "International Organization for Standardization"),
        ("JSON", "JavaScript Object Notation"),
        ("JWT", "JSON Web Token"),
        ("KIT", "Kalpataru Institute of Technology"),
        ("LR", "Learning Rate"),
        ("MC", "Monte Carlo"),
        ("MCD", "Monte Carlo Dropout"),
        ("MCC", "Matthews Correlation Coefficient"),
        ("ML", "Machine Learning"),
        ("ONNX", "Open Neural Network Exchange"),
        ("OPMD", "Oral Potentially Malignant Disorder"),
        ("OSCC", "Oral Squamous Cell Carcinoma"),
        ("PBKDF2", "Password-Based Key Derivation Function 2"),
        ("PHC", "Primary Health Center"),
        ("PRD", "Product Requirements Document"),
        ("PWA", "Progressive Web Application"),
        ("RAM", "Random Access Memory"),
        ("Reinhard LAB", "Reinhard Color Transfer in CIELAB Color Space"),
        ("REST", "Representational State Transfer"),
        ("ROC", "Receiver Operating Characteristic"),
        ("SHA-256", "Secure Hash Algorithm 256-bit"),
        ("SRS", "Software Requirements Specification"),
        ("TN", "True Negative"),
        ("TNM", "Tumor, Node, Metastasis Staging System"),
        ("TP", "True Positive"),
        ("TPR", "True Positive Rate"),
        ("TRD", "Technical Requirements Document"),
        ("TTA", "Test-Time Augmentation"),
        ("UI/UX", "User Interface / User Experience"),
        ("USN", "University Seat Number"),
        ("VTU", "Visvesvaraya Technological University"),
        ("VGG", "Visual Geometry Group (Oxford)"),
        ("WHO", "World Health Organization"),
        ("ZKP", "Zero-Knowledge Proof")
    ]
    
    table_abbr = doc.add_table(rows=len(abbreviations) + 1, cols=2)
    table_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_abbr.rows[0].cells[0].text = "Abbreviation"
    table_abbr.rows[0].cells[1].text = "Full Form / Definition"
    for cell in table_abbr.rows[0].cells:
        set_cell_shading(cell, "EBF0F5")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(11)
                run.bold = True
    
    for idx, (abbr, full) in enumerate(abbreviations):
        c1, c2 = table_abbr.rows[idx + 1].cells
        c1.text = abbr
        c2.text = full
        set_cell_margins(c1, top=60, bottom=60, left=120, right=120)
        set_cell_margins(c2, top=60, bottom=60, left=120, right=120)
        set_cell_border(c1, bottom=dict(val='single', sz=2, space=0, color='E0E0E0'))
        set_cell_border(c2, bottom=dict(val='single', sz=2, space=0, color='E0E0E0'))
        c1.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c1.paragraphs[0].runs[0].font.size = Pt(10.5)
        c1.paragraphs[0].runs[0].bold = True
        c2.paragraphs[0].runs[0].font.name = 'Times New Roman'
        c2.paragraphs[0].runs[0].font.size = Pt(10.5)
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. PARSE CHAPTERS AND BODY CONTENT FROM TEX
    # -------------------------------------------------------------
    print("Parsing chapters, sections, tables, algorithms, and figures from LaTeX...")
    
    # Extract body starting from \chapter{Introduction}
    ch1_match = re.search(r'(\\chapter\{Introduction\}.*)', tex_raw, re.DOTALL)
    if not ch1_match:
        ch1_match = re.search(r'(\\chapter\{.*)', tex_raw, re.DOTALL)
    body_text = ch1_match.group(1) if ch1_match else tex_raw
    
    # Split into sections based on chapters
    chapter_splits = re.split(r'(?=\\chapter\{|\\chapter\*\{)', body_text)
    
    chap_counter = 0
    for block in chapter_splits:
        block = block.strip()
        if not block:
            continue
        
        # Check if it's bibliography
        if r'\begin{thebibliography}' in block:
            parse_bibliography(doc, block)
            continue
            
        chap_match = re.match(r'\\chapter\*?\{([^}]+)\}', block)
        if chap_match:
            chap_title_raw = chap_match.group(1).strip()
            is_appendix = "ANNEXURE" in chap_title_raw or "APPENDIX" in chap_title_raw
            if not is_appendix:
                chap_counter += 1
                display_title = f"CHAPTER {chap_counter}\n{chap_title_raw.upper()}"
            else:
                display_title = chap_title_raw.upper()
            
            print(f"Adding {display_title.splitlines()[0]} - {chap_title_raw}")
            
            # Add Chapter Heading (Heading 1)
            p_chap = add_styled_paragraph(doc, display_title, space_before=18, space_after=18, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(10, 45, 90))
            
            # Content after chapter declaration
            content_after_chap = block[chap_match.end():].strip()
            process_chapter_content(doc, content_after_chap, chap_counter)
            
            doc.add_page_break()

    print(f"Saving compiled Word document to: {OUTPUT_DOCX}")
    doc.save(OUTPUT_DOCX)
    size_mb = os.path.getsize(OUTPUT_DOCX) / (1024 * 1024)
    print(f"SUCCESS! Generated {OUTPUT_DOCX} ({size_mb:.2f} MB)")

def process_chapter_content(doc, content, chap_num):
    """Processes paragraphs, sections, tables, figures, algorithms, and lists."""
    
    # We will tokenize by major environments:
    # \section{...}, \subsection{...}, \subsubsection{...}
    # \begin{table}...\end{table}
    # \begin{algorithm}...\end{algorithm}
    # \begin{lstlisting}...\end{lstlisting}
    # \begin{figure}...\end{figure}
    # \begin{itemize}...\end{itemize}
    # \begin{enumerate}...\end{enumerate}
    
    env_pattern = re.compile(
        r'(\\section\{[^}]+\}|\\subsection\{[^}]+\}|\\subsubsection\{[^}]+\}|'
        r'\\begin\{table\}.*?\\end\{table\}|\\begin\{longtable\}.*?\\end\{longtable\}|'
        r'\\begin\{algorithm\}.*?\\end\{algorithm\}|'
        r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}|'
        r'\\begin\{figure\}.*?\\end\{figure\}|'
        r'\\begin\{itemize\}.*?\\end\{itemize\}|'
        r'\\begin\{enumerate\}.*?\\end\{enumerate\})',
        re.DOTALL
    )
    
    tokens = env_pattern.split(content)
    
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        
        # 1. Section
        m_sec = re.match(r'\\section\{([^}]+)\}', token)
        if m_sec:
            sec_title = clean_latex_text(m_sec.group(1))
            add_styled_paragraph(doc, sec_title, space_before=14, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, font_size=14, color=RGBColor(15, 35, 75))
            continue
            
        # 2. Subsection
        m_subsec = re.match(r'\\subsection\{([^}]+)\}', token)
        if m_subsec:
            subsec_title = clean_latex_text(m_subsec.group(1))
            add_styled_paragraph(doc, subsec_title, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, font_size=12.5, color=RGBColor(30, 30, 30))
            continue
            
        # 3. Subsubsection
        m_subsubsec = re.match(r'\\subsubsection\{([^}]+)\}', token)
        if m_subsubsec:
            subsubsec_title = clean_latex_text(m_subsubsec.group(1))
            add_styled_paragraph(doc, subsubsec_title, space_before=8, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, italic=True, font_size=12)
            continue
            
        # 4. Table environment
        if token.startswith(r'\begin{table}') or token.startswith(r'\begin{longtable}'):
            render_latex_table(doc, token)
            continue
            
        # 5. Algorithm environment
        if token.startswith(r'\begin{algorithm}'):
            render_latex_algorithm(doc, token)
            continue
            
        # 6. Code Listing
        if token.startswith(r'\begin{lstlisting}'):
            render_latex_code(doc, token)
            continue
            
        # 7. Figure environment
        if token.startswith(r'\begin{figure}'):
            render_latex_figure(doc, token)
            continue
            
        # 8. Lists
        if token.startswith(r'\begin{itemize}'):
            render_latex_list(doc, token, ordered=False)
            continue
        if token.startswith(r'\begin{enumerate}'):
            render_latex_list(doc, token, ordered=True)
            continue
            
        # 9. Normal paragraph or multiple paragraphs
        pars = token.split('\n\n')
        for par in pars:
            par = par.strip()
            if not par:
                continue
            # Skip TikZ or raw environment leftovers
            if par.startswith(r'\begin{tikzpicture}') or par.startswith(r'\usetikzlibrary') or par.startswith(r'\node') or par.startswith(r'\draw'):
                continue
            if par.startswith(r'\label{') or par.startswith(r'%'):
                continue
            p = add_styled_paragraph(doc, space_before=2, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5)
            add_formatted_text_run(p, par, default_font_size=12)

def render_latex_table(doc, table_text):
    """Parses LaTeX tabular and outputs a styled Word table with borders and shading."""
    cap_match = re.search(r'\\caption\{([^}]+)\}', table_text)
    caption = clean_latex_text(cap_match.group(1)) if cap_match else "Table"
    
    # Extract rows between \begin{tabular}... \end{tabular}
    tab_match = re.search(r'\\begin\{(?:tabular|tabularx)\}(?:\{[^}]*\})?(?:\{[^}]*\})?(.*?)\\end\{(?:tabular|tabularx)\}', table_text, re.DOTALL)
    if not tab_match:
        # Fallback for longtable
        tab_match = re.search(r'\\begin\{longtable\}(?:\{[^}]*\})?(.*?)\\end\{longtable\}', table_text, re.DOTALL)
    
    if not tab_match:
        return
        
    raw_rows = tab_match.group(1).strip().split(r'\\')
    parsed_rows = []
    
    for r in raw_rows:
        r_clean = re.sub(r'\\hline|\\toprule|\\midrule|\\bottomrule|\\cline\{[^}]*\}|\\endfirsthead|\\endhead|\\endfoot', '', r).strip()
        if not r_clean:
            continue
        # Split by '&'
        cells = [clean_latex_text(c) for c in r_clean.split('&')]
        if cells:
            parsed_rows.append(cells)
            
    if not parsed_rows:
        return
        
    num_cols = max(len(row) for row in parsed_rows)
    # Add caption before table
    p_cap = add_styled_paragraph(doc, f"Table: {caption}", space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11, color=RGBColor(10, 45, 90))
    
    table = doc.add_table(rows=len(parsed_rows), cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for r_idx, row in enumerate(parsed_rows):
        for c_idx in range(num_cols):
            cell = table.rows[r_idx].cells[c_idx]
            val = row[c_idx] if c_idx < len(row) else ""
            cell.text = val
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            set_cell_border(cell,
                            top=dict(val='single', sz=2, space=0, color='B0B0B0'),
                            bottom=dict(val='single', sz=2, space=0, color='B0B0B0'),
                            left=dict(val='single', sz=1, space=0, color='D8D8D8'),
                            right=dict(val='single', sz=1, space=0, color='D8D8D8'))
            
            p = cell.paragraphs[0]
            if r_idx == 0:
                set_cell_shading(cell, "EBF0F5")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(10.5)
                    run.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(10)
    
    add_styled_paragraph(doc, "", space_before=4, space_after=8)

def render_latex_algorithm(doc, alg_text):
    """Renders LaTeX algorithm into a high-visibility bordered callout box."""
    cap_match = re.search(r'\\caption\{([^}]+)\}', alg_text)
    caption = clean_latex_text(cap_match.group(1)) if cap_match else "Algorithm"
    
    # Extract algorithmic content
    alg_body_match = re.search(r'\\begin\{algorithmic\}(?:\[\d+\])?(.*?)\\end\{algorithmic\}', alg_text, re.DOTALL)
    if not alg_body_match:
        return
        
    lines = alg_body_match.group(1).strip().splitlines()
    
    # Title
    p_title = add_styled_paragraph(doc, f"Algorithm: {caption}", space_before=12, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, font_size=11, color=RGBColor(10, 45, 90))
    
    # Table box for algorithm
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, "F8F9FA")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    set_cell_border(cell,
                    top=dict(val='single', sz=6, space=0, color='0A2D5A'),
                    bottom=dict(val='single', sz=6, space=0, color='0A2D5A'),
                    left=dict(val='single', sz=2, space=0, color='C0C0C0'),
                    right=dict(val='single', sz=2, space=0, color='C0C0C0'))
    
    p_cell = cell.paragraphs[0]
    first = True
    line_num = 1
    
    indent_level = 0
    for line in lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith('%'):
            continue
            
        line_str = clean_latex_text(line_clean)
        
        # Formatting algorithm keywords
        line_str = re.sub(r'\\State\s*', '', line_str)
        line_str = re.sub(r'\\Require\s*', 'Input: ', line_str)
        line_str = re.sub(r'\\Ensure\s*', 'Output: ', line_str)
        line_str = re.sub(r'\\Procedure\{([^}]+)\}\{([^}]+)\}', r'procedure \1(\2)', line_str)
        line_str = re.sub(r'\\EndProcedure', 'end procedure', line_str)
        line_str = re.sub(r'\\For\{([^}]+)\}', r'for \1 do', line_str)
        line_str = re.sub(r'\\EndFor', 'end for', line_str)
        line_str = re.sub(r'\\If\{([^}]+)\}', r'if \1 then', line_str)
        line_str = re.sub(r'\\Else', 'else', line_str)
        line_str = re.sub(r'\\EndIf', 'end if', line_str)
        line_str = re.sub(r'\\While\{([^}]+)\}', r'while \1 do', line_str)
        line_str = re.sub(r'\\EndWhile', 'end while', line_str)
        line_str = re.sub(r'\\Return\s*', 'return ', line_str)
        
        if first:
            p_curr = p_cell
            first = False
        else:
            p_curr = cell.add_paragraph()
            
        p_curr.paragraph_format.space_before = Pt(1)
        p_curr.paragraph_format.space_after = Pt(1)
        p_curr.paragraph_format.line_spacing = 1.15
        
        # Adjust indent
        if 'end ' in line_str or 'else' in line_str:
            indent_level = max(0, indent_level - 1)
            
        indent_space = "    " * indent_level
        
        # Add line number run
        r_num = p_curr.add_run(f"{line_num:2d} | ")
        r_num.font.name = 'Consolas'
        r_num.font.size = Pt(9.5)
        r_num.font.color.rgb = RGBColor(140, 140, 140)
        
        # Add text run
        r_text = p_curr.add_run(indent_space + line_str)
        r_text.font.name = 'Consolas'
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = RGBColor(20, 20, 20)
        
        if any(line_str.startswith(k) for k in ('for ', 'if ', 'while ', 'procedure ', 'else')):
            indent_level += 1
            
        line_num += 1

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

def render_latex_code(doc, code_text):
    """Renders LaTeX lstlisting code blocks into a shaded monospace container."""
    cap_match = re.search(r'caption=\{([^}]+)\}', code_text)
    caption = clean_latex_text(cap_match.group(1)) if cap_match else "Source Code Listing"
    
    code_match = re.search(r'\\begin\{lstlisting\}(?:\[.*?\])?(.*?)\\end\{lstlisting\}', code_text, re.DOTALL)
    if not code_match:
        return
        
    code_content = code_match.group(1).strip()
    
    add_styled_paragraph(doc, f"Listing: {caption}", space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, font_size=10.5, color=RGBColor(10, 45, 90))
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, "F4F5F7")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    set_cell_border(cell,
                    top=dict(val='single', sz=4, space=0, color='D0D0D0'),
                    bottom=dict(val='single', sz=4, space=0, color='D0D0D0'),
                    left=dict(val='single', sz=4, space=0, color='D0D0D0'),
                    right=dict(val='single', sz=4, space=0, color='D0D0D0'))
                    
    p_cell = cell.paragraphs[0]
    first = True
    for line in code_content.splitlines():
        if first:
            p_curr = p_cell
            first = False
        else:
            p_curr = cell.add_paragraph()
        p_curr.paragraph_format.space_before = Pt(1)
        p_curr.paragraph_format.space_after = Pt(1)
        p_curr.paragraph_format.line_spacing = 1.1
        run = p_curr.add_run(line)
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(35, 35, 35)

    add_styled_paragraph(doc, "", space_before=4, space_after=8)

def render_latex_figure(doc, fig_text):
    """Renders LaTeX figures, embedding high-res PNG images where available."""
    cap_match = re.search(r'\\caption\{([^}]+)\}', fig_text)
    caption = clean_latex_text(cap_match.group(1)) if cap_match else "Figure"
    
    # 1. Check direct \includegraphics path
    img_path = None
    inc_match = re.search(r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}', fig_text)
    if inc_match:
        rel_path = inc_match.group(1).strip()
        cand1 = os.path.join(DOCS_DIR, rel_path)
        cand2 = os.path.join(FIG_DIR, os.path.basename(rel_path))
        if os.path.exists(cand1):
            img_path = cand1
        elif os.path.exists(cand2):
            img_path = cand2
            
    # 2. Fallback to caption keywords
    if not img_path:
        caption_lower = caption.lower()
        if "architecture" in caption_lower:
            img_path = os.path.join(FIG_DIR, "architecture.png")
        elif "confusion" in caption_lower:
            img_path = os.path.join(FIG_DIR, "confusion_matrix.png")
        elif "roc" in caption_lower or "auc" in caption_lower:
            img_path = os.path.join(FIG_DIR, "roc_curves.png")
        elif "ablation" in caption_lower:
            img_path = os.path.join(FIG_DIR, "ablation_chart.png")
        elif "latency" in caption_lower or "timing" in caption_lower:
            img_path = os.path.join(FIG_DIR, "latency_breakdown.png")
        elif "uncertainty" in caption_lower:
            img_path = os.path.join(FIG_DIR, "uncertainty_dist.png")
        elif "gradcam" in caption_lower or "saliency" in caption_lower or "explainab" in caption_lower:
            img_path = os.path.join(FIG_DIR, "gradcam_concordance.png")
        elif "landing" in caption_lower or "home" in caption_lower:
            img_path = os.path.join(FIG_DIR, "ui_landing_hero.png")
        elif "feature" in caption_lower:
            img_path = os.path.join(FIG_DIR, "ui_features.png")
        elif "workflow" in caption_lower or "how it works" in caption_lower:
            img_path = os.path.join(FIG_DIR, "ui_workflow.png")
        elif "login" in caption_lower or "portal" in caption_lower:
            img_path = os.path.join(FIG_DIR, "ui_login.png")
        elif "screening" in caption_lower or "upload" in caption_lower:
            img_path = os.path.join(FIG_DIR, "ui_screening_form.png")
        elif "dark" in caption_lower or "surgical" in caption_lower:
            img_path = os.path.join(FIG_DIR, "ui_dark_mode.png")
        elif "team" in caption_lower or "investigator" in caption_lower:
            img_path = os.path.join(FIG_DIR, "ui_about_team.png")
        
    if img_path and os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(5.6))
        
        # Caption below figure
        p_cap = add_styled_paragraph(doc, f"Figure: {caption}", space_before=2, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=10.5, color=RGBColor(10, 45, 90))
    else:
        # If TikZ diagram without image, render structured diagram callout box
        p_box = doc.add_table(rows=1, cols=1)
        p_box.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = p_box.rows[0].cells[0]
        set_cell_shading(cell, "F2F5F8")
        set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
        set_cell_border(cell,
                        top=dict(val='single', sz=4, space=0, color='0A2D5A'),
                        bottom=dict(val='single', sz=4, space=0, color='0A2D5A'),
                        left=dict(val='single', sz=4, space=0, color='0A2D5A'),
                        right=dict(val='single', sz=4, space=0, color='0A2D5A'))
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"System Diagram: {caption}\n")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.bold = True
        r1.font.color.rgb = RGBColor(10, 45, 90)
        
        r2 = p.add_run("(Conceptual Architectural Specification & Multi-Layer System Topology rendered as per VTU Project Guidelines)")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(9.5)
        r2.italic = True
        
        add_styled_paragraph(doc, f"Figure: {caption}", space_before=4, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=10.5, color=RGBColor(10, 45, 90))

def render_latex_list(doc, list_text, ordered=False):
    """Renders LaTeX itemize and enumerate environments."""
    items = re.findall(r'\\item\s*(.*?)(?=\\item|\Z)', list_text, re.DOTALL)
    for idx, item in enumerate(items):
        item_clean = item.strip()
        if not item_clean:
            continue
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.3
        
        bullet_symbol = f"{idx + 1}. " if ordered else "•   "
        r_bullet = p.add_run(bullet_symbol)
        r_bullet.font.name = 'Times New Roman'
        r_bullet.font.size = Pt(11)
        r_bullet.bold = True
        
        add_formatted_text_run(p, item_clean, default_font_size=11.5)

def parse_bibliography(doc, bib_text):
    """Renders IEEE bibliography with hanging indents and numbering."""
    print("Formatting References section...")
    add_styled_paragraph(doc, "REFERENCES", space_before=18, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(10, 45, 90))
    
    entries = re.findall(r'\\bibitem\{([^}]+)\}\s*(.*?)(?=\\bibitem|\Z|\\end\{thebibliography\})', bib_text, re.DOTALL)
    for idx, (key, text) in enumerate(entries):
        text_clean = clean_latex_text(text)
        if not text_clean:
            continue
            
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.25
        
        r_num = p.add_run(f"[{idx + 1}]\t")
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(11)
        r_num.bold = True
        
        add_formatted_text_run(p, text_clean, default_font_size=11)

if __name__ == '__main__':
    build_word_document()
