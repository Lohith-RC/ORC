import React, { Suspense, lazy, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Navbar from './Navbar';
import Footer from './Footer';
import ErrorBoundary from './ErrorBoundary';
import { ThemeProvider } from './ThemeContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';

// Route-level code splitting via React.lazy
const Home = lazy(() => import('./Home'));
const About = lazy(() => import('./About'));
const Contact = lazy(() => import('./Contact'));
const Login = lazy(() => import('./Login'));
const Register = lazy(() => import('./Register'));
const Upload = lazy(() => import('./Upload'));
const Profile = lazy(() => import('./Profile'));

const ScrollToTop = () => {
    const { pathname } = useLocation();
    useEffect(() => {
        window.scrollTo(0, 0);
    }, [pathname]);
    return null;
};

const LoadingFallback = () => (
    <div className="flex justify-center items-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-teal-600"></div>
            <span className="font-mono text-xs text-slate-400">Loading Clinical Module...</span>
        </div>
    </div>
);

const AppContent = () => {
    const { token, isAuthenticated, login, logout } = useAuth();

    return (
        <div className="min-h-screen flex flex-col justify-between bg-slate-50 dark:bg-[#080B10] text-slate-900 dark:text-slate-100 transition-colors duration-200">
            <ScrollToTop />
            <Navbar loggedIn={isAuthenticated} onLogout={logout} />
            
            <main className="flex-grow">
                <Suspense fallback={<LoadingFallback />}>
                    <AnimatePresence mode="wait">
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/about" element={<About />} />
                            <Route path="/contact" element={<Contact />} />
                            <Route path="/login" element={<Login onLogin={login} />} />
                            <Route path="/register" element={<Register onLogin={login} />} />
                            <Route path="/upload" element={
                                <PrivateRoute>
                                    <Upload token={token} />
                                </PrivateRoute>
                            } />
                            <Route path="/profile" element={
                                <PrivateRoute>
                                    <Profile token={token} />
                                </PrivateRoute>
                            } />
                        </Routes>
                    </AnimatePresence>
                </Suspense>
            </main>

            <Footer />
        </div>
    );
};

const App = () => (
    <ErrorBoundary>
        <ThemeProvider>
            <AuthProvider>
                <Router>
                    <AppContent />
                </Router>
            </AuthProvider>
        </ThemeProvider>
    </ErrorBoundary>
);

export default App;
