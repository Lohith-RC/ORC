# Project Guide Review & Verification Checklist

**Companion Review & Action Sheet for Capstone Research Manuscript**  
**Paper Title:** *Oral Cancer Detection Using AI/ML and Deep Learning*  
**Academic Context:** Final-Year B.E. Computer Science and Engineering Capstone Project | October 2026  
**Document Status:** Companion Checklist to [`docs/RESEARCH_PAPER_GUIDE_REVIEW.docx`](file:///c:/Users/Rakshith%20YB/ORC-3/docs/RESEARCH_PAPER_GUIDE_REVIEW.docx) and [`docs/RESEARCH_PAPER_GUIDE_REVIEW.pdf`](file:///c:/Users/Rakshith%20YB/ORC-3/docs/RESEARCH_PAPER_GUIDE_REVIEW.pdf)

---

## 1. Author & Institutional Information (Confirmed Details & Guide Decisions)

*All author details have been confirmed from project records. Guide direction is requested on the final author sequence for publication submission.*

| Item | Confirmed Detail in Paper | Guide Action / Confirmation Required | Guide Response / Decision |
| :--- | :--- | :--- | :--- |
| **Student Author Byline** | Rakshith Y B, Lohith R C, Keerthi A | Confirm student author listing and author order for final manuscript | [ ] Confirmed: _____________________ |
| **Project Guide Designation** | Project Guide: Aishwarya S (in review details) | Confirm designation as Project Guide (omitted from author byline) | [ ] Confirmed: _____________________ |
| **Institution & Affiliation** | Kalpataru Institute of Technology, Tiptur (VTU) | Confirm formal institutional naming for publication submission | [ ] Confirmed: _____________________ |
| **Author Sequence Question** | Currently listed: Rakshith Y B, Lohith R C, Keerthi A | Confirm final student author sequence (Lead vs. Alphabetical vs. Department preference) | [ ] Sequence approved<br>[ ] Revised order: ______________ |
| **Target Publication Venue** | Provisional IEEE Conference A4 Format | Select target venue (IEEE Student Conference, Springer LNCS, or internal department review) | [ ] Venue selected: ________________ |

---

## 2. Critical Methodological & Repository Questions for Guide Guidance

*These items reflect verified findings from the repository audit. Guide direction is requested before initiating retrained models or submitting for external peer review.*

| No. | Verification Item & Repository Finding | Guide Action / Direction Needed | Decision / Notes |
| :---: | :--- | :--- | :--- |
| **Q1** | **Dataset Source & Provenance:** Described in comments as Kaggle, but exact URL, license terms, and curation details are missing. | Identify source Kaggle URL and confirm whether usage terms permit academic publication. | [ ] Approved / URL: _______________ |
| **Q2** | **Ethics & Patient Consent:** No Institutional Review Board (IRB) approval, human subjects protocol, or patient consent records exist in the repository. | Confirm whether external institutional ethical clearance exists or if the missing status must be permanently disclosed. | [ ] Clearance exists<br>[ ] Document as missing |
| **Q3** | **Patient Metadata:** 940 images lack patient IDs; subject overlap across partitions cannot be verified. | Determine if patient linkage keys exist; otherwise, confirm reporting the lack of patient-level isolation as a primary limitation. | [ ] Metadata available<br>[ ] Report as limitation |
| **Q4** | **Duplicate Images:** 21 duplicate groups encompassing 46 files (11 cross-partition groups with 25 files) found by cryptographic SHA-256 hash matching. | Approve deduplication protocol and re-partitioning strategy to establish a properly separated, independent test set. | [ ] Deduplication approved |
| **Q5** | **Training Scripts:** No `train.py`, loss records, optimizer configurations, or hyperparameters exist in the repository. | Check if original training code and convergence logs can be retrieved from predecessor student archives. | [ ] Script retrieved<br>[ ] Write new training script |
| **Q6** | **Pre-Training Weights:** MergedNet backbones instantiate with `weights=None` in checkpoint loader. | Confirm whether backbones were pre-trained on ImageNet or initialized from random scratch. | [ ] ImageNet pre-trained<br>[ ] Initialized from scratch |
| **Q7** | **Empirical Evaluation:** Previously reported 99.92% accuracy was generated synthetically by simulation scripts; genuine test metrics are unavailable. | Authorize execution of an empirical evaluation script on an independent, deduplicated test split. | [ ] Run empirical evaluation |
| **Q8** | **Runtime Uncertainty:** TTA and Monte Carlo dropout are implemented in code but uncalibrated and unvalidated. | Advise on runtime consistency evaluation and calibration validation roadmap. | [ ] Follow roadmap Phase 4 |
| **Q9** | **Overfitting & Regulatory Status:** 940 images vs 5,120 fused features noted as an unevaluated concern; prototype noted as unvalidated, unassessed, and not for clinical use. | Confirm that limitation disclosures meet departmental and academic standards for ethical reporting. | [ ] Approved as framed |

---

## 3. Guide Review Sign-Off & Verdict

- **Guide Name:** __________________________________________________
- **Designation / Department:** ______________________________________
- **Signature:** ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Date:** ______________________
- **Review Decision:**
  - [ ] **Approved as-is** (Proceed with manuscript in current provisional format)
  - [ ] **Approved with minor revisions** (Address items checked above)
  - [ ] **Revisions required** (Execute recommended remediation roadmap prior to submission)
