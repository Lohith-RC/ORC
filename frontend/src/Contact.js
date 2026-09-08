import React, { useState } from 'react';
import { Mail, MapPin, Send, CheckCircle2, Phone, AlertTriangle, Hospital, ShieldCheck, Clock } from 'lucide-react';

const Contact = () => {
    const [sent, setSent] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [form, setForm] = useState({
        name: '',
        email: '',
        institution: '',
        urgency: 'Routine Consultation (< 48h)',
        message: ''
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        setSubmitting(true);
        setTimeout(() => {
            setSubmitting(false);
            setSent(true);
        }, 700);
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-[#080B10] text-slate-800 dark:text-slate-100 py-16 px-4 sm:px-6 lg:px-8 font-sans transition-colors">
            <div className="max-w-6xl mx-auto space-y-12">
                {/* Header */}
                <div className="border-b border-slate-200 dark:border-slate-800 pb-8 text-center max-w-3xl mx-auto space-y-3">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-rose-500/30 bg-rose-500/10 font-mono text-[11px] tracking-wider uppercase text-rose-600 dark:text-rose-400 font-semibold">
                        <span className="w-2 h-2 bg-rose-500 rounded-full animate-pulse"></span>
                        CLINICAL REFERRAL & TELE-ONCOLOGY DESK
                    </div>
                    <h1 className="text-4xl sm:text-5xl font-serif text-slate-900 dark:text-white font-normal tracking-tight">
                        Head & Neck Oncology Referral Gateway
                    </h1>
                    <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 max-w-2xl mx-auto font-light leading-relaxed">
                        Expedited clinical communications for suspicious oral lesions, second-opinion telepathology consultations, and HL7 FHIR hospital integration inquiries.
                    </p>
                </div>

                {/* Emergency Red Warning Banner */}
                <div className="p-4 rounded-xl border border-amber-500/30 bg-amber-500/10 flex items-start gap-3.5">
                    <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                    <div className="text-xs text-amber-900 dark:text-amber-200 leading-relaxed font-sans">
                        <strong className="font-semibold block mb-0.5">Emergency Triage Notice:</strong>
                        Patients exhibiting non-healing indurated oral ulcerations lasting &gt;2 weeks, fixed cervical lymphadenopathy, or progressive trismus must be immediately referred to a specialized tertiary maxillofacial surgical center without waiting for digital consultation.
                    </div>
                </div>

                <div className="grid lg:grid-cols-12 gap-8 items-start">
                    {/* Left: Contact Form (7 cols) */}
                    <div className="lg:col-span-7 p-8 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm">
                        <div className="font-mono text-[10px] text-teal-600 dark:text-teal-400 uppercase tracking-widest mb-6 border-b border-slate-100 dark:border-slate-800 pb-3 font-semibold">
                            INSTITUTIONAL CLINICAL TRANSMISSION
                        </div>

                        {sent ? (
                            <div className="py-12 text-center space-y-3">
                                <div className="w-14 h-14 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 flex items-center justify-center mx-auto">
                                    <CheckCircle2 className="w-8 h-8" />
                                </div>
                                <h3 className="text-xl font-serif text-slate-900 dark:text-white font-medium">
                                    Clinical Case Logged
                                </h3>
                                <p className="text-xs text-slate-500 max-w-sm mx-auto font-light">
                                    Your transmission has been forwarded to the on-call oral oncology review coordinator. Escalation reference: <span className="font-mono text-teal-600 dark:text-teal-400 font-semibold">ONC-{Math.floor(100000 + Math.random() * 900000)}</span>.
                                </p>
                                <button
                                    type="button"
                                    onClick={() => setSent(false)}
                                    className="mt-4 px-4 py-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-mono text-slate-700 dark:text-slate-300 hover:bg-slate-200"
                                >
                                    Log Another Inquiry
                                </button>
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit} className="space-y-4 font-sans text-xs">
                                <div>
                                    <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1">
                                        Practitioner Name & Clinical Qualifications *
                                    </label>
                                    <input 
                                        type="text" 
                                        required
                                        value={form.name}
                                        onChange={(e) => setForm({ ...form, name: e.target.value })}
                                        placeholder="Dr. Rajesh Sharma, MDS (Oral Pathology)"
                                        className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                    />
                                </div>

                                <div>
                                    <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1">
                                        Official Hospital / Institutional Email *
                                    </label>
                                    <input 
                                        type="email" 
                                        required
                                        value={form.email}
                                        onChange={(e) => setForm({ ...form, email: e.target.value })}
                                        placeholder="rajesh.sharma@kidwai-cancer.org"
                                        className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                    />
                                </div>

                                <div>
                                    <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1">
                                        Healthcare Institution / Oncology Center *
                                    </label>
                                    <input 
                                        type="text" 
                                        required
                                        value={form.institution}
                                        onChange={(e) => setForm({ ...form, institution: e.target.value })}
                                        placeholder="Kidwai Memorial Institute of Oncology, Bangalore"
                                        className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                    />
                                </div>

                                <div>
                                    <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1">
                                        Triage Urgency Category
                                    </label>
                                    <select
                                        value={form.urgency}
                                        onChange={(e) => setForm({ ...form, urgency: e.target.value })}
                                        className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none font-mono"
                                    >
                                        <option>Routine Consultation (&lt; 48 hours)</option>
                                        <option>Suspected Invasive OSCC (Urgent Telepathology &lt; 24h)</option>
                                        <option>Rapid Growth Lesion (Longitudinal Velocity Alert)</option>
                                        <option>EHR / FHIR System Integration Collaboration</option>
                                    </select>
                                </div>

                                <div>
                                    <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1">
                                        Clinical Synopsis / Case Details *
                                    </label>
                                    <textarea 
                                        rows={4} 
                                        required
                                        value={form.message}
                                        onChange={(e) => setForm({ ...form, message: e.target.value })}
                                        placeholder="Provide patient anonymized age, lesion anatomical site, clinical duration, and specific queries regarding histopathological concordance..."
                                        className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                    ></textarea>
                                </div>

                                <button 
                                    type="submit" 
                                    disabled={submitting}
                                    className="w-full py-3 px-6 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-mono text-xs tracking-wider uppercase font-semibold flex items-center justify-center gap-2 shadow-lg shadow-teal-500/20 transition-all disabled:opacity-50"
                                >
                                    {submitting ? (
                                        <span>Dispatching to Review Board...</span>
                                    ) : (
                                        <>
                                            <Send className="w-4 h-4" />
                                            <span>Transmit Case to Review Board</span>
                                        </>
                                    )}
                                </button>
                            </form>
                        )}
                    </div>

                    {/* Right: Tertiary Centers & Directory (5 cols) */}
                    <div className="lg:col-span-5 space-y-6">
                        <div className="p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm space-y-5">
                            <h2 className="text-base font-serif font-medium text-slate-900 dark:text-white flex items-center gap-2">
                                <Hospital className="w-5 h-5 text-teal-500" />
                                <span>Tertiary Head & Neck Triage Hubs</span>
                            </h2>

                            <div className="space-y-3 font-mono text-xs">
                                <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700/50 space-y-1">
                                    <span className="text-[10px] text-rose-500 font-bold block">NATIONAL CANCER GRID</span>
                                    <div className="font-semibold text-slate-800 dark:text-slate-100 font-sans">Maxillofacial Oncology Division</div>
                                    <div className="text-slate-500 text-[11px] flex items-center gap-1.5 mt-1">
                                        <Phone className="w-3.5 h-3.5 text-slate-400" />
                                        <span>Hotline: +91 (080) 2698-4000</span>
                                    </div>
                                </div>

                                <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700/50 space-y-1">
                                    <span className="text-[10px] text-teal-600 dark:text-teal-400 font-bold block">TELE-ONCOLOGY DESK</span>
                                    <div className="font-semibold text-slate-800 dark:text-slate-100 font-sans">Regional Comprehensive Cancer Center</div>
                                    <div className="text-slate-500 text-[11px] flex items-center gap-1.5 mt-1">
                                        <Mail className="w-3.5 h-3.5 text-slate-400" />
                                        <span>triage@visionarydiagnostics.org</span>
                                    </div>
                                </div>

                                <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700/50 space-y-1">
                                    <span className="text-[10px] text-slate-500 font-bold block">RESEARCH LAB COORDINATES</span>
                                    <div className="font-semibold text-slate-800 dark:text-slate-100 font-sans">Oral Pathology AI Consortium</div>
                                    <div className="text-slate-500 text-[11px] flex items-center gap-1.5 mt-1">
                                        <MapPin className="w-3.5 h-3.5 text-slate-400" />
                                        <span>Bangalore, Karnataka, India</span>
                                    </div>
                                </div>
                            </div>

                            <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center gap-2 text-xs font-mono text-emerald-600 dark:text-emerald-400">
                                <ShieldCheck className="w-4 h-4 shrink-0" />
                                <span>End-to-End Encrypted Clinical Messaging Channel</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Contact;