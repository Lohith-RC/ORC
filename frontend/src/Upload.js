import React, { useCallback, useState, useRef, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    UploadCloud, 
    FileImage, 
    X, 
    AlertTriangle, 
    CheckCircle2, 
    Download, 
    Microscope, 
    Activity, 
    ShieldAlert, 
    ShieldCheck, 
    HelpCircle,
    FileText,
    ArrowRight
} from 'lucide-react';
import axios from 'axios';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

// --- Analog Uncertainty Caliper Visualizer ---
const UncertaintyCaliper = ({ confidence, uncertainty, prediction }) => {
    // confidence: e.g. 0.96 (0 to 1)
    // uncertainty: e.g. 0.008
    const confPct = Math.min(100, Math.max(0, confidence * 100));
    // uncertainty band width in percent (scaled for visual clarity)
    const bandWidth = Math.min(25, Math.max(4, Math.sqrt(uncertainty) * 100));
    const leftBound = Math.max(0, confPct - bandWidth / 2);
    const rightBound = Math.min(100, confPct + bandWidth / 2);
    const isUncertain = uncertainty > 0.015;

    return (
        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900/70 p-5 rounded-none my-4">
            <div className="flex items-center justify-between font-mono text-[11px] mb-2 uppercase text-stone-500">
                <span>EPISTEMIC UNCERTAINTY CALIPER</span>
                <span className={isUncertain ? 'text-amber-500 font-bold' : 'text-clinical-teal dark:text-teal-400'}>
                    σ² = {uncertainty.toFixed(5)} ({isUncertain ? 'HIGH VARIANCE' : 'STABLE CONSENSUS'})
                </span>
            </div>

            {/* Ruler Scale */}
            <div className="relative h-9 bg-stone-200/80 dark:bg-stone-800/80 rounded-none overflow-hidden my-3 border border-stone-300/80 dark:border-stone-700">
                {/* Tick marks */}
                <div className="absolute inset-0 flex justify-between px-2 items-end pb-1 pointer-events-none opacity-40 font-mono text-[8px]">
                    <span>0%</span>
                    <span>25%</span>
                    <span>50%</span>
                    <span>75%</span>
                    <span>100%</span>
                </div>

                {/* Uncertainty Range Band */}
                <div 
                    style={{ left: `${leftBound}%`, width: `${bandWidth}%` }}
                    className={`absolute top-0 bottom-0 ${isUncertain ? 'bg-amber-400/30 dark:bg-amber-400/20' : 'bg-clinical-teal/25 dark:bg-teal-400/20'} border-x-2 ${isUncertain ? 'border-amber-500' : 'border-clinical-teal'}`}
                />

                {/* Mean Confidence Indicator Point */}
                <div 
                    style={{ left: `${confPct}%` }}
                    className="absolute top-0 bottom-0 w-1 bg-stone-900 dark:bg-white z-10 -ml-0.5"
                >
                    <div className="w-2.5 h-2.5 bg-stone-900 dark:bg-white rounded-full -ml-[3px] -mt-1 shadow-sm"></div>
                </div>
            </div>

            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 pt-1">
                <span>LOWER BOUND: {leftBound.toFixed(1)}%</span>
                <span className="font-semibold text-stone-800 dark:text-stone-200">POINT ESTIMATE: {confPct.toFixed(1)}%</span>
                <span>UPPER BOUND: {rightBound.toFixed(1)}%</span>
            </div>
        </div>
    );
};

