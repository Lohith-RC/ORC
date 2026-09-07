import React, { useState } from 'react';
import { 
    X, 
    ShieldCheck, 
    Microscope, 
    CheckCircle2, 
    AlertCircle, 
    FileText, 
    Loader2 
} from 'lucide-react';
import { authFetch } from './api';

const GROUND_TRUTH_OPTIONS = [
    { value: 'OSCC_MALIGNANT', label: 'Oral Squamous Cell Carcinoma (OSCC) - Malignant', tier: 'MALIGNANT', color: 'text-rose-500' },
    { value: 'HIGH_GRADE_DYSPLASIA', label: 'High-Grade Epithelial Dysplasia (Severe)', tier: 'PRE-MALIGNANT', color: 'text-amber-500' },
    { value: 'MILD_MOD_DYSPLASIA', label: 'Mild to Moderate Dysplasia (Low Grade)', tier: 'PRE-MALIGNANT', color: 'text-amber-400' },
    { value: 'LICHEN_PLANUS', label: 'Oral Lichen Planus / Lichenoid Stomatitis', tier: 'BENIGN/INFLAMMATORY', color: 'text-teal-400' },
    { value: 'TRAUMATIC_ULCER', label: 'Traumatic Ulcer / Mechanical Keratosis', tier: 'REACTIVE', color: 'text-teal-300' },
    { value: 'BENIGN_HYPERKERATOSIS', label: 'Benign Frictional Hyperkeratosis', tier: 'BENIGN', color: 'text-teal-400' },
    { value: 'NORMAL_MUCOSA', label: 'Normal Healthy Oral Mucosa', tier: 'NORMAL', color: 'text-emerald-400' },
];

const HISTOLOGY_GRADES = [
    { value: 'NOT_APPLICABLE', label: 'Not Applicable / Benign / Non-Carcinomatous' },
    { value: 'WELL_DIFFERENTIATED', label: 'Grade 1: Well Differentiated (Keratinizing pearls)' },
    { value: 'MODERATELY_DIFFERENTIATED', label: 'Grade 2: Moderately Differentiated' },
    { value: 'POORLY_DIFFERENTIATED', label: 'Grade 3: Poorly Differentiated / Anaplastic' },
];

