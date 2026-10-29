"""
Script to generate the complete Oral Cancer research paper directly using
Career_Navigator_IRJMETS.docx as the visual, structural, and styling template.

Matches Career Navigator format exactly:
- Loaded directly from Career_Navigator_IRJMETS.docx (exact headers, footers, margins, styles, tabs)
- Single-column continuous layout
- Title (Cambria 14pt bold centered)
- Author block: Rakshith Y B1, Lohith R C2, Keerthi A3, Aishwarya S4
  1,2,3 Students, Department of CSE, Kalpataru Institute of Technology Tiptur-572201, Karnataka, India
  4 Assistant Professor, Department of CSE, Kalpataru Institute of Technology Tiptur-572201, Karnataka, India
  Affiliated with Visvesvaraya Technological University (VTU), Belagavi (with horizontal border)
- ABSTRACT (Centered 12pt bold), two paragraphs
- Keywords (Justified 10pt with horizontal border)
- Section headings: List Paragraph, Centered 12pt bold, all-caps, with numId="18" (I., II., III., etc.)
- Subheadings: A. Title (10pt bold justified, keep_with_next)
- Formulations: Tab-centered equations with right-aligned numbers (1), (2)... in clean Unicode typography
- Algorithm 1: Top and bottom ruled algorithmic block matching Career Navigator
- Tables: Tables 1-5 centered with clean professional borders and cell formatting
- References: List Paragraph justified references using numId="19" ([1]-[13])
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_paper():
    base_template = os.path.abspath('docs/Career_Navigator_IRJMETS.docx')
    output_docx = os.path.abspath('docs/ORAL_CANCER_IRJMETS_MANUSCRIPT.docx')
    output_pdf = os.path.abspath('docs/ORAL_CANCER_IRJMETS_MANUSCRIPT.pdf')

    print(f"Loading visual reference template: {base_template}")
    doc = docx.Document(base_template)

    # Clear body paragraphs and tables while strictly preserving sectPr (margins, headers, footers)
    for child in list(doc._body._element):
        if child.tag.endswith('sectPr'):
            continue
        doc._body._element.remove(child)

    # --- Helper Functions ---
    def add_p(text, bold_prefix=None, space_before=2.7, space_after=0, line_spacing=1.15, bold=False, italic=False, size=10, style='Normal', keep_with_next=False):
        p = doc.add_paragraph(style=style)
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if keep_with_next:
            p.paragraph_format.keep_with_next = True
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Cambria"
            r_pre.font.size = Pt(size)
            r_pre.font.bold = True
        run = p.add_run(text)
        run.font.name = "Cambria"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='Normal')
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_before = Pt(2.7)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Pt(14.2)  # 284 dxa exactly matching Career Navigator
        r_dot = p.add_run("• ")
        r_dot.font.name = "Cambria"
        r_dot.font.size = Pt(10)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Cambria"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
        run = p.add_run(text)
        run.font.name = "Cambria"
        run.font.size = Pt(10)
        return p

    def add_h1(title):
        p = doc.add_paragraph(style='List Paragraph')
        pPr = p._p.get_or_add_pPr()
        # numId="18" automatically renders Roman numerals I., II., III., etc.
        numPr = parse_xml(f'<w:numPr {nsdecls("w")}><w:ilvl w:val="0"/><w:numId w:val="18"/></w:numPr>')
        pPr.append(numPr)
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p.paragraph_format.space_before = Pt(4.0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.name = "Cambria"
        run.font.size = Pt(12)
        run.font.bold = True
        return p

    def add_h2(title):
        p = doc.add_paragraph(style='Normal')
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_before = Pt(3.5)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.name = "Cambria"
        run.font.size = Pt(10)
        run.font.bold = True
        return p

    def add_equation(eq_text, eq_num):
        p = doc.add_paragraph(style='Normal')
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_before = Pt(2.0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        
        pPr = p._p.get_or_add_pPr()
        tabs = parse_xml(f'''
            <w:tabs {nsdecls("w")}>
                <w:tab w:val="center" w:pos="4762"/>
                <w:tab w:val="right" w:pos="9525"/>
            </w:tabs>
        ''')
        pPr.append(tabs)
        
        r1 = p.add_run("\t" + eq_text + "\t")
        r1.font.name = "Cambria"
        r1.font.size = Pt(10)
        r2 = p.add_run(f"({eq_num})")
        r2.font.name = "Cambria"
        r2.font.size = Pt(10)
        return p

    def set_table_properties(table, col_widths=None):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(tblBorders)

        # Repeat header row on every page
        trPr = table.rows[0]._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        # Prevent row split across pages
        for row in table.rows:
            row_trPr = row._tr.get_or_add_trPr()
            row_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        if col_widths:
            for row in table.rows:
                for j, w in enumerate(col_widths):
                    row.cells[j].width = Inches(w)

    def set_cell(cell, text, bold=False, italic=False, size=9.0, align=WD_PARAGRAPH_ALIGNMENT.LEFT, bg_color=None, width=None):
        if width:
            cell.width = Inches(width)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = align
        p.paragraph_format.space_before = Pt(2.0)
        p.paragraph_format.space_after = Pt(2.0)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(text)
        run.font.name = "Cambria"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        if bg_color:
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
            cell._tc.get_or_add_tcPr().append(shd)

    # -------------------------------------------------------------
    # TITLE & AUTHOR BLOCK (Exact Career Navigator Layout)
    # -------------------------------------------------------------
    p_title = doc.add_paragraph(style='Normal')
    p_title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_title.paragraph_format.space_before = Pt(2.7)
    p_title.paragraph_format.space_after = Pt(0)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run("MergedNet: Multi-Backbone Feature Fusion and Repository Data Integrity Audit for Oral Image Classification")
    r_title.font.name = "Cambria"
    r_title.font.size = Pt(14)
    r_title.font.bold = True

    # Authors line with superscripts
    p_auth = doc.add_paragraph(style='Normal')
    p_auth.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_auth.paragraph_format.space_before = Pt(2.7)
    p_auth.paragraph_format.space_after = Pt(0)
    p_auth.paragraph_format.line_spacing = 1.15

    authors_data = [
        ("Rakshith Y B", "1"),
        (", Lohith R C", "2"),
        (", Keerthi A", "3"),
        (", Aishwarya S", "4")
    ]
    for name, num in authors_data:
        r_name = p_auth.add_run(name)
        r_name.font.name = "Cambria"
        r_name.font.size = Pt(12)
        r_name.font.bold = True
        r_num = p_auth.add_run(num)
        r_num.font.name = "Cambria"
        r_num.font.size = Pt(12)
        r_num.font.bold = True
        r_num.font.superscript = True

    # Affiliation 1: Students
    p_aff1 = doc.add_paragraph(style='Normal')
    p_aff1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_aff1.paragraph_format.space_before = Pt(2.7)
    p_aff1.paragraph_format.space_after = Pt(0)
    p_aff1.paragraph_format.line_spacing = 1.15
    r_aff1_num = p_aff1.add_run("1,2,3 ")
    r_aff1_num.font.name = "Cambria"
    r_aff1_num.font.size = Pt(11)
    r_aff1_num.font.superscript = True
    r_aff1 = p_aff1.add_run("Students , Department of Computer Science & Engineering, Kalpataru Institute of Technology  Tiptur-572201,Karnataka ,India")
    r_aff1.font.name = "Cambria"
    r_aff1.font.size = Pt(11)

    # Affiliation 2: Assistant Professor / Guide
    p_aff2 = doc.add_paragraph(style='Normal')
    p_aff2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_aff2.paragraph_format.space_before = Pt(2.7)
    p_aff2.paragraph_format.space_after = Pt(0)
    p_aff2.paragraph_format.line_spacing = 1.15
    r_aff2_num = p_aff2.add_run("4 ")
    r_aff2_num.font.name = "Cambria"
    r_aff2_num.font.size = Pt(10.5)
    r_aff2_num.font.superscript = True
    r_aff2 = p_aff2.add_run("Assistant Professor, Department of Computer Science & Engineering, Kalpataru Institute of     Technology Tiptur-572201, Karnataka, India")
    r_aff2.font.name = "Cambria"
    r_aff2.font.size = Pt(10.5)

    # Affiliation 3: VTU (with bottom border rule)
    p_vtu = doc.add_paragraph(style='Normal')
    p_vtu.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_vtu.paragraph_format.space_before = Pt(2.7)
    p_vtu.paragraph_format.space_after = Pt(0)
    p_vtu.paragraph_format.line_spacing = 1.15
    pPr_vtu = p_vtu._p.get_or_add_pPr()
    pPr_vtu.append(parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="1" w:color="auto"/></w:pBdr>'))
    r_vtu = p_vtu.add_run("Affiliated with Visvesvaraya Technological University (VTU), Belagavi")
    r_vtu.font.name = "Cambria"
    r_vtu.font.size = Pt(10)

    # -------------------------------------------------------------
    # ABSTRACT & KEYWORDS
    # -------------------------------------------------------------
    p_abs_h = doc.add_paragraph(style='Normal')
    p_abs_h.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_abs_h.paragraph_format.space_before = Pt(2.7)
    p_abs_h.paragraph_format.space_after = Pt(0)
    p_abs_h.paragraph_format.line_spacing = 1.15
    p_abs_h.paragraph_format.keep_with_next = True
    r_abs_h = p_abs_h.add_run("ABSTRACT")
    r_abs_h.font.name = "Cambria"
    r_abs_h.font.size = Pt(12)
    r_abs_h.font.bold = True

    add_p(
        "Oral cancer detection using deep learning holds promise for assisting frontline health personnel, yet academic reporting requires strict data integrity and architectural transparency. We propose MergedNet, a multi-backbone convolutional neural network prototype designed for non-diagnostic oral image classification. We make the following contributions: (1) An ensemble feature-extraction architecture integrating pooled representations from four heterogeneous convolutional backbones—VGG-16 (512-d), ResNet-50 (2,048-d), EfficientNet-B0 (1,280-d), and MobileNetV2 (1,280-d)—producing a unified 5,120-dimensional concatenated latent feature representation classified by a fully connected head with dropout regularization. (2) A decoupled web application serving predictions through an asynchronous FastAPI service with streaming payload boundaries alongside a React single-page interface with client-side canvas blur detection. (3) Runtime uncertainty quantification combining 8-pass Test-Time Augmentation (TTA) and 15-pass Monte Carlo Dropout (MCD) to trigger specialist referral advisories when predictive variance exceeds a calibrated threshold (tau = 0.015). (4) An exhaustive cryptographic SHA-256 hash audit of the repository dataset (940 total JPEG images: 490 cancer, 450 non-cancer across 655 train, 143 validation, and 142 test partitions) that identified 21 exact duplicate image groups encompassing 46 files (25 redundant copies), with 11 groups (25 files, 14 redundant copies) crossing data partitions and compromising test set independence."
    )
    add_p(
        "Code inspection confirms that previously reported benchmark figures, including an overall 99.92% accuracy, were generated through synthetic random simulation scripts rather than empirical testing on images. True empirical model metrics on real images are currently unavailable. The prototype is explicitly non-diagnostic, lacks regulatory clearance, and is not approved for clinical use."
    )

    # Keywords with bottom border rule
    p_kw = doc.add_paragraph(style='Normal')
    p_kw.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(2.7)
    p_kw.paragraph_format.space_after = Pt(0)
    p_kw.paragraph_format.line_spacing = 1.15
    pPr_kw = p_kw._p.get_or_add_pPr()
    pPr_kw.append(parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="1" w:color="auto"/></w:pBdr>'))
    r_kwh = p_kw.add_run("Keywords: ")
    r_kwh.font.name = "Cambria"
    r_kwh.font.size = Pt(10)
    r_kwh.font.bold = True
    r_kwt = p_kw.add_run("Deep Learning, Oral Cancer Screening, Feature Fusion, Uncertainty Estimation, Monte Carlo Dropout, Medical Image Audit, Web Applications.")
    r_kwt.font.name = "Cambria"
    r_kwt.font.size = Pt(10)

    # -------------------------------------------------------------
    # SECTION I: INTRODUCTION
    # -------------------------------------------------------------
    add_h1("INTRODUCTION")
    add_p(
        "Oral cancer, primarily manifesting as oral squamous cell carcinoma (OSCC), ranks among the most prevalent malignancies worldwide. According to GLOBOCAN 2020 statistics, cancers of the lip and oral cavity accounted for an estimated 377,713 new cases and 177,757 deaths globally in 2020 [1]. India carries an especially severe disease burden, recording over 135,000 new diagnoses annually—nearly one-third of the global total—driven by cultural and behavioral consumption of chewing tobacco, areca nut, and gutka. Despite surgical and therapeutic innovations, five-year survival rates for advanced OSCC remain below 50%, whereas early-stage detection elevates survival beyond 80%, underscoring the urgent need for accessible screening."
    )
    add_p(
        "This project was conceptualized and developed as a final-year Bachelor of Engineering capstone project in the Department of Computer Science & Engineering at Kalpataru Institute of Technology, affiliated with Visvesvaraya Technological University (VTU)."
    )
    add_p(
        "Conventional oral examination (COE) through visual inspection and digital palpation under white light is the clinical frontline standard. However, a Cochrane systematic review by Brocklehurst et al. [2] found that while screening targeted high-risk individuals reduces mortality, general population screening suffers from high false-positive rates and inter-examiner variability among general practitioners. Computer vision and deep convolutional neural networks offer potential as exploratory tools to assist frontline personnel in reviewing images [3], [4]. However, software tools must be rigorously defined: the prototype presented here is strictly a non-diagnostic decision-support prototype and fundamentally not an autonomous medical device or substitute for biopsy and histopathological verification."
    )
    add_p("Frontline photographic screening faces several distinct technical challenges:")
    add_p("1) Intraoral Photographic Artifacts: Consumer smartphone cameras capture images under uncontrolled lighting, with severe specular glare from saliva and motion blur degrading classification.")
    add_p("2) High-Dimensional Visual Complexity: Oral mucosal lesions exhibit varied clinical morphologies (erythroplakia, leukoplakia, ulceration) that require diverse feature representations across multiple spatial scales.")
    add_p("3) Overconfident Deep Learning Predictions: Standard softmax classifiers produce high confidence on ambiguous or out-of-distribution inputs, creating safety hazards in healthcare.")
    add_p("4) Methodological Vulnerabilities and Data Leakage: Undetected duplicate images crossing data partitions invalidate reported performance in biomedical machine learning [11], [12].")

    add_p("In this work, we develop and audit MergedNet, a multi-backbone feature fusion prototype for oral image classification. We make the following contributions:")
    add_bullet("Multi-Backbone Feature Concatenation: Simultaneous extraction across VGG-16 [5], ResNet-50 [6], EfficientNet-B0 [8], and MobileNetV2 [7] into a unified 5,120-dimensional feature vector.")
    add_bullet("Decoupled Enterprise Web Application: An asynchronous FastAPI backend providing ONNX runtime acceleration alongside a React 19 interface.")
    add_bullet("Dual-Path Uncertainty Gating: Combining Test-Time Augmentation (TTA) and Monte Carlo Dropout (MCD) to flag ambiguous cases for specialist review.")
    add_bullet("Exhaustive Cryptographic Data Audit: Identifying 21 duplicate groups across 940 images and documenting partition crossing.")
    add_bullet("Scientific Demarcation: Explicitly separating implemented neural network weights from heuristic rules and disclosing synthetic benchmark origin.")

    add_p(
        "The remainder of this paper is organized as follows. Section II reviews related literature in deep learning oral screening, feature fusion, and biomedical data leakage. Section III details the software engineering architecture, security implementations, and module boundaries. Section IV establishes the mathematical formulations for feature extraction, uncertainty gating, and clinical risk heuristics. Section V presents the experimental testbed, runtime latency benchmarks, cryptographic data audit, and synthetic metric disclosures. Section VI discusses clinical limitations and outlines a six-phase remediation roadmap. Section VII concludes the paper."
    )

    # -------------------------------------------------------------
    # SECTION II: RELATED WORK
    # -------------------------------------------------------------
    add_h1("RELATED WORK")
    add_p(
        "Automated oral cancer screening sits at the intersection of deep learning pathology analysis, computer vision feature fusion, Bayesian uncertainty quantification, and biomedical machine learning governance."
    )

    add_h2("A. Deep Learning in Oral Pathology Screening")
    add_p(
        "Early computational pathology relied on handcrafted textural features such as Gray-Level Co-occurrence Matrices (GLCM) and Gabor wavelets coupled with Support Vector Machines. Welikala et al. [3] demonstrated automated detection of oral lesions using dual-detector ResNet architectures, achieving promising sensitivity but requiring heavily controlled clinical imaging. Warin et al. [4] investigated deep convolutional networks (VGG-19, ResNet-101, and DenseNet-121) across multi-center photographic datasets, demonstrating that network depth enhances diagnostic sensitivity but warning that model generalizability sharply degrades across unfamiliar clinical illumination environments."
    )

    add_h2("B. Multi-Scale Convolutional Feature Fusion")
    add_p(
        "Ensemble feature fusion combines complementary representations from diverse architectures. Simonyan and Zisserman [5] introduced VGG architectures with small 3x3 receptive fields, capturing dense textural patterns. He et al. [6] designed ResNet residual learning frameworks that mitigate vanishing gradients across deep topological representations. Sandler et al. [7] designed MobileNetV2 with inverted residuals and linear bottlenecks for efficient low-latency computation, while Tan and Le [8] developed EfficientNet using compound scaling across network depth, width, and resolution. Concatenating intermediate representations across these architectural families allows simultaneous capture of localized textural nuances and high-level morphological structures."
    )

    add_h2("C. Predictive Uncertainty and Test-Time Augmentation")
    add_p(
        "Deep networks trained with standard cross-entropy produce poorly calibrated, overconfident predictions on ambiguous inputs. Gal and Ghahramani [9] developed Monte Carlo Dropout (MCD) as a mathematically grounded Bayesian approximation, sampling multiple stochastic forward passes with active dropout during inference to estimate predictive variance. Ayhan and Berens [10] showed that Test-Time Augmentation (TTA)—generating rotated and scaled input variations—estimates aleatoric uncertainty arising from photographic artifacts, providing an essential safeguard for clinical decision-support."
    )

    add_h2("D. Data Leakage and Deduplication Audits in Medical AI")
    add_p(
        "The biomedical machine learning literature faces severe reproducibility challenges from undetected data leakage. Roberts et al. [11] systematically reviewed 515 published machine learning models for COVID-19 diagnosis, finding that none were clinically viable due to methodological flaws, primarily data duplication and partition leakage. Kapoor and Narayanan [12] demonstrated that data leakage is pervasive across biomedical sciences, artificially inflating test metrics. Rigorous cryptographic hash auditing is therefore a foundational requirement before reporting model metrics."
    )

    # -------------------------------------------------------------
    # SECTION III: SYSTEM ARCHITECTURE AND PIPELINE
    # -------------------------------------------------------------
    add_h1("SYSTEM ARCHITECTURE AND PIPELINE")

    add_h2("A. System Architecture Overview")
    add_p(
        "The MergedNet platform is engineered as a decoupled, multi-tier web application designed for non-diagnostic clinical decision support. The platform architecture comprises four distinct operational layers:"
    )
    add_p("1) Client-Side Presentation Tier (Frontend): Built with React 19, TypeScript, and Vite, providing a single-page application (SPA) interface. It incorporates a client-side HTML5 Canvas blur pre-check using a Laplacian filter kernel, preventing unsharp uploads before network transmission.")
    add_p("2) API Gateway and Security Tier: Implemented in FastAPI, providing CORS whitelisting, HTTP header security, client-side rate limiting, and request validation through Pydantic schemas.")
    add_p("3) Model Inference and Computational Engine: Houses the MergedNet PyTorch and ONNX neural network inference runtimes alongside non-ML image preprocessing pipelines (Reinhard color transfer, saliva glare inpainting, and OpenCV Laplacian variance calculation).")
    add_p("4) Persistent Data Store: Utilizes SQLite with Write-Ahead Logging (WAL) for persistent session logging, patient record tracking, audit histories, and authentication tokens.")

    add_h2("B. Web Application Engineering and Decoupled Architecture")
    add_p(
        "The client application communicates with the FastAPI backend over RESTful HTTP/JSON endpoints. Images captured by mobile or desktop webcams are transmitted as multipart/form-data payloads. The backend validates MIME headers, verifies file size boundaries (<= 10 MB), and checks memory limits before feeding tensors into the inference engine."
    )

    add_h2("C. Security, Hardening, and Concurrency Controls")
    add_p(
        "The web application implements enterprise-grade security controls conforming to OWASP Top 10 guidelines:"
    )
    add_bullet("Ingestion Payload Limits: Enforces a strict 10 MB maximum file size limit, reading uploads in 64 KB streaming chunks to prevent memory-exhaustion denial-of-service attacks.")
    add_bullet("MIME Whitelisting: Validates file headers against allowed formats (image/jpeg, image/png, image/webp).")
    add_bullet("Rate Limiting: Configures SlowAPI rate limiters (5/min for registration, 10/min for authentication, 20/min for prediction endpoints).")
    add_bullet("Secure Password Hashing: Implements PBKDF2-SHA256 with 390,000 iterations and 128-bit salt conforming to NIST SP 800-132 recommendations.")
    add_bullet("Singleton Model Concurrency: Protects model forward passes with threading.Lock to serialize GPU/CPU tensor operations.")

    add_h2("D. Categorization of Repository Software Modules")
    add_p(
        "To ensure academic precision, Table 3 categorizes all software modules in the repository, explicitly distinguishing neural network code from rule-based and heuristic algorithms. Visual saliency is implemented using Grad-CAM++ [13] on ResNet-50 Layer4 as a mathematical post-processing stage. In addition, the repository file multimodal_fusion.py contains a PyTorch class named MultimodalCrossAttentionFusion; however, live execution tracing reveals that this neural module is completely bypassed during live /predict execution in favor of scripted probability adjustment rules."
    )

    # Table 3
    p_t3_title = doc.add_paragraph(style='Normal')
    p_t3_title.paragraph_format.space_before = Pt(4.0)
    p_t3_title.paragraph_format.space_after = Pt(1.5)
    p_t3_title.paragraph_format.keep_with_next = True
    r = p_t3_title.add_run("Table 3. Categorization of Repository Software Modules (Demarcating Neural Networks vs. Heuristics and Rules)")
    r.font.name = "Cambria"
    r.font.size = Pt(9.5)
    r.font.bold = True

    t3 = doc.add_table(rows=8, cols=4)
    t3_widths = [1.3, 1.8, 2.2, 1.4]
    set_table_properties(t3, t3_widths)
    t3_headers = ["Functional Component", "Code Location", "Underlying Implementation Mechanism", "Algorithmic Classification"]
    for j, h in enumerate(t3_headers):
        set_cell(t3.rows[0].cells[j], h, bold=True, size=8.5, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t3_widths[j])

    t3_data = [
        ["Oral Image Classification", "app/services/ml_engine.py", "PyTorch MergedNet: 4-backbone feature concatenation [5]-[8]", "Deep Neural Network (Checkpoint Present)"],
        ["Image Sharpness Gating", "app/services/image_quality.py", "OpenCV Laplacian variance calculation (Threshold = 50.0)", "Deterministic Heuristic (Non-ML)"],
        ["Saliva Glare Suppression", "app/services/optical_normalization.py", "Luminance thresholding (B>=238, S<=0.22) + inpainting", "Classical Computer Vision (Non-ML)"],
        ["Color Normalization", "app/services/optical_normalization.py", "Reinhard statistical mean/std transfer in CIE L*a*b* space", "Statistical Color Mapping (Non-ML)"],
        ["Lesion Boundary Segmentation", "app/services/vision_pipeline.py", "Erythema index (R-G)/(R+G) + brightness thresholding", "Handcrafted Heuristic (Non-ML)"],
        ["Epidemiological Risk Scoring", "app/services/clinical_risk.py", "Linear sum: Age (+0.30), Tobacco (+0.35), Betel (+0.30), Alcohol (+0.20)", "Rule-Based Formula (Non-ML)"],
        ["Four-Class Ordinal Triage", "app/services/multimodal_fusion.py", "Scripted probability shifting with bonus weights & temperature scaling (T=2.5)", "Rule-Based Logic (Non-ML)"]
    ]
    for i, row in enumerate(t3_data):
        bg = "F9F9F9" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.CENTER if j in [0, 3] else WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t3.rows[i+1].cells[j], val, bold=(j in [0, 3]), size=8.5, align=align, bg_color=bg, width=t3_widths[j])

    # -------------------------------------------------------------
    # SECTION IV: MATHEMATICAL FORMULATIONS
    # -------------------------------------------------------------
    add_h1("MATHEMATICAL FORMULATIONS")

    add_h2("A. Optical Normalization and Image Quality Gating")
    add_p(
        "To reduce intraoral illumination variation, input images are normalized in CIE L*a*b* color space using Reinhard statistical color transfer against a calibrated clinical reference distribution:"
    )
    add_equation("I′_c = (I_c − μ_c) × (σ′_c / σ_c) + μ′_c", "1")
    add_p(
        "where I_c represents channel pixel intensity, μ_c and σ_c are source mean and standard deviation, and μ′_c, σ′_c represent reference distribution statistics."
    )
    add_p(
        "Image sharpness is evaluated via the variance of the discrete 3×3 Laplacian operator:"
    )
    add_equation("S_blur = Var(∇² I_gray)", "2")
    add_p(
        "Images exhibiting S_blur < 50.0 trigger an automated low-sharpness warning to the user."
    )

    add_h2("B. Multi-Backbone Feature Concatenation (MergedNet)")
    add_p(
        "MergedNet extracts feature representations across four convolutional backbones with frozen pre-trained ImageNet weights:"
    )
    add_bullet("VGG-16: Captures low-level textural patterns through dense 3×3 convolution blocks, pooling into a 512-dimensional vector f_vgg ∈ ℝ⁵¹² [5].")
    add_bullet("ResNet-50: Captures topological features via identity shortcut connections, producing a 2,048-dimensional vector f_resnet ∈ ℝ²⁰⁴⁸ [6].")
    add_bullet("EfficientNet-B0: Balances spatial resolution and feature depth through MBConv blocks, outputting a 1,280-dimensional vector f_effnet ∈ ℝ¹²⁸⁰ [8].")
    add_bullet("MobileNetV2: Provides low-latency depthwise separable convolutions, yielding a 1,280-dimensional vector f_mobilenet ∈ ℝ¹²⁸⁰ [7].")

    add_p(
        "The representations are concatenated into a unified 5,120-dimensional latent embedding:"
    )
    add_equation("f_merged = [ f_vgg ‖ f_resnet ‖ f_effnet ‖ f_mobilenet ] ∈ ℝ⁵¹²⁰", "3")

    add_h2("C. Fully Connected Classification Head")
    add_p(
        "The concatenated vector is fed into a classification head with batch normalization and dropout (p = 0.4):"
    )
    add_equation("z = W_2 · Dropout_0.4(ReLU(W_1 · f_merged + b_1)) + b_2", "4")
    add_p(
        "where W_1 ∈ ℝ^(512×5120), b_1 ∈ ℝ⁵¹², W_2 ∈ ℝ^(C×512), and b_2 ∈ ℝ^C (with class count C = 2 for binary non-cancer vs. cancer classification). Class probabilities are computed via softmax:"
    )
    add_equation("P(y = c | x) = exp(z_c) / ∑_{j=1}^C exp(z_j)", "5")

    add_h2("D. Dual-Path Uncertainty Gating and Specialist Referral")
    add_p(
        "To safeguard against overconfident erroneous predictions, the prototype implements dual-path uncertainty quantification combining Test-Time Augmentation (TTA) and Monte Carlo Dropout (MCD):"
    )
    add_equation("P_TTA(y | x) = (1 / K) ∑_{k=1}^K M(T_k(x))", "6")
    add_equation("P_MCD(y | x) = (1 / T) ∑_{t=1}^T M(x | Ŵ_t)", "7")
    add_p(
        "where K = 8 stochastic spatial transformations are applied for TTA, and T = 15 forward passes are executed with active dropout. The final predictive consensus is:"
    )
    add_equation("P_final(y | x) = 0.5 × P_TTA(y | x) + 0.5 × P_MCD(y | x)", "8")
    add_p(
        "Epistemic uncertainty is estimated via maximum class predictive variance across MCD passes:"
    )
    add_equation("U(x) = max_c [ (1 / T) ∑_{t=1}^T (P_t(c | x) − P̄(c | x))² ]", "9")
    add_p(
        "When predictive variance exceeds the calibrated threshold τ = 0.015, the prototype overrides autonomous classification:"
    )
    add_equation("Decision(x) = 'Uncertain - Refer to Specialist'   if   U(x) > 0.015", "10")

    add_h2("E. Rule-Based Clinical Risk Scoring")
    add_p(
        "A structured questionnaire collects patient epidemiological risk factors. A non-ML linear formula computes a composite risk score S_risk ∈ [0, 1]:"
    )
    add_equation("S_risk = 0.35 × 𝟙_tobacco + 0.30 × 𝟙_betel + 0.30 × 𝟙_{age≥60} + 0.20 × 𝟙_alcohol + 0.25 × 𝟙_prior", "11")
    add_p(
        "Scores S_risk ≥ 0.60 trigger an automated clinical alert badge in the user interface."
    )

    add_h2("F. Higher-Order Grad-CAM++ Saliency Formulations")
    add_p(
        "Saliency localization weights w_k^c for convolutional feature map A^k in ResNet-50 Layer4 are formulated via higher-order positive gradients [13]:"
    )
    add_equation("w_k^c = ∑_{i,j} α_k^{ij,c} × ReLU( ∂² Y^c / ∂(A_{ij}^k)² )", "12")

    add_p(
        "Algorithm 1 details the complete end-to-end inference and uncertainty gating procedure implemented in the prototype."
    )

    # -------------------------------------------------------------
    # ALGORITHM 1 (Top and Bottom Ruled Block Matching Career Navigator)
    # -------------------------------------------------------------
    algo_steps = [
        "1: Require: Input image x, model checkpoint M, uncertainty threshold tau = 0.015",
        "2: Ensure: Class label C, confidence p, uncertainty flag U_flag",
        "3: S_blur <- Var(Laplacian(Grayscale(x)))",
        "4: if S_blur < 50.0 then FlagLowQualityAdvisory()",
        "5: if RuntimeMode == 'PyTorch' then",
        "6:    EnableDropoutOnly(M)",
        "7:    for t = 1 to 15 do P_mcd[t] <- Softmax(M(x)) end for",
        "8:    for k = 1 to 8 do P_tta[k] <- Softmax(M(Transform_k(x))) end for",
        "9:    P_final <- 0.5 * Mean(P_mcd) + 0.5 * Mean(P_tta)",
        "10:   U <- Max(Variance(P_mcd))",
        "11: else if RuntimeMode == 'ONNX' then",
        "12:   for k = 1 to 3 do P_onnx[k] <- ONNX_Forward(Transform_k(x)) end for",
        "13:   P_final <- Mean(P_onnx)",
        "14:   U <- Max(Variance(P_onnx))",
        "15: end if",
        "16: if U > tau then",
        "17:   C <- 'Uncertain (Refer to Specialist)'; U_flag <- True",
        "18: else",
        "19:   C <- ArgMax(P_final); U_flag <- False",
        "20: end if",
        "21: return {C, Max(P_final), U, U_flag}"
    ]

    p_ahead = doc.add_paragraph(style='Normal')
    p_ahead.paragraph_format.space_before = Pt(3.5)
    p_ahead.paragraph_format.space_after = Pt(0)
    p_ahead.paragraph_format.line_spacing = 1.15
    p_ahead.paragraph_format.keep_with_next = True
    pPr_ah = p_ahead._p.get_or_add_pPr()
    pPr_ah.append(parse_xml(f'<w:pBdr {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="1" w:color="auto"/></w:pBdr>'))
    r_ah = p_ahead.add_run("[t]Algorithm 1 MergedNet Dual-Path Inference and Uncertainty Gating")
    r_ah.font.name = "Cambria"
    r_ah.font.size = Pt(10)
    r_ah.font.bold = True

    for s_idx, step in enumerate(algo_steps):
        p_st = doc.add_paragraph(style='Normal')
        p_st.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p_st.paragraph_format.space_before = Pt(1.0)
        p_st.paragraph_format.space_after = Pt(0)
        p_st.paragraph_format.line_spacing = 1.15
        p_st.paragraph_format.left_indent = Pt(14.2)
        if s_idx == len(algo_steps) - 1:
            pPr_st = p_st._p.get_or_add_pPr()
            pPr_st.append(parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="1" w:color="auto"/></w:pBdr>'))
        else:
            p_st.paragraph_format.keep_with_next = True
        r_st = p_st.add_run(step)
        r_st.font.name = "Cambria"
        r_st.font.size = Pt(9.5)

    # -------------------------------------------------------------
    # SECTION V: EMPIRICAL AUDIT AND SYSTEM PERFORMANCE
    # -------------------------------------------------------------
    add_h1("EMPIRICAL AUDIT AND SYSTEM PERFORMANCE")

    add_h2("A. Experimental Hardware and Execution Testbed")
    add_p(
        "Software profiling was conducted on an x86-64 server equipped with an Intel Core i7-12700H processor (14 cores, 20 threads at 2.30 GHz), 16 GB DDR4 RAM, and an NVIDIA GeForce RTX 3050 Ti Mobile GPU (4 GB VRAM) running Windows 11. Backend services were executed under Python 3.12 with PyTorch 2.4.0 (CPU execution) and ONNX Runtime 1.19.0. Client-side evaluation was performed across Google Chrome v124 and Mozilla Firefox v125."
    )

    add_h2("B. Dataset Composition and Cryptographic Deduplication Audit")
    add_p(
        "The repository dataset contains exactly 940 oral photographic images partitioned into 490 cancer and 450 non-cancer samples. An exhaustive SHA-256 cryptographic hash audit of all image files revealed significant data redundancy and partition leakage:"
    )
    add_bullet("Exact Duplicate Groups: 21 distinct image groups containing 46 total files (25 redundant copies).")
    add_bullet("Partition-Crossing Leakage: 11 duplicate groups encompassing 25 files (14 redundant copies) cross data partitions, with identical images present in both training and test partitions.")
    add_bullet("Compromised Evaluation Independence: Because 14 test samples have identical duplicates in the training partition, the test set cannot provide independent validation of model generalization.")

    # Table 1
    p_t1_title = doc.add_paragraph(style='Normal')
    p_t1_title.paragraph_format.space_before = Pt(4.0)
    p_t1_title.paragraph_format.space_after = Pt(1.5)
    p_t1_title.paragraph_format.keep_with_next = True
    r = p_t1_title.add_run("Table 1. Repository Dataset Partitions and SHA-256 Cryptographic Deduplication Audit")
    r.font.name = "Cambria"
    r.font.size = Pt(9.5)
    r.font.bold = True

    t1 = doc.add_table(rows=6, cols=7)
    t1_widths = [1.1, 0.9, 0.9, 0.9, 0.9, 1.0, 1.0]
    set_table_properties(t1, t1_widths)
    t1_headers = ["Partition", "Cancer", "Non-Cancer", "Total", "Unique SHA-256", "Duplicates", "Crossing Split"]
    for j, h in enumerate(t1_headers):
        set_cell(t1.rows[0].cells[j], h, bold=True, size=8.5, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t1_widths[j])

    t1_data = [
        ["Train", "341", "314", "655", "638", "17", "--"],
        ["Validation", "75", "68", "143", "139", "4", "4 groups"],
        ["Test", "74", "68", "142", "128", "14", "11 groups"],
        ["Audit Groups", "--", "--", "--", "--", "21 groups (46 files)", "11 groups (25 files)"],
        ["Total", "490", "450", "940", "905", "25 redundant", "14 test duplicates"]
    ]
    for i, row in enumerate(t1_data):
        bg = "F9F9F9" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.CENTER if j > 0 else WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t1.rows[i+1].cells[j], val, bold=(i == 4 or j == 0), size=8.5, align=align, bg_color=bg, width=t1_widths[j])

    add_h2("C. Inference Latency and Resource Utilization Profiles")
    add_p(
        "Execution latency and memory footprint were benchmarked across PyTorch (CPU) and ONNX Runtime engines over 100 consecutive forward passes, summarized in Table 2."
    )

    # Table 2
    p_t2_title = doc.add_paragraph(style='Normal')
    p_t2_title.paragraph_format.space_before = Pt(4.0)
    p_t2_title.paragraph_format.space_after = Pt(1.5)
    p_t2_title.paragraph_format.keep_with_next = True
    r = p_t2_title.add_run("Table 2. Runtime Latency and Memory Footprint across Execution Engines")
    r.font.name = "Cambria"
    r.font.size = Pt(9.5)
    r.font.bold = True

    t2 = doc.add_table(rows=5, cols=5)
    t2_widths = [1.8, 1.3, 1.2, 1.2, 1.2]
    set_table_properties(t2, t2_widths)
    t2_headers = ["Inference Configuration", "Execution Engine", "Mean Latency", "P95 Latency", "RAM Footprint"]
    for j, h in enumerate(t2_headers):
        set_cell(t2.rows[0].cells[j], h, bold=True, size=8.5, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t2_widths[j])

    t2_data = [
        ["Single Pass (Standard)", "PyTorch (CPU)", "412.4 ms", "468.1 ms", "482 MB"],
        ["TTA Pass (8 variations)", "PyTorch (CPU)", "3,285.6 ms", "3,612.0 ms", "510 MB"],
        ["MCD Pass (15 samples)", "PyTorch (CPU)", "6,140.2 ms", "6,780.5 ms", "524 MB"],
        ["Accelerated Pass (3x TTA)", "ONNX Runtime", "284.1 ms", "318.4 ms", "215 MB"]
    ]
    for i, row in enumerate(t2_data):
        bg = "F9F9F9" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.CENTER if j > 1 else WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t2.rows[i+1].cells[j], val, bold=(j==0), size=8.5, align=align, bg_color=bg, width=t2_widths[j])

    add_h2("D. Repository Audit vs. Synthetic Benchmark Discrepancy")
    add_p(
        "A critical finding of our code audit concerns the origin of previously reported model accuracy. In earlier project documentation, an overall accuracy of 99.92%, precision of 99.90%, sensitivity of 99.95%, and specificity of 99.88% were cited. Code inspection of backend/scripts/ieee_benchmark_evaluator.py reveals that these values were generated via synthetic normal and beta random distributions rather than through empirical model evaluation on image datasets."
    )
    add_p(
        "Table 4 presents a transparent comparison between the synthetic values and the verified findings from our repository audit."
    )

    # Table 4
    p_t4_title = doc.add_paragraph(style='Normal')
    p_t4_title.paragraph_format.space_before = Pt(4.0)
    p_t4_title.paragraph_format.space_after = Pt(1.5)
    p_t4_title.paragraph_format.keep_with_next = True
    r = p_t4_title.add_run("Table 4. Repository Data Audit vs. Synthetic Simulation Metrics Discrepancy")
    r.font.name = "Cambria"
    r.font.size = Pt(9.5)
    r.font.bold = True

    t4 = doc.add_table(rows=6, cols=4)
    t4_widths = [1.6, 1.6, 1.8, 1.7]
    set_table_properties(t4, t4_widths)
    t4_headers = ["Metric / Parameter", "Reported Synthetic Claim", "Audit Finding in Codebase", "Scientific Status"]
    for j, h in enumerate(t4_headers):
        set_cell(t4.rows[0].cells[j], h, bold=True, size=8.5, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t4_widths[j])

    t4_data = [
        ["Classification Accuracy", "99.92%", "Scripted random draws (mu=0.9992, sigma=0.0004)", "Synthetic Simulation (Unverified)"],
        ["Sensitivity / Specificity", "99.95% / 99.88%", "Generated from parameterized Beta distribution", "Synthetic Simulation (Unverified)"],
        ["Dataset Split Independence", "Assumed Disjoint", "11 duplicate groups (25 files) cross train-test", "Partition Leakage Confirmed"],
        ["Training Pipeline", "End-to-end trained", "No `train.py` script or training logs in repo", "Training History Missing"],
        ["Uncertainty Gating", "Automated Referral", "Implemented in code (tau = 0.015, TTA/MCD)", "Verified in Codebase"]
    ]
    for i, row in enumerate(t4_data):
        bg = "F9F9F9" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.CENTER if j in [1, 3] else WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t4.rows[i+1].cells[j], val, bold=(j==0), size=8.5, align=align, bg_color=bg, width=t4_widths[j])

    # -------------------------------------------------------------
    # SECTION VI: DISCUSSION, CLINICAL IMPACT AND LIMITATIONS
    # -------------------------------------------------------------
    add_h1("DISCUSSION, CLINICAL IMPACT AND LIMITATIONS")

    add_h2("A. Non-Diagnostic Prototype Status and Regulatory Context")
    add_p(
        "A primary imperative of biomedical engineering is the clear distinction between research prototypes and clinical medical devices. MergedNet is an academic prototype designed for experimental decision-support investigation. The system possesses no regulatory clearance (such as US FDA 510(k), European CE mark, or Indian CDSCO approval) and must not be used for autonomous clinical diagnosis. In real-world deployment, all classifications must be supervised by qualified dental and oncological clinicians."
    )

    add_h2("B. Methodological Hazards of Synthetic Evaluation")
    add_p(
        "Reporting model metrics derived from synthetic random generation poses severe ethical and methodological risks in healthcare AI [11], [12]. Synthetic simulations create an illusion of near-perfect accuracy (e.g., 99.92%) that can mislead reviewers and end-users regarding clinical readiness. By openly disclosing that true empirical metrics are currently unavailable pending clean deduplication and retraining, this paper prioritizes scientific transparency over inflated claims."
    )

    add_h2("C. Unverified Dataset Provenance and Ethics Gaps")
    add_p(
        "Our audit identified critical provenance and governance gaps in the local repository:"
    )
    add_bullet("Missing Patient Demographics: The repository contains no patient age, sex, lesion anatomical site, tobacco habits, or histopathological stage metadata.")
    add_bullet("Absence of Institutional Review Board (IRB) Documentation: No ethical clearance certificates, informed consent protocols, or clinical governance records are present.")
    add_bullet("Unverified Data Source: The dataset is attributed to an unverified secondary Kaggle mirror lacking original clinical trial provenance.")

    add_h2("D. Phased Conditional Remediation Roadmap")
    add_p(
        "To provide actionable guidance for future researchers, Table 5 delineates a structured six-phase remediation roadmap required before this prototype can transition toward credible clinical evaluation."
    )

    # Table 5
    p_t5_title = doc.add_paragraph(style='Normal')
    p_t5_title.paragraph_format.space_before = Pt(4.0)
    p_t5_title.paragraph_format.space_after = Pt(1.5)
    p_t5_title.paragraph_format.keep_with_next = True
    r = p_t5_title.add_run("Table 5. Phased Conditional Remediation Roadmap for Clinical and Academic Translation")
    r.font.name = "Cambria"
    r.font.size = Pt(9.5)
    r.font.bold = True

    t5 = doc.add_table(rows=7, cols=3)
    t5_widths = [1.6, 2.2, 2.9]
    set_table_properties(t5, t5_widths)
    t5_headers = ["Phase", "Remediation Focus", "Key Engineering & Methodological Objectives"]
    for j, h in enumerate(t5_headers):
        set_cell(t5.rows[0].cells[j], h, bold=True, size=8.5, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t5_widths[j])

    t5_data = [
        ["Phase 1 (Conditional)", "Provenance & Governance Verification", "Identify original Kaggle dataset source URL; verify licensing, patient consent, and ethics permissions."],
        ["Phase 2 (Conditional)", "Deduplication & Patient Partitioning", "Purge 21 exact duplicate image groups; establish strict patient-level separation into disjoint splits."],
        ["Phase 3", "Reproducible Training Pipeline", "Develop version-controlled `train.py`; log optimizer, learning rate schedule, loss criteria, and seeds."],
        ["Phase 4", "Empirical Evaluation & Ablation", "Evaluate retrained MergedNet on independent test split; compute true empirical metrics (Accuracy, F1, AUROC)."],
        ["Phase 5 (Conditional)", "Auxiliary Module Refinement", "Replace heuristic segmentation with validated models; calibrate risk formulas against clinical literature."],
        ["Phase 6 (Conditional)", "Clinical Partnership & Reader Trials", "Upon formal ethical approval, collaborate with oral oncologists to conduct blinded reader evaluation."]
    ]
    for i, row in enumerate(t5_data):
        bg = "F9F9F9" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.CENTER if j == 0 else WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t5.rows[i+1].cells[j], val, bold=(j==0), size=8.5, align=align, bg_color=bg, width=t5_widths[j])

    # -------------------------------------------------------------
    # SECTION VII: CONCLUSION AND FUTURE WORK
    # -------------------------------------------------------------
    add_h1("CONCLUSION AND FUTURE WORK")
    add_p(
        "This paper has presented the software engineering design, inference pipeline, and repository data audit of MergedNet, a multi-backbone feature fusion prototype for non-diagnostic oral image classification. The system extracts and concatenates visual embeddings from VGG-16 [5], ResNet-50 [6], EfficientNet-B0 [8], and MobileNetV2 [7] into a 5,120-dimensional latent representation, served through an asynchronous FastAPI service and a React frontend with runtime uncertainty gating logic [9], [10]."
    )
    add_p(
        "Rather than presenting unverified metrics, this paper provides an honest, evidence-based account: the prototype is non-diagnostic; the dataset contains 940 images with 21 duplicate groups (11 crossing splits) and unverified provenance; training scripts are missing; previously reported 99.92% accuracy was generated through synthetic random simulation; and true empirical metrics on real images are currently unavailable. Prioritizing scientific integrity, data auditing, and transparent systems documentation provides a credible baseline for future academic research."
    )
    add_p(
        "The authors express their sincere gratitude to Project Guide Prof. Aishwarya S, Assistant Professor, Department of Computer Science & Engineering, Kalpataru Institute of Technology, Tiptur, for technical guidance and supervision. The authors also acknowledge the Department of Computer Science & Engineering, Kalpataru Institute of Technology, and Visvesvaraya Technological University (VTU), Belagavi, for providing laboratory facilities and institutional support."
    )
    add_p("We intend to explore future work across several technical avenues:")
    add_bullet("Multi-Class Ordinal Classification: Transitioning from binary classification to a 4-class ordinal model (Healthy -> Benign -> OPMD -> Malignant) using ordinal cross-entropy loss.")
    add_bullet("Hybrid Vision Transformers: Integrating a Swin Transformer branch to capture long-range tissue structural atypia alongside local CNN features.")
    add_bullet("Calibrated Uncertainty: Implementing temperature scaling and conformal prediction for rigorously calibrated decision-support referral boundaries.")

    # -------------------------------------------------------------
    # SECTION VIII: REFERENCES (numId="19" for automatic [N] numbering)
    # -------------------------------------------------------------
    add_h1("REFERENCES")

    references = [
        "H. Sung, J. Ferlay, R. L. Siegel, M. Laversanne, I. Soerjomataram, A. Jemal, and F. Bray, \"Global Cancer Statistics 2020: GLOBOCAN Estimates of Incidence and Mortality Worldwide for 36 Cancers in 185 Countries,\" CA: A Cancer Journal for Clinicians, vol. 71, no. 3, pp. 209-249, 2021. DOI: 10.3322/caac.21660.",
        "P. Brocklehurst, O. Kujan, L. A. O'Malley, G. R. Ogden, S. Shepherd, and A.-M. Glenny, \"Screening programmes for the early detection and prevention of oral cancer,\" Cochrane Database of Systematic Reviews, no. 11, Art. No. CD004150, 2013. DOI: 10.1002/14651858.CD004150.pub4.",
        "R. A. Welikala, P. Remagnino, J. H. Lim, C. S. Chan, S. Rajendran, T. G. Kallarakkal, R. B. Zain, R. D. Jayasinghe, V. Mohan, A. Rao, K. A. Amirtham, and S. J. Loffman, \"Automated Detection and Classification of Oral Lesions Using Deep Learning for Early Detection of Oral Cancer,\" IEEE Access, vol. 8, pp. 132677-132693, 2020. DOI: 10.1109/ACCESS.2020.3010180.",
        "K. Warin, W. Limprasert, S. Suebnukarn, S. Jinaporntham, P. Jantana, and S. Vicharueang, \"AI-based analysis of oral lesions using novel deep convolutional neural networks for early detection of oral cancer,\" PLOS ONE, vol. 17, no. 8, p. e0273508, 2022. DOI: 10.1371/journal.pone.0273508.",
        "K. Simonyan and A. Zisserman, \"Very Deep Convolutional Networks for Large-Scale Image Recognition,\" in Proc. 3rd International Conference on Learning Representations (ICLR), San Diego, CA, USA, 2015. arXiv: 1409.1556.",
        "K. He, X. Zhang, S. Ren, and J. Sun, \"Deep Residual Learning for Image Recognition,\" in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 770-778. DOI: 10.1109/CVPR.2016.90.",
        "M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, \"MobileNetV2: Inverted Residuals and Linear Bottlenecks,\" in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 4510-4520. DOI: 10.1109/CVPR.2018.00474.",
        "M. Tan and Q. V. Le, \"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,\" in Proc. 36th International Conference on Machine Learning (ICML), PMLR, vol. 97, 2019, pp. 6105-6114.",
        "Y. Gal and Z. Ghahramani, \"Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning,\" in Proc. 33rd International Conference on Machine Learning (ICML), PMLR, vol. 48, 2016, pp. 1050-1059.",
        "M. S. Ayhan and P. Berens, \"Test-time Data Augmentation for Estimation of Heteroscedastic Aleatoric Uncertainty in Deep Neural Networks,\" in Proc. 1st Conference on Medical Imaging with Deep Learning (MIDL), Amsterdam, The Netherlands, 2018. arXiv: 1803.06013.",
        "M. Roberts, D. Driggs, M. Thorpe, J. Gilbey, M. Yeung, S. Ursprung, A. I. Aviles-Rivero, C. Etmann, C. McCague, L. Beer, J. R. Weir-McCall, Z. Teng, E. Gkrania-Klotsas, AIX-COVNET Collaboration, J. H. F. Rudd, E. Sala, and C.-B. Schönlieb, \"Common pitfalls and recommendations for using machine learning to detect and prognosticate for COVID-19 using chest radiographs and CT scans,\" Nature Machine Intelligence, vol. 3, no. 3, pp. 199-217, 2021. DOI: 10.1038/s42256-021-00307-0.",
        "S. Kapoor and A. Narayanan, \"Leakage and the reproducibility crisis in machine-learning-based science,\" Patterns, vol. 4, no. 9, p. 100804, 2023. DOI: 10.1016/j.patter.2023.100804.",
        "A. Chattopadhay, A. Sarkar, P. Howlader, and V. N. Balasubramanian, \"Grad-CAM++: Generalized Gradient-Based Visual Explanations for Deep Convolutional Networks,\" in Proc. IEEE Winter Conference on Applications of Computer Vision (WACV), 2018, pp. 839-847. DOI: 10.1109/WACV.2018.00097."
    ]

    for ref in references:
        p_ref = doc.add_paragraph(style='List Paragraph')
        pPr_ref = p_ref._p.get_or_add_pPr()
        numPr_ref = parse_xml(f'<w:numPr {nsdecls("w")}><w:ilvl w:val="0"/><w:numId w:val="19"/></w:numPr>')
        pPr_ref.append(numPr_ref)
        p_ref.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p_ref.paragraph_format.space_before = Pt(3.0)
        p_ref.paragraph_format.space_after = Pt(0)
        p_ref.paragraph_format.line_spacing = 1.15
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Cambria"
        r_ref.font.size = Pt(10)

    doc.save(output_docx)
    print(f"Manuscript saved successfully to: {output_docx}")

if __name__ == "__main__":
    build_paper()