// --- Tactile Risk Switch Component ---
const RiskFactorToggle = ({ label, weight, active, onChange, note }) => {
    return (
        <div 
            onClick={() => onChange(!active)}
            className={`cursor-pointer select-none border p-3 flex items-center justify-between transition-all ${
                active 
                    ? 'border-clinical-teal bg-teal-50/50 dark:bg-teal-950/20 dark:border-teal-700' 
                    : 'border-stone-200 dark:border-stone-800 bg-stone-50/50 dark:bg-stone-900/30 hover:border-stone-300 dark:hover:border-stone-700'
            }`}
        >
            <div className="flex flex-col">
                <span className="text-xs font-mono font-medium text-stone-900 dark:text-stone-100">{label}</span>
                <span className="text-[10px] text-stone-400 font-mono mt-0.5">{note}</span>
            </div>
            <div className="flex items-center gap-2">
                <span className="font-mono text-[10px] text-clinical-teal dark:text-teal-400">{weight}</span>
                <div className={`w-9 h-5 rounded-full p-0.5 transition-colors ${active ? 'bg-clinical-teal' : 'bg-stone-300 dark:bg-stone-700'}`}>
                    <div className={`w-4 h-4 rounded-full bg-white transition-transform ${active ? 'translate-x-4' : 'translate-x-0'}`}></div>
                </div>
            </div>
        </div>
    );
};

