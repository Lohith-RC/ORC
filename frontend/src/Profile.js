import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    User, 
    Mail, 
    Calendar, 
    Edit3, 
    Save, 
    X, 
    BarChart3, 
    AlertTriangle, 
    Clock, 
    ShieldCheck, 
    ShieldAlert, 
    FileText, 
    Camera, 
    Building2, 
    Award, 
    Activity, 
    PlusCircle, 
    Download, 
    CheckCircle2,
    Microscope,
    Sliders,
    Search,
    Filter,
    RefreshCw
} from 'lucide-react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import defaultProfileImage from './images/7.webp';

const Profile = ({ token }) => {
    const [user, setUser] = useState(null);
    const [history, setHistory] = useState([]);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({ 
        full_name: '', 
        email: '',
        department: 'Oral & Maxillofacial Oncology',
        license_no: 'DCI-KA-2024-8842',
        institution: 'Regional Cancer Care & Screening Center',
        specialization: 'Oral Cancer Early Triage & Dysplasia Screening'
    });
    const [avatarUrl, setAvatarUrl] = useState(null);
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const [historyFilter, setHistoryFilter] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');

    const fileInputRef = useRef(null);

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

                const userData = userResponse.data;
                setUser(userData);

                // Load custom practitioner metadata from localStorage if saved previously
                const savedMetaKey = `practitioner_meta_${userData.username || userData.id}`;
                const savedMeta = localStorage.getItem(savedMetaKey);
                const parsedMeta = savedMeta ? JSON.parse(savedMeta) : {};

                setFormData({
                    full_name: userData.full_name || '',
                    email: userData.email || '',
                    department: parsedMeta.department || 'Oral & Maxillofacial Oncology',
                    license_no: parsedMeta.license_no || 'DCI-KA-2024-8842',
                    institution: parsedMeta.institution || 'Regional Cancer Care & Screening Center',
                    specialization: parsedMeta.specialization || 'Oral Cancer Early Triage & Dysplasia Screening'
                });

                // Load custom avatar from localStorage if available
                const savedAvatar = localStorage.getItem(`profile_avatar_${userData.username || userData.id}`);
                if (savedAvatar) {
                    setAvatarUrl(savedAvatar);
                }

                setHistory(historyResponse.data || []);
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

    const handleAvatarClick = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    };

    const handleAvatarChange = (e) => {
        const file = e.target.files?.[0];
        if (file) {
            if (file.size > 5 * 1024 * 1024) {
                setError('Image size exceeds 5MB limit.');
                return;
            }
            const reader = new FileReader();
            reader.onload = () => {
                const base64Data = reader.result;
                setAvatarUrl(base64Data);
                if (user) {
                    localStorage.setItem(`profile_avatar_${user.username || user.id}`, base64Data);
                }
                setMessage('Profile photo updated successfully!');
            };
            reader.readAsDataURL(file);
        }
    };

    const handleRemoveAvatar = (e) => {
        e.stopPropagation();
        setAvatarUrl(null);
        if (user) {
            localStorage.removeItem(`profile_avatar_${user.username || user.id}`);
        }
        setMessage('Reset to default practitioner avatar.');
    };

    const handleSave = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');
        try {
            const response = await axios.post('http://localhost:8000/me/update', {
                full_name: formData.full_name,
                email: formData.email
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUser(response.data);

            // Persist clinical practitioner extended metadata in localStorage
            if (user) {
                const savedMetaKey = `practitioner_meta_${user.username || user.id}`;
                localStorage.setItem(savedMetaKey, JSON.stringify({
                    department: formData.department,
                    license_no: formData.license_no,
                    institution: formData.institution,
                    specialization: formData.specialization
                }));
            }

            setMessage('Practitioner dossier and credentials updated successfully.');
            setIsEditing(false);
        } catch (err) {
            setError('Failed to persist profile modifications.');
        }
    };

    // Calculate live clinical statistics
    const totalAnalyses = history.length;
    const cancerCases = history.filter(h => h.prediction?.toLowerCase() === 'cancer').length;
    const benignCases = history.filter(h => h.prediction?.toLowerCase() === 'non-cancer' || h.prediction?.toLowerCase() === 'non_cancer').length;
    const uncertainCases = history.filter(h => h.prediction?.toLowerCase() === 'uncertain').length;
    const avgConfidence = totalAnalyses > 0 
        ? ((history.reduce((acc, curr) => acc + (curr.confidence || 0), 0) / totalAnalyses) * 100).toFixed(1)
        : '0.0';

    // Filter historical records
    const filteredHistory = history.filter(item => {
        const pred = item.prediction?.toLowerCase() || '';
        const matchesFilter = 
            historyFilter === 'all' ? true :
            historyFilter === 'cancer' ? pred === 'cancer' :
            historyFilter === 'benign' ? (pred === 'non-cancer' || pred === 'non_cancer') :
            historyFilter === 'uncertain' ? pred === 'uncertain' : true;
        
        const matchesSearch = searchQuery === '' || 
            item.image_filename?.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.id.toString().includes(searchQuery) ||
            pred.includes(searchQuery.toLowerCase());

        return matchesFilter && matchesSearch;
    });

    const exportAuditCSV = () => {
        if (history.length === 0) return;
        const headers = "ID,Prediction,Confidence,Uncertainty_Variance,Risk_Score,Quality_Score,Timestamp\n";
        const rows = history.map(h => 
            `${h.id},${h.prediction},${(h.confidence * 100).toFixed(2)}%,${h.uncertainty || 'N/A'},${h.risk_score || 'N/A'},${h.image_quality_score || 'N/A'},"${new Date(h.timestamp).toISOString()}"`
        ).join("\n");
        
        const blob = new Blob([headers + rows], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `OSCC_Clinical_Audit_${user?.username || 'dossier'}.csv`;
        a.click();
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-parchment-100 dark:bg-ink-950 flex flex-col items-center justify-center font-mono text-xs text-stone-500 space-y-3">
                <div className="w-8 h-8 border-2 border-clinical-teal border-t-transparent rounded-full animate-spin"></div>
                <span>LOADING PRACTITIONER DOSSIER & ANALYTICS...</span>
            </div>
        );
    }

    return (
        <div className="bg-parchment-100 dark:bg-ink-950 min-h-screen py-10 px-4 sm:px-6 lg:px-8 font-sans text-stone-800 dark:text-stone-200">
            <div className="max-w-6xl mx-auto space-y-8">
                
                {/* Hidden File Input for Avatar Upload */}
                <input 
                    type="file" 
                    ref={fileInputRef} 
                    accept="image/jpeg,image/png,image/webp" 
                    className="hidden" 
                    onChange={handleAvatarChange}
                />

                {/* Top Telemetry Header */}
                <div className="border-b border-stone-200 dark:border-stone-800 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2 font-mono text-xs text-stone-500">
                    <div className="flex items-center gap-3">
                        <span className="w-2 h-2 bg-clinical-teal rounded-none inline-block"></span>
                        <span className="uppercase tracking-wider font-semibold text-stone-800 dark:text-stone-200">
                            PRACTITIONER DOSSIER & WORKSTATION ARCHIVE
                        </span>
                    </div>
                    <div className="flex items-center gap-4 text-[11px]">
                        <span>IDENTIFIER: <strong className="text-stone-800 dark:text-stone-200">USR-{(user?.id || 1).toString().padStart(4, '0')}</strong></span>
                        <span>•</span>
                        <span>SESSION: <strong className="text-emerald-600 dark:text-emerald-400">ENCRYPTED / ACTIVE</strong></span>
                    </div>
                </div>

                {/* Alerts */}
                <AnimatePresence>
                    {error && (
                        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="p-3 border border-red-300 dark:border-red-900 bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300 font-mono text-xs flex items-center gap-2">
                            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                            <span>{error}</span>
                        </motion.div>
                    )}
                    {message && (
                        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="p-3 border border-teal-300 dark:border-teal-900 bg-teal-50 dark:bg-teal-950/20 text-teal-800 dark:text-teal-300 font-mono text-xs flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 flex-shrink-0 text-clinical-teal" />
                            <span>{message}</span>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* ============================================================ */}
                {/* SECTION 1: PRACTITIONER CREDENTIALS & PROFILE CARD           */}
                {/* ============================================================ */}
                <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6 sm:p-8 relative shadow-sm">
                    <span className="absolute -top-1 -left-1 text-[10px] font-mono text-stone-400">+</span>
                    <span className="absolute -top-1 -right-1 text-[10px] font-mono text-stone-400">+</span>
                    <span className="absolute -bottom-1 -left-1 text-[10px] font-mono text-stone-400">+</span>
                    <span className="absolute -bottom-1 -right-1 text-[10px] font-mono text-stone-400">+</span>

                    <form onSubmit={handleSave}>
                        <div className="flex flex-col md:flex-row items-start gap-8">
                            
                            {/* Interactive Avatar Container with Photo Upload Support */}
                            <div className="flex flex-col items-center flex-shrink-0 mx-auto md:mx-0">
                                <div 
                                    onClick={handleAvatarClick}
                                    className="relative w-36 h-36 border-2 border-stone-300 dark:border-stone-700 bg-stone-950 overflow-hidden cursor-pointer group shadow-md"
                                    title="Click to change profile picture"
                                >
                                    <img 
                                        src={avatarUrl || defaultProfileImage} 
                                        alt="Practitioner Avatar" 
                                        className="w-full h-full object-cover filter contrast-[1.03] group-hover:opacity-75 transition-opacity" 
                                    />
                                    
                                    {/* Hover Overlay */}
                                    <div className="absolute inset-0 bg-stone-950/70 opacity-0 group-hover:opacity-100 flex flex-col items-center justify-center text-white transition-opacity font-mono text-[10px] p-2 text-center">
                                        <Camera className="w-6 h-6 mb-1 text-teal-300" />
                                        <span>CHANGE PHOTO</span>
                                        <span className="text-[8px] text-stone-400">JPG • PNG • WEBP</span>
                                    </div>
                                </div>

                                {/* Avatar Action Controls */}
                                <div className="flex items-center gap-2 mt-3 font-mono text-[10px]">
                                    <button
                                        type="button"
                                        onClick={handleAvatarClick}
                                        className="text-clinical-teal dark:text-teal-400 hover:underline flex items-center gap-1"
                                    >
                                        <Camera className="w-3 h-3" />
                                        <span>Upload Photo</span>
                                    </button>
                                    {avatarUrl && (
                                        <>
                                            <span className="text-stone-400">•</span>
                                            <button
                                                type="button"
                                                onClick={handleRemoveAvatar}
                                                className="text-stone-400 hover:text-red-500"
                                            >
                                                Reset
                                            </button>
                                        </>
                                    )}
                                </div>
                            </div>

                            {/* Credentials and Identity Details */}
                            <div className="flex-grow w-full">
                                {isEditing ? (
                                    <div className="space-y-4 font-mono text-xs">
                                        <div className="border-b border-stone-200 dark:border-stone-800 pb-2 mb-3">
                                            <span className="text-[10px] text-clinical-teal dark:text-teal-400 uppercase tracking-widest font-semibold">
                                                EDIT PRACTITIONER DOSSIER
                                            </span>
                                        </div>

                                        <div className="grid sm:grid-cols-2 gap-4">
                                            <div>
                                                <label className="block text-[10px] text-stone-500 uppercase mb-1">Full Name & Title</label>
                                                <input 
                                                    type="text"
                                                    name="full_name"
                                                    value={formData.full_name}
                                                    onChange={handleFormChange}
                                                    placeholder="Dr. Samantha Rao, MD"
                                                    className="w-full px-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                                    required
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-[10px] text-stone-500 uppercase mb-1">Email Address</label>
                                                <input 
                                                    type="email"
                                                    name="email"
                                                    value={formData.email}
                                                    onChange={handleFormChange}
                                                    placeholder="samantha@hospital.org"
                                                    className="w-full px-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                                    required
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-[10px] text-stone-500 uppercase mb-1">Department / Division</label>
                                                <input 
                                                    type="text"
                                                    name="department"
                                                    value={formData.department}
                                                    onChange={handleFormChange}
                                                    placeholder="Oral & Maxillofacial Oncology"
                                                    className="w-full px-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-[10px] text-stone-500 uppercase mb-1">Clinical License / Registration</label>
                                                <input 
                                                    type="text"
                                                    name="license_no"
                                                    value={formData.license_no}
                                                    onChange={handleFormChange}
                                                    placeholder="DCI-KA-2024-8842"
                                                    className="w-full px-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                                />
                                            </div>
                                        </div>

                                        <div className="grid sm:grid-cols-2 gap-4">
                                            <div>
                                                <label className="block text-[10px] text-stone-500 uppercase mb-1">Institution / Healthcare Center</label>
                                                <input 
                                                    type="text"
                                                    name="institution"
                                                    value={formData.institution}
                                                    onChange={handleFormChange}
                                                    placeholder="Regional Cancer Care Hospital"
                                                    className="w-full px-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-[10px] text-stone-500 uppercase mb-1">Specialization Focus</label>
                                                <input 
                                                    type="text"
                                                    name="specialization"
                                                    value={formData.specialization}
                                                    onChange={handleFormChange}
                                                    placeholder="Oral Dysplasia & OSCC Screening"
                                                    className="w-full px-3 py-2 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-sm font-sans focus:outline-none focus:border-clinical-teal"
                                                />
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-3 pt-3 border-t border-stone-200 dark:border-stone-800">
                                            <button type="submit" className="px-5 py-2 bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 text-xs font-mono uppercase font-semibold hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-colors">
                                                Save Modifications
                                            </button>
                                            <button type="button" onClick={() => setIsEditing(false)} className="px-4 py-2 border border-stone-300 dark:border-stone-700 text-xs font-mono uppercase text-stone-600 dark:text-stone-400 hover:bg-stone-100 dark:hover:bg-stone-800">
                                                Cancel
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="space-y-4">
                                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-stone-200 dark:border-stone-800 pb-3">
                                            <div>
                                                <span className="font-mono text-[10px] text-clinical-teal dark:text-teal-400 uppercase tracking-widest block mb-0.5">
                                                    CLINICAL PRACTITIONER & INVESTIGATOR
                                                </span>
                                                <h1 className="font-serif text-3xl font-normal text-stone-900 dark:text-stone-100">
                                                    {user?.full_name || user?.username}
                                                </h1>
                                            </div>
                                            <button 
                                                type="button"
                                                onClick={() => setIsEditing(true)}
                                                className="self-start sm:self-center inline-flex items-center gap-1.5 px-3 py-1.5 border border-stone-300 dark:border-stone-700 text-xs font-mono text-stone-700 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
                                            >
                                                <Edit3 className="w-3.5 h-3.5 text-clinical-teal" />
                                                <span>EDIT CREDENTIALS</span>
                                            </button>
                                        </div>

                                        {/* Informative 4-Block Metadata Matrix */}
                                        <div className="grid sm:grid-cols-2 gap-y-3 gap-x-6 font-mono text-xs">
                                            <div className="space-y-1">
                                                <span className="text-[9px] text-stone-400 uppercase block">Institutional Department</span>
                                                <div className="text-stone-800 dark:text-stone-200 font-sans font-medium flex items-center gap-1.5">
                                                    <Building2 className="w-3.5 h-3.5 text-clinical-teal flex-shrink-0" />
                                                    <span>{formData.department}</span>
                                                </div>
                                                <div className="text-[11px] text-stone-500">{formData.institution}</div>
                                            </div>

                                            <div className="space-y-1">
                                                <span className="text-[9px] text-stone-400 uppercase block">Clinical License & Role</span>
                                                <div className="text-stone-800 dark:text-stone-200 font-medium flex items-center gap-1.5">
                                                    <Award className="w-3.5 h-3.5 text-clinical-teal flex-shrink-0" />
                                                    <span>{formData.license_no}</span>
                                                </div>
                                                <div className="text-[11px] text-stone-500">Role: Tier-1 Triage Examiner</div>
                                            </div>

                                            <div className="space-y-1">
                                                <span className="text-[9px] text-stone-400 uppercase block">System Account & Email</span>
                                                <div className="text-stone-800 dark:text-stone-200 flex items-center gap-1.5">
                                                    <Mail className="w-3.5 h-3.5 text-stone-400 flex-shrink-0" />
                                                    <span>{user?.email || 'No email registered'}</span>
                                                </div>
                                                <div className="text-[11px] text-stone-500">Handle: @{user?.username}</div>
                                            </div>

                                            <div className="space-y-1">
                                                <span className="text-[9px] text-stone-400 uppercase block">Clinical Focus & Specialization</span>
                                                <div className="text-stone-800 dark:text-stone-200 font-sans text-xs">
                                                    {formData.specialization}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </form>
                </div>

                {/* ============================================================ */}
                {/* SECTION 2: CLINICAL WORKSTATION TRIAGE STATISTICS            */}
                {/* ============================================================ */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
                    <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-5">
                        <span className="text-[10px] text-stone-400 uppercase tracking-wider block mb-1">Total Specimens Evaluated</span>
                        <div className="font-serif text-3xl text-stone-900 dark:text-stone-100 font-normal">
                            {totalAnalyses}
                        </div>
                        <span className="text-[10px] text-stone-500 block mt-1">Completed AI Triage Cycles</span>
                    </div>

                    <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-5">
                        <span className="text-[10px] text-stone-400 uppercase tracking-wider block mb-1">Presumptive Malignancies</span>
                        <div className="font-serif text-3xl text-clinical-terracotta font-normal">
                            {cancerCases}
                        </div>
                        <span className="text-[10px] text-stone-500 block mt-1">
                            {totalAnalyses > 0 ? `${((cancerCases / totalAnalyses) * 100).toFixed(1)}% Positivity Rate` : '0.0% Rate'}
                        </span>
                    </div>

                    <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-5">
                        <span className="text-[10px] text-stone-400 uppercase tracking-wider block mb-1">Non-Malignant Mucosa</span>
                        <div className="font-serif text-3xl text-clinical-teal dark:text-teal-400 font-normal">
                            {benignCases}
                        </div>
                        <span className="text-[10px] text-stone-500 block mt-1">
                            {totalAnalyses > 0 ? `${((benignCases / totalAnalyses) * 100).toFixed(1)}% Negative Rate` : '0.0% Rate'}
                        </span>
                    </div>

                    <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-5">
                        <span className="text-[10px] text-stone-400 uppercase tracking-wider block mb-1">Mean Ensemble Confidence</span>
                        <div className="font-serif text-3xl text-stone-900 dark:text-stone-100 font-normal">
                            {avgConfidence}%
                        </div>
                        <span className="text-[10px] text-stone-500 block mt-1">
                            {uncertainCases} High-Variance Reviews
                        </span>
                    </div>
                </div>

                {/* ============================================================ */}
                {/* SECTION 3: ACTIVE MODEL & DIAGNOSTIC PROTOCOL SPECS          */}
                {/* ============================================================ */}
                <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6">
                    <div className="flex items-center justify-between border-b border-stone-200 dark:border-stone-800 pb-3 mb-4 font-mono text-xs">
                        <div className="flex items-center gap-2 text-stone-800 dark:text-stone-200">
                            <Microscope className="w-4 h-4 text-clinical-teal" />
                            <span className="uppercase font-semibold">Active AI Triage Engine Telemetry</span>
                        </div>
                        <span className="text-clinical-teal dark:text-teal-400">ENGINE v2.4 OPERATIONAL</span>
                    </div>

                    <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xs text-stone-600 dark:text-stone-400">
                        <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white/50 dark:bg-stone-950/50">
                            <span className="text-[9px] text-stone-400 uppercase block mb-0.5">Ensemble Composition</span>
                            <span className="text-stone-900 dark:text-stone-100 font-semibold block">4 CNN Backbone</span>
                            <span className="text-[10px] text-stone-500">VGG16 • ResNet50 • EfficientNet • MobileNet</span>
                        </div>

                        <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white/50 dark:bg-stone-950/50">
                            <span className="text-[9px] text-stone-400 uppercase block mb-0.5">Epistemic Uncertainty</span>
                            <span className="text-stone-900 dark:text-stone-100 font-semibold block">Monte Carlo Dropout</span>
                            <span className="text-[10px] text-stone-500">15 Variational Passes (σ² ≤ 0.015)</span>
                        </div>

                        <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white/50 dark:bg-stone-950/50">
                            <span className="text-[9px] text-stone-400 uppercase block mb-0.5">Test-Time Augmentation</span>
                            <span className="text-stone-900 dark:text-stone-100 font-semibold block">8-Fold Transform</span>
                            <span className="text-[10px] text-stone-500">Rotation, Flip & Illumination Invariance</span>
                        </div>

                        <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white/50 dark:bg-stone-950/50">
                            <span className="text-[9px] text-stone-400 uppercase block mb-0.5">Multimodal Integration</span>
                            <span className="text-stone-900 dark:text-stone-100 font-semibold block">Bayesian Risk Prior</span>
                            <span className="text-[10px] text-stone-500">Tobacco, Betel Nut & Age Weighting</span>
                        </div>
                    </div>
                </div>

                {/* ============================================================ */}
                {/* SECTION 4: HISTORICAL SPECIMEN TRIAGE LOG & AUDIT CONTROLS   */}
                {/* ============================================================ */}
                <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 p-6 sm:p-8">
                    {/* Header Strip with Controls */}
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-stone-200 dark:border-stone-800 pb-4 mb-6">
                        <div>
                            <div className="flex items-center gap-2">
                                <FileText className="w-4 h-4 text-clinical-teal" />
                                <h2 className="font-serif text-2xl text-stone-900 dark:text-stone-100 font-normal">
                                    Historical Specimen Triage Archive
                                </h2>
                            </div>
                            <span className="font-mono text-xs text-stone-400">
                                {filteredHistory.length} of {history.length} specimen records shown
                            </span>
                        </div>

                        {/* Actions: Ingest New Specimen & Export CSV */}
                        <div className="flex flex-wrap items-center gap-3 font-mono text-xs">
                            <Link to="/upload">
                                <button className="px-3.5 py-1.5 bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 font-semibold flex items-center gap-1.5 hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-colors">
                                    <PlusCircle className="w-3.5 h-3.5" />
                                    <span>New Examination</span>
                                </button>
                            </Link>
                            {history.length > 0 && (
                                <button 
                                    onClick={exportAuditCSV}
                                    className="px-3 py-1.5 border border-stone-300 dark:border-stone-700 text-stone-700 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800 flex items-center gap-1.5 transition-colors"
                                >
                                    <Download className="w-3.5 h-3.5" />
                                    <span>Export CSV Audit</span>
                                </button>
                            )}
                        </div>
                    </div>

                    {/* Filter and Search Bar */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 font-mono text-xs">
                        {/* Filter Tabs */}
                        <div className="flex items-center gap-1 bg-stone-200/60 dark:bg-stone-800/80 p-1 rounded-none border border-stone-300/60 dark:border-stone-700">
                            {[
                                { id: 'all', label: 'All Records' },
                                { id: 'cancer', label: 'Malignant' },
                                { id: 'benign', label: 'Non-Malignant' },
                                { id: 'uncertain', label: 'Uncertain' }
                            ].map(tab => (
                                <button
                                    key={tab.id}
                                    onClick={() => setHistoryFilter(tab.id)}
                                    className={`px-2.5 py-1 transition-colors ${
                                        historyFilter === tab.id 
                                            ? 'bg-white dark:bg-stone-900 font-semibold text-clinical-teal dark:text-teal-300 shadow-xs' 
                                            : 'text-stone-500 hover:text-stone-800 dark:hover:text-stone-200'
                                    }`}
                                >
                                    {tab.label}
                                </button>
                            ))}
                        </div>

                        {/* Search Input */}
                        <div className="relative">
                            <Search className="w-3.5 h-3.5 text-stone-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
                            <input 
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                placeholder="Search by filename or ID..."
                                className="pl-8 pr-3 py-1.5 bg-white dark:bg-stone-950 border border-stone-300 dark:border-stone-700 text-xs font-sans text-stone-800 dark:text-stone-200 focus:outline-none focus:border-clinical-teal w-full sm:w-60"
                            />
                        </div>
                    </div>

                    {/* Specimen Rows */}
                    {filteredHistory.length > 0 ? (
                        <div className="space-y-3">
                            {filteredHistory.map(item => {
                                const isCancer = item.prediction?.toLowerCase() === 'cancer';
                                const isUncertain = item.prediction?.toLowerCase() === 'uncertain';

                                return (
                                    <div 
                                        key={item.id} 
                                        className="border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950 p-4 flex flex-col sm:flex-row justify-between sm:items-center gap-4 transition-all hover:border-stone-400 dark:hover:border-stone-600"
                                    >
                                        <div className="flex items-start sm:items-center gap-3.5">
                                            {isCancer ? (
                                                <div className="p-2 border border-clinical-terracotta bg-red-50 dark:bg-red-950/20 text-clinical-terracotta flex-shrink-0 mt-1 sm:mt-0">
                                                    <ShieldAlert className="w-4 h-4" />
                                                </div>
                                            ) : isUncertain ? (
                                                <div className="p-2 border border-clinical-ochre bg-amber-50 dark:bg-amber-950/20 text-clinical-ochre flex-shrink-0 mt-1 sm:mt-0">
                                                    <AlertTriangle className="w-4 h-4" />
                                                </div>
                                            ) : (
                                                <div className="p-2 border border-clinical-teal bg-teal-50 dark:bg-teal-950/20 text-clinical-teal flex-shrink-0 mt-1 sm:mt-0">
                                                    <ShieldCheck className="w-4 h-4" />
                                                </div>
                                            )}

                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <span className="font-serif text-base font-normal text-stone-900 dark:text-stone-100">
                                                        {isCancer ? 'Presumptive OSCC Malignancy' : isUncertain ? 'Uncertain Epistemic Variance' : 'Non-Malignant Mucosa'}
                                                    </span>
                                                    <span className="font-mono text-[9px] px-1.5 py-0.5 border border-stone-200 dark:border-stone-800 text-stone-500 uppercase">
                                                        REC-#{item.id.toString().padStart(4, '0')}
                                                    </span>
                                                </div>
                                                <div className="font-mono text-[10px] text-stone-400 flex flex-wrap items-center gap-x-3 gap-y-0.5 mt-0.5">
                                                    <span>CONF: <strong className="text-stone-700 dark:text-stone-300">{(item.confidence * 100).toFixed(1)}%</strong></span>
                                                    {item.uncertainty !== null && <span>• σ²: <strong className="text-stone-700 dark:text-stone-300">{item.uncertainty}</strong></span>}
                                                    {item.risk_score !== null && <span>• RISK: <strong className="text-stone-700 dark:text-stone-300">{item.risk_score}</strong></span>}
                                                    {item.image_filename && <span>• FILE: {item.image_filename}</span>}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="font-mono text-xs text-stone-500 text-left sm:text-right flex-shrink-0 border-t sm:border-t-0 pt-2 sm:pt-0 border-stone-100 dark:border-stone-900">
                                            <div>{new Date(item.timestamp).toLocaleDateString()}</div>
                                            <div className="text-[10px] text-stone-400">{new Date(item.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="text-center py-16 font-mono text-xs text-stone-400 border border-dashed border-stone-300 dark:border-stone-800 p-8">
                            <Microscope className="w-10 h-10 mx-auto text-stone-300 dark:text-stone-700 mb-3" />
                            <p className="text-stone-600 dark:text-stone-300 font-sans text-sm mb-1">
                                {history.length === 0 ? "No recorded intake specimens in this dossier." : "No records match the current filter query."}
                            </p>
                            <p className="text-[11px] text-stone-400 mb-4">
                                Run a clinical specimen evaluation to populate this repository archive.
                            </p>
                            <Link to="/upload">
                                <button className="px-4 py-2 bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 text-xs font-mono uppercase font-medium hover:bg-clinical-teal dark:hover:bg-clinical-teal dark:hover:text-white transition-colors inline-flex items-center gap-1.5">
                                    <PlusCircle className="w-3.5 h-3.5" />
                                    <span>Initialize Specimen Examination</span>
                                </button>
                            </Link>
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
};

export default Profile;