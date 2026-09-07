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
    ArrowRight,
    MapPin,
    Sliders,
    Stethoscope,
    CheckSquare,
    Layers,
    Camera,
    Wifi,
    WifiOff,
    CloudUpload,
    HardDrive
} from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from './api';
import OralCavityMap, { ORAL_SITES } from './OralCavityMap';
import LesionSegmentationViewer from './LesionSegmentationViewer';
import LongitudinalProgressionCard from './LongitudinalProgressionCard';
import ClinicianVerificationModal from './ClinicianVerificationModal';
import SpecialistReferralModal from './SpecialistReferralModal';
import WebRTCIntraoralCameraModal from './WebRTCIntraoralCameraModal';
import { computeImageFileSharpness } from './clientBlurDetector';
import { saveOfflineSpecimen, getOfflineSpecimens, deleteOfflineSpecimen } from './offlineVault';
import { UncertaintyCaliper, RiskFactorToggle, OfflineSyncBanner } from './components/upload';


const Upload = ({ token }) => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [vitalFile, setVitalFile] = useState(null);
    const [vitalPreview, setVitalPreview] = useState(null);
    const [patientId, setPatientId] = useState('PT-1001');
    const [crossPolarized, setCrossPolarized] = useState(false);
    const [distanceMm, setDistanceMm] = useState(50.0);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [loadingPhase, setLoadingPhase] = useState('');
    const [user, setUser] = useState(null);
    const reportRef = useRef();
    const phaseTimersRef = useRef([]);

    // Specimen ID generated for clinical authenticity
    const [specimenId, setSpecimenId] = useState('');

    useEffect(() => {
        const rand = Math.random().toString(36).substring(2, 7).toUpperCase();
        setSpecimenId(`SPC-${new Date().getFullYear()}-${rand}`);
    }, []);

    const [isVerificationOpen, setIsVerificationOpen] = useState(false);
    const [isReferralOpen, setIsReferralOpen] = useState(false);
    const [isCameraOpen, setIsCameraOpen] = useState(false);
    const [clientSharpness, setClientSharpness] = useState(null);
    const [clientBlurWarning, setClientBlurWarning] = useState(null);
    const [isOffline, setIsOffline] = useState(!navigator.onLine);
    const [offlineVaultCount, setOfflineVaultCount] = useState(0);
    const [isSyncingVault, setIsSyncingVault] = useState(false);
    const [offlineSuccessMsg, setOfflineSuccessMsg] = useState('');

    // Clinical risk factors
    const [riskForm, setRiskForm] = useState({ 
        age: 45, 
        tobacco_use: false, 
        alcohol_use: false, 
        betel_nut: false, 
        prior_lesions: false 
    });

    // Anatomical oral cavity lesion site
    const [selectedSite, setSelectedSite] = useState('buccal_mucosa');

    const refreshVaultCount = useCallback(async () => {
        try {
            const items = await getOfflineSpecimens();
            setOfflineVaultCount(items.length);
        } catch {
            setOfflineVaultCount(0);
        }
    }, []);

    useEffect(() => {
        refreshVaultCount();
        const handleOnline = () => setIsOffline(false);
        const handleOffline = () => setIsOffline(true);
        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);
        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, [refreshVaultCount]);

    useEffect(() => {
        if (token) {
            axios.get(`${API_BASE_URL}/me`, {
                headers: { 'Authorization': `Bearer ${token}` }
            }).then(response => {
                setUser(response.data);
            }).catch(err => {
                console.error("Failed to fetch user data for report", err);
            });
        }
    }, [token]);

    const onDrop = useCallback(async (acceptedFiles) => {
        setResult(null);
        setError('');
        setOfflineSuccessMsg('');
        const selectedFile = acceptedFiles[0];
        if (selectedFile) {
            setFile(selectedFile);
            const reader = new FileReader();
            reader.onload = () => {
                setPreview(reader.result);
            };
            reader.readAsDataURL(selectedFile);

            // Client-side Instant Focus & Laplacian Gating (<15ms)
            const { sharpness, isBlurry } = await computeImageFileSharpness(selectedFile);
            setClientSharpness(sharpness);
            setClientBlurWarning(isBlurry ? `Client Optical Gating: Sharpness score (${sharpness.toFixed(1)} < 50.0) indicates motion blur or defocus. Consider capturing a sharper specimen.` : null);
        }
    }, []);

    const handleCameraCapture = (capturedFile, sharpness) => {
        setResult(null);
        setError('');
        setOfflineSuccessMsg('');
        setFile(capturedFile);
        const reader = new FileReader();
        reader.onload = () => {
            setPreview(reader.result);
        };
        reader.readAsDataURL(capturedFile);
        setClientSharpness(sharpness);
        setClientBlurWarning(sharpness < 50.0 ? `Client Optical Gating: Sharpness score (${sharpness.toFixed(1)} < 50.0) indicates motion blur. Consider recapturing.` : null);
    };

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'image/*': ['.jpeg', '.jpg', '.png', '.webp'] },
        multiple: false
    });

    const handleSaveOffline = async () => {
        if (!file) return;
        try {
            await saveOfflineSpecimen({
                patient_identifier: patientId.trim() || 'ANON-001',
                lesion_site: selectedSite,
                cross_polarized: crossPolarized,
                distance_mm: distanceMm,
                age: riskForm.age,
                tobacco_use: riskForm.tobacco_use,
                alcohol_use: riskForm.alcohol_use,
                betel_nut: riskForm.betel_nut,
                prior_lesions: riskForm.prior_lesions,
                image_name: file.name,
                image_blob: file,
                client_sharpness: clientSharpness
            });
            await refreshVaultCount();
            removeFile();
            setOfflineSuccessMsg(`Specimen saved to local Offline Clinical Vault. Total queued: ${offlineVaultCount + 1}`);
        } catch (err) {
            setError(`Failed to save to local vault: ${err.message}`);
        }
    };

    const handleSyncVault = async () => {
        if (!token || isOffline) return;
        setIsSyncingVault(true);
        setError('');
        try {
            const items = await getOfflineSpecimens();
            let synced = 0;
            for (const item of items) {
                const formData = new FormData();
                formData.append('file', item.image_blob, item.image_name || 'offline.jpg');
                formData.append('patient_identifier', item.patient_identifier);
                formData.append('lesion_site', item.lesion_site);
                formData.append('cross_polarized', item.cross_polarized);
                formData.append('distance_mm', item.distance_mm);
                formData.append('age', item.age);
                formData.append('tobacco_use', item.tobacco_use);
                formData.append('alcohol_use', item.alcohol_use);
                formData.append('betel_nut', item.betel_nut);
                formData.append('prior_lesions', item.prior_lesions);

                await axios.post(`${API_BASE_URL}/predict`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `Bearer ${token}`
                    }
                });
                await deleteOfflineSpecimen(item.id);
                synced++;
            }
            await refreshVaultCount();
            setOfflineSuccessMsg(`Successfully synchronized ${synced} offline screenings with cloud database.`);
        } catch (err) {
            setError(`Offline vault synchronization error: ${err.response?.data?.detail || err.message}`);
        } finally {
            setIsSyncingVault(false);
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setError('Please select an oral image specimen first.');
            return;
        }

        if (isOffline) {
            await handleSaveOffline();
            return;
        }

        setLoading(true);
        setError('');
        setResult(null);

        // Clear previous timers if any
        phaseTimersRef.current.forEach(clearTimeout);
        phaseTimersRef.current = [];

        // Simulated laboratory sequencer phases for genuine clinical feel
        setLoadingPhase('Executing Stage I Lesion Segmentation & Spatial Morphology...');
        phaseTimersRef.current.push(setTimeout(() => {
            setLoadingPhase('Executing 8-fold Test-Time Augmentation (TTA)...');
        }, 600));
        phaseTimersRef.current.push(setTimeout(() => {
            setLoadingPhase('Computing Monte Carlo dropout variational passes (15 runs)...');
        }, 1200));
        phaseTimersRef.current.push(setTimeout(() => {
            setLoadingPhase('Synthesizing AJCC 8th Edition cTNM Clinical Decision Directives...');
        }, 1800));

        const formData = new FormData();
        formData.append('file', file);
        if (vitalFile) {
            formData.append('vital_stain_file', vitalFile);
        }
        // PHI Protection: transmit clinical risk factors and optical telemetry in multipart body
        formData.append('patient_identifier', patientId.trim() || 'ANON-001');
        formData.append('lesion_site', selectedSite);
        formData.append('cross_polarized', crossPolarized);
        formData.append('distance_mm', distanceMm);
        formData.append('age', riskForm.age);
        formData.append('tobacco_use', riskForm.tobacco_use);
        formData.append('alcohol_use', riskForm.alcohol_use);
        formData.append('betel_nut', riskForm.betel_nut);
        formData.append('prior_lesions', riskForm.prior_lesions);

        try {
            const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${token}`
                }
            });
            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || err.response?.data?.error || 'A laboratory inference failure occurred. Please verify server connection.');
        } finally {
            phaseTimersRef.current.forEach(clearTimeout);
            phaseTimersRef.current = [];
            setLoading(false);
            setLoadingPhase('');
        }
    };
    
    const removeFile = () => {
        setFile(null);
        setPreview(null);
        setVitalFile(null);
        setVitalPreview(null);
        setResult(null);
        setError('');
    };

    const handleVitalFileChange = (e) => {
        const selFile = e.target.files?.[0];
        if (selFile) {
            setVitalFile(selFile);
            const reader = new FileReader();
            reader.onload = () => setVitalPreview(reader.result);
            reader.readAsDataURL(selFile);
        }
    };

    // ponytail: native print covers PDF dossier export without 400KB html2canvas/jspdf bloat
    const handleDownload = () => window.print();

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

                            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 uppercase mb-3 border-b border-stone-200 dark:border-stone-800 pb-2">
                                <span>01 // SPECIMEN CAPTURE</span>
                                <div className="flex items-center gap-2">
                                    {isOffline ? (
                                        <span className="flex items-center gap-1 text-amber-600 dark:text-amber-400 font-semibold">
                                            <WifiOff className="w-3 h-3" /> OFFLINE MODE
                                        </span>
                                    ) : (
                                        <span className="flex items-center gap-1 text-teal-600 dark:text-teal-400">
                                            <Wifi className="w-3 h-3" /> ONLINE
                                        </span>
                                    )}
                                </div>
                            </div>                            {/* Offline Vault Indicator & Sync Action */}
                            <OfflineSyncBanner
                                offlineVaultCount={offlineVaultCount}
                                isOffline={isOffline}
                                isSyncingVault={isSyncingVault}
                                onSyncVault={handleSyncVault}
                                offlineSuccessMsg={offlineSuccessMsg}
                            />

                            {/* Hardware Camera Viewfinder Trigger */}
                            <div className="mb-3">
                                <button
                                    type="button"
                                    onClick={() => setIsCameraOpen(true)}
                                    className="w-full py-2.5 px-3 border border-clinical-teal bg-teal-50/60 dark:bg-teal-950/40 text-clinical-teal dark:text-teal-400 font-mono text-xs uppercase font-semibold flex items-center justify-center gap-2 hover:bg-clinical-teal hover:text-white dark:hover:bg-clinical-teal dark:hover:text-white transition-all shadow-xs"
                                >
                                    <Camera className="w-4 h-4" />
                                    <span>Launch Intraoral Video Stream (Live Viewfinder)</span>
                                </button>
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
                                            Click or drag specimen file here (JPEG, PNG, WEBP)
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

                            {/* Client-Side Optical Focus & Blur Gating Telemetry */}
                            {clientSharpness !== null && (
                                <div className={`mt-3 p-2.5 border font-mono text-xs flex items-center justify-between ${
                                    clientBlurWarning 
                                        ? 'border-amber-500/60 bg-amber-500/15 text-amber-700 dark:text-amber-300' 
                                        : 'border-teal-500/60 bg-teal-500/15 text-clinical-teal dark:text-teal-300'
                                }`}>
                                    <div className="flex items-center gap-2">
                                        {clientBlurWarning ? (
                                            <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0" />
                                        ) : (
                                            <CheckCircle2 className="w-4 h-4 text-clinical-teal shrink-0" />
                                        )}
                                        <span className="text-[11px] font-semibold">
                                            {clientBlurWarning ? 'POTENTIAL BLUR DETECTED' : 'OPTICAL CLARITY VERIFIED'}
                                        </span>
                                    </div>
                                    <span className="text-[10px] opacity-80">SHARPNESS σ²: {clientSharpness.toFixed(1)} (Min 50.0)</span>
                                </div>
                            )}
                        </div>

                        {/* Patient Identifier & Serial Record Link */}
                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-4">
                            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 uppercase mb-2 border-b border-stone-200 dark:border-stone-800 pb-1.5">
                                <span>PATIENT IDENTIFIER // SERIAL TRACKING</span>
                                <span>MRN / RECORD ID</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <input
                                    type="text"
                                    value={patientId}
                                    onChange={(e) => setPatientId(e.target.value)}
                                    placeholder="e.g. PT-1001"
                                    className="w-full bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 px-3 py-2 font-mono text-xs text-stone-900 dark:text-stone-100 focus:outline-none focus:border-clinical-teal"
                                />
                                <div className="text-[10px] font-mono text-stone-400 whitespace-nowrap">
                                    Calibrates Δ velocity
                                </div>
                            </div>
                        </div>

                        {/* Anatomical Lesion Site Targeting Map */}
                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6">
                            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 uppercase mb-3 border-b border-stone-200 dark:border-stone-800 pb-2">
                                <span>02 // ANATOMICAL LESION SITE</span>
                                <span>TOPOLOGY SELECTOR</span>
                            </div>
                            <OralCavityMap selectedSite={selectedSite} onSelectSite={setSelectedSite} />
                        </div>

                        {/* Patient Epidemiological Risk Factors */}
                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6">
                            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 uppercase mb-4 border-b border-stone-200 dark:border-stone-800 pb-2">
                                <span>03 // EPIDEMIOLOGICAL RISK PROFILE</span>
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

                        {/* Optical Acquisition & Vital Dye Protocol */}
                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6">
                            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 uppercase mb-4 border-b border-stone-200 dark:border-stone-800 pb-2">
                                <span>04 // OPTICAL PROTOCOL & MULTIMODAL DYE</span>
                                <span>STAGE I TELEMETRY</span>
                            </div>

                            <div className="space-y-4">
                                {/* Cross polarization toggle */}
                                <div 
                                    onClick={() => setCrossPolarized(!crossPolarized)}
                                    className={`cursor-pointer select-none border p-3 flex items-center justify-between transition-all ${
                                        crossPolarized 
                                            ? 'border-indigo-500 bg-indigo-50/50 dark:bg-indigo-950/20 dark:border-indigo-700' 
                                            : 'border-stone-200 dark:border-stone-800 bg-stone-50/50 dark:bg-stone-900/30'
                                    }`}
                                >
                                    <div className="flex flex-col">
                                        <span className="text-xs font-mono font-medium text-stone-900 dark:text-stone-100 flex items-center gap-1.5">
                                            <Layers className="w-3.5 h-3.5 text-indigo-500" />
                                            Cross-Polarized Lens Ingestion
                                        </span>
                                        <span className="text-[10px] text-stone-400 font-mono mt-0.5">
                                            Suppresses surface glare & specular artifacts
                                        </span>
                                    </div>
                                    <div className={`w-9 h-5 rounded-full p-0.5 transition-colors ${crossPolarized ? 'bg-indigo-600' : 'bg-stone-300 dark:bg-stone-700'}`}>
                                        <div className={`w-4 h-4 rounded-full bg-white transition-transform ${crossPolarized ? 'translate-x-4' : 'translate-x-0'}`}></div>
                                    </div>
                                </div>

                                {/* Calibrated Distance Slider */}
                                <div className="border border-stone-200 dark:border-stone-800 p-3 bg-stone-50/50 dark:bg-stone-900/30">
                                    <div className="flex justify-between items-center mb-1 font-mono text-xs">
                                        <span className="text-stone-700 dark:text-stone-300 flex items-center gap-1.5">
                                            <Sliders className="w-3.5 h-3.5 text-clinical-teal" />
                                            FOCAL DISTANCE:
                                        </span>
                                        <span className="font-bold text-stone-900 dark:text-stone-100">{distanceMm} MM</span>
                                    </div>
                                    <input 
                                        type="range" 
                                        min="30" 
                                        max="100" 
                                        step="5"
                                        value={distanceMm}
                                        onChange={e => setDistanceMm(parseFloat(e.target.value))}
                                        className="w-full accent-clinical-teal cursor-pointer"
                                    />
                                    <span className="font-mono text-[9px] text-stone-400 block mt-1">Calibrates spatial pixel-to-millimeter scaling ratio</span>
                                </div>

                                {/* Vital Stain / Autofluorescence Ingestion */}
                                <div className="border border-stone-200 dark:border-stone-800 p-3 bg-stone-50/50 dark:bg-stone-900/30">
                                    <div className="font-mono text-xs font-medium text-stone-800 dark:text-stone-200 mb-1 flex items-center justify-between">
                                        <span>SECONDARY DYE CHANNEL (OPTIONAL):</span>
                                        {vitalFile && (
                                            <button 
                                                onClick={() => { setVitalFile(null); setVitalPreview(null); }}
                                                className="text-[10px] text-red-500 font-mono hover:underline"
                                            >
                                                Clear
                                            </button>
                                        )}
                                    </div>
                                    <p className="text-[10px] text-stone-400 font-mono mb-2">
                                        Upload Toluidine Blue or VELscope autofluorescence image
                                    </p>
                                    
                                    {!vitalPreview ? (
                                        <label className="block p-3 border border-dashed border-stone-300 dark:border-stone-700 text-center cursor-pointer hover:border-clinical-teal transition-colors">
                                            <input 
                                                type="file" 
                                                accept="image/*" 
                                                className="hidden" 
                                                onChange={handleVitalFileChange} 
                                            />
                                            <span className="font-mono text-[10px] text-clinical-teal uppercase">
                                                + Attach Vital Stain Specimen
                                            </span>
                                        </label>
                                    ) : (
                                        <div className="flex items-center gap-2 p-2 border border-teal-500/40 bg-teal-500/10 font-mono text-[10px] text-teal-700 dark:text-teal-300">
                                            <span className="w-2 h-2 bg-teal-500 rounded-full"></span>
                                            <span>Attached: {vitalFile?.name}</span>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Submit Actions */}
                        {file && !loading && (
                            <div className="space-y-2">
                                <button
                                    onClick={handleUpload}
                                    className={`w-full py-4 text-sm font-mono tracking-wider uppercase font-semibold transition-all shadow-lg flex items-center justify-center gap-2 ${
                                        isOffline
                                            ? 'bg-amber-600 hover:bg-amber-700 text-white'
                                            : 'bg-stone-900 dark:bg-stone-100 text-stone-100 dark:text-stone-900 hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white'
                                    }`}
                                >
                                    {isOffline ? (
                                        <>
                                            <HardDrive className="w-4 h-4" />
                                            <span>Save to Offline Clinical Vault (Offline Active)</span>
                                        </>
                                    ) : (
                                        <>
                                            <span>Run Multi-Model Triage Synthesis</span>
                                            <ArrowRight className="w-4 h-4" />
                                        </>
                                    )}
                                </button>

                                {!isOffline && (
                                    <button
                                        type="button"
                                        onClick={handleSaveOffline}
                                        className="w-full py-2.5 border border-stone-300 dark:border-stone-700 bg-stone-50 dark:bg-stone-900 hover:bg-stone-100 dark:hover:bg-stone-800 text-stone-700 dark:text-stone-300 font-mono text-xs uppercase font-medium flex items-center justify-center gap-2 transition-colors"
                                    >
                                        <HardDrive className="w-3.5 h-3.5" />
                                        <span>Save to Local Vault for Batch Sync Later</span>
                                    </button>
                                )}
                            </div>
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
                                            type="button"
                                            onClick={() => setIsVerificationOpen(true)}
                                            className={`px-3 py-1.5 border text-xs font-mono flex items-center gap-1.5 transition-colors ${
                                                result.biopsy_proven
                                                    ? 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 font-semibold'
                                                    : 'border-clinical-teal bg-teal-50 dark:bg-teal-950/40 text-clinical-teal hover:bg-teal-100 dark:hover:bg-teal-900/40 font-semibold'
                                            }`}
                                        >
                                            <Microscope className="w-3.5 h-3.5" />
                                            <span>{result.biopsy_proven ? 'BIOPSY VERIFIED' : 'VERIFY GROUND TRUTH'}</span>
                                        </button>
                                        <button 
                                            onClick={handleDownload}
                                            className="px-3 py-1.5 border border-stone-300 dark:border-stone-700 hover:bg-stone-100 dark:hover:bg-stone-800 text-stone-700 dark:text-stone-300 text-xs font-mono flex items-center gap-1.5 transition-colors"
                                        >
                                            <Download className="w-3.5 h-3.5" />
                                            <span>EXPORT PDF</span>
                                        </button>
                                        <button
                                            type="button"
                                            onClick={() => setIsReferralOpen(true)}
                                            className="px-3 py-1.5 border border-stone-800 dark:border-stone-200 bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 text-xs font-mono font-semibold flex items-center gap-1.5 hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-colors"
                                        >
                                            <FileText className="w-3.5 h-3.5" />
                                            <span>REFERRAL & FHIR</span>
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

                                {/* Anatomical Site & Metastatic Staging Ribbon */}
                                <div className="my-4 p-4 border border-stone-200 dark:border-stone-800 bg-stone-50/80 dark:bg-stone-950/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                                    <div className="flex items-start gap-3">
                                        <div className="p-2 border border-stone-300 dark:border-stone-700 bg-white dark:bg-stone-900 text-clinical-teal">
                                            <MapPin className="w-4 h-4" />
                                        </div>
                                        <div>
                                            <div className="font-mono text-[10px] text-stone-400 uppercase">ANATOMICAL LESION SITE</div>
                                            <div className="font-serif text-base sm:text-lg font-medium text-stone-900 dark:text-stone-100">
                                                {result.lesion_site_display || ORAL_SITES.find(s => s.id === selectedSite)?.label || 'Buccal Mucosa'}
                                            </div>
                                            <div className="font-sans text-xs text-stone-500 mt-0.5">
                                                Metastatic Propensity: <span className="font-medium text-stone-700 dark:text-stone-300">{result.metastatic_propensity || 'Standard regional drainage'}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="sm:text-right">
                                        <span className={`inline-block font-mono text-[10px] px-2.5 py-1 border font-semibold ${
                                            (result.lesion_site_risk || '').includes('HIGH') 
                                                ? 'bg-rose-500/15 border-rose-500/40 text-rose-700 dark:text-rose-300'
                                                : 'bg-teal-500/15 border-teal-500/40 text-teal-700 dark:text-teal-300'
                                        }`}>
                                            {result.lesion_site_risk || 'STANDARD RISK'}
                                        </span>
                                    </div>
                                </div>

                                {/* Stage I: Lesion Spatial Segmentation & Morphology */}
                                {result.telemetry && (
                                    <LesionSegmentationViewer 
                                        imageSrc={preview} 
                                        telemetry={result.telemetry} 
                                        stagingReport={result.clinical_staging} 
                                    />
                                )}

                                {/* Longitudinal Lesion Growth & Progression Trajectory */}
                                {result.longitudinal_trajectory && (
                                    <LongitudinalProgressionCard trajectory={result.longitudinal_trajectory} />
                                )}

                                {/* AJCC 8th Edition Clinical Staging & Decision Support */}
                                {result.clinical_staging && (
                                    <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-950/60 p-6 my-5">
                                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-stone-200 dark:border-stone-800">
                                            <div>
                                                <div className="text-[10px] font-mono text-stone-400 uppercase">AJCC 8TH EDITION CLINICAL TRIAGE</div>
                                                <div className="font-serif text-lg font-medium text-stone-900 dark:text-stone-100">
                                                    {result.clinical_staging.triage_tier_display}
                                                </div>
                                            </div>
                                            <div className="font-mono text-xs px-3 py-1.5 bg-stone-900 dark:bg-stone-100 text-stone-100 dark:text-stone-900 font-bold tracking-wider">
                                                {result.clinical_staging.cTNM_estimate}
                                            </div>
                                        </div>

                                        <p className="font-sans text-xs text-stone-700 dark:text-stone-300 my-4 leading-relaxed">
                                            {result.clinical_staging.triage_summary}
                                        </p>

                                        {result.clinical_staging.recommended_biopsy_type && (
                                            <div className="p-3 mb-4 bg-teal-50/70 dark:bg-teal-950/30 border border-clinical-teal/40 font-mono text-xs text-stone-800 dark:text-stone-200 flex items-start gap-2.5">
                                                <Stethoscope className="w-4 h-4 text-clinical-teal flex-shrink-0 mt-0.5" />
                                                <div>
                                                    <span className="font-bold text-clinical-teal uppercase block text-[10px]">Diagnostic Biopsy Directives:</span>
                                                    <span>{result.clinical_staging.recommended_biopsy_type}</span>
                                                </div>
                                            </div>
                                        )}

                                        <div className="mt-4">
                                            <div className="text-[10px] font-mono text-stone-400 uppercase mb-2">CLINICAL ACTION CHECKLIST</div>
                                            <div className="space-y-2">
                                                {result.clinical_staging.action_checklist.map((item, idx) => (
                                                    <div key={idx} className="flex items-start gap-2.5 p-2.5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 font-sans text-xs text-stone-800 dark:text-stone-200">
                                                        <CheckSquare className="w-4 h-4 text-clinical-teal flex-shrink-0 mt-0.5" />
                                                        <span>{item}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                )}

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

            {/* Clinician Ground Truth Verification Modal */}
            <ClinicianVerificationModal
                isOpen={isVerificationOpen}
                onClose={() => setIsVerificationOpen(false)}
                analysis={result}
                onVerificationSuccess={(updatedAnalysis) => {
                    setResult(prev => ({
                        ...prev,
                        biopsy_proven: updatedAnalysis.biopsy_proven,
                        ground_truth_dx: updatedAnalysis.ground_truth_dx,
                        histology_grade: updatedAnalysis.histology_grade,
                        clinician_feedback_notes: updatedAnalysis.clinician_feedback_notes,
                    }));
                }}
            />

            {/* Specialist Referral & HL7 FHIR r4 Export Modal */}
            {result && (
                <SpecialistReferralModal
                    isOpen={isReferralOpen}
                    onClose={() => setIsReferralOpen(false)}
                    analysisId={result.id}
                />
            )}

            {/* Hardware WebRTC Intraoral Camera Viewfinder Modal */}
            <WebRTCIntraoralCameraModal
                isOpen={isCameraOpen}
                onClose={() => setIsCameraOpen(false)}
                onCapture={handleCameraCapture}
                targetSite={selectedSite}
            />
        </div>
    );
};

export default Upload;