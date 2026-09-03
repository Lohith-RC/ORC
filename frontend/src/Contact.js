import React from 'react';
import { motion } from 'framer-motion';
import { Phone, Mail, MapPin } from 'lucide-react';
import mapImage from './images/10.webp';

const Contact = () => {

    const MapPlaceholder = ({ className }) => (
        <div className={`flex items-center justify-center bg-gray-200 dark:bg-gray-700 rounded-lg ${className}`}>
            <div className="text-center">
                <MapPin className="w-16 h-16 mx-auto text-gray-400 dark:text-gray-500" />
                <span className="mt-2 block text-gray-500 dark:text-gray-400">Map Placeholder</span>
            </div>
        </div>
    );

    return (
        <div className="bg-gray-50 dark:bg-gray-900/95 min-h-screen py-20 px-4 sm:px-6 lg:px-8">
            <motion.div
                initial={{ opacity: 0, y: -50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7 }}
                className="max-w-7xl mx-auto"
            >
                <div className="text-center">
                    <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white">Get in Touch</h1>
                    <p className="mt-4 text-xl text-gray-600 dark:text-gray-300">
                        We'd love to hear from you. Whether you have a question about our services, partnerships, or anything else, our team is ready to answer all your questions.
                    </p>
                </div>

                <div className="mt-20 grid md:grid-cols-2 gap-16 items-start">
                    {/* Contact Form */}
                    <motion.div
                        initial={{ opacity: 0, x: -50 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true, amount: 0.3 }}
                        transition={{ duration: 0.8 }}
                        className="bg-white dark:bg-gray-800 p-8 sm:p-12 rounded-2xl shadow-lg"
                    >
                        <form>
                            <div className="space-y-6">
                                <div>
                                    <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Full Name</label>
                                    <input type="text" id="name" placeholder="Roy Williams" className="mt-1 block w-full px-4 py-3 rounded-md border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                                </div>
                                <div>
                                    <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Email Address</label>
                                    <input type="email" id="email" placeholder="roy.williams@example.com" className="mt-1 block w-full px-4 py-3 rounded-md border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
                                </div>
                                <div>
                                    <label htmlFor="message" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Message</label>
                                    <textarea id="message" rows="5" placeholder="Your message..." className="mt-1 block w-full px-4 py-3 rounded-md border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500"></textarea>
                                </div>
                            </div>
                            <button type="submit" className="mt-8 w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-sm text-base font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transform hover:scale-105 transition duration-300">
                                Send Message
                            </button>
                        </form>
                    </motion.div>

                    {/* Contact Info & Map */}
                    <motion.div
                        initial={{ opacity: 0, x: 50 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true, amount: 0.3 }}
                        transition={{ duration: 0.8 }}
                        className="space-y-8"
                    >
                        <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg">
                            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Contact Information</h3>
                             <div className="space-y-4">
                                <p className="flex items-center text-lg text-gray-600 dark:text-gray-300">
                                    <Mail className="w-6 h-6 mr-4 text-blue-500" />
                                    <span>contact@oralcancerai.com</span>
                                </p>
                                <p className="flex items-center text-lg text-gray-600 dark:text-gray-300">
                                    <Phone className="w-6 h-6 mr-4 text-blue-500" />
                                    <span>+1 (555) 123-4567</span>
                                </p>
                                <p className="flex items-start text-lg text-gray-600 dark:text-gray-300">
                                    <MapPin className="w-6 h-6 mr-4 mt-1 text-blue-500" />
                                    <span>123 Health Tech Avenue, <br />Innovation City, MedState 12345</span>
                                </p>
                            </div>
                        </div>
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.8, delay: 0.2 }}
                        >
                            <img src={mapImage} alt="Location Map" className="h-80 w-full object-cover rounded-2xl shadow-lg" />
                        </motion.div>
                    </motion.div>
                </div>
            </motion.div>
        </div>
    );
};

export default Contact; 