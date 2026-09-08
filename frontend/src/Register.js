import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { User, Lock, Mail, ArrowRight, UserCheck, ShieldCheck, AlertCircle } from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from './api';
import registerImage from './images/4.jpg';

const Register = ({ onLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [fullName, setFullName] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            await axios.post(`${API_BASE_URL}/register`, { 
                username: username.trim(),
                password: password,
                full_name: fullName.trim(),
                email: email.trim()
            });

            const loginParams = new URLSearchParams();
            loginParams.append('username', username.trim());
            loginParams.append('password', password);
            const loginResponse = await axios.post(`${API_BASE_URL}/login`, loginParams, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            
            onLogin(loginResponse.data.access_token);
            navigate('/upload');

        } catch (err) {
            const detail = err.response?.data?.detail;
            if (Array.isArray(detail)) {
                setError(detail.map(d => d.msg).join('. '));
            } else {
                setError(detail || 'Registration failed. The username or email might already exist.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-[85vh] bg-slate-50 dark:bg-[#080B10] flex items-center justify-center p-4 font-sans text-slate-800 dark:text-slate-200 transition-colors">
            <div className="w-full max-w-4xl mx-auto rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xl overflow-hidden grid lg:grid-cols-12">
                {/* Left Context Column (5 cols) */}
                <div className="hidden lg:flex lg:col-span-5 relative bg-slate-950 p-8 flex-col justify-between overflow-hidden">
                    <img 
                        src={registerImage} 
                        alt="Clinical Microscopy Lab" 
                        className="absolute inset-0 w-full h-full object-cover opacity-25" 
                    />
                    <div className="relative z-10 space-y-2">
                        <span className="font-mono text-[10px] text-teal-400 uppercase tracking-widest block">
                            PRACTITIONER ENROLLMENT
                        </span>
                        <h3 className="font-serif text-xl text-white font-medium">
                            Join the Oncology Screening Consortium
                        </h3>
                        <p className="text-xs text-slate-400 font-light leading-relaxed">
                            Authorized accounts enable patient timeline tracking, ground-truth biopsy verification, and automated HL7 FHIR clinical referral exports.
                        </p>
                    </div>

                    <div className="relative z-10 pt-6 border-t border-slate-800 text-[11px] font-mono text-teal-400 flex items-center gap-2">
                        <UserCheck className="w-4 h-4 shrink-0" />
                        <span>Federated Clinician Identity Management</span>
                    </div>
                </div>

                {/* Form Column (7 cols) */}
                <div className="lg:col-span-7 p-8 sm:p-12 space-y-6">
                    <div>
                        <Link to="/" className="inline-flex items-center gap-1.5 font-mono text-xs text-teal-600 dark:text-teal-400 hover:underline mb-4">
                            &larr; Return to Platform Overview
                        </Link>
                        <div className="flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-teal-500"></span>
                            <span className="font-mono text-[10px] text-slate-400 uppercase tracking-widest">
                                ENROLLMENT FORM
                            </span>
                        </div>
                        <h1 className="font-serif text-3xl sm:text-4xl text-slate-900 dark:text-white font-normal mt-1">
                            Register Clinician Profile
                        </h1>
                        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-light">
                            Create an authorized account to conduct oral screenings and manage patient dossiers.
                        </p>
                    </div>

                    {error && (
                        <div className="p-3.5 rounded-xl border border-rose-500/30 bg-rose-500/10 flex items-start gap-2 text-xs text-rose-600 dark:text-rose-400">
                            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                            <span>{error}</span>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-3.5 text-xs font-sans">
                        <div>
                            <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1">
                                Full Name & Credentials *
                            </label>
                            <input 
                                type="text" 
                                required
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                placeholder="Dr. Ananya Murthy, MDS"
                                className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none"
                            />
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            <div>
                                <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1">
                                    Username / Identifier *
                                </label>
                                <input 
                                    type="text" 
                                    required
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    placeholder="dr_ananya"
                                    className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none font-mono"
                                />
                            </div>

                            <div>
                                <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1">
                                    Hospital / Clinic Email *
                                </label>
                                <input 
                                    type="email" 
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="ananya@hospital.org"
                                    className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-[11px] font-mono uppercase text-slate-500 mb-1">
                                Security Passkey *
                            </label>
                            <input 
                                type="password" 
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••••••"
                                className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none"
                            />
                        </div>

                        <button 
                            type="submit" 
                            disabled={loading}
                            className="w-full py-3 px-6 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-mono text-xs tracking-wider uppercase font-semibold flex items-center justify-center gap-2 shadow-lg shadow-teal-500/20 transition-all disabled:opacity-50 mt-2"
                        >
                            {loading ? (
                                <span>Authorizing Practitioner Account...</span>
                            ) : (
                                <>
                                    <span>Create Authorized Account</span>
                                    <ArrowRight className="w-4 h-4" />
                                </>
                            )}
                        </button>
                    </form>

                    <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500">
                        <span>Already credentialed?</span>
                        <Link to="/login" className="text-teal-600 dark:text-teal-400 font-medium hover:underline font-mono">
                            Sign In to Workstation &rarr;
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;