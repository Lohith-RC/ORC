import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    User, 
    Mail, 
    Edit3, 
    FileText, 
    Camera, 
    PlusCircle, 
    Download, 
    CheckCircle2,
    Microscope,
    Search,
    AlertTriangle,
    ShieldAlert,
    ShieldCheck,
    Calendar,
    Clock
} from 'lucide-react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from './api';
import defaultProfileImage from './images/7.webp';
import ClinicianVerificationModal from './ClinicianVerificationModal';
import SpecialistReferralModal from './SpecialistReferralModal';

const Profile = ({ token }) => {
    const [user, setUser] = useState(null);
    const [history, setHistory] = useState([]);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({ 
        full_name: '', 
        email: ''
    });
    const [avatarUrl, setAvatarUrl] = useState(null);
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const [historyFilter, setHistoryFilter] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [verifyingAnalysis, setVerifyingAnalysis] = useState(null);
    const [referralAnalysisId, setReferralAnalysisId] = useState(null);

    const fileInputRef = useRef(null);

    useEffect(() => {
        const fetchData = async () => {
            if (!token) {
                setLoading(false);
                return;
            }
            try {
                const userPromise = axios.get(`${API_BASE_URL}/me`, { headers: { Authorization: `Bearer ${token}` } });
                const historyPromise = axios.get(`${API_BASE_URL}/me/analyses`, { headers: { Authorization: `Bearer ${token}` } });
                
                const [userResponse, historyResponse] = await Promise.all([userPromise, historyPromise]);

                const userData = userResponse.data;
                setUser(userData);

                setFormData({
                    full_name: userData.full_name || '',
                    email: userData.email || ''
                });

                // Load custom avatar from localStorage if available
                const savedAvatar = localStorage.getItem(`profile_avatar_${userData.username || userData.id}`);
                if (savedAvatar) {
                    setAvatarUrl(savedAvatar);
                }

                setHistory(historyResponse.data || []);
            } catch (err) {
                setError('Could not load profile. Please check your connection.');
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
                setError('Image size should be under 5MB.');
                return;
            }
            const reader = new FileReader();
            reader.onload = () => {
                const base64Data = reader.result;
                setAvatarUrl(base64Data);
                if (user) {
                    localStorage.setItem(`profile_avatar_${user.username || user.id}`, base64Data);
                }
                setMessage('Profile picture updated.');
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
        setMessage('Reset to default picture.');
    };

    const handleSave = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');
        try {
            const response = await axios.post(`${API_BASE_URL}/me/update`, {
                full_name: formData.full_name,
                email: formData.email
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUser(response.data);
            setMessage('Profile updated successfully.');
            setIsEditing(false);
        } catch (err) {
            setError('Failed to update profile.');
        }
    };

    // Calculate simple stats
    const totalAnalyses = history.length;
    const cancerCases = history.filter(h => h.prediction?.toLowerCase() === 'cancer').length;
    const benignCases = history.filter(h => h.prediction?.toLowerCase() === 'non-cancer' || h.prediction?.toLowerCase() === 'non_cancer').length;
    const uncertainCases = history.filter(h => h.prediction?.toLowerCase() === 'uncertain').length;
    const avgConfidence = totalAnalyses > 0 
        ? ((history.reduce((acc, curr) => acc + (curr.confidence || 0), 0) / totalAnalyses) * 100).toFixed(0)
        : '0';

    // Simple history filter
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
        const headers = "Scan_ID,Result,Confidence,Date\n";
        const rows = history.map(h => 
            `${h.id},${h.prediction},${(h.confidence * 100).toFixed(1)}%,"${new Date(h.timestamp).toLocaleDateString()}"`
        ).join("\n");
        
        const blob = new Blob([headers + rows], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `scan_history_${user?.username || 'user'}.csv`;
        a.click();
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-[#080B10] flex flex-col items-center justify-center text-sm text-slate-500 space-y-3 font-sans">
                <div className="w-8 h-8 border-2 border-teal-600 border-t-transparent rounded-full animate-spin"></div>
                <span>Loading your profile...</span>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-[#080B10] py-12 px-4 sm:px-6 lg:px-8 font-sans text-slate-800 dark:text-slate-200">
            <div className="max-w-4xl mx-auto space-y-8">
                
                {/* Hidden File Input for Avatar Upload */}
                <input 
                    type="file" 
                    ref={fileInputRef} 
                    accept="image/jpeg,image/png,image/webp" 
                    className="hidden" 
                    onChange={handleAvatarChange}
                />

                {/* Page Title */}
                <div>
                    <h1 className="text-3xl font-serif text-slate-900 dark:text-white font-normal">
                        My Profile
                    </h1>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                        View your account details and previous oral scans.
                    </p>
                </div>

                {/* Notification messages */}
                <AnimatePresence>
                    {error && (
                        <motion.div initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="p-3.5 rounded-lg border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300 text-sm flex items-center gap-2">
                            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                            <span>{error}</span>
                        </motion.div>
                    )}
                    {message && (
                        <motion.div initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="p-3.5 rounded-lg border border-teal-200 dark:border-teal-900/50 bg-teal-50 dark:bg-teal-950/20 text-teal-800 dark:text-teal-300 text-sm flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 flex-shrink-0 text-teal-600" />
                            <span>{message}</span>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* User Info Card */}
                <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-6 sm:p-8">
                    <form onSubmit={handleSave}>
                        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6">
                            
                            {/* Profile Picture */}
                            <div className="flex flex-col items-center flex-shrink-0">
                                <div 
                                    onClick={handleAvatarClick}
                                    className="relative w-24 h-24 rounded-full overflow-hidden border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800 cursor-pointer group"
                                    title="Click to change photo"
                                >
                                    <img 
                                        src={avatarUrl || defaultProfileImage} 
                                        alt="Profile" 
                                        className="w-full h-full object-cover group-hover:opacity-80 transition-opacity" 
                                    />
                                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center text-white transition-opacity">
                                        <Camera className="w-5 h-5" />
                                    </div>
                                </div>

                                <button
                                    type="button"
                                    onClick={handleAvatarClick}
                                    className="mt-2 text-xs text-teal-600 dark:text-teal-400 hover:underline"
                                >
                                    Change photo
                                </button>
                            </div>

                            {/* Details or Edit Form */}
                            <div className="flex-grow w-full text-center sm:text-left">
                                {isEditing ? (
                                    <div className="space-y-4 max-w-md">
                                        <div>
                                            <label className="block text-xs font-medium text-slate-500 uppercase mb-1">Full Name</label>
                                            <input 
                                                type="text"
                                                name="full_name"
                                                value={formData.full_name}
                                                onChange={handleFormChange}
                                                placeholder="Your Name"
                                                className="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 text-sm focus:outline-none focus:border-teal-600"
                                                required
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-xs font-medium text-slate-500 uppercase mb-1">Email</label>
                                            <input 
                                                type="email"
                                                name="email"
                                                value={formData.email}
                                                onChange={handleFormChange}
                                                placeholder="email@example.com"
                                                className="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 text-sm focus:outline-none focus:border-teal-600"
                                                required
                                            />
                                        </div>

                                        <div className="flex items-center gap-2 pt-2">
                                            <button type="submit" className="px-4 py-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 rounded-lg text-xs font-medium hover:bg-teal-600 dark:hover:bg-teal-600 dark:hover:text-white transition-colors">
                                                Save
                                            </button>
                                            <button type="button" onClick={() => setIsEditing(false)} className="px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg text-xs text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800">
                                                Cancel
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="space-y-3">
                                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                                            <div>
                                                <h2 className="text-2xl font-serif font-normal text-slate-900 dark:text-white">
                                                    {user?.full_name || user?.username}
                                                </h2>
                                                <p className="text-sm text-slate-500 dark:text-slate-400">
                                                    @{user?.username}
                                                </p>
                                            </div>
                                            <button 
                                                type="button"
                                                onClick={() => setIsEditing(true)}
                                                className="inline-flex items-center gap-1.5 self-center sm:self-start px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                                            >
                                                <Edit3 className="w-3.5 h-3.5 text-teal-600" />
                                                <span>Edit Profile</span>
                                            </button>
                                        </div>

                                        <div className="pt-2 text-sm text-slate-600 dark:text-slate-300 flex items-center justify-center sm:justify-start gap-2">
                                            <Mail className="w-4 h-4 text-slate-400" />
                                            <span>{user?.email || 'No email registered'}</span>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </form>
                </div>

                {/* Simple 4-Box Summary Stats */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-5">
                        <span className="text-xs text-slate-500 uppercase tracking-wider block mb-1">Total Scans</span>
                        <div className="font-serif text-3xl text-slate-900 dark:text-white font-normal">
                            {totalAnalyses}
                        </div>
                    </div>

                    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-5">
                        <span className="text-xs text-slate-500 uppercase tracking-wider block mb-1">Potential Cancer</span>
                        <div className="font-serif text-3xl text-rose-600 font-normal">
                            {cancerCases}
                        </div>
                    </div>

                    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-5">
                        <span className="text-xs text-slate-500 uppercase tracking-wider block mb-1">Healthy / Benign</span>
                        <div className="font-serif text-3xl text-teal-600 font-normal">
                            {benignCases}
                        </div>
                    </div>

                    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-5">
                        <span className="text-xs text-slate-500 uppercase tracking-wider block mb-1">Average Confidence</span>
                        <div className="font-serif text-3xl text-slate-900 dark:text-white font-normal">
                            {avgConfidence}%
                        </div>
                    </div>
                </div>

                {/* Previous Scans Section */}
                <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-6 sm:p-8">
                    {/* Header Strip */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4 mb-6">
                        <div>
                            <h2 className="font-serif text-2xl text-slate-900 dark:text-white font-normal">
                                Scan History
                            </h2>
                            <p className="text-xs text-slate-500 mt-0.5">
                                {filteredHistory.length} of {history.length} scans
                            </p>
                        </div>

                        {/* Actions */}
                        <div className="flex items-center gap-3">
                            <Link to="/upload">
                                <button className="px-3.5 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-700 text-white text-xs font-medium flex items-center gap-1.5 transition-colors shadow-sm">
                                    <PlusCircle className="w-3.5 h-3.5" />
                                    <span>New Scan</span>
                                </button>
                            </Link>
                            {history.length > 0 && (
                                <button 
                                    onClick={exportAuditCSV}
                                    className="px-3.5 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs flex items-center gap-1.5 transition-colors"
                                >
                                    <Download className="w-3.5 h-3.5" />
                                    <span>Export CSV</span>
                                </button>
                            )}
                        </div>
                    </div>

                    {/* Filter and Search Bar */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
                        {/* Filter Tabs */}
                        <div className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 p-1 rounded-lg">
                            {[
                                { id: 'all', label: 'All' },
                                { id: 'cancer', label: 'Cancer Likely' },
                                { id: 'benign', label: 'Healthy' },
                                { id: 'uncertain', label: 'Needs Review' }
                            ].map(tab => (
                                <button
                                    key={tab.id}
                                    onClick={() => setHistoryFilter(tab.id)}
                                    className={`px-3 py-1 rounded-md text-xs transition-colors ${
                                        historyFilter === tab.id 
                                            ? 'bg-white dark:bg-slate-900 font-medium text-slate-900 dark:text-white shadow-xs' 
                                            : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'
                                    }`}
                                >
                                    {tab.label}
                                </button>
                            ))}
                        </div>

                        {/* Search Input */}
                        <div className="relative">
                            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                            <input 
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                placeholder="Search scans..."
                                className="pl-8 pr-3 py-1.5 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 text-xs text-slate-800 dark:text-slate-200 focus:outline-none focus:border-teal-600 w-full sm:w-56"
                            />
                        </div>
                    </div>

                    {/* Scans List */}
                    {filteredHistory.length > 0 ? (
                        <div className="space-y-3">
                            {filteredHistory.map(item => {
                                const isCancer = item.prediction?.toLowerCase() === 'cancer';
                                const isUncertain = item.prediction?.toLowerCase() === 'uncertain';

                                return (
                                    <div 
                                        key={item.id} 
                                        className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/40 p-4 flex flex-col sm:flex-row justify-between sm:items-center gap-4 hover:border-slate-300 dark:hover:border-slate-700 transition-colors"
                                    >
                                        <div className="flex items-center gap-3.5">
                                            {isCancer ? (
                                                <div className="p-2.5 rounded-xl bg-red-50 dark:bg-red-950/40 text-red-600 flex-shrink-0">
                                                    <ShieldAlert className="w-5 h-5" />
                                                </div>
                                            ) : isUncertain ? (
                                                <div className="p-2.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-600 flex-shrink-0">
                                                    <AlertTriangle className="w-5 h-5" />
                                                </div>
                                            ) : (
                                                <div className="p-2.5 rounded-xl bg-teal-50 dark:bg-teal-950/40 text-teal-600 flex-shrink-0">
                                                    <ShieldCheck className="w-5 h-5" />
                                                </div>
                                            )}

                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                                                        isCancer 
                                                            ? 'bg-red-100 text-red-700 dark:bg-red-950/60 dark:text-red-300'
                                                            : isUncertain
                                                            ? 'bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300'
                                                            : 'bg-teal-100 text-teal-700 dark:bg-teal-950/60 dark:text-teal-300'
                                                    }`}>
                                                        {isCancer ? 'Cancer Detected' : isUncertain ? 'Needs Doctor Review' : 'Healthy / Normal'}
                                                    </span>

                                                    <span className="text-xs text-slate-400">
                                                        Scan #{item.id}
                                                    </span>
                                                </div>

                                                <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 flex flex-wrap items-center gap-3">
                                                    <span>Confidence: <strong className="text-slate-700 dark:text-slate-300">{(item.confidence * 100).toFixed(1)}%</strong></span>
                                                    <span>•</span>
                                                    <span>{new Date(item.timestamp).toLocaleDateString()} at {new Date(item.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                                                    {item.image_filename && (
                                                        <>
                                                            <span>•</span>
                                                            <span className="truncate max-w-[140px]">{item.image_filename}</span>
                                                        </>
                                                    )}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-2 self-end sm:self-center">
                                            <button
                                                type="button"
                                                onClick={() => setReferralAnalysisId(item.id)}
                                                className="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-teal-600 text-xs flex items-center gap-1.5 text-slate-700 dark:text-slate-300 transition-colors"
                                            >
                                                <FileText className="w-3.5 h-3.5 text-slate-400" />
                                                <span>Report</span>
                                            </button>

                                            <button
                                                type="button"
                                                onClick={() => setVerifyingAnalysis(item)}
                                                className={`px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 transition-colors ${
                                                    item.biopsy_proven || item.ground_truth_dx
                                                        ? 'bg-teal-50 dark:bg-teal-950/50 text-teal-700 dark:text-teal-300 border border-teal-200 dark:border-teal-800'
                                                        : 'border border-slate-200 dark:border-slate-700 hover:border-teal-600 text-slate-700 dark:text-slate-300'
                                                }`}
                                            >
                                                <Microscope className="w-3.5 h-3.5 text-teal-600" />
                                                <span>{item.biopsy_proven ? 'Verified' : item.ground_truth_dx ? 'Verified' : 'Verify'}</span>
                                            </button>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="text-center py-12 text-sm text-slate-500 border border-dashed border-slate-200 dark:border-slate-800 rounded-xl p-8">
                            <p className="mb-3">
                                {history.length === 0 ? "You haven't run any scans yet." : "No scans match your search."}
                            </p>
                            <Link to="/upload">
                                <button className="px-4 py-2 rounded-lg bg-teal-600 hover:bg-teal-700 text-white text-xs font-medium inline-flex items-center gap-1.5 transition-colors">
                                    <PlusCircle className="w-3.5 h-3.5" />
                                    <span>Start a New Scan</span>
                                </button>
                            </Link>
                        </div>
                    )}
                </div>
            </div>

            {/* Clinician Ground Truth Verification Modal */}
            <ClinicianVerificationModal
                isOpen={!!verifyingAnalysis}
                onClose={() => setVerifyingAnalysis(null)}
                analysis={verifyingAnalysis}
                onVerificationSuccess={(updatedAnalysis) => {
                    setHistory(prev => prev.map(h => h.id === updatedAnalysis.id ? { ...h, ...updatedAnalysis } : h));
                }}
            />

            {/* Specialist Referral Letter & Report Modal */}
            <SpecialistReferralModal
                isOpen={!!referralAnalysisId}
                onClose={() => setReferralAnalysisId(null)}
                analysisId={referralAnalysisId}
            />
        </div>
    );
};

export default Profile;