import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { User, Lock, Mail, ArrowRight, UserCheck } from 'lucide-react';
import axios from 'axios';
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
            await axios.post('http://localhost:8000/register', { 
                username: username.trim(),
                password: password,
                full_name: fullName.trim(),
                email: email.trim()
            });

            const loginParams = new URLSearchParams();
            loginParams.append('username', username.trim());
            loginParams.append('password', password);
            const loginResponse = await axios.post('http://localhost:8000/login', loginParams, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            
            onLogin(loginResponse.data.access_token);
            navigate('/profile');

        } catch (err) {
            const detail = err.response?.data?.detail;
            if (Array.isArray(detail)) {
                setError(detail.map(d => d.msg).join('. '));
            } else {
                setError(detail || 'Registration failed. Please check your credentials.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-parchment-100 dark:bg-ink-950 flex items-center justify-center p-4 font-sans text-stone-800 dark:text-stone-200">
            <div className="w-full max-w-5xl mx-auto border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 shadow-xl overflow-hidden grid lg:grid-cols-12 relative">
                <span className="absolute -top-1 -left-1 text-[10px] font-mono text-stone-400">+</span>
                <span className="absolute -top-1 -right-1 text-[10px] font-mono text-stone-400">+</span>

                {/* Imagery Column (5 cols) */}
                <div className="hidden lg:block lg:col-span-5 relative bg-stone-950 border-r border-stone-200 dark:border-stone-800">
                    <img src={registerImage} alt="Clinical Lab" className="w-full h-full object-cover filter contrast-105 opacity-80" />
                    <div className="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/40 to-transparent flex flex-col justify-end p-8 text-white">
                        <div className="font-mono text-[10px] uppercase text-clinical-teal tracking-widest mb-1">
                            RESEARCH & CLINICAL NETWORK
                        </div>
                        <h3 className="font-serif text-2xl font-light">Join the Screening Portal</h3>
                        <p className="font-mono text-xs text-stone-400 mt-2">
                            Securely track patient cohorts, export comprehensive diagnostic PDFs, and monitor triage analytics.
                        </p>
                    </div>
                </div>

                {/* Form Column (7 cols) */}
                <div className="lg:col-span-7 p-8 sm:p-14">
                    <div className="mb-6">
                        <Link to="/" className="inline-block mb-4 font-mono text-xs text-clinical-teal dark:text-teal-400 hover:underline">
                            &larr; RETURN TO REPOSITORY HOME
                        </Link>
                        <span className="font-mono text-[10px] text-stone-400 uppercase tracking-widest block mb-1">
                            REGISTRATION PROTOCOL
                        </span>
                        <h1 className="font-serif text-3xl sm:text-4xl text-stone-900 dark:text-stone-100 font-normal">
                            Create Practitioner Profile
                        </h1>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-3.5 font-mono text-xs">
                        <div>
                            <label className="block text-[10px] uppercase text-stone-500 mb-1">Full Name & Title</label>
                            <div className="relative">
                                <User className="w-4 h-4 text-stone-400 absolute left-3 top-1/2 -translate-y-1/2" />
                                <input
                                    type="text"
                                    placeholder="Dr. Samantha Rao"
                                    value={fullName}
                                    onChange={(e) => setFullName(e.target.value)}
                                    className="w-full pl-9 pr-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-[10px] uppercase text-stone-500 mb-1">Username Identifier</label>
                            <div className="relative">
                                <UserCheck className="w-4 h-4 text-stone-400 absolute left-3 top-1/2 -translate-y-1/2" />
                                <input
                                    type="text"
                                    placeholder="samantha_rao"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="w-full pl-9 pr-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-[10px] uppercase text-stone-500 mb-1">Email Address</label>
                            <div className="relative">
                                <Mail className="w-4 h-4 text-stone-400 absolute left-3 top-1/2 -translate-y-1/2" />
                                <input
                                    type="email"
                                    placeholder="samantha@hospital.org"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full pl-9 pr-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-[10px] uppercase text-stone-500 mb-1">Password</label>
                            <div className="relative">
                                <Lock className="w-4 h-4 text-stone-400 absolute left-3 top-1/2 -translate-y-1/2" />
                                <input
                                    type="password"
                                    placeholder="••••••••"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full pl-9 pr-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                    required
                                />
                            </div>
                        </div>

                        {error && (
                            <p className="p-2 border border-red-300 dark:border-red-900 bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 text-xs">
                                {error}
                            </p>
                        )}

                        <div className="pt-2">
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full py-3.5 bg-stone-900 dark:bg-stone-100 text-stone-100 dark:text-stone-900 text-xs font-mono uppercase tracking-wider font-semibold hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-colors flex items-center justify-center gap-2"
                            >
                                <span>{loading ? 'Registering Practitioner...' : 'Initialize Profile'}</span>
                                <ArrowRight className="w-4 h-4" />
                            </button>
                        </div>

                        <div className="pt-3 border-t border-stone-200 dark:border-stone-800 text-center font-sans text-xs text-stone-500">
                            Already authorized?{' '}
                            <Link to="/login" className="font-mono text-clinical-teal dark:text-teal-400 hover:underline">
                                Sign into existing profile
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Register;