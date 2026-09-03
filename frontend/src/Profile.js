import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { User, Mail, Calendar, Edit3, Save, XCircle, BarChart, AlertTriangle, Briefcase, Clock } from 'lucide-react';
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
                setError('Could not load profile data. Please try again later.');
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
            setMessage('Profile updated successfully!');
            setIsEditing(false);
        } catch (err) {
            setError('Failed to update profile. Please try again.');
        }
    };

    const AnalysisHistory = () => (
        <div className="bg-gray-50 dark:bg-gray-800/50 p-6 rounded-2xl shadow-inner">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4 flex items-center">
                <Briefcase className="mr-3 text-blue-500" />
                Analysis History
            </h3>
            {history.length > 0 ? (
                <div className="space-y-4">
                    {history.map(item => (
                        <div key={item.id} className="p-4 bg-white dark:bg-gray-700 rounded-lg shadow-sm flex justify-between items-center">
                            <div>
                                <p className="font-semibold">{item.prediction === 'cancer' ? 'Cancer Detected' : 'No Cancer Detected'}</p>
                                <p className="text-sm text-gray-500 dark:text-gray-400">Confidence: {(item.confidence * 100).toFixed(1)}%</p>
                            </div>
                            <div className="text-right text-sm text-gray-500 dark:text-gray-400">
                                <p>{new Date(item.timestamp).toLocaleDateString()}</p>
                                <p className="flex items-center justify-end"><Clock className="w-3 h-3 mr-1" />{new Date(item.timestamp).toLocaleTimeString()}</p>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center py-10 text-gray-500 dark:text-gray-400">
                     <BarChart className="w-12 h-12 mx-auto mb-3" />
                    <p>Your analysis history is empty.</p>
                    <p className="text-sm mt-1">Upload an image to see your results here.</p>
                </div>
            )}
        </div>
    );
    
    const ProfileImage = ({ className }) => (
        <div className={`relative flex-shrink-0 ${className}`}>
            <img src={profileImage} alt="Profile" className="w-full h-full rounded-full object-cover" />
            <button 
                onClick={() => setIsEditing(true)}
                className="absolute bottom-0 right-0 bg-blue-600 text-white p-2 rounded-full shadow-md hover:bg-blue-700 transition"
            >
                <Edit3 className="w-4 h-4" />
            </button>
        </div>
    );
    
    if (loading) {
        return <div className="text-center py-20">Loading profile...</div>;
    }

    return (
        <div className="bg-gray-50 dark:bg-gray-900 min-h-screen py-20 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                <AnimatePresence>
                    {error && (
                        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="bg-red-100 border border-red-400 text-red-700 dark:bg-red-900/20 dark:border-red-600 dark:text-red-300 px-4 py-3 rounded-lg relative mb-6" role="alert">
                            <AlertTriangle className="w-5 h-5 inline-block mr-2" />
                            {error}
                        </motion.div>
                    )}
                    {message && (
                         <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="bg-green-100 border border-green-400 text-green-700 dark:bg-green-900/20 dark:border-green-600 dark:text-green-300 px-4 py-3 rounded-lg relative mb-6" role="alert">
                            {message}
                        </motion.div>
                    )}
                </AnimatePresence>
                <motion.div
                    initial={{ opacity: 0, y: -50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.7 }}
                    className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden"
                >
                    <div className="p-8 md:p-12">
                        <form onSubmit={handleSave}>
                            <div className="flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-10">
                                <ProfileImage className="w-40 h-40" />
                                <div className="text-center md:text-left flex-grow">
                                    {isEditing ? (
                                        <input 
                                            type="text"
                                            name="full_name"
                                            value={formData.full_name}
                                            onChange={handleFormChange}
                                            className="text-4xl font-extrabold text-gray-900 dark:text-white bg-transparent border-b-2 border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:outline-none w-full"
                                        />
                                    ) : (
                                        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">{user.full_name}</h1>
                                    )}
                                    <p className="mt-2 text-lg text-gray-600 dark:text-gray-300">Welcome to your personal dashboard.</p>
                                    <div className="mt-6 space-y-4">
                                        <div className="flex items-center text-gray-700 dark:text-gray-200">
                                            <Mail className="w-5 h-5 mr-3 text-blue-500"/>
                                            {isEditing ? (
                                                <input 
                                                    type="email"
                                                    name="email"
                                                    value={formData.email}
                                                    onChange={handleFormChange}
                                                    className="bg-transparent border-b border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:outline-none w-full"
                                                />
                                            ) : (
                                                <span>{user.email}</span>
                                            )}
                                        </div>
                                        <div className="flex items-center text-gray-700 dark:text-gray-200">
                                            <Calendar className="w-5 h-5 mr-3 text-blue-500"/>
                                            <span>Member since: January 2024</span>
                                        </div>
                                    </div>
                                </div>
                                <div className="flex-shrink-0 flex items-center space-x-2">
                                    {isEditing ? (
                                        <>
                                            <button type="button" onClick={() => setIsEditing(false)} className="flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-full shadow-sm text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">
                                                <XCircle className="w-4 h-4 mr-2"/> Cancel
                                            </button>
                                            <button type="submit" className="flex items-center px-4 py-2 border border-transparent rounded-full shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700">
                                                <Save className="w-4 h-4 mr-2"/> Save
                                            </button>
                                        </>
                                    ) : (
                                        <button type="button" onClick={() => setIsEditing(true)} className="flex items-center px-4 py-2 border border-transparent rounded-full shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">
                                            <Edit3 className="w-4 h-4 mr-2"/> Edit Profile
                                        </button>
                                    )}
                                </div>
                            </div>
                        </form>
                    </div>
                    
                    <div className="p-8 md:p-12 border-t border-gray-200 dark:border-gray-700">
                       <AnalysisHistory />
                    </div>

                </motion.div>
            </div>
        </div>
    );
};

export default Profile;