import React, { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { Stethoscope, LogIn, UserPlus, Upload, User, LogOut, Menu, X, Info, Phone, Sun, Moon } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from './ThemeContext';

function Navbar({ loggedIn, onLogout }) {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const { theme, toggleTheme } = useTheme();

    const navLinkClasses = "flex items-center gap-2 px-3.5 py-1.5 rounded-md text-xs font-mono tracking-wider transition-colors";
    const activeClassName = "bg-stone-200/70 dark:bg-stone-800 text-clinical-teal dark:text-teal-400 font-medium border border-stone-300/60 dark:border-stone-700/60 shadow-xs";
    const inactiveClassName = "text-stone-600 dark:text-stone-400 hover:text-stone-950 dark:hover:text-stone-100 hover:bg-stone-200/40 dark:hover:bg-stone-800/40";
    
    const getNavLinkClass = ({ isActive }) => `${navLinkClasses} ${isActive ? activeClassName : inactiveClassName}`;

    const ThemeToggleButton = () => (
        <button 
            onClick={toggleTheme} 
            title={theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded border border-stone-200 dark:border-stone-800 text-stone-600 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800 text-xs font-mono transition-colors"
        >
            {theme === 'light' ? (
                <>
                    <Moon className="w-3.5 h-3.5 text-stone-700" />
                    <span className="text-[10px] uppercase font-mono tracking-wider">Dark</span>
                </>
            ) : (
                <>
                    <Sun className="w-3.5 h-3.5 text-amber-400" />
                    <span className="text-[10px] uppercase font-mono tracking-wider">Light</span>
                </>
            )}
        </button>
    );

    const navLinks = (
        <>
            <NavLink to="/about" className={getNavLinkClass}>
                <span className="text-[10px] text-stone-400 dark:text-stone-500">01</span>
                <span>ABOUT</span>
            </NavLink>
            <NavLink to="/contact" className={getNavLinkClass}>
                <span className="text-[10px] text-stone-400 dark:text-stone-500">02</span>
                <span>CONTACT</span>
            </NavLink>
            {loggedIn ? (
                <>
                    <NavLink to="/upload" className={getNavLinkClass}>
                        <span className="text-[10px] text-clinical-teal dark:text-teal-400">03</span>
                        <span>EXAMINATION</span>
                    </NavLink>
                    <NavLink to="/profile" className={getNavLinkClass}>
                        <span className="text-[10px] text-stone-400 dark:text-stone-500">04</span>
                        <span>DOSSIER</span>
                    </NavLink>
                </>
            ) : (
                <>
                    <NavLink to="/login" className={getNavLinkClass}>
                        <span className="text-[10px] text-stone-400 dark:text-stone-500">03</span>
                        <span>LOGIN</span>
                    </NavLink>
                    <NavLink to="/register" className={getNavLinkClass}>
                        <span className="text-[10px] text-stone-400 dark:text-stone-500">04</span>
                        <span>REGISTER</span>
                    </NavLink>
                </>
            )}
        </>
    );
    
    return (
        <header className="sticky top-0 z-50 bg-parchment-100/95 dark:bg-ink-950/95 backdrop-blur-md border-b border-stone-200/80 dark:border-stone-800/80 transition-colors">
            {/* Main Navigation Bar */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-20">
                    {/* Brand */}
                    <div className="flex-shrink-0 flex items-center gap-3">
                        <Link to="/" className="flex items-center gap-3 group">
                            <div className="w-9 h-9 rounded border border-stone-300 dark:border-stone-700 flex items-center justify-center bg-stone-50 dark:bg-stone-900 group-hover:border-clinical-teal transition-colors">
                                <Stethoscope className="w-4 h-4 text-clinical-teal dark:text-teal-400" />
                            </div>
                            <div className="flex flex-col">
                                <span className="font-serif text-2xl tracking-tight font-normal text-stone-900 dark:text-stone-100 leading-none">
                                    Visionary Diagnostics
                                </span>
                                <span className="font-mono text-[9px] tracking-widest text-stone-400 dark:text-stone-500 uppercase mt-1">
                                    Oral Oncology AI Triage
                                </span>
                            </div>
                        </Link>
                    </div>

                    {/* Desktop Links */}
                    <div className="hidden md:flex items-center space-x-2">
                        {navLinks}
                    </div>

                    {/* Right Controls */}
                    <div className="hidden md:flex items-center space-x-3">
                        <ThemeToggleButton />
                        {loggedIn && (
                            <button 
                                onClick={onLogout} 
                                className="flex items-center gap-1.5 px-3 py-1.5 border border-stone-300 dark:border-stone-700 rounded text-xs font-mono text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 transition-colors"
                            >
                                <LogOut className="w-3.5 h-3.5" />
                                <span>LOGOUT</span>
                            </button>
                        )}
                    </div>

                    {/* Mobile Menu Trigger */}
                    <div className="flex items-center gap-2 md:hidden">
                        <ThemeToggleButton />
                        <button 
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)} 
                            className="p-2 rounded border border-stone-300 dark:border-stone-700 text-stone-600 dark:text-stone-300"
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
                        className="md:hidden border-t border-stone-200 dark:border-stone-800 bg-parchment-100 dark:bg-ink-950 px-4 py-4 space-y-2"
                    >
                        {navLinks}
                        {loggedIn && (
                            <button 
                                onClick={onLogout} 
                                className="w-full mt-3 flex items-center justify-center gap-2 px-3 py-2 rounded text-xs font-mono text-red-600 dark:text-red-400 border border-red-200 dark:border-red-900"
                            >
                                <LogOut className="w-4 h-4" /> LOGOUT
                            </button>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </header>
    );
}

export default Navbar;