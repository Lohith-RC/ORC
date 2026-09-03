import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LogIn, User, Lock, ArrowRight } from 'lucide-react';
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
            const msg = err.response?.data?.detail || err.response?.data?.error || 'Invalid credentials. Please try again.';
            setError(msg);
        }
    };

    const ImagePlaceholder = ({ className }) => (
        <div className={`hidden lg:block relative ${className}`}>
            <img src={loginImage} alt="Login Illustration" className="absolute inset-0 w-full h-full object-cover rounded-r-2xl" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div className="relative h-full flex flex-col justify-end p-10 text-white">
                <LogIn className="w-16 h-16 mb-4 text-white" />
                <h2 className="mt-6 text-3xl font-bold">Welcome Back</h2>
                <p className="mt-2 text-gray-200">Securely access your account and analysis history.</p>
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
                <div className="p-8 sm:p-12">
                    <div className="text-center lg:text-left mb-10">
                        <Link to="/" className="inline-block mb-6 text-blue-600 dark:text-blue-400 hover:underline">
                            &larr; Back to Home
                        </Link>
                        <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white">Member Login</h1>
                        <p className="mt-2 text-gray-600 dark:text-gray-300">
                            Don't have an account?{' '}
                            <Link to="/register" className="font-semibold text-blue-600 dark:text-blue-400 hover:underline">
                                Sign up here
                            </Link>
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="relative">
                            <User className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" />
                            <input
                                type="text"
                                placeholder="Username or Email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full pl-12 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-full bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-teal-500"
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
                                className="w-full pl-12 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-full bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-teal-500"
                                required
                            />
                        </div>

                        {error && (
                            <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-red-500 text-sm text-center">
                                {error}
                            </motion.p>
                        )}

                        <div className="flex items-center justify-between">
                            <button type="button" className="text-sm text-blue-600 dark:text-blue-400 hover:underline focus:outline-none">
                                Forgot Password?
                            </button>
                        </div>

                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            type="submit"
                            className="w-full flex items-center justify-center bg-gradient-to-r from-teal-500 to-emerald-500 text-white font-bold py-3 px-4 rounded-full text-lg shadow-lg hover:shadow-xl transition-shadow duration-300"
                        >
                            <span>Sign In</span>
                            <ArrowRight className="w-5 h-5 ml-2" />
                        </motion.button>
                    </form>
                </div>

                <ImagePlaceholder />
            </motion.div>
        </div>
    );
};

export default Login; 