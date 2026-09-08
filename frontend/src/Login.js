import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LogIn, User, Lock, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from './api';
import loginImage from './images/3.jpg';

const Login = ({ onLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await axios.post(`${API_BASE_URL}/login`, formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            onLogin(response.data.access_token);
            navigate('/upload');
        } catch (err) {
            const msg = err.response?.data?.detail || err.response?.data?.error || 'Invalid credentials. Please verify your practitioner ID and password.';
            setError(msg);
        } finally {
            setLoading(false);
        }
    };

    const handleFillDemo = () => {
        setEmail('dr_clinician');
        setPassword('ClinicianPass123!');
    };

    return (
        <div className="min-h-[85vh] bg-slate-50 dark:bg-[#080B10] flex items-center justify-center p-4 font-sans text-slate-800 dark:text-slate-200 transition-colors">
            <div className="w-full max-w-4xl mx-auto rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xl overflow-hidden grid lg:grid-cols-12">
                {/* Form Column (7 cols) */}
                <div className="lg:col-span-7 p-8 sm:p-12 space-y-6">
                    <div>
                        <Link to="/" className="inline-flex items-center gap-1.5 font-mono text-xs text-teal-600 dark:text-teal-400 hover:underline mb-4">
                            &larr; Return to Platform Overview
                        </Link>
                        <div className="flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-teal-500"></span>
                            <span className="font-mono text-[10px] text-slate-400 uppercase tracking-widest">
                                CLINICAL ACCESS PORTAL
                            </span>
                        </div>
                        <h1 className="font-serif text-3xl sm:text-4xl text-slate-900 dark:text-white font-normal mt-1">
                            Practitioner Login
                        </h1>
                        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-light">
                            Enter authorized medical or dental credentials to access screening tools and patient dossiers.
                        </p>
                    </div>

                    {error && (
                        <div className="p-3.5 rounded-xl border border-rose-500/30 bg-rose-500/10 flex items-start gap-2 text-xs text-rose-600 dark:text-rose-400">
                            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                            <span>{error}</span>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4 text-xs font-sans">
                        <div>
                            <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1.5">
                                Clinician Identifier / Email *
                            </label>
                            <div className="relative">
                                <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                <input 
                                    type="text" 
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="e.g. dr_clinician"
                                    className="w-full pl-9 pr-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1.5">
                                Security Passkey *
                            </label>
                            <div className="relative">
                                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                <input 
                                    type="password" 
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="••••••••••••"
                                    className="w-full pl-9 pr-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>
                        </div>

                        <button 
                            type="submit" 
                            disabled={loading}
                            className="w-full py-3 px-6 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-mono text-xs tracking-wider uppercase font-semibold flex items-center justify-center gap-2 shadow-lg shadow-teal-500/20 transition-all disabled:opacity-50"
                        >
                            {loading ? (
                                <span>Verifying Credentials...</span>
                            ) : (
                                <>
                                    <span>Authenticate Session</span>
                                    <ArrowRight className="w-4 h-4" />
                                </>
                            )}
                        </button>
                    </form>

                    {/* Auto-fill demo credentials button */}
                    <div className="pt-1">
                        <button
                            type="button"
                            onClick={handleFillDemo}
                            className="w-full py-2 px-3 rounded-lg border border-dashed border-slate-300 dark:border-slate-700 text-slate-500 hover:text-teal-600 hover:border-teal-500 text-[11px] font-mono transition-colors text-center"
                        >
                            Auto-fill demo clinician credentials
                        </button>
                    </div>

                    <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500">
                        <span>Need clinical authorization?</span>
                        <Link to="/register" className="text-teal-600 dark:text-teal-400 font-medium hover:underline font-mono">
                            Register Clinician Profile &rarr;
                        </Link>
                    </div>
                </div>

                {/* Right Image/Context Column (5 cols) */}
                <div className="hidden lg:flex lg:col-span-5 relative bg-slate-950 p-8 flex-col justify-between overflow-hidden">
                    <img 
                        src={loginImage} 
                        alt="Pathological Inspection" 
                        className="absolute inset-0 w-full h-full object-cover opacity-25"
                    />
                    <div className="relative z-10 space-y-2">
                        <span className="font-mono text-[10px] text-teal-400 uppercase tracking-widest block">
                            SECURITY SPECIFICATION
                        </span>
                        <h3 className="font-serif text-xl text-white font-medium">
                            Role-Governed Diagnostic Environment
                        </h3>
                        <p className="text-xs text-slate-400 font-light leading-relaxed">
                            Audit-compliant session authentication conforming to HIPAA data handling rules and ISO 27799 health informatics standards.
                        </p>
                    </div>

                    <div className="relative z-10 pt-6 border-t border-slate-800 text-[11px] font-mono text-emerald-400 flex items-center gap-2">
                        <ShieldCheck className="w-4 h-4 shrink-0" />
                        <span>256-bit SHA-256 JWT Tokenization</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;