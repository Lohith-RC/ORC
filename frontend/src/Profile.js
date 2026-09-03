import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { User, Mail, Calendar, Edit3, Save, X, BarChart, AlertTriangle, Clock, ShieldCheck, ShieldAlert, FileText } from 'lucide-react';
import axios from 'axios';
import profileImage from './images/7.webp';

const Profile = ({ token }) => {
    const [user, setUser] = useState(null);
    const [history, setHistory] = useState([]);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({ full_name: '', email: '' });
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            if (!token) {
                setLoading(false);
                return;
            }
            try {
                const userPromise = axios.get('http://localhost:8000/me', { headers: { Authorization: `Bearer ${token}` } });
                const historyPromise = axios.get('http://localhost:8000/me/analyses', { headers: { Authorization: `Bearer ${token}` } });
                
                const [userResponse, historyResponse] = await Promise.all([userPromise, historyPromise]);

                setUser(userResponse.data);
                setFormData({ full_name: userResponse.data.full_name, email: userResponse.data.email });
                setHistory(historyResponse.data);
            } catch (err) {
                setError('Could not retrieve practitioner dossier. Please verify network connection.');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [token]);

    const handleFormChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSave = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');
        try {
            const response = await axios.post('http://localhost:8000/me/update', formData, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUser(response.data);
            setMessage('Practitioner profile updated successfully.');
            setIsEditing(false);
        } catch (err) {
            setError('Failed to persist profile modifications.');
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-parchment-100 dark:bg-ink-950 flex items-center justify-center font-mono text-xs text-stone-500">
                LOADING PRACTITIONER DOSSIER...
            </div>
        );
    }

    return (
        <div className="bg-parchment-100 dark:bg-ink-950 min-h-screen py-12 px-4 sm:px-6 lg:px-8 font-sans text-stone-800 dark:text-stone-200">
            <div className="max-w-5xl mx-auto space-y-8">
                {/* Header */}
                <div className="border-b border-stone-200 dark:border-stone-800 pb-4 flex items-center justify-between font-mono text-xs text-stone-500">
                    <span>PRACTITIONER DOSSIER // REPOSITORY ARCHIVE</span>
                    <span>ID: USR-{user?.id || '001'}</span>
                </div>

                {error && (
                    <div className="p-3 border border-red-300 dark:border-red-900 bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300 font-mono text-xs flex items-center gap-2">
                        <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                        <span>{error}</span>
                    </div>
                )}
                {message && (
                    <div className="p-3 border border-teal-300 dark:border-teal-900 bg-teal-50 dark:bg-teal-950/20 text-teal-800 dark:text-teal-300 font-mono text-xs flex items-center gap-2">
                        <ShieldCheck className="w-4 h-4 flex-shrink-0" />
                        <span>{message}</span>
                    </div>
                )}

                {/* Profile Overview Card */}
                <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-8 relative">
                    <span className="absolute -top-1 -left-1 text-[10px] font-mono text-stone-400">+</span>
                    <span className="absolute -top-1 -right-1 text-[10px] font-mono text-stone-400">+</span>

                    <form onSubmit={handleSave}>
                        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-8">
                            <div className="relative w-32 h-32 flex-shrink-0 border border-stone-300 dark:border-stone-700 bg-stone-950">
                                <img src={profileImage} alt="Profile" className="w-full h-full object-cover filter grayscale contrast-105" />
                                <button 
                                    type="button"
                                    onClick={() => setIsEditing(!isEditing)}
                                    className="absolute -bottom-2 -right-2 p-1.5 bg-stone-900 text-white text-xs font-mono hover:bg-clinical-teal transition-colors"
                                    title="Edit credentials"
                                >
                                    <Edit3 className="w-3.5 h-3.5" />
                                </button>
                            </div>

                            <div className="flex-grow text-center sm:text-left">
                                {isEditing ? (
                                    <div className="space-y-3 font-mono text-xs">
                                        <div>
                                            <label className="block text-[10px] text-stone-400 uppercase mb-1">Full Name</label>
                                            <input 
                                                type="text"
                                                name="full_name"
                                                value={formData.full_name}
                                                onChange={handleFormChange}
                                                className="w-full px-3 py-1.5 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-sm font-sans"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-[10px] text-stone-400 uppercase mb-1">Email</label>
                                            <input 
                                                type="email"
                                                name="email"
                                                value={formData.email}
                                                onChange={handleFormChange}
                                                className="w-full px-3 py-1.5 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-sm font-sans"
                                            />
                                        </div>
                                        <div className="flex gap-2 pt-2">
                                            <button type="submit" className="px-4 py-1.5 bg-clinical-teal text-white text-xs font-mono uppercase">
                                                Save Modifications
                                            </button>
                                            <button type="button" onClick={() => setIsEditing(false)} className="px-3 py-1.5 border border-stone-300 text-xs font-mono uppercase">
                                                Cancel
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    <div>
                                        <span className="font-mono text-[10px] text-clinical-teal dark:text-teal-400 uppercase tracking-widest block mb-1">
                                            CLINICAL PRACTITIONER
                                        </span>
                                        <h1 className="font-serif text-3xl text-stone-900 dark:text-stone-100 font-normal">
                                            {user?.full_name || user?.username}
                                        </h1>
                                        <p className="font-mono text-xs text-stone-500 mt-1">
                                            ID: @{user?.username} • {user?.email}
                                        </p>
                                        <div className="mt-4 pt-4 border-t border-stone-200 dark:border-stone-800 flex flex-wrap gap-4 font-mono text-xs text-stone-500">
                                            <span>REGISTERED: {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</span>
                                            <span>TOTAL SPECIMENS EVALUATED: {history.length}</span>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </form>
                </div>

                {/* Analysis History Log */}
                <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-8">
                    <div className="flex items-center justify-between border-b border-stone-200 dark:border-stone-800 pb-3 mb-6">
                        <div className="flex items-center gap-2">
                            <FileText className="w-4 h-4 text-clinical-teal" />
                            <h2 className="font-serif text-2xl text-stone-900 dark:text-stone-100 font-normal">
                                Historical Specimen Triage Log
                            </h2>
                        </div>
                        <span className="font-mono text-xs text-stone-400">{history.length} RECORDS</span>
                    </div>

                    {history.length > 0 ? (
                        <div className="space-y-3">
                            {history.map(item => {
                                const isCancer = item.prediction?.toLowerCase() === 'cancer';
                                const isUncertain = item.prediction?.toLowerCase() === 'uncertain';

                                return (
                                    <div 
                                        key={item.id} 
                                        className="border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950 p-4 flex flex-col sm:flex-row justify-between sm:items-center gap-4"
                                    >
                                        <div className="flex items-center gap-3">
                                            {isCancer ? (
                                                <div className="p-2 border border-clinical-terracotta bg-red-50 dark:bg-red-950/20 text-clinical-terracotta">
                                                    <ShieldAlert className="w-4 h-4" />
                                                </div>
                                            ) : isUncertain ? (
                                                <div className="p-2 border border-clinical-ochre bg-amber-50 dark:bg-amber-950/20 text-clinical-ochre">
                                                    <AlertTriangle className="w-4 h-4" />
                                                </div>
                                            ) : (
                                                <div className="p-2 border border-clinical-teal bg-teal-50 dark:bg-teal-950/20 text-clinical-teal">
                                                    <ShieldCheck className="w-4 h-4" />
                                                </div>
                                            )}

                                            <div>
                                                <div className="font-serif text-base font-normal text-stone-900 dark:text-stone-100">
                                                    {isCancer ? 'Presumptive OSCC Malignancy' : isUncertain ? 'Uncertain / Variance Outlier' : 'Non-Malignant Mucosa'}
                                                </div>
                                                <div className="font-mono text-[10px] text-stone-400 space-x-2">
                                                    <span>CONF: {(item.confidence * 100).toFixed(1)}%</span>
                                                    {item.uncertainty !== null && <span>• σ²: {item.uncertainty}</span>}
                                                    {item.risk_score !== null && <span>• RISK: {item.risk_score}</span>}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="font-mono text-xs text-stone-500 text-left sm:text-right">
                                            <div>{new Date(item.timestamp).toLocaleDateString()}</div>
                                            <div className="text-[10px] text-stone-400">{new Date(item.timestamp).toLocaleTimeString()}</div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="text-center py-12 font-mono text-xs text-stone-400">
                            NO RECORDED INTAKE SPECIMENS IN THIS DOSSIER.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Profile;