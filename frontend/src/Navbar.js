import React, { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { Stethoscope, LogIn, UserPlus, Upload, User, LogOut, Menu, X, Info, Phone, Sun, Moon } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from './ThemeContext';

function Navbar({ loggedIn, onLogout }) {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const { theme, toggleTheme } = useTheme();

    const navLinkClasses = "flex items-center px-3 py-2 rounded-md text-base font-medium transition-colors";
    const activeClassName = "bg-teal-100 dark:bg-teal-900/50 text-teal-700 dark:text-teal-300";
    const inactiveClassName = "text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white";
    
    const getNavLinkClass = ({ isActive }) => `${navLinkClasses} ${isActive ? activeClassName : inactiveClassName}`;

    const ThemeToggleButton = () => (
        <button onClick={toggleTheme} className="p-2 rounded-full text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
            {theme === 'light' ? <Moon className="w-6 h-6" /> : <Sun className="w-6 h-6 text-yellow-400" />}
        </button>
    );

    const navLinks = (
        <>
            <NavLink to="/about" className={getNavLinkClass}><Info className="w-5 h-5 mr-2" />About</NavLink>
            <NavLink to="/contact" className={getNavLinkClass}><Phone className="w-5 h-5 mr-2" />Contact</NavLink>
            {loggedIn ? (
                <>
                    <NavLink to="/upload" className={getNavLinkClass}><Upload className="w-5 h-5 mr-2" />Upload</NavLink>
                    <NavLink to="/profile" className={getNavLinkClass}><User className="w-5 h-5 mr-2" />Profile</NavLink>
                </>
            ) : (
                <>
                    <NavLink to="/login" className={getNavLinkClass}><LogIn className="w-5 h-5 mr-2" />Login</NavLink>
                    <NavLink to="/register" className={getNavLinkClass}><UserPlus className="w-5 h-5 mr-2" />Register</NavLink>
                </>
            )}
        </>
    );
    
    return (
        <nav className="bg-white/80 dark:bg-slate-950/80 backdrop-blur-md shadow-sm sticky top-0 z-50 border-b border-slate-100 dark:border-slate-800">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-20">
                    <div className="flex-shrink-0">
                        <Link to="/" className="flex items-center space-x-2 text-2xl font-bold">
                            <Stethoscope className="w-8 h-8 text-teal-600" />
                            <span className="font-display bg-gradient-to-r from-teal-500 to-blue-500 bg-clip-text text-transparent">OralCancer AI</span>
                        </Link>
                    </div>
                    <div className="hidden md:block">
                        <div className="ml-10 flex items-center space-x-4">
                            {navLinks}
                        </div>
                    </div>
                    <div className="hidden md:flex items-center space-x-4">
                        <ThemeToggleButton />
                         {loggedIn && (
                            <button onClick={onLogout} className="flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-red-600 hover:bg-red-700">
                                <LogOut className="w-5 h-5 mr-2" /> Logout
                            </button>
                        )}
                    </div>
                    <div className="-mr-2 flex md:hidden">
                        <ThemeToggleButton />
                        <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="bg-gray-100 dark:bg-gray-800 ml-2 inline-flex items-center justify-center p-2 rounded-md text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-white hover:bg-gray-200 dark:hover:bg-gray-700">
                            <span className="sr-only">Open main menu</span>
                            {mobileMenuOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
                        </button>
                    </div>
                </div>
            </div>

            <AnimatePresence>
                {mobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        className="md:hidden border-t border-gray-200 dark:border-gray-700"
                    >
                        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                            {navLinks}
                             {loggedIn && (
                                <button onClick={onLogout} className="w-full mt-2 flex items-center px-3 py-2 rounded-md text-base font-medium text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/20 hover:bg-red-100 dark:hover:bg-red-900/40">
                                    <LogOut className="w-5 h-5 mr-2" /> Logout
                                </button>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
}

export default Navbar; 