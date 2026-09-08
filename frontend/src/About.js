import React from 'react';
import { Database, Stethoscope, Award, BookOpen, GraduationCap, ShieldCheck, HeartPulse } from 'lucide-react';
import team1 from './images/5.webp';
import team2 from './images/7.webp';
import doc1 from './images/1.jpg';
import doc2 from './images/2.jpg';
import doc3 from './images/3.jpg';

const About = () => {
    return (
        <div className="min-h-screen bg-slate-50 dark:bg-[#080B10] text-slate-800 dark:text-slate-100 py-16 px-4 sm:px-6 lg:px-8 font-sans transition-colors">
            <div className="max-w-7xl mx-auto space-y-20">
                {/* Header Section */}
                <div className="border-b border-slate-200 dark:border-slate-800 pb-12 text-center max-w-4xl mx-auto space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-teal-500/30 bg-teal-500/10 font-mono text-[11px] tracking-wider uppercase text-teal-600 dark:text-teal-400 font-semibold">
                        <span className="w-2 h-2 bg-teal-500 rounded-full animate-pulse"></span>
                        ACADEMIC CHARTER & CLINICAL EPIDEMIOLOGY
                    </div>
                    <h1 className="text-4xl sm:text-5xl lg:text-6xl font-serif text-slate-900 dark:text-white font-normal tracking-tight">
                        Bridging Neural Ensembles with Point-of-Care Oral Triage
                    </h1>
                    <p className="text-base sm:text-lg text-slate-600 dark:text-slate-300 font-light leading-relaxed">
                        Engineered by researchers from Karnataka, India, under the faculty guidance of <strong>Prof. Aishwarya S</strong>. Our charter is to democratize non-invasive oral cancer screening using calibrated deep learning, native Grad-CAM++ layer activation, and epidemiological risk stratification.
                    </p>
                </div>

                {/* Clinical Burden Infographic Strip */}
                <div className="p-8 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-sm space-y-4">
                    <div className="flex items-center gap-2 font-mono text-xs font-semibold text-rose-600 dark:text-rose-400 uppercase tracking-wider">
                        <HeartPulse className="w-4 h-4" />
                        <span>THE CLINICAL IMPERATIVE</span>
                    </div>
                    <div className="grid md:grid-cols-3 gap-6 pt-2 font-mono text-xs">
                        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-700/50">
                            <span className="text-2xl font-serif font-medium text-slate-900 dark:text-white block mb-1">135,000+</span>
                            <span className="text-slate-500">Annual incident cases in India (~33% of global OSCC burden).</span>
                        </div>
                        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-700/50">
                            <span className="text-2xl font-serif font-medium text-rose-600 dark:text-rose-400 block mb-1">68–75%</span>
                            <span className="text-slate-500">Patients present at late Stages III/IV, collapsing 5-year survival to ~50%.</span>
                        </div>
                        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-700/50">
                            <span className="text-2xl font-serif font-medium text-teal-600 dark:text-teal-400 block mb-1">&gt; 90%</span>
                            <span className="text-slate-500">5-year survival when malignant lesions or OPMD are triaged in Stage I.</span>
                        </div>
                    </div>
                </div>

                {/* Faculty Project Guidance */}
                <div className="p-8 sm:p-10 rounded-2xl border border-teal-500/30 bg-teal-500/5 dark:bg-teal-950/10 space-y-4">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-teal-600 text-white flex items-center justify-center shadow-md">
                            <GraduationCap className="w-5 h-5" />
                        </div>
                        <div>
                            <span className="font-mono text-[10px] text-teal-600 dark:text-teal-400 uppercase tracking-widest block font-bold">
                                FACULTY ADVISOR & RESEARCH GUIDANCE
                            </span>
                            <h2 className="text-2xl font-serif font-medium text-slate-900 dark:text-white">
                                Prof. Aishwarya S
                            </h2>
                        </div>
                    </div>
                    <p className="text-sm text-slate-600 dark:text-slate-300 font-light leading-relaxed max-w-3xl">
                        Department of Computer Science & Engineering. Oversees theoretical validation, epistemic uncertainty formulations, and ethical clinical AI guardrails for the Visionary Diagnostics triage architecture.
                    </p>
                </div>

                {/* Student Engineering Investigators */}
                <div className="space-y-8">
                    <div className="border-b border-slate-200 dark:border-slate-800 pb-3 flex items-center justify-between">
                        <div>
                            <span className="font-mono text-[10px] text-teal-600 dark:text-teal-400 uppercase tracking-widest block font-semibold">
                                RESEARCH AUTHORS
                            </span>
                            <h2 className="text-2xl sm:text-3xl font-serif text-slate-900 dark:text-white font-normal">
                                Core Engineering Investigators
                            </h2>
                        </div>
                        <span className="font-mono text-xs text-slate-400 uppercase hidden sm:block">
                            INSTITUTIONAL PROJECT ROSTER
                        </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
                        {[
                            { 
                                name: "Keerthi A", 
                                role: "AI & Neural Architecture", 
                                desc: "Dual-stage CNN ensemble training, Grad-CAM++ layer activation backpropagation, and PyTorch optimization.", 
                                image: team1 
                            },
                            { 
                                name: "Rakshith Y B", 
                                role: "Backend & Systems Engineering", 
                                desc: "FastAPI microservices, relational ORM data layer, Redis rate limiting, and Docker cloud orchestration.", 
                                image: team2 
                            },
                            { 
                                name: "Lohith R C", 
                                role: "Platform Architect & Lead UI/UX", 
                                desc: "Clinical pathology workstation design, coffered lattice matrix, and human-in-the-loop diagnostic ergonomics.", 
                                image: '/assets/lohith_portrait.jpg' 
                            }
                        ].map((member, i) => (
                            <div
                                key={i}
                                className="p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm hover:border-teal-500/40 transition-all flex flex-col justify-between"
                            >
                                <div>
                                    <div className="aspect-square w-full mb-5 rounded-xl overflow-hidden bg-slate-950 border border-slate-200 dark:border-slate-800">
                                        <img 
                                            src={member.image} 
                                            alt={member.name} 
                                            className="w-full h-full object-cover filter contrast-[1.02] hover:scale-105 transition-transform duration-500" 
                                        />
                                    </div>
                                    <span className="font-mono text-[11px] text-teal-600 dark:text-teal-400 uppercase tracking-wider block font-semibold mb-1">
                                        {member.role}
                                    </span>
                                    <h3 className="text-xl font-serif font-medium text-slate-900 dark:text-white mb-2">
                                        {member.name}
                                    </h3>
                                    <p className="text-xs text-slate-600 dark:text-slate-400 font-light leading-relaxed">
                                        {member.desc}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Medical Advisory Board */}
                <div className="p-8 sm:p-12 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm space-y-8">
                    <div className="border-b border-slate-100 dark:border-slate-800 pb-4 flex items-center justify-between">
                        <div>
                            <span className="font-mono text-[10px] text-teal-600 dark:text-teal-400 uppercase tracking-widest block font-semibold">
                                CLINICAL BENCHMARKING
                            </span>
                            <h2 className="text-2xl sm:text-3xl font-serif text-slate-900 dark:text-white font-normal">
                                Medical Advisory & Workflow Validation
                            </h2>
                        </div>
                        <Stethoscope className="w-7 h-7 text-teal-500 hidden sm:block" />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
                        {[
                            { name: "Dr. Vishal Rao", role: "Head & Neck Surgical Oncology", clinic: "HCG Cancer Centre, Bangalore", image: doc1 },
                            { name: "Dr. Moni Abraham Kuriakose", role: "Surgical Oncology & Telepathology", clinic: "Mazumdar Shaw Medical Center", image: doc2 },
                            { name: "Dr. Vikram Kekatpure", role: "Head & Neck Surgery", clinic: "Cytecare Cancer Hospitals", image: doc3 }
                        ].map((doc, i) => (
                            <div key={i} className="flex flex-col">
                                <div className="aspect-square w-full mb-4 rounded-xl overflow-hidden bg-slate-950 border border-slate-200 dark:border-slate-800">
                                    <img src={doc.image} alt={doc.name} className="w-full h-full object-cover filter contrast-[1.02]" />
                                </div>
                                <h3 className="font-serif text-lg font-medium text-slate-900 dark:text-white">{doc.name}</h3>
                                <p className="font-mono text-xs text-teal-600 dark:text-teal-400 mt-0.5">{doc.role}</p>
                                <p className="text-xs text-slate-500 mt-1">{doc.clinic}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Benchmark Datasets */}
                <div className="space-y-6">
                    <div className="flex items-center gap-3 border-b border-slate-200 dark:border-slate-800 pb-3">
                        <Database className="w-5 h-5 text-teal-500" />
                        <h2 className="text-2xl font-serif text-slate-900 dark:text-white font-normal">
                            Validation Cohorts & Datasets
                        </h2>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                        <div className="p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm space-y-3">
                            <span className="font-mono text-[10px] text-slate-400 uppercase tracking-widest block">DATASET 01 // PUBLIC BENCHMARK</span>
                            <h3 className="text-xl font-serif text-slate-900 dark:text-white font-medium">
                                Kaggle Oral Cancer Dataset 2.0
                            </h3>
                            <p className="text-xs text-slate-600 dark:text-slate-400 font-light leading-relaxed">
                                Standardized image repository divided into stratified train, validation, and test subsets. Used for multi-architecture transfer learning baseline tuning.
                            </p>
                            <div className="font-mono text-xs text-slate-500 space-y-1 pt-2 border-t border-slate-100 dark:border-slate-800">
                                <div>• VOLUME: 5,000+ High-Resolution Intraoral Captures</div>
                                <div>• CLASSES: OSCC Carcinoma vs. Non-Malignant Mucosa</div>
                                <div>• ACCURACY BASELINE: 94.2% on Test Split</div>
                            </div>
                        </div>

                        <div className="p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm space-y-3">
                            <span className="font-mono text-[10px] text-slate-400 uppercase tracking-widest block">DATASET 02 // REGIONAL COHORT</span>
                            <h3 className="text-xl font-serif text-slate-900 dark:text-white font-medium">
                                Karnataka Regional Clinical Cohort
                            </h3>
                            <p className="text-xs text-slate-600 dark:text-slate-400 font-light leading-relaxed">
                                Sourced through regional oncology screenings with high incidence of chewable tobacco (khaini, gutka) and areca nut dysplasia cases.
                            </p>
                            <div className="font-mono text-xs text-slate-500 space-y-1 pt-2 border-t border-slate-100 dark:border-slate-800">
                                <div>• FOCUS: Early-Stage & Dysplastic OPMD Lesions</div>
                                <div>• DEMOGRAPHIC: South Asian High-Risk Epidemiological Cohort</div>
                                <div>• PURPOSE: Domain-Shift Robustness & TTA Verification</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Annotated Scientific Bibliography */}
                <div className="p-8 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm space-y-4">
                    <div className="flex items-center gap-2 font-mono text-xs font-semibold text-slate-900 dark:text-white uppercase tracking-wider">
                        <BookOpen className="w-4 h-4 text-teal-500" />
                        <span>ANNOTATED SCIENTIFIC REFERENCES</span>
                    </div>
                    <ol className="list-decimal list-inside space-y-2.5 text-xs text-slate-600 dark:text-slate-400 font-sans leading-relaxed">
                        <li>NIH / NCI — <em>Insights Into AI-Enabled Early Diagnosis of Oral Cancer: A Scoping Review</em> (2025).</li>
                        <li>Frontiers in Oral Health — <em>AI and Diagnosis of Oral Cavity Cancer from Clinical Photographs</em> (2025).</li>
                        <li>MDPI Cancers — <em>Classification of Mobile-Based Oral Cancer Images Using Vision Transformer and CNNs</em> (2024).</li>
                        <li>Gal & Ghahramani — <em>Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning</em> (ICML).</li>
                        <li>Chattopadhay et al. — <em>Grad-CAM++: Generalized Gradient-Based Visual Explanations for Deep Convolutional Networks</em> (IEEE).</li>
                    </ol>
                </div>
            </div>
        </div>
    );
};

export default About;