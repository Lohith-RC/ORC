import React, { useState, useEffect } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { 
    Stethoscope, 
    UploadCloud, 
    FileText, 
    Info, 
    Phone, 
    Sun, 
    Moon, 
    Compass, 
    Menu, 
    X, 
    LogOut, 
    LogIn, 
    UserPlus, 
    Activity, 
    ShieldCheck 
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from './ThemeContext';
import axios from 'axios';

function Navbar({ loggedIn, onLogout, onOpenManifesto }) {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [apiHealthy, setApiHealthy] = useState(null);
    const { theme, toggleTheme } = useTheme();

    useEffect(() => {
        let isMounted = true;
        const checkHealth = async () => {
            try {
                const res = await axios.get('http://127.0.0.1:8000/health', { timeout: 3000 });
                if (isMounted) setApiHealthy(res.data?.status === 'ok');
            } catch {
                if (isMounted) setApiHealthy(false);
            }
        };
        checkHealth();
        const interval = setInterval(checkHealth, 30000);
        return () => {
            isMounted = false;
            clearInterval(interval);
        };
    }, []);

    const navLinkClasses = "flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-mono tracking-wider transition-all";
    const activeClassName = "bg-teal-500/10 text-teal-600 dark:text-teal-400 font-semibold border border-teal-500/20 shadow-xs";
    const inactiveClassName = "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/60";
    
    const getNavLinkClass = ({ isActive }) => `${navLinkClasses} ${isActive ? activeClassName : inactiveClassName}`;

    const ThemeToggleButton = () => (
        <button 
            onClick={toggleTheme} 
            title={theme === 'light' ? 'Switch to Dark Surgical Mode' : 'Switch to Clinical Light Mode'}
            className="flex items-center gap-1.5 p-2 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-mono transition-colors"
        >
            {theme === 'light' ? (
                <Moon className="w-4 h-4 text-slate-700" />
            ) : (
                <Sun className="w-4 h-4 text-amber-400" />
            )}
        </button>
    );

    const navLinks = (
        <>
            <NavLink to="/" className={getNavLinkClass}>
                <span>Home</span>
            </NavLink>
            <NavLink to="/about" className={getNavLinkClass}>
                <span>About</span>
            </NavLink>
            <NavLink to="/contact" className={getNavLinkClass}>
                <span>Contact</span>
            </NavLink>
            {loggedIn ? (
                <>
                    <NavLink to="/upload" className={getNavLinkClass}>
                        <UploadCloud className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />
                        <span>New Scan</span>
                    </NavLink>
                    <NavLink to="/profile" className={getNavLinkClass}>
                        <FileText className="w-3.5 h-3.5" />
                        <span>Profile</span>
                    </NavLink>
                </>
            ) : (
                <>
                    <NavLink to="/login" className={getNavLinkClass}>
                        <LogIn className="w-3.5 h-3.5" />
                        <span>Log In</span>
                    </NavLink>
                    <NavLink to="/register" className={getNavLinkClass}>
                        <UserPlus className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />
                        <span>Register</span>
                    </NavLink>
                </>
            )}
        </>
    );
    
    return (
        <header className="sticky top-0 z-50 bg-white/80 dark:bg-[#090D14]/85 backdrop-blur-xl border-b border-slate-200/80 dark:border-slate-800/80 transition-colors">
            {/* Top Clinical Bar */}
            <div className="bg-slate-100/70 dark:bg-slate-950/70 border-b border-slate-200/50 dark:border-slate-800/50 px-4 py-1 text-[11px] font-mono text-slate-500 dark:text-slate-400 flex items-center justify-between">
                <div className="max-w-7xl mx-auto w-full flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <span className="flex items-center gap-1.5">
                            <span className={`w-2 h-2 rounded-full ${apiHealthy === true ? 'bg-emerald-500' : apiHealthy === false ? 'bg-rose-500' : 'bg-amber-400'}`}></span>
                            <span className="text-[11px] font-sans font-medium">
                                {apiHealthy === true ? 'AI Model Online & Ready' : apiHealthy === false ? 'Connecting to Model...' : 'Starting Model...'}
                            </span>
                        </span>
                        <span className="hidden sm:inline text-slate-300 dark:text-slate-700">|</span>
                        <span className="hidden sm:inline text-[11px] font-sans">Fast & Confidential Oral Health Screening</span>
                    </div>

                    <div className="flex items-center gap-4">
                        <span className="text-[11px] font-sans text-rose-600 dark:text-rose-400 font-medium flex items-center gap-1">
                            <Phone className="w-3 h-3" />
                            <span>Helpline: 1800-OSCC-STAT</span>
                        </span>
                    </div>
                </div>
            </div>

            {/* Main Navigation Bar */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Brand */}
                    <div className="flex-shrink-0 flex items-center gap-3">
                        <Link to="/" className="flex items-center gap-3 group">
                            <div className="w-9 h-9 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-sm">
                                <Stethoscope className="w-5 h-5 text-white" />
                            </div>
                            <div className="flex flex-col">
                                <span className="font-serif text-lg tracking-tight font-medium text-slate-900 dark:text-white leading-none">
                                    Oral Cancer Detection
                                </span>
                                <span className="text-[11px] text-slate-400 dark:text-slate-500 mt-0.5">
                                    AI Screening Assistant
                                </span>
                            </div>
                        </Link>
                    </div>

                    {/* Desktop Links */}
                    <div className="hidden md:flex items-center space-x-1">
                        {navLinks}
                    </div>

                    {/* Right Controls */}
                    <div className="hidden md:flex items-center space-x-2.5">
                        <ThemeToggleButton />

                        {loggedIn ? (
                            <button 
                                onClick={onLogout} 
                                className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-200 dark:border-slate-800 rounded-lg text-xs text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                            >
                                <LogOut className="w-3.5 h-3.5" />
                                <span>Sign Out</span>
                            </button>
                        ) : (
                            <Link
                                to="/upload"
                                className="px-3.5 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-700 text-white text-xs font-medium shadow-sm transition-all flex items-center gap-1.5"
                            >
                                <UploadCloud className="w-3.5 h-3.5" />
                                <span>Start Scan</span>
                            </Link>
                        )}
                    </div>

                    {/* Mobile Menu Trigger */}
                    <div className="flex items-center gap-2 md:hidden">
                        <ThemeToggleButton />
                        <button 
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)} 
                            className="p-2 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-600 dark:text-slate-300"
                        >
                            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Dropdown */}
            <AnimatePresence>
                {mobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        className="md:hidden border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-4 py-4 space-y-2"
                    >
                        {navLinks}
                        {loggedIn && (
                            <button 
                                onClick={onLogout} 
                                className="w-full mt-3 flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-xs font-mono text-rose-600 dark:text-rose-400 border border-rose-200 dark:border-rose-900"
                            >
                                <LogOut className="w-4 h-4" /> SIGN OUT
                            </button>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </header>
    );
}

export default Navbar;