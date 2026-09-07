import React, { useState, useEffect } from 'react';
import { 
    X, 
    Download, 
    Printer, 
    Building2, 
    ShieldAlert, 
    ShieldCheck, 
    FileText, 
    Share2, 
    CheckCircle2, 
    AlertCircle, 
    Loader2,
    Code2,
    Stethoscope,
    Microscope
} from 'lucide-react';
import { authFetch } from './api';

const SpecialistReferralModal = ({ isOpen, onClose, analysisId }) => {
    const [referralData, setReferralData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [exportingFhir, setExportingFhir] = useState(false);

    useEffect(() => {
        if (!isOpen || !analysisId) return;

        const fetchReferral = async () => {
            setLoading(true);
            setError('');
            try {
                const res = await authFetch(`/analyses/${analysisId}/referral`);
                if (!res.ok) {
                    throw new Error('Could not generate specialist referral summary.');
                }
                const data = await res.json();
                setReferralData(data);
            } catch (err) {
                setError(err.message || 'Failed to retrieve referral letter.');
            } finally {
                setLoading(false);
            }
        };

        fetchReferral();
    }, [isOpen, analysisId]);

    const handleDownloadFhir = async () => {
        setExportingFhir(true);
        try {
            const res = await authFetch(`/analyses/${analysisId}/fhir`);
            if (!res.ok) throw new Error('FHIR bundle export failed.');
            const fhirJson = await res.json();
            
            const blob = new Blob([JSON.stringify(fhirJson, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `FHIR-R4-Bundle-Specimen-${analysisId}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (err) {
            alert('Failed to download HL7 FHIR Bundle: ' + err.message);
        } finally {
            setExportingFhir(false);
        }
    };

    const handlePrint = () => {
        window.print();
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-xs overflow-y-auto">
            <div className="relative w-full max-w-3xl my-8 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-2xl transition-all">
                {/* Modal Top Control Strip (Non-printable) */}
                <div className="print:hidden flex items-center justify-between px-6 py-4 border-b border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-950/80">
                    <div className="flex items-center space-x-2">
                        <FileText className="w-5 h-5 text-clinical-teal" />
                        <span className="font-mono text-xs font-semibold text-stone-900 dark:text-stone-100 uppercase tracking-wider">
                            Specialist Oncology Referral Dossier // HL7 FHIR r4
                        </span>
                    </div>
                    <div className="flex items-center space-x-2">
                        <button
                            type="button"
                            onClick={handleDownloadFhir}
                            disabled={exportingFhir || loading}
                            className="px-3 py-1.5 border border-stone-300 dark:border-stone-700 hover:bg-stone-100 dark:hover:bg-stone-800 text-stone-700 dark:text-stone-300 font-mono text-xs flex items-center gap-1.5 transition-colors disabled:opacity-50"
                            title="Download standard HL7 FHIR Release 4 JSON document"
                        >
                            {exportingFhir ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Code2 className="w-3.5 h-3.5" />}
                            <span>EXPORT FHIR r4 JSON</span>
                        </button>
                        <button
                            type="button"
                            onClick={handlePrint}
                            disabled={loading}
                            className="px-3 py-1.5 bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 font-mono text-xs font-semibold flex items-center gap-1.5 hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-colors disabled:opacity-50"
                        >
                            <Printer className="w-3.5 h-3.5" />
                            <span>PRINT / SAVE PDF</span>
                        </button>
                        <button
                            type="button"
                            onClick={onClose}
                            className="p-1.5 text-stone-400 hover:text-stone-600 dark:hover:text-stone-200"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                </div>

                {/* Printable Referral Letter Document */}
                <div className="p-8 sm:p-10 font-sans text-stone-900 dark:text-stone-100 print:p-0 print:text-black">
                    {loading ? (
                        <div className="py-20 text-center font-mono text-xs text-stone-500">
                            <Loader2 className="w-8 h-8 animate-spin mx-auto text-clinical-teal mb-3" />
                            <span>Compiling Oncology Referral Dossier & HL7 Metadata...</span>
                        </div>
                    ) : error ? (
                        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 text-xs font-mono flex items-center gap-2">
                            <AlertCircle className="w-4 h-4 flex-shrink-0" />
                            <span>{error}</span>
                        </div>
                    ) : referralData ? (
                        <div className="space-y-6">
                            {/* Formal Clinic Header */}
                            <div className="flex flex-col sm:flex-row justify-between sm:items-start gap-4 pb-6 border-b-2 border-stone-800 dark:border-stone-200">
                                <div>
                                    <div className="font-mono text-[10px] text-stone-500 uppercase tracking-widest">
                                        DEPARTMENT OF HEAD & NECK ONCOLOGY // MAXILLOFACIAL TRIAGE
                                    </div>
                                    <h1 className="font-serif text-2xl font-bold text-stone-950 dark:text-white tracking-tight mt-1">
                                        {referralData.referring_clinician.facility}
                                    </h1>
                                    <div className="font-mono text-xs text-stone-600 dark:text-stone-400 mt-1">
                                        Ref Provider: {referralData.referring_clinician.name} • Contact: {referralData.referring_clinician.email}
                                    </div>
                                </div>
                                <div className="font-mono text-right text-xs">
                                    <div className="text-[10px] text-stone-400">DOCUMENT ACCESSION</div>
                                    <div className="font-bold text-stone-900 dark:text-stone-100">{referralData.referral_reference_id}</div>
                                    <div className="text-stone-500 text-[11px] mt-0.5">{referralData.referral_date}</div>
                                </div>
                            </div>

                            {/* Urgency Notification Banner */}
                            <div className={`p-4 border-2 font-mono text-xs flex items-center justify-between ${
                                referralData.urgency.includes('URGENT')
                                    ? 'border-rose-600 bg-rose-50 dark:bg-rose-950/30 text-rose-800 dark:text-rose-200'
                                    : 'border-teal-600 bg-teal-50 dark:bg-teal-950/30 text-teal-800 dark:text-teal-200'
                            }`}>
                                <div className="flex items-center gap-2.5">
                                    <ShieldAlert className="w-5 h-5 flex-shrink-0" />
                                    <div>
                                        <div className="font-bold tracking-wider">{referralData.urgency}</div>
                                        <div className="text-[11px] font-sans opacity-90 mt-0.5">
                                            Prioritized clinical consultation indicated for diagnostic histopathology.
                                        </div>
                                    </div>
                                </div>
                                <span className="text-[10px] px-2 py-0.5 border font-semibold">
                                    {referralData.diagnostic_findings.triage_tier.split(' ')[0]}
                                </span>
                            </div>

                            {/* Patient & Anamnesis Profile Grid */}
                            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs border border-stone-200 dark:border-stone-800 p-4 bg-stone-50/70 dark:bg-stone-950/50">
                                <div>
                                    <span className="text-[9px] text-stone-400 block uppercase">Patient MRN</span>
                                    <span className="font-bold text-stone-900 dark:text-stone-100">{referralData.patient.mrn_identifier}</span>
                                </div>
                                <div>
                                    <span className="text-[9px] text-stone-400 block uppercase">Lesion Topography</span>
                                    <span className="font-bold text-stone-900 dark:text-stone-100">{referralData.patient.anatomical_site}</span>
                                </div>
                                <div>
                                    <span className="text-[9px] text-stone-400 block uppercase">Clinical Risk Score</span>
                                    <span className="font-bold text-stone-900 dark:text-stone-100">{(referralData.patient.clinical_risk_score * 100).toFixed(0)}% (Epidemiological)</span>
                                </div>
                                <div>
                                    <span className="text-[9px] text-stone-400 block uppercase">Presumptive cTNM</span>
                                    <span className="font-bold text-clinical-teal">{referralData.diagnostic_findings.ajcc_8th_ctnm.split(' ')[0]}</span>
                                </div>
                            </div>

                            {/* Deep Vision Diagnostic Findings */}
                            <div>
                                <h3 className="font-serif text-base font-bold text-stone-900 dark:text-stone-100 border-b border-stone-200 dark:border-stone-800 pb-1.5 mb-3 flex items-center gap-2">
                                    <Microscope className="w-4 h-4 text-clinical-teal" />
                                    <span>AI Diagnostic Vision & Morphometric Telemetry</span>
                                </h3>
                                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 font-mono text-xs">
                                    <div className="p-2.5 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950">
                                        <span className="text-[9px] text-stone-400 block">CLASSIFICATION VERDICT</span>
                                        <span className={`font-bold text-sm ${referralData.diagnostic_findings.ai_verdict === 'CANCER' ? 'text-rose-600' : 'text-teal-600'}`}>
                                            {referralData.diagnostic_findings.ai_verdict} ({referralData.diagnostic_findings.confidence_percentage}%)
                                        </span>
                                    </div>
                                    <div className="p-2.5 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950">
                                        <span className="text-[9px] text-stone-400 block">CALIBRATED DIAMETER</span>
                                        <span className="font-bold text-stone-900 dark:text-stone-100 text-sm">
                                            {referralData.diagnostic_findings.calibrated_diameter_mm} mm
                                        </span>
                                    </div>
                                    <div className="p-2.5 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950">
                                        <span className="text-[9px] text-stone-400 block">ESTIMATED SURFACE AREA</span>
                                        <span className="font-bold text-stone-900 dark:text-stone-100 text-sm">
                                            {referralData.diagnostic_findings.surface_area_mm2} mm²
                                        </span>
                                    </div>
                                    <div className="p-2.5 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950">
                                        <span className="text-[9px] text-stone-400 block">BORDER IRREGULARITY</span>
                                        <span className="font-bold text-stone-900 dark:text-stone-100 text-sm">
                                            {referralData.diagnostic_findings.border_irregularity_index}
                                        </span>
                                    </div>
                                    <div className="p-2.5 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950">
                                        <span className="text-[9px] text-stone-400 block">EPISTEMIC UNCERTAINTY (σ²)</span>
                                        <span className="font-bold text-stone-900 dark:text-stone-100 text-sm">
                                            {referralData.diagnostic_findings.epistemic_uncertainty_sigma2}
                                        </span>
                                    </div>
                                    <div className="p-2.5 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950">
                                        <span className="text-[9px] text-stone-400 block">HISTOLOGY STATUS</span>
                                        <span className="font-bold text-clinical-teal text-sm">
                                            {referralData.pathology_verification.biopsy_proven ? 'BIOPSY PROVEN' : 'PENDING PATHOLOGY'}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            {/* Biopsy Directive Directive */}
                            <div className="p-4 border-l-4 border-clinical-teal bg-teal-50/40 dark:bg-teal-950/20">
                                <h4 className="font-mono text-xs font-bold text-stone-900 dark:text-stone-100 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                                    <Stethoscope className="w-3.5 h-3.5 text-clinical-teal" />
                                    <span>Recommended Biopsy Topography & Clinical Protocol</span>
                                </h4>
                                <p className="font-sans text-xs text-stone-700 dark:text-stone-300 leading-relaxed">
                                    {referralData.biopsy_directive}
                                </p>
                            </div>

                            {/* Clinician Signature Strip */}
                            <div className="pt-8 border-t border-stone-200 dark:border-stone-800 flex justify-between items-end font-mono text-xs">
                                <div>
                                    <div className="font-serif text-sm font-semibold text-stone-900 dark:text-stone-100">
                                        {referralData.referring_clinician.name}
                                    </div>
                                    <div className="text-stone-500 text-[11px]">{referralData.referring_clinician.role} Examiner</div>
                                    <div className="text-[10px] text-stone-400">Oral Oncology AI Diagnostic System</div>
                                </div>
                                <div className="text-right">
                                    <div className="w-44 border-b border-stone-400 dark:border-stone-600 mb-1"></div>
                                    <div className="text-[10px] text-stone-400 uppercase">Referring Clinician Signature</div>
                                </div>
                            </div>
                        </div>
                    ) : null}
                </div>
            </div>
        </div>
    );
};

export default SpecialistReferralModal;