const ClinicianVerificationModal = ({ isOpen, onClose, analysis, onVerificationSuccess }) => {
    const [groundTruthDx, setGroundTruthDx] = useState(analysis?.ground_truth_dx || 'OSCC_MALIGNANT');
    const [biopsyProven, setBiopsyProven] = useState(analysis?.biopsy_proven || true);
    const [histologyGrade, setHistologyGrade] = useState(analysis?.histology_grade || 'NOT_APPLICABLE');
    const [notes, setNotes] = useState(analysis?.clinician_feedback_notes || '');
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    if (!isOpen || !analysis) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setError('');
        setSuccessMessage('');

        try {
            const payload = {
                ground_truth_dx: groundTruthDx,
                biopsy_proven: biopsyProven,
                histology_grade: histologyGrade,
                clinician_feedback_notes: notes.trim() || null,
            };

            const response = await authFetch(`/analyses/${analysis.id}/verify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.detail || 'Failed to submit pathology verification.');
            }

            const updated = await response.json();
            setSuccessMessage('Ground truth histopathology confirmed & persisted to flywheel database.');
            if (onVerificationSuccess) {
                onVerificationSuccess(updated);
            }
            setTimeout(() => {
                onClose();
            }, 1200);
        } catch (err) {
            setError(err.message || 'Error recording verification.');
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-xs">
            <div className="relative w-full max-w-xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-2xl transition-all duration-200">
                {/* Modal Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-950/60">
                    <div className="flex items-center space-x-3">
                        <div className="p-2 bg-clinical-teal/10 border border-clinical-teal/30 text-clinical-teal">
                            <Microscope className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className="font-serif text-lg font-semibold text-stone-900 dark:text-stone-100">
                                Pathology Verification & Ground-Truth
                            </h3>
                            <p className="font-mono text-xs text-stone-500">
                                SPECIMEN #{analysis.id} // MRN: {analysis.patient_identifier || 'ANON-001'} // SITE: {analysis.lesion_site || 'Unspecified'}
                            </p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-1.5 text-stone-400 hover:text-stone-600 dark:hover:text-stone-200 transition-colors"
                        disabled={submitting}
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Status Bar: AI Initial Prediction Context */}
                <div className="px-6 py-2.5 bg-stone-100/70 dark:bg-stone-950/30 border-b border-stone-200 dark:border-stone-800 flex items-center justify-between text-xs font-mono">
                    <div className="flex items-center space-x-2">
                        <span className="text-stone-500">AI PREDICTION:</span>
                        <span className={`font-bold uppercase ${analysis.prediction?.toLowerCase() === 'cancer' ? 'text-rose-500' : 'text-teal-400'}`}>
                            {analysis.prediction} ({(analysis.confidence * 100).toFixed(1)}%)
                        </span>
                    </div>
                    <div className="text-stone-500">
                        UNCERTAINTY σ²: <span className="font-bold text-stone-700 dark:text-stone-300">{(analysis.uncertainty || 0).toFixed(4)}</span>
                    </div>
                </div>

                {/* Modal Body Form */}
                <form onSubmit={handleSubmit} className="p-6 space-y-5">
                    {error && (
                        <div className="p-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/50 flex items-center space-x-2 text-rose-700 dark:text-rose-300 text-xs font-mono">
                            <AlertCircle className="w-4 h-4 flex-shrink-0" />
                            <span>{error}</span>
                        </div>
                    )}

                    {successMessage && (
                        <div className="p-3 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900/50 flex items-center space-x-2 text-emerald-700 dark:text-emerald-300 text-xs font-mono">
                            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                            <span>{successMessage}</span>
                        </div>
                    )}

                    {/* Ground Truth Diagnosis */}
                    <div>
                        <label className="block font-mono text-xs text-stone-600 dark:text-stone-400 mb-1.5 uppercase font-medium">
                            Definitive Histopathological Diagnosis
                        </label>
                        <select
                            value={groundTruthDx}
                            onChange={(e) => setGroundTruthDx(e.target.value)}
                            className="w-full px-3 py-2 bg-stone-50 dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-xs font-sans focus:outline-hidden focus:border-clinical-teal"
                            disabled={submitting}
                        >
                            {GROUND_TRUTH_OPTIONS.map((opt) => (
                                <option key={opt.value} value={opt.value}>
                                    [{opt.tier}] {opt.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Biopsy Proven Confirmation Checkbox */}
                    <div className="p-3 border border-stone-200 dark:border-stone-800 bg-stone-50/50 dark:bg-stone-950/50 flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <input
                                type="checkbox"
                                id="biopsy_proven_cb"
                                checked={biopsyProven}
                                onChange={(e) => setBiopsyProven(e.target.checked)}
                                className="w-4 h-4 text-clinical-teal bg-stone-100 border-stone-300 rounded-xs focus:ring-clinical-teal"
                                disabled={submitting}
                            />
                            <label htmlFor="biopsy_proven_cb" className="cursor-pointer">
                                <div className="text-xs font-semibold text-stone-900 dark:text-stone-100">
                                    Biopsy-Proven Histological Confirmation
                                </div>
                                <div className="text-[11px] text-stone-500">
                                    Verified via formal scalpel punch/incisional biopsy pathology report.
                                </div>
                            </label>
                        </div>
                        <ShieldCheck className={`w-5 h-5 ${biopsyProven ? 'text-clinical-teal' : 'text-stone-400'}`} />
                    </div>

                    {/* Histological Differentiation Grade */}
                    <div>
                        <label className="block font-mono text-xs text-stone-600 dark:text-stone-400 mb-1.5 uppercase font-medium">
                            Histological Differentiation Grade
                        </label>
                        <select
                            value={histologyGrade}
                            onChange={(e) => setHistologyGrade(e.target.value)}
                            className="w-full px-3 py-2 bg-stone-50 dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-xs font-sans focus:outline-hidden focus:border-clinical-teal"
                            disabled={submitting}
                        >
                            {HISTOLOGY_GRADES.map((g) => (
                                <option key={g.value} value={g.value}>
                                    {g.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Pathology Accession / Clinical Notes */}
                    <div>
                        <label className="block font-mono text-xs text-stone-600 dark:text-stone-400 mb-1.5 uppercase font-medium">
                            Pathology Notes & Lab Docket Number
                        </label>
                        <textarea
                            rows={3}
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                            placeholder="e.g. Lab Accession #PATH-2026-8941. Infiltrative margins confirmed with negative lymphovascular invasion."
                            className="w-full px-3 py-2 bg-stone-50 dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-xs font-mono focus:outline-hidden focus:border-clinical-teal"
                            disabled={submitting}
                        />
                    </div>

                    {/* Modal Actions */}
                    <div className="flex items-center justify-end space-x-3 pt-3 border-t border-stone-200 dark:border-stone-800">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 text-xs font-mono text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-100 transition-colors"
                            disabled={submitting}
                        >
                            CANCEL
                        </button>
                        <button
                            type="submit"
                            disabled={submitting}
                            className="flex items-center space-x-2 px-5 py-2 bg-clinical-teal text-white hover:bg-teal-600 text-xs font-mono font-semibold transition-all duration-150 disabled:opacity-50 shadow-xs"
                        >
                            {submitting ? (
                                <>
                                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                    <span>COMMITTING...</span>
                                </>
                            ) : (
                                <>
                                    <CheckCircle2 className="w-3.5 h-3.5" />
                                    <span>SUBMIT GROUND TRUTH</span>
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ClinicianVerificationModal;
