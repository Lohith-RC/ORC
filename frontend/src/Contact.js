import React, { useState } from 'react';
import { Mail, MapPin, Send, CheckCircle2 } from 'lucide-react';

const Contact = () => {
    const [sent, setSent] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        setSent(true);
    };

    return (
        <div className="bg-parchment-100 dark:bg-ink-950 min-h-screen py-16 px-4 sm:px-6 lg:px-8 font-sans text-stone-800 dark:text-stone-200">
            <div className="max-w-5xl mx-auto">
                {/* Header */}
                <div className="border-b border-stone-200 dark:border-stone-800 pb-8 mb-12 text-center">
                    <div className="inline-flex items-center gap-2 font-mono text-[11px] tracking-wider uppercase text-clinical-teal dark:text-teal-400 mb-3">
                        <span className="w-2 h-2 bg-clinical-teal inline-block"></span>
                        COMMUNICATIONS // CLINICAL INQUIRIES & RESEARCH COLLABORATION
                    </div>
                    <h1 className="font-serif text-4xl sm:text-5xl text-stone-900 dark:text-stone-100 font-light tracking-tight mb-4">
                        Contact Laboratory & Research Team
                    </h1>
                    <p className="font-sans text-base text-stone-600 dark:text-stone-400 max-w-2xl mx-auto font-light leading-relaxed">
                        For academic inquiries, dataset access requests, or healthcare institutional integration of the OSCC triage engine.
                    </p>
                </div>

                <div className="grid md:grid-cols-12 gap-12 items-start">
                    {/* Left: Contact Form (7 cols) */}
                    <div className="md:col-span-7 border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-8 relative">
                        <span className="absolute -top-1 -left-1 text-[10px] font-mono text-stone-400">+</span>
                        <span className="absolute -top-1 -right-1 text-[10px] font-mono text-stone-400">+</span>

                        <div className="font-mono text-[10px] text-stone-500 uppercase tracking-widest mb-6 border-b border-stone-200 dark:border-stone-800 pb-2">
                            TRANSMISSION DISPATCH FORM
                        </div>

                        {sent ? (
                            <div className="py-12 text-center">
                                <CheckCircle2 className="w-12 h-12 text-clinical-teal mx-auto mb-4" />
                                <h3 className="font-serif text-2xl text-stone-900 dark:text-stone-100 font-normal mb-2">
                                    Transmission Logged
                                </h3>
                                <p className="font-sans text-xs text-stone-500 max-w-sm mx-auto font-light">
                                    Your research inquiry has been dispatched to the engineering team. Expect a response within 24–48 hours.
                                </p>
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit} className="space-y-4 font-mono text-xs">
                                <div>
                                    <label className="block text-[10px] uppercase text-stone-500 mb-1">Full Name & Credentials</label>
                                    <input 
                                        type="text" 
                                        required
                                        placeholder="Dr. Samantha Rao, MD"
                                        className="w-full px-3 py-2.5 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                    />
                                </div>

                                <div>
                                    <label className="block text-[10px] uppercase text-stone-500 mb-1">Institutional / Email Address</label>
                                    <input 
                                        type="email" 
                                        required
                                        placeholder="samantha.rao@hospital.org"
                                        className="w-full px-3 py-2.5 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                    />
                                </div>

                                <div>
                                    <label className="block text-[10px] uppercase text-stone-500 mb-1">Subject / Clinical Department</label>
                                    <input 
                                        type="text" 
                                        placeholder="Oncology Screening Trial Integration"
                                        className="w-full px-3 py-2.5 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                    />
                                </div>

                                <div>
                                    <label className="block text-[10px] uppercase text-stone-500 mb-1">Message / Inquiry Details</label>
                                    <textarea 
                                        rows="5"
                                        required
                                        placeholder="Please provide details regarding your inquiry or proposed clinical evaluation..."
                                        className="w-full px-3 py-2.5 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                    ></textarea>
                                </div>

                                <button 
                                    type="submit"
                                    className="w-full py-3.5 bg-stone-900 dark:bg-stone-100 text-stone-100 dark:text-stone-900 text-xs font-mono uppercase tracking-wider font-semibold hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-colors flex items-center justify-center gap-2 mt-6"
                                >
                                    <Send className="w-3.5 h-3.5" />
                                    <span>Transmit Communication</span>
                                </button>
                            </form>
                        )}
                    </div>

                    {/* Right: Department Details (5 cols) */}
                    <div className="md:col-span-5 space-y-6">
                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6">
                            <span className="font-mono text-[10px] text-stone-400 uppercase tracking-widest block mb-2">RESEARCH INSTITUTION</span>
                            <h3 className="font-serif text-xl font-normal text-stone-900 dark:text-stone-100 mb-3">
                                Department of Computer Science & Engineering
                            </h3>
                            <div className="font-mono text-xs text-stone-600 dark:text-stone-400 space-y-2">
                                <div className="flex items-start gap-2">
                                    <MapPin className="w-4 h-4 text-clinical-teal flex-shrink-0 mt-0.5" />
                                    <span>Karnataka, India</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <Mail className="w-4 h-4 text-clinical-teal flex-shrink-0 mt-0.5" />
                                    <span>research@oralcancer-ai.org</span>
                                </div>
                            </div>
                        </div>

                        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6">
                            <span className="font-mono text-[10px] text-stone-400 uppercase tracking-widest block mb-2">ACADEMIC SUPERVISION</span>
                            <h3 className="font-serif text-lg font-medium text-stone-900 dark:text-stone-100">
                                Prof. Aishwarya S
                            </h3>
                            <p className="font-sans text-xs text-stone-500 mt-1 font-light leading-relaxed">
                                Project Guide & Academic Supervisor. Overseeing clinical model validation and ethical deep learning compliance.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Contact;