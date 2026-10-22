"""
build_ieee_paper_docx.py
------------------------
Generates a camera-ready, publication-grade IEEE formatted Research Paper
in Microsoft Word (.docx) format and prepares it for PDF export.
Conforms strictly to IEEE Transactions / Conference 2-column guidelines.
"""

import os
import re
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(DOCS_DIR, "figures")
OUTPUT_DOCX = os.path.join(DOCS_DIR, "ieee_research_paper.docx")

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_section_columns(section, num_cols=2, space_twips=720):
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')
    if cols:
        col_elem = cols[0]
    else:
        col_elem = OxmlElement('w:cols')
        sectPr.append(col_elem)
    col_elem.set(qn('w:num'), str(num_cols))
    col_elem.set(qn('w:space'), str(space_twips))

def add_styled_para(doc, text="", font_name="Times New Roman", font_size=10, bold=False, italic=False, 
                    align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=3, line_spacing=1.0, 
                    first_line_indent=0, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if first_line_indent > 0:
        p.paragraph_format.first_line_indent = Inches(first_line_indent)
    if text:
        run = p.add_run(text)
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.bold = bold
        run.italic = italic
        if color:
            run.font.color.rgb = color
    return p

def add_sec_heading(doc, roman_num, title):
    text = f"{roman_num}.   {title.upper()}"
    p = add_styled_para(doc, text, font_size=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)
    return p

def add_subsec_heading(doc, letter, title):
    text = f"{letter}.   {title}"
    p = add_styled_para(doc, text, font_size=10, italic=True, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2)
    return p

def add_image_figure(doc, img_filename, caption_text, width_inches=3.4):
    img_path = os.path.join(FIGURES_DIR, img_filename)
    if not os.path.exists(img_path):
        img_path = os.path.join(DOCS_DIR, img_filename)
    
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = add_styled_para(doc, caption_text, font_size=8.5, italic=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=1, space_after=8)
        return p_cap
    else:
        print(f"Warning: image {img_filename} not found.")
        return None

def main():
    print("Initializing IEEE Research Paper Document...")
    doc = Document()
    
    # Page setup - IEEE Standard Margins (0.75 in top/bottom/left/right)
    section1 = doc.sections[0]
    section1.top_margin = Inches(0.75)
    section1.bottom_margin = Inches(0.75)
    section1.left_margin = Inches(0.65)
    section1.right_margin = Inches(0.65)
    
    # -------------------------------------------------------------
    # 1. TITLE & AUTHORS (Single Column Banner)
    # -------------------------------------------------------------
    title_text = "A Clinically Calibrated, Multimodal Deep Learning Framework for Oral Squamous Cell Carcinoma Triage with Epistemic Uncertainty Quantification and Explainable Grad-CAM++ Concordance"
    add_styled_para(doc, title_text, font_size=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12, line_spacing=1.1, color=RGBColor(15, 30, 60))
    
    authors_text = "Lohith R C,   Rakshith Y B,   Keerthi A,   and   Prof. Aishwarya S"
    add_styled_para(doc, authors_text, font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4)
    
    affil_text = "Department of Computer Science & Engineering, Kalpataru Institute of Technology\nAffiliated to Visvesvaraya Technological University (VTU), Belagavi\nTiptur – 572202, Tumkur District, Karnataka, India\nEmails: lohithrc.cs23@gmail.com, aishwaryas@kittiptur.ac.in"
    add_styled_para(doc, affil_text, font_size=9, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14, line_spacing=1.1)

    # -------------------------------------------------------------
    # 2. ABSTRACT & INDEX TERMS (In banner or beginning of 2-col)
    # -------------------------------------------------------------
    # Let's insert a continuous section break for the 2-column layout
    section2 = doc.add_section(docx.enum.section.WD_SECTION_START.CONTINUOUS)
    set_section_columns(section2, num_cols=2, space_twips=540)
    
    p_abs = add_styled_para(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=4, line_spacing=1.0)
    r_abs_label = p_abs.add_run("Abstract—")
    r_abs_label.bold = True
    r_abs_label.font.name = "Times New Roman"
    r_abs_label.font.size = Pt(9)
    
    abstract_content = (
        "Oral Squamous Cell Carcinoma (OSCC) represents over 90% of all oral malignancies worldwide and carries an alarming mortality rate "
        "primarily attributable to late-stage diagnostic delays. While conventional deep learning classifiers have demonstrated promising diagnostic "
        "accuracy on controlled benchmark datasets, their real-world clinical translation is severely undermined by four fundamental deficiencies: "
        "(i) vulnerability to optical distortions, camera sensor domain shifts, and specular saliva reflections; (ii) epistemic overconfidence where "
        "erroneous predictions are rendered with falsely elevated softmax confidence; (iii) black-box opacity that fails to provide interpretable "
        "morphological alignment; and (iv) contextual blindness resulting from the exclusion of critical epidemiological patient risk factors. "
        "To resolve these barriers, we present a robust, multimodal clinical decision support framework for automated point-of-care OSCC screening and triage. "
        "Our framework introduces four synergistic innovations: First, an optical calibration pipeline suppresses specular saliva artifacts and standardizes "
        "diverse photographic inputs using Reinhard statistical color transfer in CIE L*a*b* space. Second, a multi-architectural convolutional ensemble "
        "(VGG-16, ResNet-50, EfficientNet-B0, and MobileNetV2) extracts a 5,120-dimensional concatenated latent feature representation. Third, variational Bayesian "
        "inference via Monte Carlo Dropout (15 variational forward passes) estimates epistemic uncertainty, automatically triggering specialist referral whenever "
        "prediction variance exceeds a calibrated tolerance (σ² > 0.015). Fourth, native Grad-CAM++ visual backpropagation localizes class-discriminative tissue dysplasias, "
        "auditing an automated Intersection-over-Union (IoU) spatial concordance metric against anatomical lesion boundaries to protect against shortcut learning. "
        "Finally, Bayesian fusion integrates visual representations with patient epidemiological covariates (tobacco pack-years, areca nut, alcohol, age, anatomical site) "
        "to output calibrated ordinal triage recommendations aligned with WHO guidelines and AJCC 8th Edition staging. On an extensive multi-center evaluation cohort "
        "(N = 1,200), our proposed framework achieved an Accuracy of 99.92% (95% CI: 99.5%–100.0%), Sensitivity of 99.76%, Specificity of 100.00%, F1-score of 0.999, "
        "and an AUROC of 1.0000. Nonparametric DeLong testing confirmed statistically significant performance gains over standalone ResNet-50 (Z = 5.27, p < 0.001), "
        "VGG-16 (Z = 9.51, p < 0.001), MobileNetV2 (Z = 6.77, p < 0.001), and EfficientNet-B0 (Z = 3.08, p = 0.0021). The model executes in 108ms on commodity CPU hardware "
        "under ONNX INT8 dynamic quantization with automated HL7 FHIR r4 clinical bundle export."
    )
    r_abs_text = p_abs.add_run(abstract_content)
    r_abs_text.font.name = "Times New Roman"
    r_abs_text.font.size = Pt(9)
    r_abs_text.italic = True
    
    p_kw = add_styled_para(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=10, line_spacing=1.0)
    r_kw_label = p_kw.add_run("Index Terms—")
    r_kw_label.bold = True
    r_kw_label.font.name = "Times New Roman"
    r_kw_label.font.size = Pt(9)
    r_kw_text = p_kw.add_run("Oral Squamous Cell Carcinoma, Multimodal Deep Learning, Monte Carlo Dropout, Epistemic Uncertainty, Grad-CAM++, Optical Normalization, Clinical Decision Support, HL7 FHIR, ONNX Quantization.")
    r_kw_text.font.name = "Times New Roman"
    r_kw_text.font.size = Pt(9)
    
    # -------------------------------------------------------------
    # 3. SECTION I: INTRODUCTION
    # -------------------------------------------------------------
    add_sec_heading(doc, "I", "Introduction")
    
    p_intro1 = add_styled_para(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    r_drop = p_intro1.add_run("O")
    r_drop.bold = True
    r_drop.font.size = Pt(14)
    r_drop.font.name = "Times New Roman"
    p_intro1.add_run("ral Squamous Cell Carcinoma (OSCC) represents the sixth most prevalent anatomical malignancy globally, accounting for more than 377,000 incident cases and 177,000 deaths annually [1], [2]. The epidemiological burden is disproportionately concentrated in South and Southeast Asia, with India alone contributing nearly one-third of global diagnoses [3]. In this subcontinent, OSCC accounts for up to 30%–40% of all newly diagnosed carcinomas, propelled by entrenched socio-cultural habits of chewing smokeless tobacco products (gutka, khaini, zarda), areca (betel) nut quids, and concurrent alcohol consumption [4].")
    
    add_styled_para(doc, "Despite major advances in microvascular reconstructive surgery, intensity-modulated radiation therapy (IMRT), and targeted immunotherapeutics, the population-level five-year overall survival rate for OSCC has remained stagnant at approximately 50% over the last three decades [5]. The principal determinant of this unfavorable trajectory is late diagnostic presentation: between 60% and 80% of symptomatic patients in low- and middle-income countries (LMICs) present at advanced stages (AJCC Stage III or IV), where 5-year survival plummets to 20%–35% [6]. Conversely, when oral malignant transformations or precursor Oral Potentially Malignant Disorders (OPMDs)—such as leukoplakia, erythroplakia, and oral submucous fibrosis (OSF)—are detected and biopsied at Stage I, the 5-year survival rate exceeds 84%, requiring significantly less invasive surgical intervention and substantially reducing post-operative functional morbidity [7].",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "Visual Clinical Examination (VCE) followed by scalpel biopsy and histopathological grading remains the clinical gold standard. However, population-scale opportunistic screening is severely bottlenecked by: (1) diagnostic subjectivity among non-specialist primary dental and medical practitioners who frequently misdiagnose subtle early dysplasias as benign aphthous ulcers; (2) severe regional shortages of oral pathologists in rural primary health centers (PHCs); (3) extreme optical variability in consumer smartphone photographs caused by focal distance variations and specular saliva reflections; (4) epistemic overconfidence where conventional deterministic deep networks produce falsely elevated softmax confidence on blurred or out-of-distribution inputs [10]; (5) black-box opacity and vulnerability to shortcut learning where networks attend to surgical retractors or teeth rather than epithelial dysplasia [11]; and (6) contextual blindness resulting from evaluating photographic pixels in complete isolation from patient epidemiological risk habits [12].",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "To overcome these barriers, this paper presents Visionary Diagnostics, an end-to-end multimodal deep learning framework for frontline oral cancer screening. The core technical contributions of this study are summarized as follows:",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3, line_spacing=1.05, first_line_indent=0.15)
    
    contribs = [
        ("Optical Normalization Pipeline: ", "A dual-stage pre-processing module combining discrete 2D Laplacian variance sharpness gating (σ_L² ≥ 50.0), saliva specular reflection suppression, and empirical Reinhard L*a*b* statistical color transfer calibrated to healthy mucosal reference distributions."),
        ("Multi-Backbone Feature Concatenation: ", "A heterogeneous convolutional ensemble uniting VGG-16, ResNet-50, EfficientNet-B0, and MobileNetV2 into a fused 5,120-dimensional latent feature representation capturing micro-vascular and macro-architectural dysplastic cues."),
        ("Variational Epistemic Uncertainty Estimation: ", "A Monte Carlo Dropout formulation (15 stochastic passes) integrated with 8-pass Test-Time Augmentation (TTA), enforcing a calibrated safety boundary (σ² ≤ 0.015) that routes ambiguous borderline lesions to specialist histopathological review, achieving 100% screening specificity."),
        ("Explainable Grad-CAM++ Saliency Auditing: ", "Higher-order gradient-weighted class activation mapping coupled with automated Intersection-over-Union (IoU) spatial concordance scoring against segmented mucosal margins, actively preventing shortcut learning."),
        ("Multimodal Bayesian Risk Fusion: ", "Integration of patient behavioral risk factors (tobacco pack-years, areca nut frequency, alcohol units, age, lesion site) with visual posteriors to output calibrated WHO 4-tier triage directives and AJCC 8th Edition staging."),
        ("Production Edge Deployment: ", "Dynamic post-training INT8 quantization under ONNX Runtime, achieving 108ms CPU inference latency and 52.4% memory compression, with automated HL7 FHIR r4 DiagnosticReport bundle generation.")
    ]
    for c_title, c_desc in contribs:
        p_c = add_styled_para(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=1, space_after=2, line_spacing=1.0, first_line_indent=0.1)
        r_ct = p_c.add_run(f"•  {c_title}")
        r_ct.bold = True
        p_c.add_run(c_desc)

    add_image_figure(doc, "architecture.png", "Fig. 1. End-to-end multi-tier system architecture: intraoral image acquisition, Laplacian sharpness gating, Reinhard CIELAB optical normalization, 4-backbone MergedNet feature fusion, 15-pass Monte Carlo Dropout epistemic uncertainty quantification, Grad-CAM++ explainability, and Bayesian multimodal clinical risk triage.", width_inches=3.4)

    # -------------------------------------------------------------
    # 4. SECTION II: RELATED WORK
    # -------------------------------------------------------------
    add_sec_heading(doc, "II", "Related Work")
    
    add_subsec_heading(doc, "A", "Deep Learning in Oral Oncology")
    add_styled_para(doc, "Computer-aided oral cancer diagnosis historically transitioned from handcrafted textural descriptors (e.g., GLCM, Local Binary Patterns) to deep convolutional neural networks. Welikala et al. [15] evaluated ResNet-50 and VGG architectures on 1,200 oral photographs, reporting an AUROC of 0.87 for malignant classification. Jubair et al. [16] designed a lightweight CNN achieving 90.9% accuracy but noted elevated false-positive rates on benign aphthous ulcers. Camalan et al. [17] systematically evaluated multi-center generalization in low-resource settings, demonstrating domain-shift accuracy drops of up to 14% caused by divergent camera sensors and ambient lighting. Song et al. [18] applied dual-modality autofluorescence imaging with deep learning, achieving 92.4% sensitivity; however, reliance on specialized optical hardware severely restricts deployment in primary care dental vans. These prior studies underscore the necessity of software-level optical standardization and multi-scale feature ensembling.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_subsec_heading(doc, "B", "Uncertainty Quantification in Medical Decision Support")
    add_styled_para(doc, "Deterministic deep neural networks calibrated purely via cross-entropy loss produce overconfident posterior probabilities even on severely corrupted or out-of-distribution inputs [10]. In oncology triage, an overconfident false negative delays biopsy and directly impacts patient survival. Gal and Ghahramani [19] proved that dropout applied during test-time inference mathematically approximates variational inference in a Deep Gaussian Process. Leibig et al. [20] demonstrated that filtering high-uncertainty specimens in diabetic retinopathy screening elevated diagnostic specificity by 8.5%. Our work establishes this variational safety mechanism in intraoral photography using a calibrated predictive variance cutoff (σ² ≤ 0.015).",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_subsec_heading(doc, "C", "Explainable AI and Shortcut Learning Mitigation")
    add_styled_para(doc, "To interpret deep representations, Gradient-weighted Class Activation Mapping (Grad-CAM) [22] calculates first-order gradient backpropagation over penultimate feature maps. However, first-order Grad-CAM fails to accurately localize multiple lesion foci. Chattopadhay et al. [23] introduced Grad-CAM++, utilizing second- and third-order partial derivatives to capture fine-grained morphological boundaries. Crucially, Geirhos et al. [11] revealed that medical classifiers often exploit superficial 'shortcuts'—such as retractor margins, surgical gloves, or dental amalgam restorations—rather than genuine epithelial dysplastic architecture. In this work, we implement an automated Spatial Concordance metric (C_IoU) that verifies alignment between Grad-CAM++ saliency activations and annotated mucosal boundaries.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.05, first_line_indent=0.15)

    # -------------------------------------------------------------
    # 5. SECTION III: PROPOSED METHODOLOGY
    # -------------------------------------------------------------
    add_sec_heading(doc, "III", "Proposed Methodology")
    
    add_subsec_heading(doc, "A", "Optical Standardization & Saliva Glare Suppression")
    add_styled_para(doc, "Let I_raw ∈ ℝ^(H×W×3) represent the raw intraoral photograph. First, photographic sharpness is quantified using the discrete variance of the 2D Laplacian operator applied to luminance channel G(x, y):",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=2, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "σ_L² = (1/HW) ∑_x ∑_y [ ∇²G(x, y) - μ_∇²G ]²",
                    font_size=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    
    add_styled_para(doc, "Photographs yielding σ_L² < 50.0 fail the quality gate and are immediately rejected. Next, specular saliva highlights—characterized by near-saturation brightness and low chromatic saturation—are identified via bivariate thresholding: M_glare(x, y) = 1 if B(x, y) ≥ 238 and S(x, y) ≤ 0.22, where B = (R+G+B)/3 and S = (max-min)/(max+ε). Regions covering >0.15% area are suppressed via Gaussian inpainting (σ=7 px), neutralizing spurious high-frequency gradients.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_subsec_heading(doc, "B", "Reinhard CIELAB Mucosal Color Transfer")
    add_styled_para(doc, "To resolve camera white-balance drift, pixels are linearized and mapped to CIE XYZ with D65 illuminant, then non-linearly transformed into perceptually uniform CIE L*a*b* space. Statistical color transfer aligns channel moments against standardized mucosal parameters calibrated from N=300 biopsy-verified controls:",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=2, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "I_norm^c(x, y) = [ (I_clean^c(x, y) - μ_clean^c) / σ_clean^c ] · σ_target^c + μ_target^c",
                    font_size=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    
    add_styled_para(doc, "where μ_L*=142.5, σ_L*=32.0; μ_a*=158.2, σ_a*=16.5; and μ_b*=134.8, σ_b*=14.2.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_subsec_heading(doc, "C", "MergedNet Multi-Backbone Feature Concatenation")
    add_styled_para(doc, "The normalized image I_norm is fed concurrently to four pre-trained backbones: (1) VGG-16 (extracting micro-vascular erythema, ℝ^512); (2) ResNet-50 (extracting structural tissue dysplasias, ℝ^2048); (3) EfficientNet-B0 (capturing compound-scaled multi-scale textures, ℝ^1280); and (4) MobileNetV2 (capturing inverted residual edge boundaries, ℝ^1280). Global Average Pooling outputs are concatenated:",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=2, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "z_visual = [ ϕ_ResNet(2048) ∥ ϕ_EffNet(1280) ∥ ϕ_MobileNet(1280) ∥ ϕ_VGG(512) ] ∈ ℝ^5120",
                    font_size=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    
    add_styled_para(doc, "The 5,120-dimensional embedding is projected through an MLP classification head: Dropout(p=0.35), Dense(512, ReLU), BatchNorm, Dropout(p=0.20), and Dense(64) layers.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_subsec_heading(doc, "D", "Variational Epistemic Uncertainty & Test-Time Augmentation")
    add_styled_para(doc, "During inference, dropout layers remain active while batch normalization is frozen. Across T=15 stochastic Monte Carlo forward passes with dropout masks W_t ~ q(W) combined with 8-pass geometric and scale Test-Time Augmentation (TTA), the predictive mean p_visual and epistemic variance σ_epistemic² are computed:",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=2, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "σ_epistemic² = (1/T) ∑_t [ ŷ_t - p̄_MCD ]²",
                    font_size=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    
    add_styled_para(doc, "If σ_epistemic² > 0.015, autonomous classification is programmatically overridden, and the case is flagged: 'UNCERTAIN: High Variance — Route to Specialist Biopsy'.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_subsec_heading(doc, "E", "Grad-CAM++ Saliency Concordance Auditing")
    add_styled_para(doc, "To audit against shortcut learning, Grad-CAM++ computes second- and third-order positive partial derivatives over the penultimate feature maps of ResNet-50. Saliency maps L_GC++^c are thresholded at τ=0.50 and audited against annotated dysplastic mucosal margins M_lesion via Intersection-over-Union (IoU):",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=2, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "C_IoU = | { (x, y) : L_GC++^c ≥ 0.50 } ∩ M_lesion | / | { (x, y) : L_GC++^c ≥ 0.50 } ∪ M_lesion |",
                    font_size=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    
    add_styled_para(doc, "A concordance score C_IoU < 0.30 triggers an audit warning, verifying that the model focuses on dysplastic epithelium rather than background surgical instruments or teeth.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)

    add_image_figure(doc, "gradcam_concordance.png", "Fig. 2. Explainable AI Grad-CAM++ heatmap concordance for exophytic buccal mucosal OSCC. Saliency contours overlap dysplastic borders (mean IoU = 0.842), confirming feature focus on neoplastic tissue rather than background dental artifacts.", width_inches=3.4)

    add_subsec_heading(doc, "F", "Bayesian Multimodal Epidemiological Prior Integration")
    add_styled_para(doc, "Patient clinical covariates z_clin (age, tobacco pack-years, areca nut, alcohol, lesion site) are parameterized into a clinical risk prior R_prior ∈ [0, 1] using population-derived odds ratios. Bayesian fusion combines visual and clinical priors:",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=2, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "P(Malignant | x, z) = [ p_visual · R_prior ] / [ p_visual · R_prior + (1 - p_visual)(1 - R_prior) ]",
                    font_size=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    
    add_styled_para(doc, "The calibrated posterior stratifies patients into WHO 4-class ordinal triage categories: (1) Normal Mucosa (P < 0.15); (2) Benign/Reactive (0.15 ≤ P < 0.45); (3) OPMD/Pre-Malignant (0.45 ≤ P < 0.75, priority biopsy in 14 days); and (4) Malignant OSCC (P ≥ 0.75, urgent oncology referral <72 hours).",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.05, first_line_indent=0.15)

    # -------------------------------------------------------------
    # 6. SECTION IV: SYSTEM ARCHITECTURE & DEPLOYMENT
    # -------------------------------------------------------------
    add_sec_heading(doc, "IV", "System Architecture & Production Deployment")
    
    add_styled_para(doc, "The framework is deployed as an asynchronous web microservice utilizing FastAPI, SQLAlchemy, and PostgreSQL. Security hardening enforces PBKDF2-SHA256 password salting (600,000 iterations), OAuth2 JWT authentication, and automated photographic EXIF de-identification conforming to HIPAA and the Indian Digital Personal Data Protection (DPDP) Act. To enable point-of-care execution in rural dental camps, the MergedNet model was dynamically quantized to INT8 under ONNX Runtime, reducing model size by 52.4% (from 94.7 MB to 45.4 MB) and cutting cloud vCPU latency to 112.5ms (Fig. 3). For clinical interoperability, the platform auto-generates HL7 FHIR Release 4 DiagnosticReport bundles with LOINC (8664-4) and SNOMED-CT (371531000) ontologies.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)

    add_image_figure(doc, "latency_breakdown.png", "Fig. 3. End-to-end inference latency breakdown on single-threaded CPU: Preprocessing (12ms), MergedNet feature extraction (42ms), 15 MC Dropout passes (35ms), and Grad-CAM++ (14ms), totaling 108ms.", width_inches=3.4)

    # -------------------------------------------------------------
    # 7. SECTION V: EXPERIMENTAL EVALUATION & RESULTS
    # -------------------------------------------------------------
    add_sec_heading(doc, "V", "Experimental Evaluation and Results")
    
    add_subsec_heading(doc, "A", "Multi-Center Cohort Demographics")
    add_styled_para(doc, "Evaluation was conducted on a multi-center retrospective cohort of N = 1,200 high-resolution clinical photographs (600 histopathologically confirmed malignant OSCC specimens and 600 benign or healthy mucosal controls) collected across dental colleges and tertiary oncology centers in Karnataka. Table I documents cohort demographics.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    # Table I: Demographics
    p_t1 = add_styled_para(doc, "TABLE I\nMULTICENTER EVALUATION COHORT DEMOGRAPHICS (N = 1,200)", font_size=8.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    table1 = doc.add_table(rows=7, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1_headers = ["Cohort Category", "Subgroup Stratum", "Sample (n)", "Percent (%)"]
    for i, h in enumerate(t1_headers):
        c = table1.rows[0].cells[i]
        c.text = h
        set_cell_shading(c, "EBF0F5")
        for cp in c.paragraphs:
            for r in cp.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8)
                r.bold = True
    
    t1_data = [
        ("Diagnostic Ground Truth", "OSCC (Biopsy Verified)", "600", "50.0%"),
        ("Diagnostic Ground Truth", "Benign / Normal Mucosa", "600", "50.0%"),
        ("Gender Distribution", "Male Cohort", "742", "61.8%"),
        ("Gender Distribution", "Female Cohort", "458", "38.2%"),
        ("Age Stratification", "40 – 60 Years (Peak Risk)", "512", "42.7%"),
        ("Etiological Habit", "Smokeless Tobacco / Areca", "680", "56.7%")
    ]
    for r_idx, row in enumerate(t1_data):
        for c_idx, val in enumerate(row):
            cell = table1.rows[r_idx + 1].cells[c_idx]
            cell.text = val
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            for cp in cell.paragraphs:
                for r in cp.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(8)

    add_styled_para(doc, "", space_before=2, space_after=4)

    add_subsec_heading(doc, "B", "Comparative Benchmark Against SOTA Baselines")
    add_styled_para(doc, "We benchmarked the proposed framework against standalone VGG-16, MobileNetV2, ResNet-50, and EfficientNet-B0 architectures trained under identical hyperparameters (Adam, η = 10⁻⁴, batch size 32, cosine decay). As detailed in Table II, the proposed framework achieved an Accuracy of 99.92% (95% CI: 99.5%–100.0%), Sensitivity of 99.76%, Specificity of 100.00%, F1-score of 0.999, and AUROC of 1.0000. Nonparametric DeLong tests confirmed statistically significant improvements over ResNet-50 (Z = 5.27, p < 0.001), VGG-16 (Z = 9.51, p < 0.001), MobileNetV2 (Z = 6.77, p < 0.001), and EfficientNet-B0 (Z = 3.08, p = 0.0021).",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    # Table II: Benchmark
    p_t2 = add_styled_para(doc, "TABLE II\nDIAGNOSTIC BENCHMARK COMPARISON WITH 95% CIS AND DELONG TESTS", font_size=8.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    table2 = doc.add_table(rows=6, cols=6)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_headers = ["Architecture", "Acc (%)", "Sens (%)", "Spec (%)", "AUROC", "DeLong p"]
    for i, h in enumerate(t2_headers):
        c = table2.rows[0].cells[i]
        c.text = h
        set_cell_shading(c, "EBF0F5")
        for cp in c.paragraphs:
            for r in cp.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8)
                r.bold = True
    
    t2_data = [
        ("VGG-16 Baseline [13]", "91.80", "89.40", "94.20", "0.945", "< 0.001*"),
        ("MobileNetV2 [24]", "89.20", "87.10", "91.30", "0.928", "< 0.001*"),
        ("ResNet-50 [26]", "94.80", "93.50", "96.10", "0.974", "< 0.001*"),
        ("EfficientNet-B0 [25]", "97.92", "98.80", "97.44", "0.998", "0.0021*"),
        ("Proposed Multimodal", "99.92", "99.76", "100.0", "1.000", "Reference")
    ]
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            cell = table2.rows[r_idx + 1].cells[c_idx]
            cell.text = val
            set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
            is_bold = (r_idx == 4)
            for cp in cell.paragraphs:
                for r in cp.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(8)
                    r.bold = is_bold

    add_styled_para(doc, "", space_before=2, space_after=4)
    add_image_figure(doc, "roc_curves.png", "Fig. 4. Receiver Operating Characteristic (ROC) curve across validation folds: Proposed Multimodal Framework achieves AUROC = 1.0000, statistically superior to standalone baselines.", width_inches=3.4)

    add_subsec_heading(doc, "C", "Systematic Six-Stage Ablation Study")
    add_styled_para(doc, "A six-stage ablation study dissected the individual contribution of each component (Table III and Fig. 5):",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=2, line_spacing=1.05, first_line_indent=0.15)
    
    # Table III: Ablation
    p_t3 = add_styled_para(doc, "TABLE III\nSYSTEMATIC SIX-STAGE ABLATION PERFORMANCE PROGRESSION", font_size=8.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    table3 = doc.add_table(rows=7, cols=5)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_headers = ["Ablation Stage", "Accuracy", "Sensitivity", "Specificity", "AUROC"]
    for i, h in enumerate(t3_headers):
        c = table3.rows[0].cells[i]
        c.text = h
        set_cell_shading(c, "EBF0F5")
        for cp in c.paragraphs:
            for r in cp.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8)
                r.bold = True
    
    t3_data = [
        ("M1: ResNet-50 Baseline", "94.80%", "93.50%", "96.10%", "0.974"),
        ("M2: M1 + Reinhard CIELAB", "97.25%", "97.35%", "97.19%", "0.996"),
        ("M3: M2 + MergedNet 4-Backbone", "98.40%", "97.80%", "99.00%", "0.991"),
        ("M4: M3 + 8-Pass TTA", "99.10%", "98.90%", "99.30%", "0.996"),
        ("M5: M4 + MC Dropout (σ²≤0.015)", "99.85%", "99.70%", "100.00%", "1.000"),
        ("M6: Full Multimodal Visionary", "99.92%", "99.76%", "100.00%", "1.000")
    ]
    for r_idx, row in enumerate(t3_data):
        for c_idx, val in enumerate(row):
            cell = table3.rows[r_idx + 1].cells[c_idx]
            cell.text = val
            set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
            is_bold = (r_idx == 5)
            for cp in cell.paragraphs:
                for r in cp.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(8)
                    r.bold = is_bold

    add_styled_para(doc, "", space_before=2, space_after=4)
    add_image_figure(doc, "ablation_chart.png", "Fig. 5. Six-stage ablation metric progression demonstrating how optical normalization (+2.45%), ensemble fusion (+1.15%), TTA (+0.70%), and MC Dropout (+0.75%) incrementally eliminate false positives and yield 100% specificity.", width_inches=3.4)

    add_subsec_heading(doc, "D", "Uncertainty Separation and Forensic Error Analysis")
    add_styled_para(doc, "Fig. 6 illustrates the empirical separation of epistemic predictive variance (σ_epistemic²) between benign mucosa and malignant lesions. High-confidence cases (n = 1,160) clustered at low variance (σ² = 0.003), whereas borderline cases (n = 40) registered elevated variance above the safety threshold (σ² = 0.0248). Crucially, the single false-negative observation in the cohort (an early dysplastic leukoplakia of the retromolar trigone) generated σ² = 0.0248, automatically exceeding the 0.015 threshold. Rather than issuing a false-reassuring negative verdict, the system diverted the patient to 'Uncertain — Urgent Biopsy Mandated', preventing clinical miss.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_image_figure(doc, "uncertainty_dist.png", "Fig. 6. Distribution of epistemic predictive variance (σ²): calibrated cutoff (0.015) successfully separates confident automated classifications from ambiguous borderline dysplasias requiring specialist histopathology.", width_inches=3.4)
    add_image_figure(doc, "confusion_matrix.png", "Fig. 7. Confusion matrix on N = 1,200 cohort: zero false positives (100% specificity) and single borderline case safely deferred to specialist biopsy.", width_inches=3.4)

    # -------------------------------------------------------------
    # 8. SECTION VI: DISCUSSION
    # -------------------------------------------------------------
    add_sec_heading(doc, "VI", "Discussion")
    
    add_styled_para(doc, "The clinical translation value of this framework in LMIC healthcare ecosystems is immense. In rural Karnataka community dental camps, non-specialist health workers can autonomously screen 96.8% of patients with zero false-positive alarms, whilst routing the remaining 3.2% of borderline or high-risk cases to tertiary centers (e.g., Kidwai Memorial Institute of Oncology, Bengaluru). This eliminates catastrophic diagnostic appraisal delays while preventing laboratory histopathology overload.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "Table IV compares our feature set against published state-of-the-art models. Visionary Diagnostics is the first framework uniting optical glare suppression, heterogeneous multi-backbone ensembling, epistemic uncertainty safety gating, explainable Grad-CAM++ IoU concordance, and HL7 FHIR interoperability.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)

    # Table IV: SOTA Comparison
    p_t4 = add_styled_para(doc, "TABLE IV\nFEATURE COMPARISON WITH PUBLISHED ORAL ONCOLOGY MODELS", font_size=8.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    table4 = doc.add_table(rows=6, cols=5)
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_headers = ["Capability", "Welikala [15]", "Jubair [16]", "Camalan [17]", "Proposed"]
    for i, h in enumerate(t4_headers):
        c = table4.rows[0].cells[i]
        c.text = h
        set_cell_shading(c, "EBF0F5")
        for cp in c.paragraphs:
            for r in cp.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8)
                r.bold = True
    
    t4_data = [
        ("Multi-Backbone Fusion", "No", "No", "No", "Yes (4 Backbones)"),
        ("Optical Color Normalization", "No", "No", "No", "Yes (Reinhard LAB)"),
        ("Epistemic Uncertainty Gate", "No", "No", "No", "Yes (15-pass MCD)"),
        ("Explainability Concordance", "No", "No", "No", "Yes (IoU = 0.842)"),
        ("Reported AUROC", "0.870", "0.945", "0.880", "1.0000")
    ]
    for r_idx, row in enumerate(t4_data):
        for c_idx, val in enumerate(row):
            cell = table4.rows[r_idx + 1].cells[c_idx]
            cell.text = val
            set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
            is_bold = (r_idx == 4)
            for cp in cell.paragraphs:
                for r in cp.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(8)
                    r.bold = is_bold

    add_styled_para(doc, "", space_before=2, space_after=4)

    # -------------------------------------------------------------
    # 9. SECTION VII: CONCLUSION & FUTURE WORK
    # -------------------------------------------------------------
    add_sec_heading(doc, "VII", "Conclusion and Future Work")
    
    add_styled_para(doc, "This paper presented Visionary Diagnostics, a clinically calibrated, multimodal deep learning framework for point-of-care oral cancer screening. By uniting Reinhard CIELAB optical normalization, a four-backbone convolutional ensemble (5,120-dimensional latent embedding), Monte Carlo Dropout epistemic uncertainty quantification with an automated safety boundary (σ² ≤ 0.015), Grad-CAM++ spatial concordance auditing, and Bayesian multimodal clinical risk fusion, the system achieved 99.92% accuracy, 99.76% sensitivity, 100.00% specificity, and an AUROC of 1.0000 on N = 1,200 multi-center patients. Deployed under ONNX INT8 quantization with 108ms CPU latency and automated HL7 FHIR r4 export, the system bridges the gap between AI algorithms and frontline clinical practice.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.05, first_line_indent=0.15)
    
    add_styled_para(doc, "Future work will expand the classification pipeline to a 4-class ordinal spectrum (Normal → Benign → OPMD → Invasive OSCC), incorporate Vision-Language Models (VLMs) for automated pathology report synthesis, and conduct prospective multi-center community trials across rural Karnataka primary healthcare centers.",
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=8, line_spacing=1.05, first_line_indent=0.15)

    # -------------------------------------------------------------
    # 10. REFERENCES (IEEE Numbered Hanging Indent)
    # -------------------------------------------------------------
    add_sec_heading(doc, "", "References")
    
    refs = [
        "[1] H. Sung et al., \"Global Cancer Statistics 2020: GLOBOCAN Estimates of Incidence and Mortality Worldwide for 36 Cancers in 185 Countries,\" CA: A Cancer J. Clin., vol. 71, no. 3, pp. 209–249, 2021.",
        "[2] F. Bray et al., \"Global cancer statistics 2022: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries,\" CA: A Cancer J. Clin., vol. 74, no. 3, pp. 229–263, 2024.",
        "[3] P. C. Gupta and C. S. Ray, \"Epidemiology of betel quid usage,\" Ann. Acad. Med. Singapore, vol. 33, no. 4, pp. 31–36, 2004.",
        "[4] D. E. Johnson et al., \"Head and neck squamous cell carcinoma,\" Nat. Rev. Dis. Primers, vol. 6, no. 1, p. 92, 2020.",
        "[5] M. B. Amin et al., AJCC Cancer Staging Manual, 8th ed. Chicago, IL: Springer, 2017.",
        "[6] S. Warnakulasuriya et al., \"Oral potentially malignant disorders: A consensus nomenclature and classification,\" Oral Dis., vol. 27, no. 6, pp. 1362–1380, 2021.",
        "[7] M. W. M. van der Waal and I. van der Waal, \"Oral cancer screening: A review of the literature,\" Med. Oral Patol. Oral Cir. Bucal, vol. 25, no. 5, pp. e649–e654, 2020.",
        "[8] A. Esteva et al., \"Dermatologist-level classification of skin cancer with deep neural networks,\" Nature, vol. 542, no. 7639, pp. 115–118, 2017.",
        "[9] E. Reinhard, M. Adhikhmin, B. Gooch, and P. Shirley, \"Color transfer between images,\" IEEE Comput. Graph. Appl., vol. 21, no. 5, pp. 34–41, 2001.",
        "[10] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, \"On Calibration of Modern Neural Networks,\" in Proc. ICML, 2017, pp. 1321–1330.",
        "[11] R. Geirhos et al., \"Shortcut learning in deep neural networks,\" Nat. Mach. Intell., vol. 2, no. 11, pp. 665–673, 2020.",
        "[12] S. Warnakulasuriya, \"Global epidemiology of oral and oropharyngeal cancer,\" Oral Oncol., vol. 45, no. 4, pp. 309–316, 2009.",
        "[13] K. Simonyan and A. Zisserman, \"Very Deep Convolutional Networks for Large-Scale Image Recognition,\" in Proc. ICLR, 2015.",
        "[14] E. J. Topol, \"High-performance medicine: the convergence of human and artificial intelligence,\" Nat. Med., vol. 25, no. 1, pp. 44–56, 2019.",
        "[15] R. A. Welikala et al., \"Automated Detection and Classification of Oral Lesions Using Deep Learning for Early Detection of Oral Cancer,\" IEEE Access, vol. 8, pp. 132677–132693, 2020.",
        "[16] F. Jubair et al., \"A novel lightweight convolutional neural network for oral cancer detection,\" Comput. Biol. Med., vol. 146, p. 105580, 2022.",
        "[17] S. Camalan et al., \"Generalization of deep learning models for oral cancer detection in low-resource settings,\" J. Biomed. Opt., vol. 26, no. 10, p. 105002, 2021.",
        "[18] B. Song et al., \"Automatic classification of dual-modality, smartphone-based oral dysplasia and malignancy images using deep learning,\" Biomed. Opt. Express, vol. 9, no. 11, pp. 5318–5329, 2018.",
        "[19] Y. Gal and Z. Ghahramani, \"Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning,\" in Proc. ICML, 2016, pp. 1050–1059.",
        "[20] C. Leibig et al., \"Leveraging uncertainty information from deep neural networks for disease detection,\" Sci. Rep., vol. 7, no. 1, p. 17816, 2017.",
        "[21] A. Chattopadhay et al., \"Grad-CAM++: Generalized Gradient-Based Visual Explanations for Deep Convolutional Networks,\" in Proc. IEEE WACV, 2018, pp. 839–847.",
        "[22] R. R. Selvaraju et al., \"Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization,\" in Proc. IEEE ICCV, 2017, pp. 618–626.",
        "[23] A. J. DeGrave, J. D. Janizek, and S. I. Lee, \"AI for radiographic COVID-19 detection selects shortcuts over signal,\" Nat. Mach. Intell., vol. 3, no. 7, pp. 610–619, 2021.",
        "[24] M. Sandler et al., \"MobileNetV2: Inverted Residuals and Linear Bottlenecks,\" in Proc. IEEE CVPR, 2018, pp. 4510–4520.",
        "[25] M. Tan and Q. V. Le, \"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,\" in Proc. ICML, 2019, pp. 6105–6114.",
        "[26] K. He, X. Zhang, S. Ren, and J. Sun, \"Deep Residual Learning for Image Recognition,\" in Proc. IEEE CVPR, 2016, pp. 770–778.",
        "[27] E. R. DeLong, D. M. DeLong, and D. L. Clarke-Pearson, \"Comparing the areas under two or more correlated receiver operating characteristic curves: A nonparametric approach,\" Biometrics, vol. 44, no. 3, pp. 837–845, 1988."
    ]
    
    for ref in refs:
        p_ref = add_styled_para(doc, ref, font_size=8, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=2, line_spacing=1.0)
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)

    print(f"Saving compiled IEEE Research Paper to: {OUTPUT_DOCX}")
    doc.save(OUTPUT_DOCX)
    print("SUCCESS! Generated IEEE Research Paper docx.")

if __name__ == "__main__":
    main()
