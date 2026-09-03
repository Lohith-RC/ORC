import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Navbar from './Navbar';
import Home from './Home';
import About from './About';
import Contact from './Contact';
import Login from './Login';
import Register from './Register';
import Upload from './Upload';
import Profile from './Profile';

const App = () => {
    const [token, setToken] = useState(null);

    useEffect(() => {
        const storedToken = localStorage.getItem('token');
        if (storedToken) {
            setToken(storedToken);
        }
    }, []);

    const handleLogin = (newToken) => {
        localStorage.setItem('token', newToken);
        setToken(newToken);
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setToken(null);
    };
    
    const PrivateRoute = ({ children }) => {
        return token ? children : <Navigate to="/login" />;
    };

    return (
        <Router>
            <div className="bg-white dark:bg-gray-900 transition-colors duration-300">
                <Navbar loggedIn={!!token} onLogout={handleLogout} />
                <AnimatePresence mode="wait">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/about" element={<About />} />
                        <Route path="/contact" element={<Contact />} />
                        <Route path="/login" element={<Login onLogin={handleLogin} />} />
                        <Route path="/register" element={<Register onLogin={handleLogin} />} />
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
            </div>
        </Router>
    );
};

export default App;
