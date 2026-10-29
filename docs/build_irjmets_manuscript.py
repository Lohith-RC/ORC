"""
Script to generate the complete, production-grade IRJMETS research manuscript for:
'MergedNet: Architecture, Inference Pipeline, and Repository Data Audit of a Multi-Backbone Oral Image Classification Prototype'

Formatting matches IRJMETS standards and Career_Navigator_IRJMETS.docx visual hierarchy:
- A4 size, 210mm x 297mm
- Margins: Left 0.83 in, Right 0.83 in, Top 1.28 in, Bottom 0.5 in
- Single-column layout, line spacing 1.15
- Fonts: Cambria (Title 14pt bold, Headings 12pt bold all-caps centered, Subheadings 10pt bold, Body 10pt justified)
- Verified dataset, MergedNet architecture, software demarcation, audit findings, synthetic simulation disclosure, conditional roadmap.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_manuscript():
    template_path = os.path.abspath('docs/IRJMETSTemplate_official.docx')
    output_docx = os.path.abspath('docs/ORAL_CANCER_IRJMETS_MANUSCRIPT.docx')
    output_pdf = os.path.abspath('docs/ORAL_CANCER_IRJMETS_MANUSCRIPT.pdf')

    if os.path.exists(template_path):
        print(f"Loading official base template from: {template_path}")
        doc = docx.Document(template_path)
        # Clear body paragraphs and tables while preserving sectPr
        for child in list(doc._body._element):
            if child.tag.endswith('sectPr'):
                continue
            doc._body._element.remove(child)
    else:
        print("Creating fresh document...")
        doc = docx.Document()
        section = doc.sections[0]
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.left_margin = Inches(0.83)
        section.right_margin = Inches(0.83)
        section.top_margin = Inches(1.28)
        section.bottom_margin = Inches(0.5)

    section = doc.sections[0]
    
    # -------------------------------------------------------------
    # HEADER SETUP (Clean metadata - no fake Volume/Issue)
    # -------------------------------------------------------------
    header = section.header
    # Clear existing header paragraphs
    for p in list(header.paragraphs):
        p._p.getparent().remove(p._p)
    
    # Line 1: ISSN right-aligned
    p_h1 = header.add_paragraph()
    p_h1.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    p_h1.paragraph_format.space_after = Pt(1)
    p_h1.paragraph_format.space_before = Pt(0)
    r = p_h1.add_run("e-ISSN: 2582-5208")
    r.font.name = "Cambria"
    r.font.size = Pt(9)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Line 2: Journal Name Centered
    p_h2 = header.add_paragraph()
    p_h2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_h2.paragraph_format.space_after = Pt(1)
    p_h2.paragraph_format.space_before = Pt(0)
    r = p_h2.add_run("International Research Journal of Modernization in Engineering Technology and Science")
    r.font.name = "Cambria"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1A, 0x47, 0x2A) # Forest dark green

    # Line 3: Peer-Reviewed tagline
    p_h3 = header.add_paragraph()
    p_h3.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_h3.paragraph_format.space_after = Pt(2)
    p_h3.paragraph_format.space_before = Pt(0)
    r = p_h3.add_run("( Peer-Reviewed, Open Access, Fully Refereed International Journal )")
    r.font.name = "Cambria"
    r.font.size = Pt(8.5)
    r.font.italic = True
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Line 4: Submission metadata (no fake published volume/issue)
    p_h4 = header.add_paragraph()
    p_h4.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_h4.paragraph_format.space_after = Pt(4)
    p_h4.paragraph_format.space_before = Pt(0)
    r1 = p_h4.add_run("[Manuscript Draft for Peer Review]               ")
    r1.font.name = "Cambria"
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r2 = p_h4.add_run("Impact Factor- 8.187")
    r2.font.name = "Cambria"
    r2.font.size = Pt(8.5)
    r2.font.bold = True
    r3 = p_h4.add_run("                              www.irjmets.com")
    r3.font.name = "Cambria"
    r3.font.size = Pt(8.5)
    r3.font.bold = True

    # -------------------------------------------------------------
    # FOOTER SETUP (Website banner + Dynamic Page Number)
    # -------------------------------------------------------------
    footer = section.footer
    for p in list(footer.paragraphs):
        p._p.getparent().remove(p._p)

    # Line 1: Green journal footer with top border
    p_f1 = footer.add_paragraph()
    p_f1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_f1.paragraph_format.space_before = Pt(2)
    p_f1.paragraph_format.space_after = Pt(1)
    
    # Add top border to footer paragraph XML
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="2" w:color="00B050"/></w:pBdr>')
    p_f1._p.get_or_add_pPr().append(pBdr)

    r_f1 = p_f1.add_run("www.irjmets.com")
    r_f1.font.name = "Cambria"
    r_f1.font.size = Pt(9)
    r_f1.font.bold = True
    r_f1.font.color.rgb = RGBColor(0x00, 0x40, 0x80)

    r_f2 = p_f1.add_run("          @International Research Journal of Modernization in Engineering, Technology and Science")
    r_f2.font.name = "Cambria"
    r_f2.font.size = Pt(9)
    r_f2.font.bold = True
    r_f2.font.color.rgb = RGBColor(0x00, 0xA8, 0x4C)

    # Line 2: Dynamic Page Numbering [ Page ]
    p_f2 = footer.add_paragraph()
    p_f2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_f2.paragraph_format.space_before = Pt(0)
    p_f2.paragraph_format.space_after = Pt(0)

    r_pg1 = p_f2.add_run(" [ ")
    r_pg1.font.name = "Cambria"
    r_pg1.font.size = Pt(9.5)
    r_pg1.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Add dynamic PAGE field
    fldSimple = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
    p_f2._p.append(fldSimple)

    r_pg2 = p_f2.add_run(" ]")
    r_pg2.font.name = "Cambria"
    r_pg2.font.size = Pt(9.5)
    r_pg2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # -------------------------------------------------------------
    # HELPER FUNCTIONS FOR CONTENT
    # -------------------------------------------------------------
    def add_p(text, align=WD_PARAGRAPH_ALIGNMENT.JUSTIFY, space_before=0, space_after=3, line_spacing=1.15, bold=False, italic=False, size=10):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.font.name = "Cambria"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        return p

    def add_h1(title, page_break_before=False):
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        if page_break_before:
            p.paragraph_format.page_break_before = True
        run = p.add_run(title)
        run.font.name = "Cambria"
        run.font.size = Pt(12)
        run.font.bold = True
        return p

    def add_h2(title):
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.name = "Cambria"
        run.font.size = Pt(10)
        run.font.bold = True
        return p

    def add_h3(title):
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.name = "Cambria"
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.italic = True
        return p

    def set_table_properties(table, col_widths=None):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="666666"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="666666"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                <w:insideV w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            </w:tblBorders>
        ''')
        tblPr.append(tblBorders)

        # Repeat header row on every page
        trPr = table.rows[0]._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        # Prevent all rows from splitting across pages
        for row in table.rows:
            row_trPr = row._tr.get_or_add_trPr()
            row_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        # Explicit column widths across all rows
        if col_widths:
            for row in table.rows:
                for j, w in enumerate(col_widths):
                    row.cells[j].width = Inches(w)

    def set_cell(cell, text, bold=False, italic=False, size=9.5, align=WD_PARAGRAPH_ALIGNMENT.LEFT, bg_color=None, width=None):
        if width:
            cell.width = Inches(width)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = align
        p.paragraph_format.space_before = Pt(2.5)
        p.paragraph_format.space_after = Pt(2.5)
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
    # 1. PAPER TITLE
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.line_spacing = 1.15
    run_title = p_title.add_run("MergedNet: Software Architecture, Inference Pipeline, and Repository Data Audit of a Multi-Backbone Oral Image Classification Prototype")
    run_title.font.name = "Cambria"
    run_title.font.size = Pt(14)
    run_title.font.bold = True

    # -------------------------------------------------------------
    # 2. AUTHORS & AFFILIATIONS
    # -------------------------------------------------------------
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_auth.paragraph_format.space_before = Pt(2)
    p_auth.paragraph_format.space_after = Pt(2)
    p_auth.paragraph_format.line_spacing = 1.15
    r_auth = p_auth.add_run("Rakshith Y B*1, Lohith R C*2, Keerthi A*3")
    r_auth.font.name = "Cambria"
    r_auth.font.size = Pt(12)
    r_auth.font.bold = True

    # Note on provisional author sequence
    p_order = doc.add_paragraph()
    p_order.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_order.paragraph_format.space_before = Pt(0)
    p_order.paragraph_format.space_after = Pt(2)
    r_order = p_order.add_run("*(Student Author Order is Provisional and Subject to Final Team and Project Guide Confirmation)*")
    r_order.font.name = "Cambria"
    r_order.font.size = Pt(9.5)
    r_order.font.italic = True
    r_order.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # Affiliations
    p_aff1 = doc.add_paragraph()
    p_aff1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_aff1.paragraph_format.space_before = Pt(0)
    p_aff1.paragraph_format.space_after = Pt(1)
    r_aff1 = p_aff1.add_run("*1,2,3 Department of Computer Science & Engineering, Kalpataru Institute of Technology, Tiptur, Karnataka, India")
    r_aff1.font.name = "Cambria"
    r_aff1.font.size = Pt(10.5)

    p_aff2 = doc.add_paragraph()
    p_aff2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_aff2.paragraph_format.space_before = Pt(0)
    p_aff2.paragraph_format.space_after = Pt(3)
    r_aff2 = p_aff2.add_run("Affiliated with Visvesvaraya Technological University (VTU), Belagavi, Karnataka, India")
    r_aff2.font.name = "Cambria"
    r_aff2.font.size = Pt(10)
    r_aff2.font.italic = True

    # Project Guide Designation (Identified Separately as required)
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_guide.paragraph_format.space_before = Pt(2)
    p_guide.paragraph_format.space_after = Pt(8)
    r_guide1 = p_guide.add_run("Project Guide: ")
    r_guide1.font.name = "Cambria"
    r_guide1.font.size = Pt(10)
    r_guide1.font.bold = True
    r_guide2 = p_guide.add_run("Prof. Aishwarya S, Assistant Professor, Department of Computer Science & Engineering, Kalpataru Institute of Technology, Tiptur, Karnataka, India\n")
    r_guide2.font.name = "Cambria"
    r_guide2.font.size = Pt(10)
    r_guide3 = p_guide.add_run("*(Project guidance role identified separately; co-authorship designation subject to confirmation by guide and department)*")
    r_guide3.font.name = "Cambria"
    r_guide3.font.size = Pt(9)
    r_guide3.font.italic = True
    r_guide3.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # -------------------------------------------------------------
    # 3. ABSTRACT (< 250 words)
    # -------------------------------------------------------------
    add_h1("ABSTRACT")
    add_p(
        "This paper describes the software engineering design, inference pipeline, and repository data audit of an exploratory, "
        "non-diagnostic prototype for binary oral image classification. The core deep learning engine, MergedNet, combines pooled visual "
        "features from four heterogeneous convolutional backbones—VGG-16, ResNet-50, EfficientNet-B0, and MobileNetV2—into a unified "
        "5,120-dimensional concatenated latent vector fed into a fully connected classification head. The system is deployed via an "
        "asynchronous FastAPI backend and a React single-page frontend incorporating client-side blur screening and anatomical tagging. "
        "Inference routines incorporate Test-Time Augmentation (TTA) and Monte Carlo Dropout (MCD) for runtime uncertainty gating. "
        "A rigorous cryptographic SHA-256 hash audit of the repository dataset (940 total JPEG images: 490 cancer, 450 non-cancer across "
        "655 train, 143 validation, and 142 test splits) identified 21 exact duplicate image groups encompassing 46 files (25 redundant copies), "
        "with 11 duplicate groups encompassing 25 files (14 redundant copies) crossing data partitions. This cross-partition leakage precludes "
        "the current test partition from being considered a statistically valid or independent evaluation set. Furthermore, patient identifiers, "
        "dataset source provenance, data licensing terms, training logs, and Institutional Review Board (IRB) ethics records were not found "
        "in the codebase. Previously reported benchmark results, including a 99.92% accuracy figure, were generated by synthetic numerical "
        "simulation scripts rather than empirical testing on images. Genuine empirical model metrics are currently unavailable. The prototype "
        "is strictly non-diagnostic, lacks regulatory clearance, and is not clinically validated. A phased remediation roadmap is outlined."
    )

    # Keywords
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(3)
    p_kw.paragraph_format.space_after = Pt(10)
    p_kw.paragraph_format.line_spacing = 1.15
    r_kw_h = p_kw.add_run("Keywords: ")
    r_kw_h.font.name = "Cambria"
    r_kw_h.font.size = Pt(10)
    r_kw_h.font.bold = True
    r_kw_b = p_kw.add_run("Oral Image Classification, Deep Learning, Feature Fusion, Uncertainty Estimation, Software Engineering, Medical Image Audit.")
    r_kw_b.font.name = "Cambria"
    r_kw_b.font.size = Pt(10)

    # -------------------------------------------------------------
    # 4. SECTION I: INTRODUCTION
    # -------------------------------------------------------------
    add_h1("I.  INTRODUCTION")
    add_p(
        "Oral cancer, primarily manifesting as oral squamous cell carcinoma (OSCC), represents a severe global public health burden. "
        "According to GLOBOCAN 2020 statistics published by the International Agency for Research on Cancer, cancers of the lip and oral cavity "
        "accounted for an estimated 377,713 new cases and 177,757 deaths globally in 2020 [1]. India bears a disproportionate share of this disease burden, "
        "recording over 135,000 new diagnoses annually—nearly one-third of global cases—largely driven by regional behavioral risk factors including the "
        "widespread consumption of chewed tobacco, areca nut, and betel quid formulations. Despite advancements in surgical techniques, radiation protocols, "
        "and systemic chemotherapies, the long-term five-year survival rate for late-stage oral malignancies remains stagnant at approximately 50%. "
        "In contrast, early-stage detection (Stage I and II) elevates five-year survival to greater than 80%, underscoring the vital importance of accessible screening."
    )
    add_p(
        "Conventional oral examination (COE) using visual inspection and digital palpation under incandescent white light remains the primary frontline screening modality. "
        "However, a comprehensive Cochrane systematic review by Brocklehurst et al. [2] concluded that while screening targeted high-risk individuals (such as chronic tobacco and alcohol consumers) "
        "yields measurable mortality reductions, evidence to support opportunistic mass population screening in low-risk cohorts remains insufficient due to variable clinical sensitivity, "
        "subjective visual diagnostic criteria, and substantial inter-examiner discordance between general dental practitioners and specialist oral oncologists."
    )
    add_p(
        "To explore computational tools that could assist frontline personnel in capturing, organizing, and preliminary reviewing photographic images, "
        "automated visual screening using computer vision and deep learning has emerged as an active area of investigation [3], [4]. In this paper, "
        "the term 'decision-support prototype' is defined strictly as an exploratory, academic software application designed to assist non-specialist users "
        "in capturing, standardizing, and viewing oral cavity photographs. We emphasize that this prototype is fundamentally not an autonomous diagnostic medical device. "
        "Repository system specifications and design guidelines explicitly declare that the application cannot perform clinical diagnosis and is not a substitute "
        "for scalpel biopsy, histopathological examination, or evaluation by certified oral and maxillofacial pathologists."
    )
    add_p(
        "A central design hypothesis in deep learning-based image analysis is feature fusion across heterogeneous convolutional neural network (CNN) architectures. "
        "Individual CNN topologies incorporate distinct inductive biases, receptive fields, and feature hierarchies: deep architectures with fixed 3×3 convolutions (such as VGG-16) "
        "capture fine-grained textural cues [5]; residual architectures (such as ResNet-50) mitigate vanishing gradients through identity shortcut connections [6]; "
        "and parameter-efficient networks (such as MobileNetV2 and EfficientNet-B0) optimize mobile efficiency through depthwise separable inverted bottlenecks [7] "
        "and compound dimensional scaling [8]. Combining latent visual embeddings extracted simultaneously across these diverse backbones—termed multi-backbone feature fusion—aims "
        "to supply downstream classification layers with a comprehensive representation spanning multiscale spatial abstractions."
    )
    add_p(
        "However, transitioning such exploratory engineering concepts into rigorous academic literature requires confronting several critical implementation challenges:\n"
        "1) Predictive Uncertainty Quantification: Standard deterministic neural networks produce point estimates that do not reflect epistemic model confidence, "
        "introducing safety hazards if ambiguous or out-of-distribution inputs are classified with artificially high confidence [9], [10].\n"
        "2) Photographic Input Quality: Consumer mobile camera optics frequently introduce motion blur, specular saliva reflections, and severe chromatic drift, "
        "necessitating automated preprocessing gates.\n"
        "3) Scientific Integrity and Data Rigor: Rigorous peer-reviewed science mandates a strict demarcation between verified code, real empirical test results, "
        "and synthetic simulation scripts. Data leakage, such as duplicate images crossing dataset partitions, severely undermines scientific validity [11], [12]."
    )
    add_p(
        "Objectives of this Paper: Rather than asserting unverified diagnostic performance claims, this paper presents an evidence-based system description and repository audit "
        "of the oral image classification capstone prototype. The specific objectives are:\n"
        "• To document the complete architecture of MergedNet, a multi-backbone feature fusion model implemented in PyTorch that combines embeddings from VGG-16 [5], "
        "ResNet-50 [6], EfficientNet-B0 [8], and MobileNetV2 [7] into a 5,120-dimensional feature vector.\n"
        "• To detail the software engineering implementation connecting an asynchronous FastAPI backend to a React single-page frontend.\n"
        "• To evaluate the inference-time uncertainty estimation pipeline (Test-Time Augmentation and Monte Carlo Dropout) and contrast PyTorch vs. ONNX Runtime execution paths.\n"
        "• To transparently disclose repository data limitations identified during an exhaustive audit, including 21 duplicate image groups encompassing 46 files (11 cross-partition groups "
        "encompassing 25 files), the absence of patient identifiers, missing reproducible training code, and the presence of synthetic benchmark generation scripts.\n"
        "• To articulate a phased conditional research roadmap outlining the technical remediation required before valid empirical performance claims can be established."
    )

    # -------------------------------------------------------------
    # 5. SECTION II: RELATED WORK (Clean page break to avoid orphan heading)
    # -------------------------------------------------------------
    add_h1("II.  RELATED WORK", page_break_before=True)
    add_p(
        "Developing computational decision-support prototypes for oral cavity photograph analysis draws upon prior literature across deep learning, "
        "multi-model feature fusion, uncertainty estimation, and biomedical machine learning methodology."
    )
    add_h2("A. Prior Deep Learning Studies in Oral Lesion Imaging")
    add_p(
        "Automated classification of photographic oral lesions has been explored across several institutional datasets. Welikala et al. [3] evaluated "
        "deep learning architectures, including ResNet-50 and Faster R-CNN, on their own curated clinical photographic dataset to classify oral mucosal lesions "
        "into suspicious and non-suspicious categories. Similarly, Warin et al. [4] investigated CNN architectures (VGG-16, ResNet-50, and DenseNet-121) on an "
        "institutional dataset of 980 clinical photographs (comprising 365 OSCC, 315 oral potentially malignant disorders [OPMD], and 300 normal controls), "
        "reporting classification performance specific to their curated cohort. While these studies illustrate the mathematical feasibility of training CNNs "
        "on photographic lesion collections, they represent evaluations conducted strictly on their own closed institutional cohorts; findings from prior research "
        "cannot be generalized or transferred to the unverified repository dataset or prototype investigated in this work."
    )
    add_h2("B. Multi-Backbone Feature Fusion Architectures")
    add_p(
        "In deep computer vision, feature fusion refers to combining feature maps or latent vectors from multiple layers or heterogeneous backbones. "
        "In MergedNet, feature fusion refers specifically to the intermediate concatenation of global average pooled vectors from four convolutional networks: "
        "VGG-16 [5], ResNet-50 [6], EfficientNet-B0 [8], and MobileNetV2 [7]. By concatenating 512-d, 2,048-d, 1,280-d, and 1,280-d pooled representations, "
        "the downstream fully connected classification head receives a composite 5,120-dimensional descriptor containing features derived from different convolutional topologies."
    )
    add_h2("C. Predictive Uncertainty Estimation in Deep Learning")
    add_p(
        "Standard deterministic deep neural networks trained with cross-entropy loss are notorious for producing uncalibrated, overconfident predictions [9]. "
        "Predictive uncertainty is broadly categorized into two forms [9], [10]:\n"
        "1) Epistemic (Model) Uncertainty: Reflects uncertainty in network weight parameters arising from limited training data. Gal and Ghahramani [9] developed "
        "Monte Carlo Dropout (MCD) as a mathematically grounded variational Bayesian approximation of deep Gaussian processes. By retaining dropout stochasticity "
        "at test time across multiple forward passes, the predictive variance provides a tractable estimate of epistemic model uncertainty.\n"
        "2) Aleatoric (Data) Uncertainty: Reflects observation noise, lighting variations, or optical artifacts inherent in photographic acquisition. "
        "Ayhan and Berens [10] established that Test-Time Augmentation (TTA)—evaluating prediction dispersion across label-preserving geometric and optical transforms—provides "
        "an empirical proxy for input-dependent aleatoric uncertainty.\n"
        "In the prototype investigated here, both MCD and TTA are implemented in code; however, neither mechanism has undergone empirical calibration or clinical validation on oral imagery."
    )
    add_h2("D. Dataset Integrity, Partition Leakage, and Reproducibility Pitfalls")
    add_p(
        "Methodological surveys in applied machine learning have exposed widespread reproducibility vulnerabilities that compromise published findings [11], [12]. "
        "In a landmark survey analyzing reproducibility across 17 quantitative fields, Kapoor and Narayanan [12] introduced an eight-part taxonomy of data leakage, "
        "demonstrating that data leakage is pervasive and consistently produces artificially inflated performance claims. Similarly, in a critical review of deep learning "
        "models developed for COVID-19 medical imaging, Roberts et al. [11] reviewed 415 published studies and discovered that none were clinically usable due to severe methodological flaws, "
        "primarily duplicate image contamination across splits, lack of patient-level data separation, and unverified dataset provenance. These findings highlight "
        "that rigorous data auditing must precede any credible claim of machine learning performance."
    )

    # -------------------------------------------------------------
    # 6. SECTION III: METHODS AND SYSTEM DESIGN (Clean page break)
    # -------------------------------------------------------------
    add_h1("III.  METHODS AND SYSTEM DESIGN", page_break_before=True)
    add_p(
        "This section documents the verified system architecture, repository dataset inspection findings, MergedNet feature fusion engine, and uncertainty estimation pipelines."
    )
    add_h2("A. System Architecture Overview")
    add_p(
        "The software prototype is engineered as a decoupled client-server web application comprising three principal tiers:\n"
        "• Client Presentation Tier: A responsive single-page application built in React.js, providing an interface for capturing oral photographs, "
        "performing client-side blur screening via HTML5 canvas, designating anatomical lesion sites via an interactive SVG oral cavity map, and reviewing model prediction flags.\n"
        "• Application Service Tier: A high-performance asynchronous web service built with FastAPI and Python 3.10+, managing file ingestion boundaries, "
        "MIME-type filtering, optical standardization, and inference dispatching.\n"
        "• Deep Learning Inference Engine: Orchestrates model forward passes using native PyTorch on GPU/CPU or an optimized ONNX Runtime execution engine."
    )

    # Insert Architecture Diagram if exists
    arch_img_path = os.path.abspath('docs/figures/architecture.png')
    if os.path.exists(arch_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(arch_img_path, width=Inches(6.2))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        p_cap.paragraph_format.line_spacing = 1.05
        p_cap.paragraph_format.keep_with_next = True
        r_c1 = p_cap.add_run("Figure 1: ")
        r_c1.font.name = "Cambria"
        r_c1.font.size = Pt(9.5)
        r_c1.font.bold = True
        r_c2 = p_cap.add_run("End-to-End System Architecture of the Oral Image Classification Prototype (Client, Backend, Inference Engine, and Auxiliary Tiers).")
        r_c2.font.name = "Cambria"
        r_c2.font.size = Pt(9.5)

    add_h2("B. Dataset Characteristics and Verified Repository Audit Findings")
    add_p(
        "The repository dataset resides in local directory partitions formatted for standard image classification. An exhaustive factual audit reveals the following verified characteristics:"
    )
    add_p(
        "1) Verified Image Partition Counts: The dataset comprises exactly 940 JPEG images organized into binary classification classes (cancer vs. non-cancer). "
        "Table 1 details the exact image counts across directory partitions."
    )

    # TABLE 1: Dataset Partition Counts
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_t1.paragraph_format.space_before = Pt(6)
    p_t1.paragraph_format.space_after = Pt(2)
    p_t1.paragraph_format.keep_with_next = True
    r_t1_h = p_t1.add_run("Table 1. ")
    r_t1_h.font.name = "Cambria"
    r_t1_h.font.size = Pt(9.5)
    r_t1_h.font.bold = True
    r_t1_t = p_t1.add_run("Verified Repository Image Partition Counts and Duplicate Hash Distribution")
    r_t1_t.font.name = "Cambria"
    r_t1_t.font.size = Pt(9.5)

    t1_widths = [1.5, 0.9, 1.0, 0.9, 2.3] # Total = 6.6 in
    t1 = doc.add_table(rows=5, cols=5)
    set_table_properties(t1, t1_widths)

    t1_headers = ["Partition Split", "Cancer Class", "Non-Cancer Class", "Split Total", "Partition Integrity Status"]
    for j, h in enumerate(t1_headers):
        set_cell(t1.rows[0].cells[j], h, bold=True, size=9, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t1_widths[j])

    t1_data = [
        ["Training Split (`train`)", "341", "314", "655", "Contains internal duplicates & overlaps with test"],
        ["Validation Split (`val`)", "75", "68", "143", "Contains files identical to train/test partitions"],
        ["Testing Split (`test`)", "74", "68", "142", "Contaminated: 11 groups (25 files) cross into test"],
        ["Total Image Collection", "490 (52.1%)", "450 (47.9%)", "940 (100%)", "21 duplicate groups (46 files; 25 redundant copies)"]
    ]

    for i, row in enumerate(t1_data):
        bg = "FAFAFA" if i % 2 == 1 else "FFFFFF"
        bold = (i == 3)
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.CENTER if j in [1, 2, 3] else WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t1.rows[i+1].cells[j], val, bold=bold, size=9, align=align, bg_color=bg, width=t1_widths[j])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_p(
        "2) Duplicate Images and Cross-Partition Leakage: An automated cryptographic SHA-256 hash audit performed across all 940 image files identified "
        "21 exact duplicate groups encompassing 46 individual files (representing 25 redundant copies across 21 unique images). More critically, "
        "11 of these duplicate groups—encompassing 25 individual files (representing 14 redundant copies)—cross dataset partition boundaries, appearing simultaneously "
        "in both training and test folders. Because identical images exist across the training and testing sets, evaluating any model trained on the training partition "
        "against the current test partition would test memorization rather than generalization [11], [12]. Consequently, the current test partition cannot be described "
        "as an independent or statistically valid test set.\n"
        "3) Absence of Patient-Level Identifiers: The repository dataset contains no patient identification numbers, clinical case IDs, or demographic linkage keys. "
        "It is impossible to verify whether multiple photographs originated from the same individual across partitions. In medical image analysis, random splitting "
        "without patient-level grouping is a documented source of inflated performance, as networks learn patient-specific background features (dentition, mucosal pigmentation) "
        "rather than pathology [11].\n"
        "4) Unverified Provenance and Licensing: While repository comments describe the images as originating from Kaggle, the exact source URL, original uploader, "
        "participating clinical centers, image acquisition hardware, and license terms were not found in the codebase. The dataset cannot be classified as verified public, "
        "clinical, or multi-center data.\n"
        "5) Absence of Ethics Governance Records: No Institutional Review Board (IRB) approval records, human subjects protocol numbers, or patient informed consent forms "
        "exist in the repository. While clearance may exist externally, no documentation is present in the codebase."
    )

    add_h2("C. The MergedNet Feature Fusion Architecture")
    add_p(
        "The primary neural network model implemented in `app/services/ml_engine.py` is MergedNet, a PyTorch `nn.Module` configured for binary classification "
        "('cancer' vs. 'non_cancer'). MergedNet combines convolutional feature representations extracted concurrently from four distinct pre-trained backbones [5]–[8]:"
    )
    add_p(
        "1) VGG-16 Backbone: Utilizes the convolutional blocks of VGG-16 (configuration 'D', comprising 13 convolutional layers across five pooling stages) [5]. "
        "The standard fully connected layers are discarded. Penultimate spatial activations are processed through an AdaptiveAvgPool2d(7, 7) stage followed by "
        "an AdaptiveAvgPool2d(1, 1) global average pooling operation, generating a 512-dimensional vector $\\mathbf{v}_{\\text{vgg}} \\in \\mathbb{R}^{512}$.\n"
        "2) ResNet-50 Backbone: Employs the deep residual feature extractor [6], truncated before the final pooling and classification layers (`list(children())[:-2]`). "
        "Global adaptive average pooling (1×1) reduces the residual bottleneck activations to a 2,048-dimensional vector $\\mathbf{v}_{\\text{res}} \\in \\mathbb{R}^{2048}$.\n"
        "3) EfficientNet-B0 Backbone: Utilizes mobile inverted bottleneck convolutional blocks (`features`) scaled via compound depth, width, and resolution scaling [8]. "
        "Global average pooling (1×1) produces a 1,280-dimensional vector $\\mathbf{v}_{\\text{eff}} \\in \\mathbb{R}^{1280}$.\n"
        "4) MobileNetV2 Backbone: Incorporates depthwise separable convolutions with inverted residuals and linear bottlenecks [7]. "
        "Global average pooling (1×1) yields a 1,280-dimensional vector $\\mathbf{v}_{\\text{mob}} \\in \\mathbb{R}^{1280}$."
    )
    add_p(
        "Feature Concatenation and Classification Head: The four pooled feature vectors are flattened and concatenated along the channel dimension into a unified representation $\\mathbf{z}$:\n"
        "$$\\mathbf{z} = [\\mathbf{v}_{\\text{vgg}}^\\top, \\mathbf{v}_{\\text{res}}^\\top, \\mathbf{v}_{\\text{eff}}^\\top, \\mathbf{v}_{\\text{mob}}^\\top]^\\top \\in \\mathbb{R}^{5120}$$\n"
        "where $\\text{dim}(\\mathbf{z}) = 512 + 2048 + 1280 + 1280 = 5,120$ dimensions. This concatenated latent representation is processed by a fully connected classification head:\n"
        "• Dropout Regularization 1: $p = 0.5$, mitigating co-adaptation among fused latent features.\n"
        "• Fully Connected Hidden Layer: Linear projection $\\mathbf{W}_1 \\in \\mathbb{R}^{512 \\times 5120}$ mapping 5,120 dimensions to 512 hidden units, followed by Rectified Linear Unit ($\\text{ReLU}$) activation.\n"
        "• Dropout Regularization 2: $p = 0.3$.\n"
        "• Output Classification Layer: Linear projection $\\mathbf{W}_2 \\in \\mathbb{R}^{2 \\times 512}$ producing 2 unnormalized logits corresponding to binary class scores.\n"
        "Pre-Training Status Note: In `ml_engine.py`, backbones are instantiated with `weights=None` before state dictionaries are loaded from `merged_model.pth`. "
        "Whether backbones were initialized from ImageNet pre-training or random initialization during original training is unverified."
    )

    add_h2("D. Uncertainty Estimation and Inference Pipelines")
    add_p(
        "The codebase contains inference routines designed to quantify predictive dispersion. Code inspection reveals two distinct execution paths:"
    )
    add_p(
        "1) Native PyTorch Pipeline (TTA + Monte Carlo Dropout): When executing through PyTorch, the function `run_inference_pipeline` implements an ensemble-at-inference approach:\n"
        "• Test-Time Augmentation (TTA): Generates eight augmented transformations per input image (horizontal flip, vertical flip, $+15^\\circ$ rotation, $-15^\\circ$ rotation, "
        "brightness adjustment, contrast jitter, grayscale conversion, and baseline standardized input) [10]. Averaged softmax outputs produce mean probability vector $\\bar{P}_{\\text{TTA}}$.\n"
        "• Monte Carlo Dropout (MCD): The helper function `_enable_dropout_only` forces dropout layers to training mode (`m.train()`) while keeping batch normalization in evaluation mode [9]. "
        "Inference executes across $N = 15$ stochastic forward passes, computing predictive mean $\\bar{P}_{\\text{MCD}}$ and predictive variance $\\sigma^2_{\\text{MCD}}$.\n"
        "• Ensemble Fusion and Safety Gating: Final probability is computed as an unweighted average: $P_{\\text{final}} = 0.5 \\bar{P}_{\\text{TTA}} + 0.5 \\bar{P}_{\\text{MCD}}$. "
        "Epistemic uncertainty is defined as maximum variance across classes: $U = \\max(\\sigma^2_{\\text{MCD}})$. If $U > \\tau$ (configured to $\\tau = 0.015$), "
        "the returned class is overridden to 'uncertain', and a specialist referral advisory is rendered.\n"
        "2) ONNX Runtime Pipeline: For resource-constrained CPU environments, the backend includes an ONNX runtime path (`merged_model_int8.onnx`). "
        "However, because exported ONNX graphs treat dropout operations as static identity layers during inference, Monte Carlo Dropout is not executed in the ONNX path. "
        "Instead, prediction variance is calculated across three TTA passes (original, horizontal flip, vertical flip). Table 2 highlights these operational differences."
    )

    # TABLE 2: Inference Path Comparison
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_t2.paragraph_format.space_before = Pt(6)
    p_t2.paragraph_format.space_after = Pt(2)
    p_t2.paragraph_format.keep_with_next = True
    r_t2_h = p_t2.add_run("Table 2. ")
    r_t2_h.font.name = "Cambria"
    r_t2_h.font.size = Pt(9.5)
    r_t2_h.font.bold = True
    r_t2_t = p_t2.add_run("Operational Comparison of PyTorch Native vs. ONNX Runtime Inference Execution Paths")
    r_t2_t.font.name = "Cambria"
    r_t2_t.font.size = Pt(9.5)

    t2_widths = [1.6, 2.5, 2.5] # Total = 6.6 in
    t2 = doc.add_table(rows=6, cols=3)
    set_table_properties(t2, t2_widths)

    t2_headers = ["Operational Parameter", "Native PyTorch Inference Path", "ONNX Runtime Inference Path"]
    for j, h in enumerate(t2_headers):
        set_cell(t2.rows[0].cells[j], h, bold=True, size=9, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t2_widths[j])

    t2_data = [
        ["Model Weight Artifact", "`merged_model.pth` (~94.7 MB, FP32)", "`merged_model_int8.onnx` (~47.7 MB, INT8)"],
        ["Test-Time Augmentation", "8 geometric & photometric transforms", "3 passes (base + horizontal/vertical flips)"],
        ["Monte Carlo Dropout", "Active (15 stochastic forward passes)", "Inactive (Dropout is identity in ONNX eval)"],
        ["Uncertainty Metric Origin", "MCD predictive variance ($\\sigma^2_{\\text{MCD}}$)", "TTA empirical variance across 3 passes"],
        ["Safety Override Logic", "Variance > 0.015 flags class as 'uncertain'", "Variance > 0.015 flags class as 'uncertain'"]
    ]

    for i, row in enumerate(t2_data):
        bg = "FAFAFA" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.CENTER if j == 0 else WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t2.rows[i+1].cells[j], val, bold=False, size=9, align=align, bg_color=bg, width=t2_widths[j])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # 7. SECTION IV: IMPLEMENTATION (Clean page break)
    # -------------------------------------------------------------
    add_h1("IV.  IMPLEMENTATION", page_break_before=True)
    add_p(
        "This section details the software implementation and presents a rigorous demarcation between machine learning neural networks "
        "and auxiliary rule-based or heuristic modules."
    )
    add_h2("A. Backend Web Service Implementation")
    add_p(
        "The backend service is engineered using FastAPI and Python 3.10+:\n"
        "• Asynchronous I/O and Concurrency: Model forward passes are dispatched via `anyio.to_thread.run_sync` to execute inference in worker thread pools, "
        "preventing blocking of the asyncio event loop during compute-heavy tensor operations.\n"
        "• Streaming Ingestion Boundaries: Incoming file payloads are streamed in 64 KB chunks up to an enforced 10 MB maximum limit. "
        "MIME types are strictly validated against an image whitelist (`image/jpeg`, `image/png`, `image/webp`).\n"
        "• Model Lifecycle: Model checkpoints are instantiated during server startup as singleton objects protected by a `threading.Lock` to serialize execution."
    )
    add_h2("B. Frontend Interface Implementation")
    add_p(
        "The client application is built with React.js (Node.js 18+):\n"
        "• Client-Side Blur Screening: An HTML5 canvas utility computes grayscale image gradient variance, offering immediate preliminary blur warnings before upload.\n"
        "• Anatomical Subsite Tagging: An interactive SVG oral cavity selector enables users to annotate lesion locations (buccal mucosa, tongue, floor of mouth, gingiva, palate).\n"
        "• Responsive Reporting UI: Displays classification output badges, blur advisories, uncertainty flags, and structured risk questionnaires."
    )
    add_h2("C. Categorization of Repository Software Modules")
    add_p(
        "To ensure academic precision and prevent conflating algorithmic components, Table 3 categorizes all analytical modules present in the repository, "
        "explicitly distinguishing neural network models from rule-based heuristics, classical computer vision, and mathematical post-processing. "
        "In particular, visual saliency interpretability is implemented using Grad-CAM++ [13], computing positive partial derivatives over the penultimate "
        "feature maps of ResNet-50 Layer4 as a mathematical post-processing stage rather than an end-to-end trained explainability architecture."
    )

    # TABLE 3: Software Component Categorization
    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_t3.paragraph_format.space_before = Pt(6)
    p_t3.paragraph_format.space_after = Pt(2)
    p_t3.paragraph_format.keep_with_next = True
    r_t3_h = p_t3.add_run("Table 3. ")
    r_t3_h.font.name = "Cambria"
    r_t3_h.font.size = Pt(9.5)
    r_t3_h.font.bold = True
    r_t3_t = p_t3.add_run("Factual Categorization of Repository Software Modules (Demarcating Neural Networks vs. Heuristics and Rules)")
    r_t3_t.font.name = "Cambria"
    r_t3_t.font.size = Pt(9.5)

    t3_widths = [1.4, 1.4, 2.3, 1.5] # Total = 6.6 in
    t3 = doc.add_table(rows=10, cols=4)
    set_table_properties(t3, t3_widths)

    t3_headers = ["Functional Component", "Code Location", "Underlying Implementation Mechanism", "Algorithmic Classification"]
    for j, h in enumerate(t3_headers):
        set_cell(t3.rows[0].cells[j], h, bold=True, size=9, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t3_widths[j])

    t3_data = [
        ["Oral Image Classification", "app/services/ml_engine.py", "PyTorch MergedNet: 4-backbone feature concatenation [5]-[8]", "Deep Neural Network (Checkpoint Present)"],
        ["Image Sharpness Gating", "app/services/image_quality.py", "OpenCV Laplacian variance calculation (Threshold = 50.0)", "Deterministic Heuristic (Non-ML)"],
        ["Saliva Glare Suppression", "app/services/optical_normalization.py", "Luminance thresholding (B>=238, S<=0.22) + inpainting", "Classical Computer Vision (Non-ML)"],
        ["Color Normalization", "app/services/optical_normalization.py", "Reinhard statistical mean/std transfer in CIE L*a*b* space", "Statistical Color Mapping (Non-ML)"],
        ["Lesion Boundary Segmentation", "app/services/vision_pipeline.py", "Erythema index (R-G)/(R+G) + brightness thresholding", "Handcrafted Heuristic (Non-ML)"],
        ["Epidemiological Risk Scoring", "app/services/clinical_risk.py", "Linear sum: Age (+0.30), Tobacco (+0.35), Betel (+0.30), Alcohol (+0.20)", "Rule-Based Formula (Non-ML)"],
        ["Four-Class Ordinal Triage", "app/services/multimodal_fusion.py", "Scripted probability shifting with bonus weights & temperature scaling (T=2.5)", "Rule-Based Logic (Non-ML)"],
        ["AJCC Clinical Staging", "app/services/clinical_staging.py", "Decision tree mapping user-entered diameter and site to stage", "Rule-Based Decision Tree (Non-ML)"],
        ["Visual Saliency (Grad-CAM++)", "app/services/xai_cam.py", "Gradient-weighted Class Activation Mapping on ResNet-50 Layer4 [13]", "Mathematical Post-Processing"]
    ]

    for i, row in enumerate(t3_data):
        bg = "FAFAFA" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t3.rows[i+1].cells[j], val, bold=(j==3 and "Neural Network" in val), size=8.5, align=align, bg_color=bg, width=t3_widths[j])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_p(
        "Important Note on Latent Cross-Attention Code: The repository file `app/services/multimodal_fusion.py` contains a PyTorch module named "
        "`MultimodalCrossAttentionFusion`. Live code tracing reveals that this module is completely bypassed during live `/predict` execution. "
        "Instead, the endpoint invokes `evaluate_multimodal_ordinal_triage`, which applies scripted linear adjustments to model probabilities."
    )
    add_h2("D. Model Checkpoint Status and Missing Training History")
    add_p(
        "The repository contains two compiled model weights files: `merged_model.pth` (PyTorch state dict, 94.7 MB) and `merged_model_int8.onnx` (47.7 MB). "
        "However, an exhaustive search reveals that no training scripts (`train.py`), hyperparameter configs, loss criteria, optimizer parameters (e.g., AdamW, SGD), "
        "learning rate schedules, or epoch loss logs exist in the repository. Furthermore, no training or validation loss curves are present. "
        "Consequently, the training history and hyperparameter choices that produced the checkpoint cannot be independently reproduced or verified from the codebase."
    )

    # -------------------------------------------------------------
    # 8. SECTION V: EVALUATION STATUS AND LIMITATIONS
    # -------------------------------------------------------------
    add_h1("V.  EVALUATION STATUS AND LIMITATIONS", page_break_before=False)
    add_p(
        "Rigorous scientific reporting requires complete transparency regarding how performance figures were generated and what evaluation evidence exists."
    )
    add_h2("A. Disclosure of Synthetic Benchmark Generation Scripts")
    add_p(
        "Prior drafts and internal project documents cited extraordinary classification metrics, including an overall accuracy of 99.92%, 100.00% specificity, "
        "99.76% sensitivity, and an AUROC of 1.0000 on a supposed cohort of 1,200 subjects. In addition, comparative baseline tables purported to demonstrate "
        "statistically significant superiority over standalone ResNet-50, VGG-16, EfficientNet-B0, and MobileNetV2 models."
    )
    add_p(
        "Inspection of the evaluation script (`backend/scripts/ieee_benchmark_evaluator.py`) reveals that these reported figures were generated entirely through "
        "synthetic numerical simulation rather than empirical evaluation on real images. Specifically:\n"
        "1) The script defines a benchmark simulation function (`run_comparative_benchmark`) that establishes a synthetic sample size ($N = 1,200$) and draws class predictions "
        "and probabilities from parameterized random number generators (using normal and beta statistical distributions).\n"
        "2) Baseline comparisons and ablation metrics were generated by computing statistical summaries across these synthetic distributions rather than running models on test images.\n"
        "3) The script automatically formatted and exported these synthetic numbers into LaTeX tables (`ieee_tables.tex`) and JSON files (`ieee_benchmark_results.json`).\n"
        "These synthetic numbers represent an exploratory simulation utility created during software development; they do not represent real experimental findings. "
        "Accordingly, all synthetic figures are strictly excluded from this paper."
    )
    add_h2("B. Absence of Empirical Model Metrics")
    add_p(
        "Inspection of the repository found no verified empirical evaluation of `merged_model.pth` across the repository's image collection. Consequently:\n"
        "• Valid empirical test-set metrics—including Accuracy, Sensitivity, Specificity, F1-Score, and AUROC—are currently unavailable.\n"
        "• This paper makes no claims of high classification performance, diagnostic accuracy, or algorithmic superiority over baseline models."
    )

    # TABLE 4: Audit Disclosures vs Synthetic Claims
    p_t4 = doc.add_paragraph()
    p_t4.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_t4.paragraph_format.space_before = Pt(6)
    p_t4.paragraph_format.space_after = Pt(2)
    p_t4.paragraph_format.keep_with_next = True
    r_t4_h = p_t4.add_run("Table 4. ")
    r_t4_h.font.name = "Cambria"
    r_t4_h.font.size = Pt(9.5)
    r_t4_h.font.bold = True
    r_t4_t = p_t4.add_run("Factual Audit Disclosures vs. Previously Reported Synthetic Benchmark Artifacts")
    r_t4_t.font.name = "Cambria"
    r_t4_t.font.size = Pt(9.5)

    t4_widths = [1.5, 2.5, 2.6] # Total = 6.6 in
    t4 = doc.add_table(rows=6, cols=3)
    set_table_properties(t4, t4_widths)

    t4_headers = ["Investigation Dimension", "Previously Reported Claims (Synthetic Scripts)", "Verified Repository Audit Findings"]
    for j, h in enumerate(t4_headers):
        set_cell(t4.rows[0].cells[j], h, bold=True, size=9, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t4_widths[j])

    t4_data = [
        ["Reported Accuracy & Metrics", "99.92% Accuracy, 1.0000 AUROC, 99.76% Sens, 100% Spec", "Generated synthetically by `ieee_benchmark_evaluator.py`; genuine metrics unavailable"],
        ["Evaluated Patient Cohort", "Asserted 1,200 multicenter clinical patients", "Repository contains exactly 940 images (490 cancer, 450 non-cancer); 0 patient IDs"],
        ["Test Set Partition Quality", "Claimed independent, multicenter testing cohort", "Contaminated: 11 duplicate groups (25 files) cross train/val/test partitions"],
        ["Training & Loss Logs", "Asserted converged loss curves and learning rates", "Missing: No training scripts (`train.py`), optimizers, or loss logs found in repository"],
        ["Clinical Validation Status", "Asserted validated clinical triage tool", "Unvalidated: Non-diagnostic prototype; lacks IRB approval and regulatory clearance"]
    ]

    for i, row in enumerate(t4_data):
        bg = "FAFAFA" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t4.rows[i+1].cells[j], val, bold=(j==0), size=9, align=align, bg_color=bg, width=t4_widths[j])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_h2("C. Data Integrity and Methodological Limitations")
    add_p(
        "1) Cross-Partition Duplicate Contamination: The presence of 11 cross-partition duplicate image groups encompassing 25 files directly violates the fundamental "
        "machine learning requirement for independent training and testing sets [11], [12]. If the checkpoint was trained on the supplied training split, evaluating it "
        "on the current test split risks measuring image memorization rather than generalized lesion feature extraction.\n"
        "2) Lack of Patient-Level Isolation: Without patient identifiers, subject overlap between splits cannot be evaluated, creating an acute risk of feature leakage [11].\n"
        "3) Severe Parameter-to-Sample Imbalance: Fusing four CNN backbones yields a 5,120-dimensional latent embedding. Fitting a 5,120-dimensional classification head on a cohort "
        "of only 655 training images introduces extreme vulnerability to catastrophic overfitting, especially in the absence of documented regularization and augmentation policies."
    )
    add_h2("D. Ethical, Regulatory, and Clinical Boundaries")
    add_p(
        "1) Ethical Documentation Absence: No Institutional Review Board (IRB) approvals, human research protocols, or patient informed consent records were found in the codebase.\n"
        "2) Lack of Clinical Validation: The prototype has not undergone prospective clinical trials, blinded reader studies with qualified clinicians, or validation across external hospitals.\n"
        "3) Regulatory Status: The software possesses no medical device clearance or regulatory authorization (e.g., FDA 510(k), CE-IVD, CDSCO). It is strictly a non-diagnostic prototype "
        "and is not intended or approved for clinical patient triage or diagnostic decision-making."
    )

    # -------------------------------------------------------------
    # 9. SECTION VI: DISCUSSION
    # -------------------------------------------------------------
    add_h1("VI.  DISCUSSION")
    add_p(
        "This section discusses the engineering contributions of the prototype, highlights methodological lessons for applied medical AI, "
        "and defines a structured remediation roadmap."
    )
    add_h2("A. Software Engineering Contributions")
    add_p(
        "The primary contribution of this work lies in the systems engineering architecture of a multi-backbone image classification application:\n"
        "• Modular Feature Fusion: MergedNet demonstrates an operational implementation for extracting, pooling, and concatenating representations from four diverse CNN topologies [5]–[8].\n"
        "• Uncertainty Logic Integration: The codebase demonstrates how Test-Time Augmentation [10] and Monte Carlo Dropout [9] can be embedded into HTTP service endpoints to flag ambiguous predictions.\n"
        "• Robust Asynchronous Architecture: The separation of a React client from an asynchronous, memory-bounded FastAPI service demonstrates practical software engineering for deep learning inference."
    )
    add_h2("B. Methodological Lessons for Medical AI Research")
    add_p(
        "The audit of this undergraduate capstone repository yields vital methodological lessons for applied artificial intelligence:\n"
        "1) Mandatory Cryptographic Hash Auditing: Performing SHA-256 hash checks and patient-level verification must be treated as mandatory initial steps before training or evaluating models [11], [12].\n"
        "2) Transparent Reporting vs. Synthetic Artifacts: Rigorous academic integrity demands that exploratory simulation scripts be transparently disclosed rather than mistaken for empirical findings.\n"
        "3) Clear Component Demarcation: Auxiliary clinical risk questionnaires and staging calculators must be clearly documented as rule-based formulas rather than conflated with trained neural networks."
    )
    add_h2("C. Phased Conditional Remediation Roadmap")
    add_p(
        "To establish a foundation for future academic investigation, Table 5 delineates a structured, phased remediation roadmap."
    )

    # TABLE 5: Remediation Roadmap
    p_t5 = doc.add_paragraph()
    p_t5.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_t5.paragraph_format.space_before = Pt(6)
    p_t5.paragraph_format.space_after = Pt(2)
    p_t5.paragraph_format.keep_with_next = True
    r_t5_h = p_t5.add_run("Table 5. ")
    r_t5_h.font.name = "Cambria"
    r_t5_h.font.size = Pt(9.5)
    r_t5_h.font.bold = True
    r_t5_t = p_t5.add_run("Phased Conditional Remediation and Technical Roadmap")
    r_t5_t.font.name = "Cambria"
    r_t5_t.font.size = Pt(9.5)

    t5_widths = [1.3, 1.8, 3.5] # Total = 6.6 in
    t5 = doc.add_table(rows=7, cols=3)
    set_table_properties(t5, t5_widths)

    t5_headers = ["Phase", "Remediation Focus", "Key Engineering & Methodological Objectives"]
    for j, h in enumerate(t5_headers):
        set_cell(t5.rows[0].cells[j], h, bold=True, size=9, align=WD_PARAGRAPH_ALIGNMENT.CENTER, bg_color="EAEAEA", width=t5_widths[j])

    t5_data = [
        ["Phase 1 (Conditional)", "Provenance & Governance Verification", "Identify original Kaggle dataset source URL; verify licensing, patient consent, and ethics permissions."],
        ["Phase 2 (Conditional)", "Deduplication & Patient Partitioning", "Purge 21 exact duplicate image groups; establish strict patient-level separation into disjoint splits."],
        ["Phase 3", "Reproducible Training Pipeline", "Develop version-controlled `train.py`; log optimizer, learning rate schedule, loss criteria, and seeds."],
        ["Phase 4", "Empirical Evaluation & Ablation", "Evaluate retrained MergedNet on independent test split; compute true empirical metrics (Accuracy, F1, AUROC)."],
        ["Phase 5 (Conditional)", "Auxiliary Module Refinement", "Replace heuristic segmentation with validated models; calibrate risk formulas against clinical literature."],
        ["Phase 6 (Conditional)", "Clinical Partnership & reader Trials", "Upon formal ethical approval, collaborate with oral oncologists to conduct blinded reader evaluation."]
    ]

    for i, row in enumerate(t5_data):
        bg = "FAFAFA" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            align = WD_PARAGRAPH_ALIGNMENT.CENTER if j == 0 else WD_PARAGRAPH_ALIGNMENT.LEFT
            set_cell(t5.rows[i+1].cells[j], val, bold=(j==0), size=9, align=align, bg_color=bg, width=t5_widths[j])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # 10. SECTION VII: CONCLUSION
    # -------------------------------------------------------------
    add_h1("VII.  CONCLUSION")
    add_p(
        "This paper has documented the software architecture, inference pipeline, and repository data audit of an exploratory, "
        "non-diagnostic prototype for binary oral image classification. The engineering framework implements MergedNet, a multi-backbone "
        "convolutional model concatenating pooled visual representations from VGG-16 [5], ResNet-50 [6], EfficientNet-B0 [8], and MobileNetV2 [7] "
        "into a 5,120-dimensional feature vector, served through a decoupled FastAPI backend and React frontend with runtime uncertainty gating logic [9], [10]."
    )
    add_p(
        "Rather than asserting unverified performance figures, this paper provides an objective, evidence-based account of the prototype's implementation and current limitations:\n"
        "• The prototype is strictly non-diagnostic, lacks regulatory clearance, and has not undergone clinical validation.\n"
        "• The repository dataset comprises 940 JPEG images (490 cancer, 450 non-cancer) with unverified provenance, absent patient IDs, and no IRB ethics documentation.\n"
        "• A cryptographic SHA-256 hash audit identified 21 duplicate groups encompassing 46 files, with 11 groups (25 files) crossing partition boundaries, "
        "precluding the current test split from being considered an independent or statistically valid evaluation set.\n"
        "• Training scripts are absent from the repository, and previously reported benchmark results (including 99.92% accuracy) were generated by synthetic simulation scripts.\n"
        "• Genuine empirical classification metrics on real images are currently unavailable.\n"
        "By prioritizing scientific integrity, data transparency, and objective engineering documentation over premature performance assertions, "
        "this paper provides an honest baseline and transparent roadmap for future academic research."
    )

    # -------------------------------------------------------------
    # 11. ACKNOWLEDGEMENTS (Clean page break to group with References)
    # -------------------------------------------------------------
    add_h1("ACKNOWLEDGEMENTS", page_break_before=True)
    add_p(
        "The authors express their sincere gratitude to Project Guide Prof. Aishwarya S, Assistant Professor, Department of Computer Science & Engineering, "
        "Kalpataru Institute of Technology, Tiptur, for guidance, technical suggestions, and academic supervision throughout this capstone project. "
        "The authors also acknowledge the Department of Computer Science & Engineering, Kalpataru Institute of Technology, and Visvesvaraya Technological University (VTU), "
        "Belagavi, for providing computing infrastructure, laboratory facilities, and institutional support."
    )

    # -------------------------------------------------------------
    # 12. REFERENCES (Strictly matching text citations [1] to [13])
    # -------------------------------------------------------------
    add_h1("REFERENCES")

    references = [
        "[1] H. Sung, J. Ferlay, R. L. Siegel, M. Laversanne, I. Soerjomataram, A. Jemal, and F. Bray, \"Global Cancer Statistics 2020: GLOBOCAN Estimates of Incidence and Mortality Worldwide for 36 Cancers in 185 Countries,\" CA: A Cancer Journal for Clinicians, vol. 71, no. 3, pp. 209-249, 2021. DOI: 10.3322/caac.21660.",
        "[2] P. Brocklehurst, O. Kujan, L. A. O'Malley, G. R. Ogden, S. Shepherd, and A.-M. Glenny, \"Screening programmes for the early detection and prevention of oral cancer,\" Cochrane Database of Systematic Reviews, no. 11, Art. No. CD004150, 2013. DOI: 10.1002/14651858.CD004150.pub4.",
        "[3] R. A. Welikala, P. Remagnino, J. H. Lim, C. S. Chan, S. Rajendran, T. G. Kallarakkal, R. B. Zain, R. D. Jayasinghe, V. Mohan, A. Rao, K. A. Amirtham, and S. J. Loffman, \"Automated Detection and Classification of Oral Lesions Using Deep Learning for Early Detection of Oral Cancer,\" IEEE Access, vol. 8, pp. 132677-132693, 2020. DOI: 10.1109/ACCESS.2020.3010180.",
        "[4] K. Warin, W. Limprasert, S. Suebnukarn, S. Jinaporntham, P. Jantana, and S. Vicharueang, \"AI-based analysis of oral lesions using novel deep convolutional neural networks for early detection of oral cancer,\" PLOS ONE, vol. 17, no. 8, p. e0273508, 2022. DOI: 10.1371/journal.pone.0273508.",
        "[5] K. Simonyan and A. Zisserman, \"Very Deep Convolutional Networks for Large-Scale Image Recognition,\" in Proc. 3rd International Conference on Learning Representations (ICLR), San Diego, CA, USA, 2015. arXiv: 1409.1556.",
        "[6] K. He, X. Zhang, S. Ren, and J. Sun, \"Deep Residual Learning for Image Recognition,\" in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 770-778. DOI: 10.1109/CVPR.2016.90.",
        "[7] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, \"MobileNetV2: Inverted Residuals and Linear Bottlenecks,\" in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 4510-4520. DOI: 10.1109/CVPR.2018.00474.",
        "[8] M. Tan and Q. V. Le, \"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,\" in Proc. 36th International Conference on Machine Learning (ICML), PMLR, vol. 97, 2019, pp. 6105-6114.",
        "[9] Y. Gal and Z. Ghahramani, \"Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning,\" in Proc. 33rd International Conference on Machine Learning (ICML), PMLR, vol. 48, 2016, pp. 1050-1059.",
        "[10] M. S. Ayhan and P. Berens, \"Test-time Data Augmentation for Estimation of Heteroscedastic Aleatoric Uncertainty in Deep Neural Networks,\" in Proc. 1st Conference on Medical Imaging with Deep Learning (MIDL), Amsterdam, The Netherlands, 2018. arXiv: 1803.06013.",
        "[11] M. Roberts, D. Driggs, M. Thorpe, J. Gilbey, M. Yeung, S. Ursprung, A. I. Aviles-Rivero, C. Etmann, C. McCague, L. Beer, J. R. Weir-McCall, Z. Teng, E. Gkrania-Klotsas, AIX-COVNET Collaboration, J. H. F. Rudd, E. Sala, and C.-B. Schönlieb, \"Common pitfalls and recommendations for using machine learning to detect and prognosticate for COVID-19 using chest radiographs and CT scans,\" Nature Machine Intelligence, vol. 3, no. 3, pp. 199-217, 2021. DOI: 10.1038/s42256-021-00307-0.",
        "[12] S. Kapoor and A. Narayanan, \"Leakage and the reproducibility crisis in machine-learning-based science,\" Patterns, vol. 4, no. 9, p. 100804, 2023. DOI: 10.1016/j.patter.2023.100804.",
        "[13] A. Chattopadhay, A. Sarkar, P. Howlader, and V. N. Balasubramanian, \"Grad-CAM++: Generalized Gradient-Based Visual Explanations for Deep Convolutional Networks,\" in Proc. IEEE Winter Conference on Applications of Computer Vision (WACV), 2018, pp. 839-847. DOI: 10.1109/WACV.2018.00097."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Cambria"
        r_ref.font.size = Pt(9.5)

    # Save document
    doc.save(output_docx)
    print(f"Manuscript saved successfully to: {output_docx}")

    return output_docx, output_pdf

if __name__ == "__main__":
    docx_file, pdf_file = create_manuscript()
    print("Manuscript generation completed.")
