import React from 'react';
import { motion } from 'framer-motion';
import { Database, Stethoscope, Award, CheckCircle2 } from 'lucide-react';
import team1 from './images/5.webp';
import team2 from './images/7.webp';
import team3 from './images/8.jpg';
import doc1 from './images/1.jpg';
import doc2 from './images/2.jpg';
import doc3 from './images/3.jpg';

const About = () => {
    return (
        <div className="bg-parchment-100 dark:bg-ink-950 text-stone-800 dark:text-stone-200 min-h-screen py-16 px-4 sm:px-6 lg:px-8 font-sans">
            <div className="max-w-7xl mx-auto">
                {/* Header Section */}
                <div className="border-b border-stone-200 dark:border-stone-800 pb-12 mb-16 text-center max-w-4xl mx-auto">
                    <div className="inline-flex items-center gap-2 font-mono text-[11px] tracking-wider uppercase text-clinical-teal dark:text-teal-400 mb-4">
                        <span className="w-2 h-2 bg-clinical-teal inline-block"></span>
                        ACADEMIC INITIATIVE // ENGINEERING & ONCOLOGY
                    </div>
                    <h1 className="font-serif text-4xl sm:text-5xl lg:text-6xl text-stone-900 dark:text-stone-100 font-light tracking-tight mb-6">
                        Bridging Neural Ensembles with Clinical Triage
                    </h1>
                    <p className="font-sans text-base sm:text-lg text-stone-600 dark:text-stone-300 font-light leading-relaxed">
                        Developed by engineering researchers from Karnataka, India, under the guidance of Prof. Aishwarya S. Our objective is to democratize non-invasive oral cancer screening using calibrated deep learning and epidemiological risk modeling.
                    </p>
                </div>

                {/* Student Team Section */}
                <div className="mb-20">
                    <div className="flex items-center justify-between border-b border-stone-200 dark:border-stone-800 pb-3 mb-8">
                        <h2 className="font-serif text-2xl sm:text-3xl text-stone-900 dark:text-stone-100 font-normal">
                            Core Engineering Investigators
                        </h2>
                        <span className="font-mono text-xs text-stone-400 uppercase">PROJECT CONTRIBUTORS</span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                        {[
                            { name: "Keerthi A", role: "AI & ML Architecture", desc: "Ensemble training, TTA pipelines, and PyTorch optimization.", image: team1 },
                            { name: "Rakshith Y B", role: "Backend & Systems", desc: "FastAPI inference service, SQLite ORM, and rate limiting.", image: team2 },
                            { name: "Lohith R C", role: "Frontend & UI/UX Design", desc: "Clinical pathology workstation and human-centric design.", image: team3 }
                        ].map((member, i) => (
                            <div
                                key={i}
                                className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6 relative group"
                            >
                                <span className="absolute -top-1 -left-1 text-[10px] font-mono text-stone-400">+</span>
                                <span className="absolute -top-1 -right-1 text-[10px] font-mono text-stone-400">+</span>
                                <div className="aspect-square w-full mb-4 overflow-hidden bg-stone-950">
                                    <img 
                                        src={member.image} 
                                        alt={member.name} 
                                        className="w-full h-full object-cover filter grayscale contrast-105 group-hover:grayscale-0 transition-all duration-500" 
                                    />
                                </div>
                                <span className="font-mono text-[10px] text-clinical-teal dark:text-teal-400 uppercase tracking-wider block mb-1">
                                    {member.role}
                                </span>
                                <h3 className="font-serif text-xl font-normal text-stone-900 dark:text-stone-100 mb-2">
                                    {member.name}
                                </h3>
                                <p className="font-sans text-xs text-stone-600 dark:text-stone-400 font-light leading-relaxed">
                                    {member.desc}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Clinical Advisors Section */}
                <div className="mb-20 border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-8 sm:p-12">
                    <div className="border-b border-stone-200 dark:border-stone-800 pb-4 mb-8 flex items-center justify-between">
                        <div>
                            <span className="font-mono text-[10px] text-clinical-teal uppercase tracking-widest block mb-1">CLINICAL COLLABORATION</span>
                            <h2 className="font-serif text-2xl sm:text-3xl text-stone-900 dark:text-stone-100 font-normal">
                                Medical Advisory & Workflow Validation
                            </h2>
                        </div>
                        <Stethoscope className="w-8 h-8 text-clinical-teal hidden sm:block" />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
                        {[
                            { name: "Dr. Vishal Rao", role: "Head & Neck Oncology", clinic: "HCG Cancer Centre, Bangalore", image: doc1 },
                            { name: "Dr. Moni Abraham Kuriakose", role: "Surgical Oncology", clinic: "Mazumdar Shaw Medical Center", image: doc2 },
                            { name: "Dr. Vikram Kekatpure", role: "Head & Neck Surgery", clinic: "Cytecare Cancer Hospitals", image: doc3 }
                        ].map((doc, i) => (
                            <div key={i} className="flex flex-col">
                                <div className="aspect-square w-full mb-4 overflow-hidden bg-stone-950 border border-stone-300 dark:border-stone-700">
                                    <img src={doc.image} alt={doc.name} className="w-full h-full object-cover filter contrast-[1.02]" />
                                </div>
                                <h3 className="font-serif text-lg font-medium text-stone-900 dark:text-stone-100">{doc.name}</h3>
                                <p className="font-mono text-xs text-clinical-teal dark:text-teal-400 mt-0.5">{doc.role}</p>
                                <p className="font-sans text-xs text-stone-500 mt-1">{doc.clinic}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Training Datasets */}
                <div className="mb-12">
                    <div className="flex items-center gap-3 border-b border-stone-200 dark:border-stone-800 pb-3 mb-8">
                        <Database className="w-5 h-5 text-clinical-teal" />
                        <h2 className="font-serif text-2xl text-stone-900 dark:text-stone-100 font-normal">
                            Evaluation Benchmark Datasets
                        </h2>
                    </div>

                    <div className="grid md:grid-cols-2 gap-8">
                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6">
                            <span className="font-mono text-[10px] text-stone-400 uppercase tracking-widest block mb-1">DATASET 01 // PUBLIC BENCHMARK</span>
                            <h3 className="font-serif text-xl font-normal text-stone-900 dark:text-stone-100 mb-3">
                                Kaggle Oral Cancer Dataset 2.0
                            </h3>
                            <p className="text-xs text-stone-600 dark:text-stone-400 font-light leading-relaxed mb-4">
                                Standardized image repository divided into stratified train, validation, and test subsets. Used for multi-architecture transfer learning baseline tuning.
                            </p>
                            <div className="font-mono text-[11px] text-stone-500 space-y-1">
                                <div>• VOLUME: 5,000+ High-Resolution Captures</div>
                                <div>• CLASSES: Carcinoma vs. Non-Malignant Mucosa</div>
                                <div>• ACCURACY BASELINE: 94.2% on Test Split</div>
                            </div>
                        </div>

                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6">
                            <span className="font-mono text-[10px] text-stone-400 uppercase tracking-widest block mb-1">DATASET 02 // REGIONAL COHORT</span>
                            <h3 className="font-serif text-xl font-normal text-stone-900 dark:text-stone-100 mb-3">
                                Karnataka Regional Clinical Cohort
                            </h3>
                            <p className="text-xs text-stone-600 dark:text-stone-400 font-light leading-relaxed mb-4">
                                Sourced through regional oncology screenings with high incidence of chewable tobacco (khaini, gutka) and areca nut dysplasia cases.
                            </p>
                            <div className="font-mono text-[11px] text-stone-500 space-y-1">
                                <div>• FOCUS: Early-Stage & Dysplastic Lesions</div>
                                <div>• DEMOGRAPHIC: South Asian Epidemiological Cohort</div>
                                <div>• PURPOSE: Domain-Shift Robustness & TTA Verification</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default About;