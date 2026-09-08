import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, HeartPulse, Compass, ExternalLink, Activity, Phone, Mail } from 'lucide-react';

export default function Footer({ onOpenManifesto }) {
    return (
        <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-[#070A0F] text-slate-600 dark:text-slate-400 font-sans transition-colors">
            {/* Top Institutional Strip */}
            <div className="border-b border-slate-100 dark:border-slate-900 py-4 px-4 sm:px-6 lg:px-8 bg-slate-50/50 dark:bg-slate-950/40">
                <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-xs font-mono">
                    <div className="flex items-center gap-2 text-teal-600 dark:text-teal-400">
                        <ShieldCheck className="w-4 h-4 text-teal-500" />
                        <span className="font-medium">HL7 FHIR R4 & DICOM Standards Ready · End-to-End Encrypted Triage</span>
                    </div>
                    <div className="flex items-center gap-4 text-slate-500">
                        <span>Bangalore Oncology Research Consortium</span>
                        <span>•</span>
                        <span>Karnataka, India</span>
                    </div>
                </div>
            </div>

            {/* Main Multi-column Directory */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
                <div className="grid grid-cols-1 md:grid-cols-12 gap-10">
                    {/* Brand Col (5 cols) */}
                    <div className="md:col-span-5 space-y-4">
                        <div className="flex items-center gap-3">
                            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-600 to-teal-700 flex items-center justify-center text-white shadow-md shadow-teal-600/20">
                                <HeartPulse className="w-5 h-5 text-white" />
                            </div>
                            <div>
                                <span className="font-serif text-xl font-medium tracking-tight text-slate-900 dark:text-white block">
                                    Visionary Diagnostics
                                </span>
                                <span className="font-mono text-[9px] uppercase tracking-widest text-slate-400">
                                    Clinical OSCC AI Triage & Longitudinal Platform
                                </span>
                            </div>
                        </div>

                        <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm leading-relaxed font-light">
                            Enterprise clinical decision support instrument engineered for point-of-care oral cancer screening. Integrating native PyTorch Grad-CAM++ layer activation, Reinhard mucosal color normalization, and WHO 4-tier ordinal pathology triage.
                        </p>

                        <div className="pt-2 flex items-center gap-2">
                            <Compass className="w-4 h-4 text-amber-500" />
                            <span className="font-mono text-xs text-slate-700 dark:text-slate-300">
                                System Architect & Lead UI/UX: <strong className="font-semibold text-slate-900 dark:text-white">Lohith R C</strong>
                            </span>
                        </div>
                    </div>

                    {/* Scientific Protocols (3 cols) */}
                    <div className="md:col-span-3 space-y-3">
                        <h4 className="font-mono text-xs font-semibold text-slate-900 dark:text-slate-200 uppercase tracking-wider">
                            Clinical Framework
                        </h4>
                        <ul className="space-y-2 font-mono text-xs text-slate-500 dark:text-slate-400">
                            <li>• Native PyTorch Grad-CAM++</li>
                            <li>• Reinhard LAB Color Transfer</li>
                            <li>• Specular Saliva Glare Filter</li>
                            <li>• 4-Class Ordinal Triage (0–3)</li>
                            <li>• AJCC 8th TNM Staging</li>
                            <li>• HL7 FHIR R4 Bundle Export</li>
                        </ul>
                    </div>

                    {/* Investigators & Guidance (4 cols) */}
                    <div className="md:col-span-4 space-y-3">
                        <h4 className="font-mono text-xs font-semibold text-slate-900 dark:text-slate-200 uppercase tracking-wider">
                            Institutional Guidance & Team
                        </h4>
                        <div className="space-y-2 text-xs">
                            <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800/80">
                                <span className="font-mono text-[10px] text-teal-600 dark:text-teal-400 block font-medium">PROJECT GUIDANCE</span>
                                <span className="font-semibold text-slate-800 dark:text-slate-200">Prof. Aishwarya S</span>
                                <p className="text-[11px] text-slate-500">Department of Computer Science & Engineering</p>
                            </div>
                            <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800/80">
                                <span className="font-mono text-[10px] text-teal-600 dark:text-teal-400 block font-medium">CORE INVESTIGATORS</span>
                                <span className="font-medium text-slate-700 dark:text-slate-300">Keerthi A · Rakshith Y B · Lohith R C</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Bottom Legal & Ethics Bar */}
                <div className="mt-12 pt-6 border-t border-slate-200 dark:border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] font-mono text-slate-400">
                    <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400">
                        <Activity className="w-3.5 h-3.5 shrink-0" />
                        <span>CLINICAL MANDATE: FOR ADJUVANT TRIAGE ONLY. NOT A REPLACEMENT FOR SCALPEL HISTOPATHOLOGY.</span>
                    </div>
                    <div>
                        &copy; {new Date().getFullYear()} Visionary Diagnostics Consortium. All rights reserved.
                    </div>
                </div>
            </div>
        </footer>
    );
}
