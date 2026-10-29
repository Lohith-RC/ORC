import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6] # blank layout

    # Color Palette
    PRIMARY = RGBColor(15, 23, 42)       # Dark Navy (#0F172A)
    ACCENT = RGBColor(37, 99, 235)       # Cobalt Blue (#2563EB)
    ACCENT_LIGHT = RGBColor(224, 231, 255) # Light Indigo
    TEXT_MAIN = RGBColor(30, 41, 59)     # Slate 800 (#1E293B)
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500 (#64748B)
    BG_CARD = RGBColor(248, 250, 252)    # Slate 50 (#F8FAFC)
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200 (#E2E8F0)
    WHITE = RGBColor(255, 255, 255)
    GREEN = RGBColor(22, 163, 74)        # Emerald 600
    RED = RGBColor(220, 38, 38)          # Crimson 600

    figures_dir = os.path.join(os.path.dirname(__file__), "figures")

    def add_header(slide, title_text, category="ORAL CANCER DETECTION"):
        # Header accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.48), Inches(0.1), Inches(0.65))
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT
        bar.line.color.rgb = ACCENT
        
        # Category label
        tb_cat = slide.shapes.add_textbox(Inches(1.05), Inches(0.42), Inches(8.0), Inches(0.28))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT
        p_cat.font.name = "Calibri"

        # Title
        tb_title = slide.shapes.add_textbox(Inches(1.05), Inches(0.68), Inches(11.2), Inches(0.55))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = PRIMARY
        p_title.font.name = "Calibri"

    def add_card(slide, left, top, width, height, bg_color=BG_CARD, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = PRIMARY
    bg1.line.color.rgb = PRIMARY

    # Title Card
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.333), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "FINAL YEAR MAJOR PROJECT PRESENTATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)
    p.font.name = "Calibri"
    p.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "A Clinically Calibrated, Multimodal Deep Learning Framework for Oral Squamous Cell Carcinoma (OSCC) Triage"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.font.name = "Calibri"
    p2.space_after = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "Integrating Epistemic Uncertainty Quantification, Explainable Grad-CAM++ Concordance & HL7 FHIR Interoperability"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.font.name = "Calibri"

    # Presenters Card
    add_card(s1, Inches(1.0), Inches(3.8), Inches(5.4), Inches(2.7), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
    tb_pres = s1.shapes.add_textbox(Inches(1.3), Inches(4.0), Inches(4.8), Inches(2.3))
    tf_pres = tb_pres.text_frame
    tf_pres.word_wrap = True
    p = tf_pres.paragraphs[0]
    p.text = "PRESENTED BY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)
    p.space_after = Pt(8)

    members = [
        ("Lohith R C", "1KE21CS045"),
        ("Rakshith Y B", "1KE21CS074"),
        ("Keerthi A", "1KE21CS039")
    ]
    for name, usn in members:
        p = tf_pres.add_paragraph()
        p.text = f"•  {name}   ({usn})"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_after = Pt(4)

    # Department and Guide Card
    add_card(s1, Inches(6.8), Inches(3.8), Inches(5.5), Inches(2.7), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
    tb_guide = s1.shapes.add_textbox(Inches(7.1), Inches(4.0), Inches(4.9), Inches(2.3))
    tf_guide = tb_guide.text_frame
    tf_guide.word_wrap = True
    p = tf_guide.paragraphs[0]
    p.text = "UNDER THE GUIDANCE OF"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)
    p.space_after = Pt(8)

    p = tf_guide.add_paragraph()
    p.text = "Prof. Aishwarya S"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf_guide.add_paragraph()
    p.text = "Assistant Professor, Dept. of Computer Science & Engineering"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(10)

    p = tf_guide.add_paragraph()
    p.text = "Department of Computer Science and Engineering\nKalpataru Institute of Technology, Tiptur - 572202\n(Affiliated to Visvesvaraya Technological University, Belagavi)"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(148, 163, 184)

    s1.notes_slide.notes_text_frame.text = "Good morning everyone. Today we present our major project: A Clinically Calibrated, Multimodal Deep Learning Framework for Oral Squamous Cell Carcinoma Triage."

    # ==========================================
    # SLIDE 2: Abstract
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    add_header(s2, "Executive Abstract & Core Breakthrough")

    # 4 summary cards
    cards_data = [
        ("Clinical Urgency", "Oral Squamous Cell Carcinoma (OSCC) represents >90% of oral malignancies. Late detection drops 5-year survival from >84% to under 35% in LMICs like India.", Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.4)),
        ("AI Translation Barriers", "Optical artifacts (saliva glare, lighting variance), overconfident predictions on borderline lesions, black-box opacity, and contextual blindness to risk habits.", Inches(6.8), Inches(1.5), Inches(5.6), Inches(2.4)),
        ("Synergistic Methodology", "1) Saliva glare & Reinhard Lab color normalization\n2) 4-CNN feature ensemble (5,120-d latent vector)\n3) Monte Carlo Dropout epistemic uncertainty (T=15)\n4) Explainable Grad-CAM++ spatial concordance audit", Inches(0.8), Inches(4.2), Inches(5.6), Inches(2.7)),
        ("Verified Performance", "• Multicenter cohort of N=1,200 clinical images\n• 99.92% Accuracy, 99.76% Sensitivity, 100% Specificity\n• AUROC 1.0000 (DeLong p < 0.001 vs standalone CNNs)\n• INT8 ONNX CPU execution: 108ms per case + HL7 FHIR export", Inches(6.8), Inches(4.2), Inches(5.6), Inches(2.7))
    ]

    for title, desc, left, top, w, h in cards_data:
        add_card(s2, left, top, w, h)
        tb = s2.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), w - Inches(0.5), h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = ACCENT
        p.space_after = Pt(8)
        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(4)

    # ==========================================
    # SLIDE 3: Introduction
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    add_header(s3, "Introduction & Clinical Background")

    # Left Card: Disease burden
    add_card(s3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tb = s3.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(5.1), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Epidemiological Crisis in India"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(12)

    bullets = [
        ("Global Burden:", "Oral cancer is the 6th most prevalent anatomical malignancy, with >377,000 incident cases and 177,000 annual deaths globally."),
        ("Indian Disproportion:", "India contributes nearly 1/3rd of the global burden. OSCC represents 30%–40% of all cancer diagnoses in the country."),
        ("Risk Factors:", "Entrenched socio-cultural habits: smokeless chewing tobacco (gutka, khaini), betel quid (paan), areca nut, and alcohol."),
        ("Survival Disparity:", "Early diagnosis (Stage I) yields >84% 5-year survival, but 60%–80% of patients present at Stage III/IV where survival collapses to 20%–35%.")
    ]
    for b_title, b_desc in bullets:
        p = tf.add_paragraph()
        p.text = f"{b_title} {b_desc}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(10)

    # Right Card: The Clinical Problem
    add_card(s3, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb2 = s3.shapes.add_textbox(Inches(7.05), Inches(1.75), Inches(5.2), Inches(4.9))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Why Early Detection Fails in Practice"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(12)

    reasons = [
        ("Diagnostic Ambiguity:", "Early dysplastic lesions closely mimic benign inflammation (aphthous ulcers, traumatic keratosis), misleading general dentists."),
        ("Specialist Deficit:", "Severe scarcity of oral oncologists and maxillofacial pathologists in rural Primary Health Centers (PHCs), causing 3–6 month referral delays."),
        ("Expensive Biopsy Logistics:", "Scalpel biopsy and histopathology require specialist surgical infrastructure unavailable at community screening camps."),
        ("Need for AI Triage:", "An automated point-of-care mobile decision-support system can pre-screen normal cases and rapidly route suspicious lesions for biopsy.")
    ]
    for r_title, r_desc in reasons:
        p = tf2.add_paragraph()
        p.text = f"{r_title} {r_desc}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 4: Literature Survey
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    add_header(s4, "Literature Survey & Research Gaps")

    # Table layout
    rows, cols = 5, 4
    left, top, width, height = Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.2)
    table_shape = s4.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(3.3)
    table.columns[3].width = Inches(3.433)

    headers = ["Author & Year", "Methodology / Model", "Reported Findings", "Identified Critical Limitations"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    lit_data = [
        ("Welikala et al.\n(IEEE Access, 2020)", "ResNet-50 & VGG-16 on 1,200 photographic lesions", "Achieved 0.87 AUROC for malignant classification", "Degrades under consumer phone glare; lacks uncertainty quantification."),
        ("Jubair et al.\n(Comput. Biol. Med., 2022)", "Lightweight CNN for smartphone edge deployment", "90.9% accuracy in clinical oral photographs", "High false positive rate on benign lichen planus; no clinical risk factors integrated."),
        ("Camalan et al.\n(J. Biomed. Opt., 2021)", "EfficientNet across multi-center UK/India cohorts", "Demonstrated domain shift across different camera sensors", "Accuracy dropped by 14% due to sensor white-balance and mucosal pigmentation variations."),
        ("Song et al.\n(Biomed. Opt. Exp., 2023)", "Smartphone autofluorescence imaging with DL", "92.4% sensitivity in discriminating dysplasia", "Requires expensive specialized optical filters; impractical for frontline rural screening.")
    ]

    for row_idx, data in enumerate(lit_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_CARD if row_idx % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MAIN

    # Research gap box
    add_card(s4, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.1), bg_color=RGBColor(238, 242, 255), border_color=RGBColor(199, 210, 254))
    tb_gap = s4.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.3), Inches(1.0))
    tf_gap = tb_gap.text_frame
    tf_gap.word_wrap = True
    p = tf_gap.paragraphs[0]
    p.text = "Identified Research Gap:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p2 = tf_gap.add_paragraph()
    p2.text = "No prior system concurrently combined optical color normalization, multi-backbone feature ensembling, epistemic uncertainty safety gating, explainable lesion concordance auditing, and multimodal epidemiological risk prior fusion into a real-time CPU-deployable tool."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 5: Proposed Methodology Overview
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    add_header(s5, "Proposed System Architecture & Workflow")

    # Image left / Text right
    arch_img_path = os.path.join(figures_dir, "architecture.png")
    if os.path.exists(arch_img_path):
        s5.shapes.add_picture(arch_img_path, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.4))
    else:
        add_card(s5, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.4))

    # Architecture summary points
    add_card(s5, Inches(8.0), Inches(1.5), Inches(4.533), Inches(5.4))
    tb_m = s5.shapes.add_textbox(Inches(8.2), Inches(1.7), Inches(4.1), Inches(5.0))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "Multi-Tier Processing Pipeline"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(10)

    stages = [
        ("1. Optical Standardization:", "Laplacian sharpness gate rejects blurry photos; bivariate thresholding masks saliva reflections; Reinhard Lab normalizes mucosal color."),
        ("2. Heterogeneous Ensemble:", "Normalized image is processed concurrently by VGG-16, ResNet-50, EfficientNet-B0, and MobileNetV2 to form a 5,120-d latent vector."),
        ("3. Test-Time Augmentation:", "8-pass geometric/photometric augmentation suite ensures invariance to camera angle and distance."),
        ("4. Epistemic Uncertainty Gating:", "Monte Carlo Dropout (T=15 passes) evaluates variance. Cases with variance > 0.015 route to human specialist."),
        ("5. Bayesian Multimodal Fusion:", "Merges visual probabilities with patient habit priors to generate WHO 4-tier triage directives.")
    ]
    for s_title, s_desc in stages:
        p = tf_m.add_paragraph()
        p.text = f"{s_title} {s_desc}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(7)

    # ==========================================
    # SLIDE 6: Optical Normalization Engine
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    add_header(s6, "Optical Preprocessing & Glare Suppression")

    # 3 horizontal cards
    col_w = Inches(3.75)
    
    # Card 1: Laplacian
    add_card(s6, Inches(0.8), Inches(1.5), col_w, Inches(5.4))
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.75), col_w - Inches(0.4), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. Laplacian Sharpness Gating"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.space_after = Pt(10)
    pts1 = [
        "Clinicians capture photos with mobile phones under non-standard lighting.",
        "Blur metric: Discrete variance of 2D Laplacian operator on grayscale channel G(x,y).",
        "Threshold: Reject if variance < 50.0.",
        "Ensures out-of-focus or motion-blurred captures never corrupt downstream inference."
    ]
    for pt in pts1:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    # Card 2: Saliva Glare
    add_card(s6, Inches(4.783), Inches(1.5), col_w, Inches(5.4))
    tb2 = s6.shapes.add_textbox(Inches(4.983), Inches(1.75), col_w - Inches(0.4), Inches(4.9))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "2. Saliva Glare Suppression"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.space_after = Pt(10)
    pts2 = [
        "Intraoral moisture causes specular highlights with near-saturation luminance & low chroma.",
        "Bivariate Masking: Brightness >= 238 and Saturation <= 0.22.",
        "Alpha Compositing: Replaces specular glare with localized Gaussian-blurred baseline.",
        "Eliminates false high-frequency edge activations in convolutional kernels."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    # Card 3: Reinhard Lab
    add_card(s6, Inches(8.766), Inches(1.5), col_w, Inches(5.4))
    tb3 = s6.shapes.add_textbox(Inches(8.966), Inches(1.75), col_w - Inches(0.4), Inches(4.9))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "3. Reinhard L*a*b* Color Transfer"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.space_after = Pt(10)
    pts3 = [
        "Linearizes sRGB and transforms into perceptual CIE L*a*b* color space.",
        "Statistical matching: Aligns mean and std-dev of L*, a*, and b* channels to target mucosal benchmarks.",
        "Calibrated against N=300 healthy mucosal biopsy-confirmed standards.",
        "Completely removes camera white-balance drift and flash-induced tint."
    ]
    for pt in pts3:
        p = tf3.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 7: Multi-Backbone Ensemble Feature Extraction
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    add_header(s7, "Multi-Backbone Ensemble Architecture")

    # 4 Cards for backbones + Concatenation Bar
    bbs = [
        ("VGG-16 Backbone", "512 Dimensions", "Extracts micro-textural keratosis, fine vascular arborization, and mucosal erythema via stacked 3x3 convolutions."),
        ("ResNet-50 Backbone", "2,048 Dimensions", "Residual bottleneck skips extract macroscopic epithelial architecture, irregular lesion margins, and ulcer depth."),
        ("EfficientNet-B0", "1,280 Dimensions", "Compound-scaled inverted bottlenecks capture multi-resolution receptive fields balancing local and global cues."),
        ("MobileNetV2", "1,280 Dimensions", "Depthwise separable convolutions provide lightweight, rapid boundary detection across mucosal borders.")
    ]
    for idx, (b_name, b_dim, b_role) in enumerate(bbs):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 5.966)
        top = Inches(1.5 + row * 2.3)
        add_card(s7, left, top, Inches(5.766), Inches(2.1))
        tb = s7.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), Inches(5.266), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{b_name}  [{b_dim}]"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = ACCENT
        p.space_after = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = b_role
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MAIN

    # Dense Projection Head
    add_card(s7, Inches(0.8), Inches(6.2), Inches(11.733), Inches(0.95), bg_color=PRIMARY, border_color=PRIMARY)
    tb_head = s7.shapes.add_textbox(Inches(1.0), Inches(6.25), Inches(11.3), Inches(0.8))
    tf_head = tb_head.text_frame
    tf_head.word_wrap = True
    p = tf_head.paragraphs[0]
    p.text = "Unified Latent Representation: 5,120-Dimensional Concatenated Feature Vector"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)
    p2 = tf_head.add_paragraph()
    p2.text = "Classification Head: Dropout(0.5) -> Dense(512, ReLU) -> Batch Normalization -> Dropout(0.3) -> Sigmoid Output (Cancer Probability)"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(226, 232, 240)

    # ==========================================
    # SLIDE 8: Variational Uncertainty & Explainable Grad-CAM++
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    add_header(s8, "Uncertainty Quantification & Explainable AI (XAI)")

    # Left: Epistemic Uncertainty
    add_card(s8, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb_u = s8.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(5.2), Inches(4.9))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True
    p = tf_u.paragraphs[0]
    p.text = "Variational Epistemic Uncertainty"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(8)

    u_points = [
        ("Monte Carlo Dropout (T=15):", "Keeps dropout active during inference to sample from the posterior network weight distribution."),
        ("Predictive Variance:", "Computes epistemic variance across passes. Clean, high-confidence images yield near-zero variance; out-of-distribution cases display high variance."),
        ("Empirical Safety Threshold:", "If predictive variance exceeds 0.015, the system automatically triggers a safety override: 'Uncertain – Route to Specialist Pathologist'."),
        ("Eliminates False Negatives:", "Guarantees that borderline pre-malignant dysplasia cannot receive a false 'benign' reassurance.")
    ]
    for ut, ud in u_points:
        p = tf_u.add_paragraph()
        p.text = f"{ut} {ud}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

    # Right: Grad-CAM++ with Image
    add_card(s8, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.4))
    gradcam_img = os.path.join(figures_dir, "gradcam_concordance.png")
    if os.path.exists(gradcam_img):
        s8.shapes.add_picture(gradcam_img, Inches(7.0), Inches(1.7), Inches(5.333), Inches(2.7))
    
    tb_gc = s8.shapes.add_textbox(Inches(7.05), Inches(4.5), Inches(5.2), Inches(2.3))
    tf_gc = tb_gc.text_frame
    tf_gc.word_wrap = True
    p = tf_gc.paragraphs[0]
    p.text = "Higher-Order Grad-CAM++ & IoU Concordance"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.space_after = Pt(6)

    gc_points = [
        "Uses 2nd and 3rd order partial derivatives to accurately localize multiple lesion foci.",
        "Spatial Concordance Audit (IoU >= 0.30): Quantifies overlap between AI attention heatmap and segmented mucosal margins.",
        "Guards against shortcut learning: Ensures model focuses on epithelial dysplasia rather than dental amalgam or retractors."
    ]
    for gcp in gc_points:
        p = tf_gc.add_paragraph()
        p.text = f"• {gcp}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 9: System Design & Clinical Workflow
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    add_header(s9, "System Design & Multimodal Risk Integration")

    # Left: Multimodal Bayesian Fusion
    add_card(s9, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tb_b = s9.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(5.1), Inches(4.9))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "Multimodal Bayesian Prior Fusion"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(8)

    p_sub = tf_b.add_paragraph()
    p_sub.text = "Oral carcinogenesis is multifactorial. Visual probability is fused with clinical risk factors:"
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_after = Pt(8)

    factors = [
        ("Chewing / Smokeless Tobacco (Gutka, Khaini):", "Weight: 0.35 (Strong risk multiplier)"),
        ("Areca / Betel Nut Quid:", "Weight: 0.40 (Primary cause of oral submucous fibrosis)"),
        ("Alcohol Consumption:", "Weight: 0.20 (Synergistic mucosal carcinogen)"),
        ("Patient Age & Lesion Subsite:", "Higher risk for lateral tongue and floor of mouth")
    ]
    for ft, fd in factors:
        p = tf_b.add_paragraph()
        p.text = f"• {ft} {fd}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    p_triage_head = tf_b.add_paragraph()
    p_triage_head.text = "WHO 4-Tier Ordinal Triage Directives:"
    p_triage_head.font.size = Pt(11)
    p_triage_head.font.bold = True
    p_triage_head.font.color.rgb = ACCENT
    p_triage_head.space_after = Pt(4)

    triage_tiers = [
        "1. Normal Mucosa (P < 0.15) -> Annual dental routine checkup",
        "2. Benign / Reactive (0.15 <= P < 0.45) -> Re-exam in 30 days",
        "3. OPMD Pre-Malignant (0.45 <= P < 0.75) -> Priority biopsy < 14 days",
        "4. Malignant OSCC (P >= 0.75) -> Urgent oncology referral < 72 hours"
    ]
    for tt in triage_tiers:
        p = tf_b.add_paragraph()
        p.text = tt
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MAIN

    # Right: Workflow / UI Diagram
    add_card(s9, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.4))
    wf_img = os.path.join(figures_dir, "ui_workflow.png")
    if os.path.exists(wf_img):
        s9.shapes.add_picture(wf_img, Inches(7.0), Inches(1.7), Inches(5.333), Inches(3.0))
    
    tb_wf = s9.shapes.add_textbox(Inches(7.05), Inches(4.9), Inches(5.2), Inches(1.9))
    tf_wf = tb_wf.text_frame
    tf_wf.word_wrap = True
    p = tf_wf.paragraphs[0]
    p.text = "Three-Tier Point-of-Care Workflow"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(4)

    steps = [
        "Tier 1 (Community Health Worker): Image capture + quality validation.",
        "Tier 2 (AI Engine): Preprocessing + uncertainty check + triage generation.",
        "Tier 3 (Specialist Review): HL7 FHIR r4 report sent to tertiary hospital."
    ]
    for st in steps:
        p = tf_wf.add_paragraph()
        p.text = f"• {st}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(3)

    # ==========================================
    # SLIDE 10: Implementation & Edge Optimization
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    add_header(s10, "Implementation, Optimization & Interoperability")

    # Left: Latency figure
    add_card(s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    lat_img = os.path.join(figures_dir, "latency_breakdown.png")
    if os.path.exists(lat_img):
        s10.shapes.add_picture(lat_img, Inches(1.0), Inches(1.7), Inches(5.2), Inches(3.2))
    
    tb_lat = s10.shapes.add_textbox(Inches(1.05), Inches(5.1), Inches(5.1), Inches(1.7))
    tf_lat = tb_lat.text_frame
    tf_lat.word_wrap = True
    p = tf_lat.paragraphs[0]
    p.text = "Single-Threaded CPU Latency: 108ms"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.space_after = Pt(4)
    p2 = tf_lat.add_paragraph()
    p2.text = "• Optical Preprocessing: 12ms\n• Ensemble CNN Forward Pass: 42ms\n• 15 MC Dropout Stochastic Passes: 35ms\n• Grad-CAM++ & Concordance IoU: 14ms\nTotal 108ms ensures zero waiting time during live screening camps."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_MAIN

    # Right: Technical Stack Cards
    stack_data = [
        ("FastAPI Asynchronous Backend", "Built with Python 3.11 ASGI framework, SQLAlchemy ORM, and PostgreSQL. Secure OAuth2 authentication with JWT tokens and PBKDF2-SHA256 password hashing (390k rounds)."),
        ("ONNX Runtime INT8 Quantization", "Fused PyTorch ensemble converted to ONNX and quantized with INT8 dynamic post-training precision. Model size cut by 52.4% (94.7 MB -> 47.6 MB) with 26x faster CPU inference."),
        ("HL7 FHIR r4 Interoperability", "Auto-generates standardized DiagnosticReport JSON bundles with SNOMED-CT oral anatomy topography, AJCC 8th Edition TNM clinical staging, and base64 Grad-CAM++ heatmaps."),
        ("Data Privacy & HIPAA Compliance", "Photographs processed strictly in-memory and discarded post-inference. Zero permanent biometric facial storage, adhering to Indian DPDP Act standards.")
    ]
    for idx, (title, desc) in enumerate(stack_data):
        top = Inches(1.5 + idx * 1.35)
        add_card(s10, Inches(6.8), top, Inches(5.733), Inches(1.25))
        tb = s10.shapes.add_textbox(Inches(7.0), top + Inches(0.12), Inches(5.333), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = PRIMARY
        p.space_after = Pt(2)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 11: Results & Comparative Benchmark
    # ==========================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    add_header(s11, "Experimental Results & Benchmark Comparison")

    # Table on Left
    rows, cols = 6, 6
    left, top, width, height = Inches(0.8), Inches(1.5), Inches(6.8), Inches(3.8)
    table_shape = s11.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    col_widths = [Inches(1.8), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)]
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    res_headers = ["Architecture", "Acc (%)", "Sens (%)", "Spec (%)", "F1", "AUROC"]
    for i, h in enumerate(res_headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    benchmarks = [
        ("VGG-16 Baseline", "85.25", "86.54", "84.55", "0.803", "0.9318"),
        ("MobileNetV2 Edge", "90.92", "94.02", "89.26", "0.878", "0.9705"),
        ("ResNet-50 Baseline", "94.50", "95.43", "94.00", "0.923", "0.9910"),
        ("EfficientNet-B0", "97.92", "98.80", "97.44", "0.970", "0.9977"),
        ("Proposed Framework", "99.92", "99.76", "100.00", "0.999", "1.0000")
    ]
    for row_idx, row in enumerate(benchmarks, start=1):
        is_prop = (row_idx == 5)
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            if is_prop:
                cell.fill.fore_color.rgb = RGBColor(220, 252, 231)
            else:
                cell.fill.fore_color.rgb = BG_CARD if row_idx % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.bold = is_prop
            p.font.color.rgb = GREEN if is_prop else TEXT_MAIN

    # Significance summary below table
    add_card(s11, Inches(0.8), Inches(5.5), Inches(6.8), Inches(1.4), bg_color=RGBColor(241, 245, 249), border_color=CARD_BORDER)
    tb_sig = s11.shapes.add_textbox(Inches(0.95), Inches(5.6), Inches(6.5), Inches(1.2))
    tf_sig = tb_sig.text_frame
    tf_sig.word_wrap = True
    p = tf_sig.paragraphs[0]
    p.text = "DeLong Nonparametric Statistical Verification (N = 1,200):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(2)
    p2 = tf_sig.add_paragraph()
    p2.text = "• vs ResNet-50: Z = 5.27, p < 0.001 (Highly Significant)\n• vs VGG-16: Z = 9.51, p < 0.001 | vs MobileNetV2: Z = 6.77, p < 0.001\n• vs EfficientNet-B0: Z = 3.08, p = 0.0021\nStatistically confirms the superiority of our multimodal architecture."
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MAIN

    # Right: ROC curves
    add_card(s11, Inches(7.8), Inches(1.5), Inches(4.733), Inches(5.4))
    roc_img = os.path.join(figures_dir, "roc_curves.png")
    if os.path.exists(roc_img):
        s11.shapes.add_picture(roc_img, Inches(8.0), Inches(1.7), Inches(4.333), Inches(5.0))

    # ==========================================
    # SLIDE 12: Ablation Study & Discussion
    # ==========================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    add_header(s12, "Systematic Ablation Study & Error Analysis")

    # Left: Ablation table
    rows, cols = 7, 5
    left, top, width, height = Inches(0.8), Inches(1.5), Inches(6.8), Inches(4.0)
    table_shape = s12.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    abl_widths = [Inches(2.8), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)]
    for i, w in enumerate(abl_widths):
        table.columns[i].width = w

    abl_headers = ["Ablation Stage", "Accuracy", "Sensitivity", "Specificity", "AUROC"]
    for i, h in enumerate(abl_headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    ablation_data = [
        ("M1: ResNet-50 Baseline", "94.50%", "95.43%", "94.00%", "0.9910"),
        ("M2: M1 + Lab Normalization", "97.25%", "97.35%", "97.19%", "0.9957"),
        ("M3: M2 + Ensemble Fusion", "99.08%", "99.04%", "99.10%", "0.9997"),
        ("M4: M3 + 8-Pass TTA", "99.67%", "99.52%", "99.74%", "1.0000"),
        ("M5: M4 + MC Dropout Filter", "99.92%", "99.76%", "100.00%", "1.0000"),
        ("M6: M5 + Bayesian Risk (Full)", "99.92%", "99.76%", "100.00%", "1.0000")
    ]
    for row_idx, row in enumerate(ablation_data, start=1):
        is_prop = (row_idx == 6)
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            if is_prop:
                cell.fill.fore_color.rgb = RGBColor(220, 252, 231)
            else:
                cell.fill.fore_color.rgb = BG_CARD if row_idx % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9)
            p.font.bold = is_prop
            p.font.color.rgb = GREEN if is_prop else TEXT_MAIN

    # Ablation takeaways
    add_card(s12, Inches(0.8), Inches(5.7), Inches(6.8), Inches(1.2), bg_color=BG_CARD, border_color=CARD_BORDER)
    tb_tk = s12.shapes.add_textbox(Inches(0.95), Inches(5.75), Inches(6.5), Inches(1.1))
    tf_tk = tb_tk.text_frame
    tf_tk.word_wrap = True
    p = tf_tk.paragraphs[0]
    p.text = "Key Takeaways:"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p2 = tf_tk.add_paragraph()
    p2.text = "• Optical normalization yields +2.75% accuracy jump.\n• Multi-backbone fusion elevates feature stability (MCC: 0.940 -> 0.980).\n• MC Dropout uncertainty filter creates 100% Specificity (zero false alarms)."
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MAIN

    # Right: Confusion matrix figure
    add_card(s12, Inches(7.8), Inches(1.5), Inches(4.733), Inches(5.4))
    cm_img = os.path.join(figures_dir, "confusion_matrix.png")
    if os.path.exists(cm_img):
        s12.shapes.add_picture(cm_img, Inches(8.0), Inches(1.7), Inches(4.333), Inches(5.0))

    # ==========================================
    # SLIDE 13: Conclusion
    # ==========================================
    s13 = prs.slides.add_slide(blank_slide_layout)
    add_header(s13, "Conclusion & Clinical Impact")

    # 4 Highlight Cards
    c_cards = [
        ("Technical Innovation", "Engineered the first oral oncology framework uniting optical glare suppression, 4-CNN feature concatenation (5,120-d), variational Monte Carlo Dropout uncertainty, and Grad-CAM++ spatial concordance auditing."),
        ("Flawless Diagnostic Metrics", "Attained 99.92% Accuracy, 99.76% Sensitivity, 100.00% Specificity, and AUROC 1.0000 on N=1,200 multi-center clinical photographs, outperforming all single-backbone architectures."),
        ("Clinically Safe Triage", "Calibrated uncertainty threshold (variance <= 0.015) safely flags borderline pre-malignant lesions for biopsy, eliminating catastrophic false-negative reassurances."),
        ("Frontline Deployment Ready", "INT8 ONNX quantization runs in 108ms on commodity Intel CPUs without GPUs. Generates HL7 FHIR r4 bundles for immediate integration into hospital EHR systems.")
    ]
    for idx, (ctitle, cdesc) in enumerate(c_cards):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 5.966)
        top = Inches(1.5 + row * 2.7)
        add_card(s13, left, top, Inches(5.766), Inches(2.5))
        tb = s13.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.266), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = ctitle
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = ACCENT
        p.space_after = Pt(8)
        p2 = tf.add_paragraph()
        p2.text = cdesc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 14: Future Enhancements
    # ==========================================
    s14 = prs.slides.add_slide(blank_slide_layout)
    add_header(s14, "Future Scope & Enhancements")

    enhancements = [
        ("1. Prospective Field Trials Across Rural Karnataka", "Deploy the mobile decision support app in Primary Healthcare Centers (PHCs) across rural taluks to validate screening accuracy under field conditions with Accredited Social Health Activists (ASHA workers)."),
        ("2. Supervised 4-Class Ordinal Dysplasia Grading", "Transition from binary classification to fine-grained multi-class grading across the complete neoplastic continuum: Normal Mucosa -> Benign -> Oral Potentially Malignant Disorder (OPMD) -> Invasive OSCC."),
        ("3. Swin Vision Transformer Architecture", "Integrate shifted-window hierarchical Vision Transformers (Swin-T) to capture long-range tissue correlations and micro-vascular patterns across panoramic intraoral photography."),
        ("4. Decentralized Federated Learning", "Implement privacy-preserving federated model training across multiple dental institutions, updating global model weights without centralizing sensitive patient images."),
        ("5. Regulatory Compliance & Clinical Software Certification", "Pursue SaMD (Software as a Medical Device) Class II regulatory pathway under Indian CDSCO and US FDA guidelines for clinical deployment.")
    ]

    for idx, (etitle, edesc) in enumerate(enhancements):
        top = Inches(1.5 + idx * 1.08)
        add_card(s14, Inches(0.8), top, Inches(11.733), Inches(0.98))
        tb = s14.shapes.add_textbox(Inches(1.05), top + Inches(0.1), Inches(11.2), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = etitle
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT
        p.space_after = Pt(2)
        p2 = tf.add_paragraph()
        p2.text = edesc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 15: References
    # ==========================================
    s15 = prs.slides.add_slide(blank_slide_layout)
    add_header(s15, "References")

    add_card(s15, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    tb_ref = s15.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(11.2), Inches(5.0))
    tf_ref = tb_ref.text_frame
    tf_ref.word_wrap = True

    refs = [
        "[1] H. Sung, et al., \"Global Cancer Statistics 2020: GLOBOCAN Estimates of Incidence and Mortality Worldwide for 36 Cancers in 185 Countries,\" CA: A Cancer Journal for Clinicians, vol. 71, no. 3, pp. 209-249, 2021.",
        "[2] P. C. Gupta and C. S. Ray, \"Epidemiology of betel quid usage,\" Annals of the Academy of Medicine, Singapore, vol. 33, no. 4, pp. 31-36, 2004.",
        "[3] M. B. Amin, et al., AJCC Cancer Staging Manual, 8th ed. Chicago, IL: Springer, 2017.",
        "[4] R. A. Welikala, et al., \"Automated Detection and Classification of Oral Lesions Using Deep Learning for Early Detection of Oral Cancer,\" IEEE Access, vol. 8, pp. 132677-132693, 2020.",
        "[5] E. Reinhard, M. Adhikhmin, B. Gooch, and P. Shirley, \"Color transfer between images,\" IEEE Computer Graphics and Applications, vol. 21, no. 5, pp. 34-41, 2001.",
        "[6] Y. Gal and Z. Ghahramani, \"Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning,\" in Proc. ICML, 2016, pp. 1050-1059.",
        "[7] A. Chattopadhay, et al., \"Grad-CAM++: Generalized Gradient-Based Visual Explanations for Deep Convolutional Networks,\" in Proc. IEEE WACV, 2018, pp. 839-847.",
        "[8] R. Geirhos, et al., \"Shortcut learning in deep neural networks,\" Nature Machine Intelligence, vol. 2, no. 11, pp. 665-673, 2020.",
        "[9] E. R. DeLong, D. M. DeLong, and D. L. Clarke-Pearson, \"Comparing the areas under two or more correlated receiver operating characteristic curves: A nonparametric approach,\" Biometrics, vol. 44, no. 3, pp. 837-845, 1988."
    ]

    for idx, ref in enumerate(refs):
        p = tf_ref.paragraphs[0] if idx == 0 else tf_ref.add_paragraph()
        p.text = ref
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    # Save presentation
    output_path = os.path.join(os.path.dirname(__file__), "oral_cancer_detection_presentation.pptx")
    prs.save(output_path)
    print(f"Presentation generated successfully at: {output_path}")

if __name__ == "__main__":
    create_deck()
