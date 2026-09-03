import React, { useEffect, useState, useRef } from 'react';
import { motion, useScroll, useTransform, useMotionValue, useSpring } from 'framer-motion';
import { CheckCircle, Shield, Zap, Target, Activity, Heart, Cpu, Star, Microscope, ArrowRight, UploadCloud, UserCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

import heroImage from './images/1.jpg';
import detailedFeatureImage from './images/8.webp';

// --- Reusable 3D Tilt Card ---
const TiltCard = ({ children, className }) => {
    const x = useMotionValue(0);
    const y = useMotionValue(0);
    const mouseXSpring = useSpring(x);
    const mouseYSpring = useSpring(y);
    const rotateX = useTransform(mouseYSpring, [-0.5, 0.5], ["17.5deg", "-17.5deg"]);
    const rotateY = useTransform(mouseXSpring, [-0.5, 0.5], ["-17.5deg", "17.5deg"]);

    const handleMouseMove = (e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const width = rect.width;
        const height = rect.height;
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;
        const xPct = mouseX / width - 0.5;
        const yPct = mouseY / height - 0.5;
        x.set(xPct);
        y.set(yPct);
    };

    const handleMouseLeave = () => {
        x.set(0);
        y.set(0);
    };

    return (
        <motion.div
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
            style={{ rotateY, rotateX, transformStyle: "preserve-3d" }}
            className={`relative ${className}`}
        >
            <div style={{ transform: "translateZ(50px)" }} className="h-full">
                {children}
            </div>
        </motion.div>
    );
};

const FeatureCard = ({ icon, title, description, delay = 0 }) => (
    <TiltCard className="h-full">
        <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-50px" }}
            transition={{ delay, duration: 0.8, ease: "easeOut" }}
            className="h-full bg-white/40 dark:bg-slate-800/40 backdrop-blur-2xl border border-white/40 dark:border-slate-700/50 rounded-3xl p-8 shadow-2xl relative overflow-hidden group"
        >
            <div className="absolute top-0 right-0 -mt-4 -mr-4 w-32 h-32 bg-gradient-to-br from-teal-400/30 to-blue-500/20 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-700"></div>
            <div className="mb-6 inline-flex p-4 rounded-2xl bg-teal-100/50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400 ring-1 ring-inset ring-teal-500/20 shadow-[0_0_15px_rgba(20,184,166,0.2)]">
                {icon}
            </div>
            <h3 className="text-2xl font-display font-semibold text-slate-900 dark:text-white mb-3">{title}</h3>
            <p className="text-slate-600 dark:text-slate-300 leading-relaxed font-light">{description}</p>
        </motion.div>
    </TiltCard>
);

const Home = () => {
    const { scrollYProgress } = useScroll();
    const backgroundY = useTransform(scrollYProgress, [0, 1], ["0%", "50%"]);
    const textY = useTransform(scrollYProgress, [0, 1], ["0%", "200%"]);

    // Mouse tracking for dynamic background glow
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    
    useEffect(() => {
        const updateMousePosition = (e) => {
            setMousePosition({ x: e.clientX, y: e.clientY });
        };
        window.addEventListener('mousemove', updateMousePosition);
        return () => window.removeEventListener('mousemove', updateMousePosition);
    }, []);

    return (
        <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-200 overflow-hidden font-sans min-h-screen relative selection:bg-teal-500/30"
        >
            {/* Dynamic Interactive Background */}
            <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
                <motion.div 
                    animate={{
                        x: mousePosition.x - 300,
                        y: mousePosition.y - 300,
                    }}
                    transition={{ type: "spring", damping: 50, stiffness: 50, mass: 1 }}
                    className="absolute w-[600px] h-[600px] rounded-full bg-teal-400/10 dark:bg-teal-600/10 blur-[100px]"
                />
                <motion.div 
                    animate={{
                        x: mousePosition.x - 400,
                        y: mousePosition.y - 400,
                    }}
                    transition={{ type: "spring", damping: 80, stiffness: 30, mass: 2 }}
                    className="absolute w-[800px] h-[800px] rounded-full bg-blue-400/5 dark:bg-blue-600/10 blur-[120px]"
                />
                {/* Noise texture overlay for a premium look */}
                <div className="absolute inset-0 opacity-[0.015] dark:opacity-[0.03]" style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=%220 0 200 200%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noiseFilter%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.65%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noiseFilter)%22/%3E%3C/svg%3E")' }}></div>
            </div>

            {/* Hero Section */}
            <section className="relative min-h-screen flex items-center justify-center pt-20 pb-16 px-4 sm:px-6 lg:px-8 z-10">
                <div className="max-w-7xl mx-auto w-full flex flex-col lg:flex-row items-center gap-16">
                    <div className="lg:w-1/2 text-center lg:text-left">
                        <motion.div style={{ y: textY }}>
                            <motion.div
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ duration: 0.8, ease: "easeOut" }}
                                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/40 dark:bg-slate-800/50 text-teal-700 dark:text-teal-300 font-medium text-sm mb-8 backdrop-blur-md border border-white/60 dark:border-slate-700 shadow-sm"
                            >
                                <span className="relative flex h-3 w-3">
                                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
                                  <span className="relative inline-flex rounded-full h-3 w-3 bg-teal-500"></span>
                                </span>
                                AI-Powered Intelligence Loop
                            </motion.div>
                            
                            <motion.h1 
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.9, delay: 0.2, ease: "easeOut" }}
                                className="text-6xl lg:text-8xl font-display font-extrabold text-slate-900 dark:text-white tracking-tighter mb-6 leading-[1.05]"
                            >
                                Visionary <br/>
                                <span className="text-transparent bg-clip-text bg-gradient-to-br from-teal-400 via-emerald-500 to-blue-600">Diagnostics</span>
                            </motion.h1>
                            
                            <motion.p 
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.9, delay: 0.4, ease: "easeOut" }}
                                className="text-xl text-slate-600 dark:text-slate-300 mb-10 max-w-2xl mx-auto lg:mx-0 leading-relaxed font-light"
                            >
                                Step into the future of healthcare. Experience a frictionless, non-invasive oral cancer screening ecosystem driven by cutting-edge neural architectures.
                            </motion.p>
                            
                            <motion.div 
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.9, delay: 0.6, ease: "easeOut" }}
                                className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-5"
                            >
                                <Link to="/upload" className="w-full sm:w-auto">
                                    <button className="group relative w-full inline-flex items-center justify-center gap-3 px-8 py-4 bg-slate-900 dark:bg-white text-white dark:text-slate-900 rounded-full font-medium text-lg overflow-hidden transition-transform active:scale-95">
                                        <div className="absolute inset-0 bg-gradient-to-r from-teal-500 to-emerald-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                                        <span className="relative z-10 flex items-center gap-2 group-hover:text-white transition-colors duration-300">
                                            Initialize Scan <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                        </span>
                                    </button>
                                </Link>
                                <Link to="/about" className="w-full sm:w-auto">
                                    <button className="group w-full px-8 py-4 bg-transparent border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-200 rounded-full font-medium text-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-all duration-300">
                                        Explore the Science
                                    </button>
                                </Link>
                            </motion.div>
                        </motion.div>
                    </div>

                    <div className="lg:w-1/2 w-full max-w-2xl lg:max-w-none relative perspective-1000 mt-16 lg:mt-0">
                        <TiltCard>
                            <motion.div
                                initial={{ opacity: 0, scale: 0.8, rotateY: 15 }}
                                animate={{ opacity: 1, scale: 1, rotateY: 0 }}
                                transition={{ duration: 1.2, delay: 0.4, ease: "easeOut" }}
                                className="relative rounded-[2.5rem] overflow-hidden shadow-2xl border border-white/20 bg-white/10 backdrop-blur-xl p-2"
                            >
                                <div className="absolute inset-0 bg-gradient-to-tr from-teal-500/20 to-blue-500/20 blur-xl z-0"></div>
                                <img src={heroImage} alt="Clinical Scanning" className="relative z-10 w-full h-auto rounded-[2rem] object-cover mix-blend-overlay dark:mix-blend-normal opacity-90" />
                                
                                {/* Holographic UI Overlay */}
                                <div className="absolute inset-0 z-20 flex flex-col justify-end p-8">
                                    <motion.div 
                                        animate={{ y: [0, -10, 0] }}
                                        transition={{ repeat: Infinity, duration: 5, ease: "easeInOut" }}
                                        className="bg-white/10 dark:bg-slate-900/60 backdrop-blur-md border border-white/20 p-5 rounded-2xl flex items-center gap-5 w-max shadow-2xl"
                                    >
                                        <div className="relative">
                                            <div className="absolute inset-0 bg-teal-500 blur-md opacity-50 rounded-full animate-pulse"></div>
                                            <div className="relative p-3 bg-teal-500 rounded-xl">
                                                <Activity className="w-6 h-6 text-white" />
                                            </div>
                                        </div>
                                        <div>
                                            <p className="text-xs font-medium text-slate-200 dark:text-slate-300 uppercase tracking-wider mb-1">Live Inference</p>
                                            <p className="text-2xl font-bold font-display text-white">Detecting Anomalies...</p>
                                        </div>
                                    </motion.div>
                                </div>
                            </motion.div>
                        </TiltCard>
                    </div>
                </div>
            </section>

            {/* Infinite Marquee Section */}
            <div className="w-full py-8 bg-white/30 dark:bg-slate-900/50 backdrop-blur-md border-y border-white/20 dark:border-slate-800/50 overflow-hidden relative z-10">
                <div className="flex w-[200%] animate-[marquee_20s_linear_infinite] whitespace-nowrap">
                    {[...Array(10)].map((_, i) => (
                        <div key={i} className="flex items-center justify-center gap-16 px-8 text-slate-400 dark:text-slate-500 font-display font-semibold text-xl uppercase tracking-widest">
                            <span className="flex items-center gap-2"><Cpu className="w-5 h-5"/> PyTorch Models</span>
                            <span className="flex items-center gap-2"><Zap className="w-5 h-5"/> React Architecture</span>
                            <span className="flex items-center gap-2"><Shield className="w-5 h-5"/> HIPAA Compliant</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Core Mechanics Section */}
            <section className="py-32 relative z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center max-w-3xl mx-auto mb-20">
                        <motion.h2 
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            className="text-4xl md:text-5xl font-display font-bold text-slate-900 dark:text-white mb-6"
                        >
                            Orchestrating <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-emerald-500">Precision</span>
                        </motion.h2>
                        <motion.p 
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.1 }}
                            className="text-xl text-slate-600 dark:text-slate-400 font-light"
                        >
                            A symphony of advanced neural networks analyzing thousands of micro-patterns simultaneously to deliver an unparalleled diagnostic edge.
                        </motion.p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8 perspective-1000">
                        <FeatureCard
                            icon={<Microscope className="w-8 h-8" />}
                            title="Cellular-Level Analysis"
                            description="Our convolutional nets extract deep features, recognizing textures and morphological shifts invisible to the naked eye."
                            delay={0.1}
                        />
                        <FeatureCard
                            icon={<Shield className="w-8 h-8" />}
                            title="Zero-Knowledge Privacy"
                            description="Images are processed entirely in memory and immediately discarded. Your biometric data is never stored without explicit consent."
                            delay={0.2}
                        />
                        <FeatureCard
                            icon={<Zap className="w-8 h-8" />}
                            title="Ensemble Intelligence"
                            description="We don't rely on one model. We cross-reference predictions across ResNet, MobileNet, and EfficientNet for maximal certainty."
                            delay={0.3}
                        />
                    </div>
                </div>
            </section>

            {/* Immersive Deep Dive Section */}
            <section className="py-32 relative overflow-hidden z-10">
                <motion.div style={{ y: backgroundY }} className="absolute inset-0 bg-slate-900 dark:bg-slate-950 z-0">
                    <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1530497610245-94d3c16cda28?q=80&w=2000&auto=format&fit=crop')] opacity-10 bg-cover bg-center mix-blend-overlay"></div>
                    <div className="absolute inset-0 bg-gradient-to-b from-transparent via-slate-900/80 to-slate-900"></div>
                </motion.div>

                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                    <div className="grid lg:grid-cols-2 gap-20 items-center">
                        <motion.div 
                            initial={{ opacity: 0, x: -50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true }}
                            className="relative"
                        >
                            <div className="relative rounded-[2rem] overflow-hidden shadow-[0_0_50px_rgba(20,184,166,0.3)] border border-teal-500/30 group">
                                <div className="absolute inset-0 bg-teal-900/40 mix-blend-overlay z-10 group-hover:bg-transparent transition-colors duration-700"></div>
                                <img src={detailedFeatureImage} alt="Neural Network Visualization" className="w-full h-[600px] object-cover scale-105 group-hover:scale-100 transition-transform duration-1000 ease-out" />
                                
                                {/* Scanner Line Animation */}
                                <motion.div 
                                    animate={{ top: ["0%", "100%", "0%"] }}
                                    transition={{ repeat: Infinity, duration: 4, ease: "linear" }}
                                    className="absolute left-0 right-0 h-1 bg-teal-400 shadow-[0_0_20px_#2dd4bf] z-20"
                                />
                            </div>
                        </motion.div>

                        <motion.div 
                            initial={{ opacity: 0, x: 50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true }}
                        >
                            <h2 className="text-4xl md:text-5xl font-display font-bold text-white mb-8">Redefining the Diagnostic Paradigm</h2>
                            <p className="text-xl text-slate-300 mb-10 leading-relaxed font-light">
                                We are moving away from reactive healthcare. Our platform introduces a proactive, hyper-accessible layer of pre-clinical screening, democratizing advanced oncology tools.
                            </p>
                            
                            <div className="space-y-8">
                                {[
                                    { icon: Target, title: "Precision Mapping", desc: "Isolates and highlights areas of interest with bounding-box accuracy." },
                                    { icon: Heart, title: "Patient Empowerment", desc: "Designed to reduce clinical anxiety through transparent, easily understood reporting." }
                                ].map((item, i) => (
                                    <div key={i} className="flex gap-6 group">
                                        <div className="flex-shrink-0 mt-1">
                                            <div className="w-14 h-14 rounded-2xl bg-white/10 backdrop-blur-md flex items-center justify-center border border-white/20 group-hover:border-teal-400/50 group-hover:bg-teal-900/30 transition-all duration-300">
                                                <item.icon className="w-7 h-7 text-teal-400" />
                                            </div>
                                        </div>
                                        <div>
                                            <h4 className="text-2xl font-display font-semibold text-white mb-2">{item.title}</h4>
                                            <p className="text-slate-400 text-lg">{item.desc}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* Call to Action */}
            <section className="py-32 relative z-10 overflow-hidden">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-tr from-teal-400/20 to-blue-500/20 blur-[120px] rounded-full z-0 pointer-events-none"></div>
                <div className="max-w-4xl mx-auto px-4 text-center relative z-10">
                    <motion.h2 
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        className="text-5xl md:text-7xl font-display font-bold text-slate-900 dark:text-white mb-8 tracking-tight"
                    >
                        Ready to Take Control?
                    </motion.h2>
                    <motion.p 
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.2 }}
                        className="text-2xl text-slate-600 dark:text-slate-300 mb-12 font-light"
                    >
                        Join thousands of patients and practitioners relying on AI-driven insights.
                    </motion.p>
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.4 }}
                    >
                        <Link to="/register">
                            <button className="px-10 py-5 bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-400 hover:to-emerald-400 text-white rounded-full font-bold text-xl shadow-[0_0_40px_rgba(20,184,166,0.4)] hover:shadow-[0_0_60px_rgba(20,184,166,0.6)] transition-all duration-300 transform hover:scale-105">
                                Create Your Secure Account
                            </button>
                        </Link>
                    </motion.div>
                </div>
            </section>
            
            {/* Custom Tailwind utilities for the marquee animation */}
            <style jsx>{`
                @keyframes marquee {
                    0% { transform: translateX(0%); }
                    100% { transform: translateX(-50%); }
                }
                .animate-\\[marquee_20s_linear_infinite\\] {
                    animation: marquee 20s linear infinite;
                }
            `}</style>
        </motion.div>
    );
};

export default Home;