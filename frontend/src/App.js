import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Navbar from './Navbar';
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

const LoadingFallback = () => (
    <div className="flex justify-center items-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>
);

const AppContent = () => {
    const { token, isAuthenticated, login, logout } = useAuth();

    return (
        <div className="bg-white dark:bg-gray-900 transition-colors duration-300 min-h-screen">
            <Navbar loggedIn={isAuthenticated} onLogout={logout} />
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
