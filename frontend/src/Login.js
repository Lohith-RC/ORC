import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LogIn, User, Lock, ArrowRight, Shield } from 'lucide-react';
import axios from 'axios';
import loginImage from './images/3.jpg';

const Login = ({ onLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await axios.post('http://localhost:8000/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            onLogin(response.data.access_token);
            navigate('/profile');
        } catch (err) {
            const msg = err.response?.data?.detail || err.response?.data?.error || 'Invalid credentials. Please verify your username and password.';
            setError(msg);
        }
    };

    return (
        <div className="min-h-screen bg-parchment-100 dark:bg-ink-950 flex items-center justify-center p-4 font-sans text-stone-800 dark:text-stone-200">
            <div className="w-full max-w-5xl mx-auto border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 shadow-xl overflow-hidden grid lg:grid-cols-12 relative">
                <span className="absolute -top-1 -left-1 text-[10px] font-mono text-stone-400">+</span>
                <span className="absolute -top-1 -right-1 text-[10px] font-mono text-stone-400">+</span>
                
                {/* Form Column (7 cols) */}
                <div className="lg:col-span-7 p-8 sm:p-14">
                    <div className="mb-8">
                        <Link to="/" className="inline-block mb-4 font-mono text-xs text-clinical-teal dark:text-teal-400 hover:underline">
                            &larr; RETURN TO REPOSITORY HOME
                        </Link>
                        <span className="font-mono text-[10px] text-stone-400 uppercase tracking-widest block mb-1">
                            AUTH PROTOCOL // CLINICAL ACCESS
                        </span>
                        <h1 className="font-serif text-3xl sm:text-4xl text-stone-900 dark:text-stone-100 font-normal">
                            Practitioner Login
                        </h1>
                        <p className="font-sans text-xs text-stone-500 mt-2">
                            Enter authorized credentials to access patient screening history and analysis records.
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4 font-mono text-xs">
                        <div>
                            <label className="block text-[10px] uppercase text-stone-500 mb-1">Username or Identifier</label>
                            <div className="relative">
                                <User className="w-4 h-4 text-stone-400 absolute left-3 top-1/2 -translate-y-1/2" />
                                <input
                                    type="text"
                                    placeholder="Enter username"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full pl-9 pr-3 py-2.5 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
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
                                    className="w-full pl-9 pr-3 py-2.5 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 text-sm font-sans focus:outline-none focus:border-clinical-teal"
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
                                className="w-full py-3.5 bg-stone-900 dark:bg-stone-100 text-stone-100 dark:text-stone-900 text-xs font-mono uppercase tracking-wider font-semibold hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-colors flex items-center justify-center gap-2"
                            >
                                <span>Authenticate Session</span>
                                <ArrowRight className="w-4 h-4" />
                            </button>
                        </div>

                        <div className="pt-4 border-t border-stone-200 dark:border-stone-800 text-center font-sans text-xs text-stone-500">
                            Need authorization?{' '}
                            <Link to="/register" className="font-mono text-clinical-teal dark:text-teal-400 hover:underline">
                                Register new clinician account
                            </Link>
                        </div>
                    </form>
                </div>

                {/* Right Aesthetic Imagery (5 cols) */}
                <div className="hidden lg:block lg:col-span-5 relative bg-stone-950 border-l border-stone-200 dark:border-stone-800">
                    <img src={loginImage} alt="Clinical Lab" className="w-full h-full object-cover filter contrast-105 opacity-80" />
                    <div className="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/40 to-transparent flex flex-col justify-end p-8 text-white">
                        <div className="font-mono text-[10px] uppercase text-clinical-teal tracking-widest mb-1">
                            SECURE ACCESS CONTROL
                        </div>
                        <h3 className="font-serif text-2xl font-light">Visionary Diagnostics</h3>
                        <p className="font-mono text-xs text-stone-400 mt-2">
                            JWT 256-bit encrypted authentication layer. Protected health information safeguards active.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;