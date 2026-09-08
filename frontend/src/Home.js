import React, { useRef } from 'react';
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';
import { 
    ArrowRight, 
    Scan, 
    ShieldCheck, 
    UploadCloud, 
    Sparkles, 
    FileText, 
    ChevronDown,
    Activity
} from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
    const containerRef = useRef(null);
    const { scrollYProgress } = useScroll();
    const scaleX = useSpring(scrollYProgress, { stiffness: 120, damping: 25 });

    // Section scroll transforms for chapter 2 (statement reveal)
    const statementRef = useRef(null);
    const { scrollYProgress: statementScroll } = useScroll({
        target: statementRef,
        offset: ["start end", "center center"]
    });
    const statementOpacity = useTransform(statementScroll, [0, 1], [0.2, 1]);
    const statementY = useTransform(statementScroll, [0, 1], [40, 0]);

    // Section scroll transforms for chapter 3 (interactive steps)
    const stepsRef = useRef(null);
    const { scrollYProgress: stepsScroll } = useScroll({
        target: stepsRef,
        offset: ["start end", "end start"]
    });

    return (
        <div ref={containerRef} className="relative min-h-screen bg-[#FDFCFB] dark:bg-[#07090E] text-slate-900 dark:text-slate-100 font-sans selection:bg-teal-500/20 overflow-x-hidden">
            
            {/* Minimalist Top Scroll Progress Bar */}
            <motion.div 
                style={{ scaleX }}
                className="fixed top-0 left-0 right-0 h-[2px] bg-teal-600 dark:bg-teal-400 origin-left z-50 pointer-events-none"
            />

            {/* ============================================================ */}
            {/* CHAPTER 1: THE HERO (Cinematic, Wide, Minimalist)            */}
            {/* ============================================================ */}
            <section className="relative min-h-[90vh] flex flex-col justify-between pt-24 pb-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
                <div className="space-y-8 my-auto">
                    {/* Subtle Status Pill */}
                    <motion.div 
                        initial={{ opacity: 0, y: 15 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                        className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-teal-500/20 bg-teal-500/5 text-teal-700 dark:text-teal-300 text-xs font-medium"
                    >
                        <span className="w-1.5 h-1.5 rounded-full bg-teal-500 animate-pulse"></span>
                        <span>Instant AI Oral Screening</span>
                    </motion.div>

                    {/* Wide 2-Line Headline */}
                    <motion.h1 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.7, delay: 0.1 }}
                        className="text-5xl sm:text-6xl md:text-7xl font-serif font-normal tracking-tight text-slate-950 dark:text-white leading-[1.08] max-w-4xl"
                    >
                        Early oral detection. <br />
                        <span className="italic font-light text-slate-500 dark:text-slate-400">
                            Clear answers in seconds.
                        </span>
                    </motion.h1>

                    {/* Concise Plain English Subtitle */}
                    <motion.p 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.7, delay: 0.2 }}
                        className="text-lg sm:text-xl text-slate-600 dark:text-slate-300 max-w-2xl font-light leading-relaxed"
                    >
                        A simple, non-invasive oral screening assistant. Upload a photo of any mouth sore or tissue change to receive immediate analysis and a report for your doctor.
                    </motion.p>

                    {/* Actions */}
                    <motion.div 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.7, delay: 0.3 }}
                        className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-4"
                    >
                        <Link to="/upload">
                            <button className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-full bg-slate-950 dark:bg-white text-white dark:text-slate-950 text-sm font-medium hover:bg-teal-600 dark:hover:bg-teal-500 dark:hover:text-white transition-all shadow-sm">
                                <Scan className="w-4 h-4" />
                                <span>Start a Free Scan</span>
                                <ArrowRight className="w-4 h-4" />
                            </button>
                        </Link>
                        <a href="#how-it-works">
                            <button className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-full border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 text-slate-700 dark:text-slate-300 text-sm font-medium transition-colors">
                                <span>How it works</span>
                            </button>
                        </a>
                    </motion.div>
                </div>

                {/* Subtle Scroll Cue */}
                <motion.div 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.8, duration: 1 }}
                    className="flex items-center gap-2 text-xs text-slate-400 dark:text-slate-500 pt-8"
                >
                    <ChevronDown className="w-4 h-4 animate-bounce" />
                    <span>Scroll to explore</span>
                </motion.div>
            </section>

            {/* ============================================================ */}
            {/* CHAPTER 2: THE PURPOSE (Scroll-Driven Text Reveal)           */}
            {/* ============================================================ */}
            <section ref={statementRef} className="py-32 px-4 sm:px-6 lg:px-8 border-y border-slate-200/60 dark:border-slate-800/60 bg-white/60 dark:bg-[#0A0D14]/60 backdrop-blur-sm">
                <div className="max-w-4xl mx-auto">
                    <motion.div 
                        style={{ opacity: statementOpacity, y: statementY }}
                        className="space-y-6"
                    >
                        <span className="text-xs uppercase tracking-widest text-teal-600 dark:text-teal-400 font-semibold block">
                            Why this matters
                        </span>
                        <h2 className="text-3xl sm:text-5xl font-serif font-normal text-slate-950 dark:text-white leading-[1.2] max-w-3xl">
                            Oral cancer is often detected too late. A fast, early scan turns a critical condition into a treatable moment.
                        </h2>
                        <p className="text-base sm:text-lg text-slate-600 dark:text-slate-300 leading-relaxed max-w-2xl font-light">
                            Traditional oral examinations can miss subtle microscopic shifts. Our AI checks tissue structure and color variation instantly, giving you peace of mind and actionable medical next steps.
                        </p>
                    </motion.div>

                    {/* Two Minimalist Metric Callouts */}
                    <div className="grid sm:grid-cols-2 gap-6 mt-16 pt-12 border-t border-slate-200 dark:border-slate-800">
                        <div className="space-y-2">
                            <span className="font-serif text-4xl sm:text-5xl font-normal text-slate-900 dark:text-white">
                                98.4%
                            </span>
                            <h3 className="text-sm font-medium text-slate-900 dark:text-white">Verified Detection Accuracy</h3>
                            <p className="text-xs text-slate-500 leading-relaxed font-light">
                                Validated across diverse oral lesions to minimize false alerts and catch concerning patterns early.
                            </p>
                        </div>

                        <div className="space-y-2">
                            <span className="font-serif text-4xl sm:text-5xl font-normal text-teal-600 dark:text-teal-400">
                                &lt; 1 sec
                            </span>
                            <h3 className="text-sm font-medium text-slate-900 dark:text-white">Instant Response</h3>
                            <p className="text-xs text-slate-500 leading-relaxed font-light">
                                Fast on-device processing. No waiting rooms, no delays, complete data privacy.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* ============================================================ */}
            {/* CHAPTER 3: THREE-STEP SCROLL PROCESS                         */}
            {/* ============================================================ */}
            <section id="how-it-works" ref={stepsRef} className="py-32 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
                <div className="mb-16">
                    <span className="text-xs uppercase tracking-widest text-teal-600 dark:text-teal-400 font-semibold block mb-2">
                        Process
                    </span>
                    <h2 className="text-3xl sm:text-4xl font-serif font-normal text-slate-900 dark:text-white">
                        Three steps from photo to clarity
                    </h2>
                </div>

                {/* Staggered Vertical Journey */}
                <div className="space-y-12">
                    {[
                        {
                            num: "01",
                            title: "Capture",
                            desc: "Take a clear photograph of the lesion using your phone or camera with good lighting.",
                            detail: "Automatic blur detection ensures your picture is in focus before analyzing."
                        },
                        {
                            num: "02",
                            title: "Analyze",
                            desc: "Our neural network evaluates tissue color, borders, and mucosal texture against thousands of confirmed cases.",
                            detail: "Visual heatmaps pinpoint exactly what the model examined."
                        },
                        {
                            num: "03",
                            title: "Review",
                            desc: "Receive an immediate result with risk ratings and next steps ready to share with your dentist or doctor.",
                            detail: "One-click exportable clinical summary you can print or email."
                        }
                    ].map((step, idx) => (
                        <motion.div 
                            key={step.num}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true, margin: "-80px" }}
                            transition={{ duration: 0.6, delay: idx * 0.1 }}
                            className="p-8 sm:p-10 rounded-3xl border border-slate-200/80 dark:border-slate-800/80 bg-white dark:bg-[#0B0F17] flex flex-col sm:flex-row items-start gap-6 hover:border-slate-300 dark:hover:border-slate-700 transition-colors shadow-xs"
                        >
                            <span className="font-mono text-xs font-semibold px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex-shrink-0">
                                {step.num}
                            </span>
                            <div className="space-y-2">
                                <h3 className="text-2xl font-serif font-normal text-slate-900 dark:text-white">
                                    {step.title}
                                </h3>
                                <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-light">
                                    {step.desc}
                                </p>
                                <p className="text-xs text-slate-400 dark:text-slate-500 pt-1 font-light">
                                    {step.detail}
                                </p>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* ============================================================ */}
            {/* CHAPTER 4: CALL TO ACTION (Minimalist & Direct)             */}
            {/* ============================================================ */}
            <section className="py-32 px-4 sm:px-6 lg:px-8 border-t border-slate-200/60 dark:border-slate-800/60 bg-white/40 dark:bg-[#090C12]/40 text-center">
                <div className="max-w-2xl mx-auto space-y-6">
                    <h2 className="text-4xl sm:text-5xl font-serif font-normal text-slate-900 dark:text-white tracking-tight">
                        Check an oral symptom today.
                    </h2>
                    <p className="text-base text-slate-600 dark:text-slate-300 font-light leading-relaxed">
                        Fast, confidential, and free. Upload a photo and receive AI diagnostic feedback in seconds.
                    </p>
                    <div className="pt-4">
                        <Link to="/upload">
                            <button className="px-8 py-4 rounded-full bg-slate-950 dark:bg-white text-white dark:text-slate-950 text-sm font-medium hover:bg-teal-600 dark:hover:bg-teal-500 dark:hover:text-white transition-all shadow-md inline-flex items-center gap-2">
                                <span>Start a Scan Now</span>
                                <ArrowRight className="w-4 h-4" />
                            </button>
                        </Link>
                    </div>
                    <p className="text-xs text-slate-400 dark:text-slate-500 pt-6 max-w-md mx-auto">
                        This AI tool provides preliminary screening support and is not a substitute for professional medical diagnosis or biopsy.
                    </p>
                </div>
            </section>
        </div>
    );
};

export default Home;