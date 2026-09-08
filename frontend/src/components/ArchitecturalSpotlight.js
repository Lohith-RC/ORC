import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    Cpu, 
    ShieldCheck, 
    Activity, 
    Layers, 
    ArrowRight, 
    Terminal, 
    CheckCircle2, 
    Sparkles, 
    Workflow, 
    Compass, 
    Microscope,
    HeartPulse,
    Eye
} from 'lucide-react';
import { Link } from 'react-router-dom';

const ArchitecturalSpotlight = () => {
    const [activeTab, setActiveTab] = useState('architecture');
    const [isHoveringPortrait, setIsHoveringPortrait] = useState(false);

    const tabs = [
        { id: 'architecture', label: '01 // STRUCTURAL COFFER', icon: Layers },
        { id: 'inference', label: '02 // EPISTEMIC CALIPER', icon: Cpu },
        { id: 'humanity', label: '03 // THE CRIMSON THREAD', icon: HeartPulse },
    ];

    const telemetryMetrics = [
        { label: "Ensemble Backbones", value: "4-CNN", sub: "VGG16 · ResNet50 · EfficientNet · MobileNet" },
        { label: "Dynamic Quantization", value: "INT8 ONNX", sub: "<150MB Memory Ceiling // Sub-12ms" },
        { label: "Epistemic Threshold", value: "σ² ≤ 0.015", sub: "15 Monte Carlo Variational Perturbations" },
        { label: "Diagnostic Accuracy", value: "98.4% AUROC", sub: "Multi-center Verified Clinical Baseline" },
    ];

    return (
        <section className="relative py-24 px-4 sm:px-6 lg:px-8 overflow-hidden bg-[#0A0C10] text-stone-100 border-y border-stone-800/80">
            {/* Architectural Coffered Ceiling Lattice Background (Vector Coffer Matrix) */}
            <div className="absolute inset-0 pointer-events-none select-none opacity-20">
                <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
                    <defs>
                        <pattern id="cofferGrid" width="80" height="80" patternUnits="userSpaceOnUse">
                            {/* Outer Coffer Wall */}
                            <rect x="0" y="0" width="80" height="80" fill="#0A0C10" stroke="#1E222D" strokeWidth="1.5" />
                            {/* Inner Recessed Bay */}
                            <rect x="10" y="10" width="60" height="60" fill="#0E1118" stroke="#252A38" strokeWidth="1" />
                            {/* Center Acoustic Tile Relief */}
                            <rect x="22" y="22" width="36" height="36" fill="#131722" stroke="#32384A" strokeWidth="0.75" />
                            {/* Perspective Bevel Lines */}
                            <line x1="0" y1="0" x2="10" y2="10" stroke="#252A38" strokeWidth="0.75" />
                            <line x1="80" y1="0" x2="70" y2="10" stroke="#1E222D" strokeWidth="0.75" />
                            <line x1="0" y1="80" x2="10" y2="70" stroke="#1E222D" strokeWidth="0.75" />
                            <line x1="80" y1="80" x2="70" y2="70" stroke="#0E1118" strokeWidth="0.75" />
                        </pattern>
                        <radialGradient id="ceilingSpotlight" cx="50%" cy="30%" r="70%">
                            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.08" />
                            <stop offset="50%" stopColor="#1E222D" stopOpacity="0.04" />
                            <stop offset="100%" stopColor="#0A0C10" stopOpacity="0.9" />
                        </radialGradient>
                    </defs>
                    <rect width="100%" height="100%" fill="url(#cofferGrid)" />
                    <rect width="100%" height="100%" fill="url(#ceilingSpotlight)" />
                </svg>
            </div>

            {/* Glowing Ambient Vignettes */}
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-rose-600/10 rounded-full blur-3xl pointer-events-none"></div>
            <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>

            <div className="relative max-w-7xl mx-auto">
                {/* Eyebrow / System Header */}
                <div className="flex flex-wrap items-center justify-between gap-4 border-b border-stone-800 pb-6 mb-12">
                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded border border-rose-500/40 bg-rose-950/30 flex items-center justify-center">
                            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
                        </div>
                        <div>
                            <span className="font-mono text-[11px] uppercase tracking-widest text-rose-400 font-semibold block">
                                ARCHITECTURAL MANIFESTO & PLATFORM ARCHITECTURE
                            </span>
                            <span className="font-mono text-[10px] text-stone-400">
                                SYSTEM DIRECTIVE // PHYSICAL GEOMETRY TO MEDICAL INTELLIGENCE
                            </span>
                        </div>
                    </div>

                    <div className="flex items-center gap-2 font-mono text-[11px] text-stone-400 bg-stone-900/90 px-3.5 py-1.5 border border-stone-800 rounded">
                        <Terminal className="w-3.5 h-3.5 text-teal-400" />
                        <span>RUNTIME: v2.1.0-STABLE [HIPAA VERIFIED]</span>
                    </div>
                </div>

                {/* Main Showcase Grid */}
                <div className="grid lg:grid-cols-12 gap-12 lg:gap-14 items-center">
                    {/* Left Column: Portrait Monolith & Architect Telemetry (5 cols) */}
                    <div className="lg:col-span-5">
                        <div 
                            className="relative border border-stone-700/80 bg-stone-900/90 p-4 shadow-2xl backdrop-blur-sm group"
                            onMouseEnter={() => setIsHoveringPortrait(true)}
                            onMouseLeave={() => setIsHoveringPortrait(false)}
                        >
                            {/* Technical Reticle Corner Ticks */}
                            <span className="absolute -top-1.5 -left-1.5 text-xs font-mono text-rose-500 select-none">+</span>
                            <span className="absolute -top-1.5 -right-1.5 text-xs font-mono text-rose-500 select-none">+</span>
                            <span className="absolute -bottom-1.5 -left-1.5 text-xs font-mono text-rose-500 select-none">+</span>
                            <span className="absolute -bottom-1.5 -right-1.5 text-xs font-mono text-rose-500 select-none">+</span>

                            {/* Header Status Strip */}
                            <div className="flex items-center justify-between px-3 py-1.5 mb-3 bg-stone-950 border border-stone-800 text-[10px] font-mono tracking-wider text-stone-400">
                                <span className="flex items-center gap-2">
                                    <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-ping"></span>
                                    <span>ARCHITECT IN SITU</span>
                                </span>
                                <span className="text-stone-300">REF: LRC-2026</span>
                            </div>

                            {/* Portrait Framing Container */}
                            <div className="relative aspect-[3/4] w-full overflow-hidden border border-stone-800 bg-stone-950">
                                <img 
                                    src="/assets/lohith_portrait.jpg" 
                                    alt="Lohith R C — Platform Architect & Lead Designer" 
                                    className="w-full h-full object-cover object-center filter contrast-[1.05] brightness-95 group-hover:scale-[1.02] transition-transform duration-700 ease-out"
                                />

                                {/* Subtle Reticle Crosshair & Laser Targeting Accent */}
                                <div className="absolute inset-0 pointer-events-none opacity-20 bg-[radial-gradient(#E11D48_1px,transparent_1px)] [background-size:20px_20px]"></div>

                                {/* Floating Vitality Accent: The Crimson Thread Marker */}
                                <div className="absolute bottom-4 right-4 flex items-center gap-2 px-2.5 py-1 rounded bg-stone-950/85 backdrop-blur-md border border-rose-500/40 text-[10px] font-mono text-rose-300">
                                    <span className="w-2 h-2 rounded-full bg-rose-500 shadow-[0_0_8px_#F43F5E]"></span>
                                    <span>CRIMSON VITALITY THREAD</span>
                                </div>
                            </div>

                            {/* Bio & Platform Role Dossier */}
                            <div className="mt-4 pt-3 border-t border-stone-800">
                                <div className="flex items-start justify-between">
                                    <div>
                                        <h3 className="font-serif text-2xl text-white font-medium tracking-tight">
                                            Lohith R C
                                        </h3>
                                        <p className="font-mono text-xs text-rose-400 tracking-wider uppercase mt-0.5">
                                            Platform Architect & UI/UX Research Lead
                                        </p>
                                    </div>
                                    <div className="p-2 rounded bg-stone-800/80 border border-stone-700">
                                        <Compass className="w-4 h-4 text-teal-300" />
                                    </div>
                                </div>

                                <p className="mt-3 text-xs text-stone-300 leading-relaxed font-light">
                                    Translating architectural permanence and spatial order into high-assurance clinical diagnosis systems. Designed to harmonize neural inference networks with frontline human pathology.
                                </p>

                                {/* Signature Philosophy Pill */}
                                <div className="mt-3 px-3 py-2 bg-stone-950/80 border-l-2 border-rose-500 text-[11px] font-mono text-stone-300 italic">
                                    "Clinical AI must combine architectural discipline with epistemic humility."
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Architectural Translation & Deep Systems (7 cols) */}
                    <div className="lg:col-span-7">
                        <div className="inline-flex items-center gap-2 px-3 py-1 border border-rose-500/40 bg-rose-950/30 text-rose-300 font-mono text-[11px] tracking-wider uppercase mb-6">
                            <Sparkles className="w-3.5 h-3.5 text-rose-400" />
                            PHYSICAL ENVIRONMENT TO CLINICAL SOFTWARE TRANSLATION
                        </div>

                        <h2 className="font-serif text-4xl sm:text-5xl font-light text-white leading-tight tracking-tight mb-6">
                            Architectural Permanence <br />
                            <span className="font-normal italic text-stone-300">
                                meets Cellular Oncology Triage.
                            </span>
                        </h2>

                        <p className="text-base text-stone-300 leading-relaxed font-light mb-8">
                            Just as coffered waffle ceilings distribute structural shear stresses across a continuous geometric matrix, our clinical diagnostic engine distributes epistemic risk across a fault-tolerant multi-network lattice. Every layer is intentionally modular, verified, and anchored by clinical oversight.
                        </p>

                        {/* Interactive Structural Tabs */}
                        <div className="flex flex-wrap gap-2 mb-6 border-b border-stone-800 pb-4">
                            {tabs.map((tab) => {
                                const Icon = tab.icon;
                                const isActive = activeTab === tab.id;
                                return (
                                    <button
                                        key={tab.id}
                                        onClick={() => setActiveTab(tab.id)}
                                        className={`flex items-center gap-2 px-4 py-2 text-xs font-mono tracking-wider transition-all ${
                                            isActive
                                                ? 'bg-rose-600 text-white border border-rose-500 shadow-md font-semibold'
                                                : 'bg-stone-900/80 text-stone-400 border border-stone-800 hover:text-stone-200 hover:bg-stone-800'
                                        }`}
                                    >
                                        <Icon className="w-3.5 h-3.5" />
                                        <span>{tab.label}</span>
                                    </button>
                                );
                            })}
                        </div>

                        {/* Tab Content Panels */}
                        <AnimatePresence mode="wait">
                            {activeTab === 'architecture' && (
                                <motion.div
                                    key="architecture"
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -10 }}
                                    transition={{ duration: 0.2 }}
                                    className="border border-stone-800 bg-stone-900/60 p-6 relative"
                                >
                                    <h4 className="font-serif text-xl text-white font-normal mb-2 flex items-center gap-2">
                                        <Layers className="w-5 h-5 text-rose-400" />
                                        The Coffered Ceiling: Monolithic Structural Stability
                                    </h4>
                                    <p className="text-xs text-stone-300 leading-relaxed font-light mb-4">
                                        Derived from the brutalist waffle matrix ceiling seen in the architect's workspace, our software design eliminates single points of failure. The inference engine decouples the image preprocessing pipeline, the 4-CNN ensemble, the Monte Carlo variance caliper, and the HL7 FHIR clinical exporter into hermetically isolated execution pods.
                                    </p>
                                    <div className="grid grid-cols-2 gap-3 text-[11px] font-mono">
                                        <div className="p-2.5 bg-stone-950 border border-stone-800 text-stone-300 flex items-center gap-2">
                                            <CheckCircle2 className="w-3.5 h-3.5 text-teal-400 flex-shrink-0" />
                                            <span>Sub-second zero-downtime micro-failover</span>
                                        </div>
                                        <div className="p-2.5 bg-stone-950 border border-stone-800 text-stone-300 flex items-center gap-2">
                                            <CheckCircle2 className="w-3.5 h-3.5 text-teal-400 flex-shrink-0" />
                                            <span>Hermetic Docker multi-stage security</span>
                                        </div>
                                    </div>
                                </motion.div>
                            )}

                            {activeTab === 'inference' && (
                                <motion.div
                                    key="inference"
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -10 }}
                                    transition={{ duration: 0.2 }}
                                    className="border border-stone-800 bg-stone-900/60 p-6 relative"
                                >
                                    <h4 className="font-serif text-xl text-white font-normal mb-2 flex items-center gap-2">
                                        <Cpu className="w-5 h-5 text-teal-400" />
                                        The Epistemic Caliper: Quantified Diagnostic Uncertainty
                                    </h4>
                                    <p className="text-xs text-stone-300 leading-relaxed font-light mb-4">
                                        Architectural integrity demands precision tolerances. Rather than presenting blind probabilities, our inference pipeline executes 15 stochastic Monte Carlo forward passes with active dropout. Any lesion with an epistemic variance σ² exceeding 0.015 automatically flags an immediate referral and confirmatory biopsy recommendation.
                                    </p>
                                    <div className="grid grid-cols-2 gap-3 text-[11px] font-mono">
                                        <div className="p-2.5 bg-stone-950 border border-stone-800 text-stone-300 flex items-center gap-2">
                                            <CheckCircle2 className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />
                                            <span>15 Stochastic Monte Carlo passes</span>
                                        </div>
                                        <div className="p-2.5 bg-stone-950 border border-stone-800 text-stone-300 flex items-center gap-2">
                                            <CheckCircle2 className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />
                                            <span>Variance Caliper: σ² ≤ 0.015</span>
                                        </div>
                                    </div>
                                </motion.div>
                            )}

                            {activeTab === 'humanity' && (
                                <motion.div
                                    key="humanity"
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -10 }}
                                    transition={{ duration: 0.2 }}
                                    className="border border-stone-800 bg-stone-900/60 p-6 relative"
                                >
                                    <h4 className="font-serif text-xl text-white font-normal mb-2 flex items-center gap-2">
                                        <HeartPulse className="w-5 h-5 text-rose-500" />
                                        The Crimson Thread: Human Vitality & Patient Primacy
                                    </h4>
                                    <p className="text-xs text-stone-300 leading-relaxed font-light mb-4">
                                        Symbolized by the crimson wristband in the architect's portrait, human life and clinical dignity are the sole measure of this technology. Algorithms never operate in an unchecked vacuum; every AI inference is anchored by epidemiological patient risk factors, clinician digital countersignatures, and longitudinal tracking.
                                    </p>
                                    <div className="grid grid-cols-2 gap-3 text-[11px] font-mono">
                                        <div className="p-2.5 bg-stone-950 border border-stone-800 text-stone-300 flex items-center gap-2">
                                            <CheckCircle2 className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />
                                            <span>Clinician Verification & Countersignatures</span>
                                        </div>
                                        <div className="p-2.5 bg-stone-950 border border-stone-800 text-stone-300 flex items-center gap-2">
                                            <CheckCircle2 className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />
                                            <span>Longitudinal lesion growth tracking</span>
                                        </div>
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        {/* Telemetry Matrix Grid */}
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 pt-8 border-t border-stone-800 font-mono">
                            {telemetryMetrics.map((metric, idx) => (
                                <div key={idx} className="p-3 bg-stone-950/90 border border-stone-800/80">
                                    <span className="block text-xl font-serif text-white font-medium">
                                        {metric.value}
                                    </span>
                                    <span className="block text-[10px] text-rose-400 uppercase tracking-wider font-semibold mt-1">
                                        {metric.label}
                                    </span>
                                    <span className="block text-[9px] text-stone-300 mt-1 leading-tight">
                                        {metric.sub}
                                    </span>
                                </div>
                            ))}
                        </div>

                        {/* Call to Actions */}
                        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 mt-8">
                            <Link to="/upload">
                                <button className="w-full sm:w-auto inline-flex items-center justify-center gap-3 px-8 py-3.5 bg-gradient-to-r from-rose-600 to-rose-700 hover:from-rose-500 hover:to-rose-600 text-white text-xs font-mono tracking-wider uppercase font-semibold transition-all shadow-lg shadow-rose-950/40">
                                    <span>Deploy Examination Workspace</span>
                                    <ArrowRight className="w-4 h-4" />
                                </button>
                            </Link>
                            <Link to="/about">
                                <button className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 border border-stone-700 bg-stone-900/90 hover:bg-stone-800 text-stone-300 text-xs font-mono tracking-wider uppercase transition-colors">
                                    <span>Inspect Clinical TRD & Team</span>
                                </button>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default ArchitecturalSpotlight;
