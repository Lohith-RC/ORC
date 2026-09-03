import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    Microscope, 
    ArrowRight, 
    Activity, 
    ShieldCheck, 
    Layers, 
    Sparkles, 
    FileText, 
    Check, 
    AlertCircle, 
    SlidersHorizontal,
    CornerDownRight
} from 'lucide-react';
import { Link } from 'react-router-dom';

import heroImage from './images/1.jpg';
import detailedFeatureImage from './images/8.webp';

// --- Interactive Pathologist's Inspection Viewport with Magnifying Loupe ---
const PathologistLoupeViewer = () => {
    const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
    const [isHovered, setIsHovered] = useState(false);
    const [zoomPos, setZoomPos] = useState({ x: 50, y: 50 });
    const containerRef = useRef(null);

    const handleMouseMove = (e) => {
        if (!containerRef.current) return;
        const rect = containerRef.current.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const xPct = Math.max(0, Math.min(100, (x / rect.width) * 100));
        const yPct = Math.max(0, Math.min(100, (y / rect.height) * 100));

        setMousePos({ x, y });
        setZoomPos({ x: xPct, y: yPct });
    };

    return (
        <div className="relative w-full">
            {/* Corner Ticks */}
            <span className="absolute -top-2 -left-2 text-[11px] font-mono text-stone-400 select-none">+</span>
            <span className="absolute -top-2 -right-2 text-[11px] font-mono text-stone-400 select-none">+</span>
            <span className="absolute -bottom-2 -left-2 text-[11px] font-mono text-stone-400 select-none">+</span>
            <span className="absolute -bottom-2 -right-2 text-[11px] font-mono text-stone-400 select-none">+</span>

            {/* Viewport Card */}
            <div 
                ref={containerRef}
                onMouseMove={handleMouseMove}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                className="relative rounded-none overflow-hidden border border-stone-300 dark:border-stone-800 bg-stone-100 dark:bg-stone-900 cursor-crosshair group shadow-xl"
            >
                {/* Specimen Header Metadata Strip */}
                <div className="flex items-center justify-between px-4 py-2 border-b border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-950 font-mono text-[10px] tracking-wider text-stone-500 uppercase">
                    <span className="flex items-center gap-2">
                        <span className="w-1.5 h-1.5 bg-clinical-teal rounded-full animate-pulse"></span>
                        VIEWPORT // SPECIMEN-0428-A
                    </span>
                    <span>MAG: {isHovered ? '2.5X LOUPE' : '1.0X OVERVIEW'}</span>
                    <span>COORD: {Math.round(zoomPos.x * 4.8)}µm, {Math.round(zoomPos.y * 3.6)}µm</span>
                </div>

                {/* Main Clinical Image */}
                <div className="relative aspect-[4/3] w-full overflow-hidden bg-stone-950 select-none">
                    <img 
                        src={heroImage} 
                        alt="Oral Lesion Examination" 
                        className="w-full h-full object-cover filter contrast-[1.02] brightness-95"
                    />

                    {/* Reticle / Hairline Grid Overlay */}
                    <div className="absolute inset-0 pointer-events-none opacity-20 dark:opacity-30 bg-[radial-gradient(#1B5E54_1px,transparent_1px)] [background-size:24px_24px]"></div>

                    {/* Magnification Loupe on Hover */}
                    <AnimatePresence>
                        {isHovered && (
                            <motion.div 
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.8 }}
                                transition={{ duration: 0.15 }}
                                style={{
                                    left: `${mousePos.x - 70}px`,
                                    top: `${mousePos.y - 70}px`,
                                }}
                                className="pointer-events-none absolute w-36 h-36 rounded-full border-2 border-clinical-teal shadow-2xl overflow-hidden z-30 bg-stone-950"
                            >
                                <div 
                                    style={{
                                        backgroundImage: `url(${heroImage})`,
                                        backgroundPosition: `${zoomPos.x}% ${zoomPos.y}%`,
                                        backgroundSize: '350%',
                                        backgroundRepeat: 'no-repeat',
                                        width: '100%',
                                        height: '100%',
                                    }}
                                />
                                {/* Crosshair lines */}
                                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                                    <div className="w-full h-[0.5px] bg-clinical-teal/70"></div>
                                    <div className="h-full w-[0.5px] bg-clinical-teal/70 absolute"></div>
                                    <div className="w-4 h-4 border border-clinical-teal/60 rounded-full absolute"></div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Telemetry HUD Badge */}
                    <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between p-3 rounded bg-stone-950/85 backdrop-blur-md border border-stone-800/80 text-stone-200 font-mono text-[11px]">
                        <div className="flex items-center gap-3">
                            <div className="p-1.5 bg-clinical-teal/30 border border-clinical-teal/50 rounded">
                                <Activity className="w-3.5 h-3.5 text-teal-300" />
                            </div>
                            <div>
                                <span className="text-stone-400 block text-[9px] uppercase tracking-widest">Ensemble Confidence</span>
                                <span className="font-semibold text-white tracking-wide">96.8% [95.2% – 98.4%]</span>
                            </div>
                        </div>
                        <div className="text-right">
                            <span className="text-stone-400 block text-[9px] uppercase tracking-widest">Epistemic Variance</span>
                            <span className="text-emerald-400 font-medium">σ² = 0.007 (High Consensus)</span>
                        </div>
                    </div>
                </div>

                {/* Sub-strip: Model Votes */}
                <div className="grid grid-cols-4 divide-x divide-stone-200 dark:divide-stone-800 bg-stone-50 dark:bg-stone-950 border-t border-stone-200 dark:border-stone-800 font-mono text-[10px] text-stone-600 dark:text-stone-400 py-2 text-center">
                    <div>VGG16: <span className="text-stone-900 dark:text-stone-200 font-semibold">0.95</span></div>
                    <div>ResNet50: <span className="text-stone-900 dark:text-stone-200 font-semibold">0.98</span></div>
                    <div>EfficientNet: <span className="text-stone-900 dark:text-stone-200 font-semibold">0.97</span></div>
                    <div>MobileNet: <span className="text-stone-900 dark:text-stone-200 font-semibold">0.96</span></div>
                </div>
            </div>
            
            <p className="font-mono text-[10px] text-stone-400 text-center mt-2">
                HOVER TO ENGAGE MICROSCOPIC INSPECTION LOUPE // 2.5X OPTICAL MAGNIFICATION
            </p>
        </div>
    );
};