const Upload = ({ token }) => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [loadingPhase, setLoadingPhase] = useState('');
    const [user, setUser] = useState(null);
    const reportRef = useRef();

    // Specimen ID generated for clinical authenticity
    const [specimenId, setSpecimenId] = useState('');

    useEffect(() => {
        const rand = Math.random().toString(36).substring(2, 7).toUpperCase();
        setSpecimenId(`SPC-${new Date().getFullYear()}-${rand}`);
    }, []);

    // Clinical risk factors
    const [riskForm, setRiskForm] = useState({ 
        age: 45, 
        tobacco_use: false, 
        alcohol_use: false, 
        betel_nut: false, 
        prior_lesions: false 
    });

    useEffect(() => {
        if (token) {
            axios.get('http://localhost:8000/me', {
                headers: { 'Authorization': `Bearer ${token}` }
            }).then(response => {
                setUser(response.data);
            }).catch(err => {
                console.error("Failed to fetch user data for report", err);
            });
        }
    }, [token]);

    const onDrop = useCallback(acceptedFiles => {
        setResult(null);
        setError('');
        const selectedFile = acceptedFiles[0];
        if (selectedFile) {
            setFile(selectedFile);
            const reader = new FileReader();
            reader.onload = () => {
                setPreview(reader.result);
            };
            reader.readAsDataURL(selectedFile);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'image/*': ['.jpeg', '.jpg', '.png', '.webp'] },
        multiple: false
    });

    const handleUpload = async () => {
        if (!file) {
            setError('Please select an oral image specimen first.');
            return;
        }
        setLoading(true);
        setError('');
        setResult(null);

        // Simulated laboratory sequencer phases for genuine clinical feel
        setLoadingPhase('Verifying image resolution & Laplacian blur variance...');
        setTimeout(() => {
            setLoadingPhase('Executing 8-fold Test-Time Augmentation (TTA)...');
        }, 800);
        setTimeout(() => {
            setLoadingPhase('Computing Monte Carlo dropout variational passes (15 runs)...');
        }, 1600);

        const formData = new FormData();
        formData.append('file', file);
        const params = new URLSearchParams({
            age: riskForm.age,
            tobacco_use: riskForm.tobacco_use,
            alcohol_use: riskForm.alcohol_use,
            betel_nut: riskForm.betel_nut,
            prior_lesions: riskForm.prior_lesions,
        });

        try {
            const response = await axios.post(`http://localhost:8000/predict?${params.toString()}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${token}`
                }
            });
            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || err.response?.data?.error || 'A laboratory inference failure occurred. Please verify server connection.');
        } finally {
            setLoading(false);
            setLoadingPhase('');
        }
    };
    
    const removeFile = () => {
        setFile(null);
        setPreview(null);
        setResult(null);
        setError('');
    };

    const handleDownload = () => {
        const input = reportRef.current;
        if (input) {
            html2canvas(input, { scale: 2, useCORS: true }).then((canvas) => {
                const imgData = canvas.toDataURL('image/png');
                const pdf = new jsPDF('p', 'mm', 'a4');
                const pdfWidth = pdf.internal.pageSize.getWidth();
                const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
                pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
                pdf.save(`OralCancer_Triage_${specimenId}.pdf`);
            });
        }
    };

    return (
        <div className="bg-parchment-100 dark:bg-ink-950 min-h-screen py-10 px-4 sm:px-6 lg:px-8 font-sans text-stone-800 dark:text-stone-200">
            <div className="max-w-7xl mx-auto">
                {/* Header Metadata Ribbon */}
                <div className="border-b border-stone-200 dark:border-stone-800 pb-6 mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
                    <div>
                        <div className="inline-flex items-center gap-2 font-mono text-[11px] tracking-wider uppercase text-clinical-teal dark:text-teal-400 mb-2">
                            <span className="w-2 h-2 bg-clinical-teal inline-block"></span>
                            LABORATORY INTAKE // OSCC SCREENING
                        </div>
                        <h1 className="font-serif text-3xl sm:text-4xl text-stone-900 dark:text-stone-100 font-normal">
                            Specimen Examination & Triage
                        </h1>
                    </div>
                    <div className="font-mono text-xs text-stone-500 text-left md:text-right space-y-1">
                        <div>DOCKET: <span className="font-semibold text-stone-800 dark:text-stone-200">{specimenId}</span></div>
                        <div>DATE: {new Date().toLocaleDateString()} {new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                    </div>
                </div>

                {error && (
                    <div className="mb-6 p-4 border border-red-300 dark:border-red-900 bg-red-50 dark:bg-red-950/30 text-red-700 dark:text-red-300 font-mono text-xs flex items-center gap-3">
                        <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                        <span>{error}</span>
                    </div>
                )}

                {/* Asymmetric 2-Column Workstation Layout */}
                <div className="grid lg:grid-cols-12 gap-8 items-start">
                    {/* ============================================================ */}
                    {/* LEFT PANEL: Specimen Upload & Risk Form (5 cols)             */}
                    {/* ============================================================ */}
                    <div className="lg:col-span-5 space-y-6">
                        {/* Specimen Dropzone Card */}
                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6 relative">
                            {/* Corner Marks */}
                            <span className="absolute -top-1 -left-1 text-[10px] font-mono text-stone-400">+</span>
                            <span className="absolute -top-1 -right-1 text-[10px] font-mono text-stone-400">+</span>
                            <span className="absolute -bottom-1 -left-1 text-[10px] font-mono text-stone-400">+</span>
                            <span className="absolute -bottom-1 -right-1 text-[10px] font-mono text-stone-400">+</span>

                            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 uppercase mb-4 border-b border-stone-200 dark:border-stone-800 pb-2">
                                <span>01 // SPECIMEN CAPTURE</span>
                                <span>ACCEPTED: JPEG • PNG • WEBP</span>
                            </div>

                            <AnimatePresence mode="wait">
                                {!preview ? (
                                    <div
                                        {...getRootProps()}
                                        className={`p-8 border-2 border-dashed text-center cursor-pointer transition-colors ${
                                            isDragActive 
                                                ? 'border-clinical-teal bg-teal-50/50 dark:bg-teal-950/20' 
                                                : 'border-stone-300 dark:border-stone-700 hover:border-stone-400 dark:hover:border-stone-600 bg-white/50 dark:bg-stone-950/50'
                                        }`}
                                    >
                                        <input {...getInputProps()} />
                                        <Microscope className="w-10 h-10 mx-auto text-stone-400 mb-3" />
                                        <p className="font-serif text-base text-stone-800 dark:text-stone-200 mb-1">
                                            {isDragActive ? 'Drop oral lesion photograph...' : 'Ingest Clinical Photograph'}
                                        </p>
                                        <p className="font-mono text-[11px] text-stone-400">
                                            Click or drag specimen file here
                                        </p>
                                    </div>
                                ) : (
                                    <div className="relative border border-stone-300 dark:border-stone-700 bg-stone-950 p-2">
                                        <div className="aspect-video w-full overflow-hidden relative">
                                            <img src={preview} alt="Specimen Preview" className="w-full h-full object-cover" />
                                            <div className="absolute top-2 left-2 bg-stone-900/80 backdrop-blur-md px-2 py-1 font-mono text-[9px] text-white">
                                                {file.name} ({(file.size / 1024).toFixed(1)} KB)
                                            </div>
                                        </div>
                                        <button 
                                            onClick={removeFile} 
                                            className="absolute top-4 right-4 p-1 bg-stone-900 text-white hover:bg-red-600 transition-colors"
                                            title="Remove image"
                                        >
                                            <X className="w-4 h-4" />
                                        </button>
                                    </div>
                                )}
                            </AnimatePresence>
                        </div>

                        {/* Patient Epidemiological Risk Factors */}
                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6">
                            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 uppercase mb-4 border-b border-stone-200 dark:border-stone-800 pb-2">
                                <span>02 // EPIDEMIOLOGICAL RISK PROFILE</span>
                                <span>PRIOR WEIGHTING</span>
                            </div>

                            <div className="space-y-3">
                                {/* Age Slider */}
                                <div className="border border-stone-200 dark:border-stone-800 p-3 bg-stone-50/50 dark:bg-stone-900/30">
                                    <div className="flex justify-between items-center mb-1 font-mono text-xs">
                                        <span className="text-stone-700 dark:text-stone-300">PATIENT AGE:</span>
                                        <span className="font-bold text-stone-900 dark:text-stone-100">{riskForm.age} YEARS</span>
                                    </div>
                                    <input 
                                        type="range" 
                                        min="18" 
                                        max="90" 
                                        value={riskForm.age}
                                        onChange={e => setRiskForm(p => ({...p, age: parseInt(e.target.value)}))}
                                        className="w-full accent-clinical-teal cursor-pointer"
                                    />
                                    <span className="font-mono text-[9px] text-stone-400 block mt-1">Age &gt; 45 exponentially elevates oral mucosal vulnerability</span>
                                </div>

                                <RiskFactorToggle 
                                    label="Habitual Tobacco Usage" 
                                    weight="+0.35 OR" 
                                    note="Cigarettes, bidi, or chewing tobacco"
                                    active={riskForm.tobacco_use} 
                                    onChange={v => setRiskForm(p => ({...p, tobacco_use: v}))}
                                />
                                <RiskFactorToggle 
                                    label="Frequent Alcohol Ingestion" 
                                    weight="+0.20 OR" 
                                    note="Synergistic co-carcinogen with tobacco"
                                    active={riskForm.alcohol_use} 
                                    onChange={v => setRiskForm(p => ({...p, alcohol_use: v}))}
                                />
                                <RiskFactorToggle 
                                    label="Betel Quid / Areca Nut Usage" 
                                    weight="+0.30 OR" 
                                    note="High correlation with oral submucous fibrosis"
                                    active={riskForm.betel_nut} 
                                    onChange={v => setRiskForm(p => ({...p, betel_nut: v}))}
                                />
                                <RiskFactorToggle 
                                    label="Prior Leukoplakia / Erythroplakia" 
                                    weight="+0.25 OR" 
                                    note="Pre-existing mucosal premalignancy"
                                    active={riskForm.prior_lesions} 
                                    onChange={v => setRiskForm(p => ({...p, prior_lesions: v}))}
                                />
                            </div>
                        </div>

                        {/* Submit Action */}
                        {file && !loading && (
                            <button
                                onClick={handleUpload}
                                className="w-full py-4 bg-stone-900 dark:bg-stone-100 text-stone-100 dark:text-stone-900 text-sm font-mono tracking-wider uppercase font-semibold hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-all shadow-lg flex items-center justify-center gap-2"
                            >
                                <span>Run Multi-Model Triage Synthesis</span>
                                <ArrowRight className="w-4 h-4" />
                            </button>
                        )}
                    </div>

                    {/* ============================================================ */}
                    {/* RIGHT PANEL: Diagnostic Verdict & Uncertainty Caliper (7 cols)*/}
                    {/* ============================================================ */}
                    <div className="lg:col-span-7">
                        {loading ? (
                            <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-12 text-center min-h-[400px] flex flex-col items-center justify-center">
                                <div className="w-12 h-12 border-2 border-clinical-teal border-t-transparent rounded-full animate-spin mb-6"></div>
                                <span className="font-mono text-xs text-clinical-teal uppercase tracking-widest block mb-2">
                                    INFERENCE SEQUENCER IN PROGRESS
                                </span>
                                <h3 className="font-serif text-2xl text-stone-900 dark:text-stone-100 font-normal mb-3">
                                    Analyzing Oral Micro-Architecture
                                </h3>
                                <p className="font-mono text-xs text-stone-500 max-w-sm">
                                    {loadingPhase}
                                </p>
                            </div>
                        ) : result ? (
                            <div ref={reportRef} className="border border-stone-300 dark:border-stone-800 bg-white dark:bg-stone-900 p-8 relative shadow-lg">
                                {/* Docket Stamp Header */}
                                <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 pb-6 border-b border-stone-200 dark:border-stone-800 font-mono text-xs">
                                    <div>
                                        <div className="text-[10px] text-stone-400 uppercase">OFFICIAL CLINICAL TRIAGE REPORT</div>
                                        <div className="font-bold text-stone-900 dark:text-stone-100 text-sm">{specimenId}</div>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <button 
                                            onClick={handleDownload}
                                            className="px-3 py-1.5 border border-stone-300 dark:border-stone-700 hover:bg-stone-100 dark:hover:bg-stone-800 text-stone-700 dark:text-stone-300 text-xs font-mono flex items-center gap-1.5 transition-colors"
                                        >
                                            <Download className="w-3.5 h-3.5" />
                                            <span>EXPORT PDF DOSSIER</span>
                                        </button>
                                    </div>
                                </div>

                                {/* Primary Verdict Stamp */}
                                <div className="my-6">
                                    {result.prediction.toLowerCase() === 'cancer' ? (
                                        <div className="border-2 border-clinical-terracotta bg-red-50/50 dark:bg-red-950/20 p-5">
                                            <div className="flex items-center gap-3">
                                                <ShieldAlert className="w-7 h-7 text-clinical-terracotta flex-shrink-0" />
                                                <div>
                                                    <span className="font-mono text-[10px] text-clinical-terracotta tracking-widest uppercase block">
                                                        CLASSIFICATION VERDICT // HIGH SUSPICION
                                                    </span>
                                                    <h2 className="font-serif text-2xl sm:text-3xl text-clinical-terracotta font-medium">
                                                        Presumptive OSCC Malignancy
                                                    </h2>
                                                </div>
                                            </div>
                                            <p className="font-sans text-xs text-stone-700 dark:text-stone-300 mt-3 font-normal leading-relaxed">
                                                Tissue features correlate strongly with Oral Squamous Cell Carcinoma. Prompt histological biopsy and specialist maxillofacial or oncological referral is indicated.
                                            </p>
                                        </div>
                                    ) : result.prediction.toLowerCase() === 'uncertain' ? (
                                        <div className="border-2 border-clinical-ochre bg-amber-50/50 dark:bg-amber-950/20 p-5">
                                            <div className="flex items-center gap-3">
                                                <HelpCircle className="w-7 h-7 text-clinical-ochre flex-shrink-0" />
                                                <div>
                                                    <span className="font-mono text-[10px] text-clinical-ochre tracking-widest uppercase block">
                                                        VARIANCE WARNING // INCONCLUSIVE INFERENCE
                                                    </span>
                                                    <h2 className="font-serif text-2xl sm:text-3xl text-clinical-ochre font-medium">
                                                        Uncertain Classification (σ² &gt; 0.015)
                                                    </h2>
                                                </div>
                                            </div>
                                            <p className="font-sans text-xs text-stone-700 dark:text-stone-300 mt-3 font-normal leading-relaxed">
                                                Model disagreement across Monte Carlo perturbation passes exceeds safe clinical thresholds. Re-capture photograph under uniform lighting or conduct direct clinical examination.
                                            </p>
                                        </div>
                                    ) : (
                                        <div className="border-2 border-clinical-teal bg-teal-50/50 dark:bg-teal-950/20 p-5">
                                            <div className="flex items-center gap-3">
                                                <ShieldCheck className="w-7 h-7 text-clinical-teal dark:text-teal-400 flex-shrink-0" />
                                                <div>
                                                    <span className="font-mono text-[10px] text-clinical-teal dark:text-teal-400 tracking-widest uppercase block">
                                                        CLASSIFICATION VERDICT // BENIGN / NORMAL
                                                    </span>
                                                    <h2 className="font-serif text-2xl sm:text-3xl text-clinical-teal dark:text-teal-400 font-medium">
                                                        Non-Malignant Mucosa
                                                    </h2>
                                                </div>
                                            </div>
                                            <p className="font-sans text-xs text-stone-700 dark:text-stone-300 mt-3 font-normal leading-relaxed">
                                                No high-confidence dysplasia or carcinomatous biomarkers detected. Maintain regular oral health screening interval.
                                            </p>
                                        </div>
                                    )}
                                </div>

                                {/* Analog Caliper Display */}
                                <UncertaintyCaliper 
                                    confidence={result.confidence}
                                    uncertainty={result.uncertainty}
                                    prediction={result.prediction}
                                />

                                {/* Multimodal Telemetry Metrics */}
                                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-4 border-y border-stone-200 dark:border-stone-800 font-mono text-xs">
                                    <div>
                                        <span className="text-[9px] text-stone-400 block uppercase">Confidence</span>
                                        <span className="font-bold text-stone-900 dark:text-stone-100 text-sm">
                                            {(result.confidence * 100).toFixed(1)}%
                                        </span>
                                    </div>
                                    <div>
                                        <span className="text-[9px] text-stone-400 block uppercase">Risk Score</span>
                                        <span className="font-bold text-stone-900 dark:text-stone-100 text-sm">
                                            {(result.clinical_risk_score * 100).toFixed(0)} / 100
                                        </span>
                                    </div>
                                    <div>
                                        <span className="text-[9px] text-stone-400 block uppercase">TTA Passes</span>
                                        <span className="font-bold text-stone-900 dark:text-stone-100 text-sm">
                                            {result.tta_passes}-Fold
                                        </span>
                                    </div>
                                    <div>
                                        <span className="text-[9px] text-stone-400 block uppercase">Image Quality</span>
                                        <span className={`font-bold text-sm ${result.image_quality === 'acceptable' ? 'text-emerald-500' : 'text-amber-500'}`}>
                                            {result.image_quality.toUpperCase()}
                                        </span>
                                    </div>
                                </div>

                                {result.clinical_alert && (
                                    <div className="mt-4 p-3 bg-amber-50 dark:bg-amber-950/20 border border-amber-300 dark:border-amber-800 text-amber-800 dark:text-amber-300 font-mono text-[11px] flex items-center gap-2">
                                        <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                                        <span>EPIDEMIOLOGICAL ALERT: Patient risk score exceeds 0.60 threshold due to habitual tobacco/betel nut usage.</span>
                                    </div>
                                )}

                                {/* Legal & Clinical Disclaimer */}
                                <p className="font-mono text-[9px] text-stone-400 dark:text-stone-500 mt-6 leading-relaxed uppercase">
                                    DISCLAIMER: This report is an assistive clinical screening metric generated by neural network ensemble inference. It does not constitute a definitive medical diagnosis. In all cases of persistent oral lesions, clinical biopsy and histopathological verification remain mandatory.
                                </p>
                            </div>
                        ) : (
                            <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-12 text-center min-h-[400px] flex flex-col items-center justify-center">
                                <Microscope className="w-12 h-12 text-stone-400 mb-4" />
                                <h3 className="font-serif text-2xl text-stone-900 dark:text-stone-100 font-normal mb-2">
                                    Workstation Ready
                                </h3>
                                <p className="font-sans text-xs text-stone-500 max-w-sm font-light leading-relaxed">
                                    Select or drop an oral image specimen on the left panel, configure relevant patient risk factors, and initiate the multi-model analysis.
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Upload;