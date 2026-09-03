import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { UserPlus, User, Lock, Mail, ArrowRight } from 'lucide-react';
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

            // Auto-login after successful registration
            const loginParams = new URLSearchParams();
            loginParams.append('username', username.trim());
            loginParams.append('password', password);
            const loginResponse = await axios.post('http://localhost:8000/login', loginParams, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            
            onLogin(loginResponse.data.access_token);
            navigate('/profile');

        } catch (err) {
            // Show the real validation error from the server
            const detail = err.response?.data?.detail;
            if (Array.isArray(detail)) {
                setError(detail.map(d => d.msg).join('. '));
            } else {
                setError(detail || 'Registration failed. Please try a different username or email.');
            }
        } finally {
            setLoading(false);
        }
    };
    
    const ImagePlaceholder = ({ className }) => (
        <div className={`hidden lg:block relative ${className}`}>
            <img src={registerImage} alt="Register Illustration" className="absolute inset-0 w-full h-full object-cover rounded-l-2xl" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div className="relative h-full flex flex-col justify-end p-10 text-white">
                <UserPlus className="w-16 h-16 mb-4" />
                <h2 className="text-3xl font-bold">Join Our Community</h2>
                <p className="mt-2 text-gray-200">Create an account to get free, confidential analysis and track your results.</p>
            </div>
        </div>
    );


    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-6xl mx-auto bg-white dark:bg-gray-800/50 rounded-2xl shadow-xl overflow-hidden grid lg:grid-cols-2"
            >
                <div className="p-8 sm:p-12 lg:order-2">
                    <div className="text-center lg:text-left mb-10">
                         <Link to="/" className="inline-block mb-6 text-blue-600 dark:text-blue-400 hover:underline">
                            &larr; Back to Home
                        </Link>
                        <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white">Create Account</h1>
                        <p className="mt-2 text-gray-600 dark:text-gray-300">
                            Already have an account?{' '}
                            <Link to="/login" className="font-semibold text-blue-600 dark:text-blue-400 hover:underline">
                                Sign in
                            </Link>
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="relative">
                            <User className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" />
                            <input
                                type="text"
                                placeholder="Full Name"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                className="w-full pl-12 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-full bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>
                        <div className="relative">
                            <UserPlus className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" />
                            <input
                                type="text"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="w-full pl-12 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-full bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>
                        <div className="relative">
                            <Mail className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" />
                            <input
                                type="email"
                                placeholder="Email Address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full pl-12 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-full bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>
                        <div className="relative">
                            <Lock className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" />
                            <input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full pl-12 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-full bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>

                        {error && (
                            <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-red-500 text-sm text-center">
                                {error}
                            </motion.p>
                        )}
                        
                        <p className="text-xs text-gray-400 dark:text-gray-500 text-center">Password must be at least 6 characters.</p>

                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            type="submit"
                            disabled={loading}
                            className="w-full flex items-center justify-center bg-gradient-to-r from-teal-500 to-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-full text-lg shadow-lg hover:shadow-xl transition-shadow duration-300"
                        >
                            <span>{loading ? 'Creating Account...' : 'Create Account'}</span>
                            {!loading && <ArrowRight className="w-5 h-5 ml-2" />}
                        </motion.button>
                    </form>
                </div>
                
                <ImagePlaceholder className="lg:order-1" />

            </motion.div>
        </div>
    );
};

export default Register; 