const Home = () => {
    return (
        <div className="bg-parchment-100 dark:bg-ink-950 text-stone-800 dark:text-stone-200 min-h-screen transition-colors font-sans selection:bg-clinical-teal/20">
            {/* Subdued Archival Grid Background */}
            <div className="fixed inset-0 pointer-events-none opacity-[0.035] dark:opacity-[0.05] bg-[radial-gradient(#1B5E54_1px,transparent_1px)] [background-size:32px_32px]"></div>

            {/* ============================================================ */}
            {/* HERO SECTION: Editorial Asymmetry                           */}
            {/* ============================================================ */}
            <section className="relative pt-16 pb-20 px-4 sm:px-6 lg:px-8 border-b border-stone-200/80 dark:border-stone-800/80">
                <div className="max-w-7xl mx-auto">
                    <div className="grid lg:grid-cols-12 gap-12 lg:gap-16 items-center">
                        {/* Left Editorial Narrative (7 cols) */}
                        <div className="lg:col-span-7">
                            <div className="inline-flex items-center gap-2 px-3 py-1 border border-stone-300 dark:border-stone-700 bg-stone-100/80 dark:bg-stone-900/80 text-stone-700 dark:text-stone-300 font-mono text-[11px] tracking-wider uppercase mb-8">
                                <span className="w-2 h-2 bg-clinical-teal rounded-none inline-block"></span>
                                PROTOCOL 01 // MULTIMODAL CLINICAL TRIAGE
                            </div>

                            <h1 className="font-serif text-5xl sm:text-6xl lg:text-7xl font-light tracking-tight text-stone-900 dark:text-stone-100 leading-[1.08] mb-6">
                                Early oral cancer detection, <br />
                                <span className="font-normal italic text-stone-600 dark:text-stone-400">
                                    refined by epistemic certainty.
                                </span>
                            </h1>

                            <p className="font-sans text-lg text-stone-600 dark:text-stone-300 max-w-2xl leading-relaxed font-normal mb-8">
                                A specialized clinical screening ecosystem that fuses a 4-architecture deep convolutional ensemble with Monte Carlo dropout uncertainty quantification and epidemiological risk stratification. Engineered as an authoritative triage instrument for clinicians and frontline screening.
                            </p>

                            {/* Key Performance Indicators */}
                            <div className="grid grid-cols-3 gap-6 py-6 border-y border-stone-200 dark:border-stone-800 my-8 font-mono">
                                <div>
                                    <span className="block text-2xl lg:text-3xl font-serif text-stone-900 dark:text-stone-100 font-normal">95.4%</span>
                                    <span className="text-[10px] uppercase tracking-wider text-stone-500">Ensemble Sensitivity</span>
                                </div>
                                <div>
                                    <span className="block text-2xl lg:text-3xl font-serif text-stone-900 dark:text-stone-100 font-normal">&lt;120ms</span>
                                    <span className="text-[10px] uppercase tracking-wider text-stone-500">Inference Latency</span>
                                </div>
                                <div>
                                    <span className="block text-2xl lg:text-3xl font-serif text-stone-900 dark:text-stone-100 font-normal">4-CNN</span>
                                    <span className="text-[10px] uppercase tracking-wider text-stone-500">Deep Architectures</span>
                                </div>
                            </div>

                            {/* Call to Action Buttons */}
                            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4">
                                <Link to="/upload">
                                    <button className="w-full sm:w-auto inline-flex items-center justify-center gap-3 px-8 py-3.5 bg-stone-900 dark:bg-stone-100 text-stone-100 dark:text-stone-900 text-sm font-mono tracking-wider uppercase font-semibold hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-all shadow-md">
                                        <span>Initialize Scan Dossier</span>
                                        <ArrowRight className="w-4 h-4" />
                                    </button>
                                </Link>
                                <Link to="/about">
                                    <button className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 border border-stone-300 dark:border-stone-700 text-stone-700 dark:text-stone-300 text-sm font-mono tracking-wider uppercase hover:bg-stone-100 dark:hover:bg-stone-900 transition-colors">
                                        <span>Review Clinical TRD</span>
                                    </button>
                                </Link>
                            </div>
                        </div>

                        {/* Right Examination Stage (5 cols) */}
                        <div className="lg:col-span-5">
                            <PathologistLoupeViewer />
                        </div>
                    </div>
                </div>
            </section>

            {/* ============================================================ */}
            {/* SECTION 2: The Classical Blindspot vs. The Diagnostic Triad */}
            {/* ============================================================ */}
            <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-b border-stone-200/80 dark:border-stone-800/80">
                <div className="mb-14">
                    <span className="font-mono text-xs text-clinical-teal uppercase tracking-widest block mb-2">
                        02 // CLINICAL ARCHITECTURE CRITIQUE
                    </span>
                    <h2 className="font-serif text-3xl sm:text-4xl text-stone-900 dark:text-stone-100 font-normal">
                        Why standard AI models fail in clinical practice
                    </h2>
                </div>

                <div className="grid md:grid-cols-2 gap-8">
                    {/* The Classical Blindspot Card */}
                    <div className="border border-red-200 dark:border-red-950/60 bg-red-50/30 dark:bg-red-950/10 p-8 rounded-none relative">
                        <div className="flex items-center gap-2 text-xs font-mono tracking-wider uppercase text-red-700 dark:text-red-400 mb-4">
                            <AlertCircle className="w-4 h-4" />
                            THE CLASSICAL BLINDSPOT (STANDARD AI)
                        </div>
                        <h3 className="font-serif text-2xl text-stone-900 dark:text-stone-100 font-medium mb-4">
                            Overconfident Softmax & Context Blindness
                        </h3>
                        <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed mb-6 font-light">
                            Traditional standalone neural networks force an overconfident binary output (0 or 1) regardless of image ambiguity, lighting corruption, or lesion edge blur. They evaluate pixels in isolation while ignoring patient tobacco, betel nut, and lesion chronicity.
                        </p>
                        <ul className="space-y-3 font-mono text-xs text-stone-600 dark:text-stone-400">
                            <li className="flex items-start gap-2">
                                <span className="text-red-500 font-bold">✕</span>
                                <span>Zero Epistemic Uncertainty: Cannot report "I am uncertain"</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="text-red-500 font-bold">✕</span>
                                <span>Domain-shift fragility against mobile camera lighting</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="text-red-500 font-bold">✕</span>
                                <span>Treats 70-year-old habitual tobacco users the same as non-smokers</span>
                            </li>
                        </ul>
                    </div>

                    {/* The Visionary Triad Card */}
                    <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900/60 p-8 rounded-none relative">
                        <div className="flex items-center gap-2 text-xs font-mono tracking-wider uppercase text-clinical-teal dark:text-teal-400 mb-4">
                            <ShieldCheck className="w-4 h-4" />
                            THE VISIONARY DIAGNOSTIC TRIAD
                        </div>
                        <h3 className="font-serif text-2xl text-stone-900 dark:text-stone-100 font-medium mb-4">
                            Ensemble Synthesis + Epistemic Caliper
                        </h3>
                        <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed mb-6 font-light">
                            Our architecture mitigates clinical risk through three coupled systems: a multi-model consensus voting engine, Monte Carlo variational dropout to quantify epistemic variance, and epidemiological Bayesian risk integration.
                        </p>
                        <ul className="space-y-3 font-mono text-xs text-stone-600 dark:text-stone-400">
                            <li className="flex items-start gap-2">
                                <span className="text-clinical-teal font-bold">✓</span>
                                <span>Multi-CNN Consensus (VGG16 + ResNet50 + EfficientNet + MobileNet)</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="text-clinical-teal font-bold">✓</span>
                                <span>15 Monte Carlo Perturbations quantify variance (σ² &gt; 0.015 flags biopsy)</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="text-clinical-teal font-bold">✓</span>
                                <span>Multimodal risk scoring adjusts triage thresholds dynamically</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </section>

            {/* ============================================================ */}
            {/* SECTION 3: 4-Stage Clinical Sequence                         */}
            {/* ============================================================ */}
            <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-b border-stone-200/80 dark:border-stone-800/80">
                <div className="mb-14">
                    <span className="font-mono text-xs text-clinical-teal uppercase tracking-widest block mb-2">
                        03 // CLINICAL PIPELINE STAGES
                    </span>
                    <h2 className="font-serif text-3xl sm:text-4xl text-stone-900 dark:text-stone-100 font-normal">
                        Rigorous diagnostic methodology
                    </h2>
                </div>

                <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    {[
                        {
                            step: "STAGE 01",
                            title: "Laplacian Quality Gate",
                            desc: "Images are inspected for motion blur using Laplacian variance. Corrupt or blurry captures are rejected before compute cycles are wasted.",
                            metric: "Threshold: Var > 50"
                        },
                        {
                            step: "STAGE 02",
                            title: "Test-Time Augmentation",
                            desc: "8 transformed passes (zoomed, rotated, flipped) evaluate the specimen to eliminate lighting or angle bias.",
                            metric: "Passes: 8-Fold TTA"
                        },
                        {
                            step: "STAGE 03",
                            title: "Monte Carlo Dropout",
                            desc: "Active dropout layers generate 15 stochastic forward passes to capture epistemic uncertainty and model disagreement.",
                            metric: "Uncertainty: σ² Variance"
                        },
                        {
                            step: "STAGE 04",
                            title: "Epidemiological Triage",
                            desc: "Computer vision predictions are fused with patient risk factors (tobacco, alcohol, betel nut, prior lesions) to output an authoritative report.",
                            metric: "Output: Clinical PDF"
                        }
                    ].map((item, idx) => (
                        <div key={idx} className="border border-stone-200 dark:border-stone-800 bg-stone-50/60 dark:bg-stone-900/40 p-6 flex flex-col justify-between">
                            <div>
                                <span className="font-mono text-[10px] tracking-widest text-stone-400 block mb-3">{item.step}</span>
                                <h3 className="font-serif text-xl font-normal text-stone-900 dark:text-stone-100 mb-3">{item.title}</h3>
                                <p className="text-xs text-stone-600 dark:text-stone-400 font-light leading-relaxed mb-6">{item.desc}</p>
                            </div>
                            <div className="pt-3 border-t border-stone-200 dark:border-stone-800 font-mono text-[10px] text-clinical-teal dark:text-teal-400 uppercase">
                                {item.metric}
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* ============================================================ */}
            {/* SECTION 4: Dignified Call to Action                           */}
            {/* ============================================================ */}
            <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto text-center">
                <div className="inline-flex p-3 border border-stone-300 dark:border-stone-700 bg-stone-100 dark:bg-stone-900 rounded-none mb-6">
                    <Microscope className="w-6 h-6 text-clinical-teal" />
                </div>
                <h2 className="font-serif text-4xl sm:text-5xl text-stone-900 dark:text-stone-100 font-light mb-6">
                    Conduct an AI-Assisted Clinical Evaluation
                </h2>
                <p className="text-base text-stone-600 dark:text-stone-300 max-w-2xl mx-auto leading-relaxed font-light mb-10">
                    Upload clinical photographs for instant multi-network inference, variance measurement, and printable triage documentation. All data is processed locally with zero patient tracking.
                </p>
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                    <Link to="/upload">
                        <button className="px-9 py-4 bg-stone-900 dark:bg-stone-100 text-stone-100 dark:text-stone-900 text-sm font-mono tracking-wider uppercase font-semibold hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-colors">
                            Launch Examination Workstation
                        </button>
                    </Link>
                </div>
                <p className="font-mono text-[10px] text-stone-400 uppercase tracking-widest mt-8">
                    CLINICAL NOTICE: FOR TRIAGE ASSISTANCE & SCREENING ONLY // NOT A DEFINITIVE REPLACEMENT FOR BIOPSY
                </p>
            </section>
        </div>
    );
};

export default Home;