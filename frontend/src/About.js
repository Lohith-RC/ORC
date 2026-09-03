import React from 'react';
import { motion } from 'framer-motion';
import { Users, Target, Award, GitCommit, Users2, FlaskConical, Rocket, Database, Stethoscope } from 'lucide-react';
import team1 from './images/5.webp';
import team2 from './images/7.webp';
import team3 from './images/8.jpg';
import team4 from './images/9.webp';
import team5 from './images/10.webp';
import doc1 from './images/1.jpg';
import doc2 from './images/2.jpg';
import doc3 from './images/3.jpg';

const About = () => {
    return (
        <div className="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 py-20 sm:py-28 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                {/* Header Section */}
                <motion.div
                    initial={{ opacity: 0, y: -50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.7 }}
                    className="text-center mb-20"
                >
                    <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent mb-4">
                        A Student Initiative for Better Healthcare
                    </h1>
                    <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
                        We are a passionate team of engineering students from Karnataka, India, leveraging artificial intelligence to build accessible early-detection tools for oral cancer under the esteemed guidance of Prof. Aishwarya S.
                    </p>
                </motion.div>

                {/* Student Team Section */}
                <div className="mb-24">
                    <h2 className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-4">Meet the Student Developers</h2>
                    <p className="text-center text-gray-500 mb-16 max-w-2xl mx-auto">
                        Developed with passion by a dedicated team of student engineers committed to applying technology for social good.
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10">
                        {[
                            { name: "Keerthi A", role: "AI & ML Engineer", image: team1 },
                            { name: "Rakshith Y B", role: "Backend Developer", image: team2 },
                            { name: "Lohith R C", role: "Frontend & UI/UX", image: team3 }
                        ].map((member, i) => (
                            <motion.div
                                key={i}
                                className="text-center bg-gray-50 dark:bg-gray-800/50 p-6 rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300"
                                initial={{ opacity: 0, y: 50 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: i * 0.1 }}
                            >
                                <img src={member.image} alt={member.name} className="w-32 h-32 rounded-full mx-auto mb-4 object-cover ring-4 ring-blue-100 dark:ring-blue-900" />
                                <h3 className="text-xl font-bold text-gray-800 dark:text-white">{member.name}</h3>
                                <p className="text-blue-600 dark:text-blue-400 font-medium">{member.role}</p>
                                <p className="text-sm text-gray-500 mt-2">Student Developer</p>
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* Doctors Section */}
                <div className="mb-24 bg-blue-50 dark:bg-gray-800/80 rounded-3xl p-10 sm:p-16">
                    <h2 className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-4">Our Medical Advisors</h2>
                    <p className="text-center text-gray-600 dark:text-gray-300 mb-16 max-w-2xl mx-auto">
                        Our AI models and clinical workflows are advised and validated by renowned oral oncology experts from top cancer research institutes across Karnataka.
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-10">
                        {[
                            { name: "Dr. Vishal Rao", role: "Head of Head & Neck Oncology", clinic: "HCG Cancer Centre, Bangalore", image: doc1 },
                            { name: "Dr. Moni Abraham Kuriakose", role: "Director of Surgical Oncology", clinic: "Mazumdar Shaw Medical Center", image: doc2 },
                            { name: "Dr. Vikram Kekatpure", role: "Senior Consultant, Head & Neck Surgery", clinic: "Cytecare Cancer Hospitals", image: doc3 }
                        ].map((doc, i) => (
                            <motion.div
                                key={i}
                                className="text-center bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-md hover:shadow-xl transition-all duration-300"
                                initial={{ opacity: 0, scale: 0.9 }}
                                whileInView={{ opacity: 1, scale: 1 }}
                                viewport={{ once: true }}
                                transition={{ delay: i * 0.1 }}
                            >
                                <div className="relative inline-block">
                                    <img src={doc.image} alt={doc.name} className="w-40 h-40 rounded-full mx-auto mb-4 object-cover ring-4 ring-indigo-100 dark:ring-indigo-900" />
                                    <div className="absolute bottom-2 right-2 bg-blue-600 p-2 rounded-full text-white">
                                        <Stethoscope className="w-5 h-5" />
                                    </div>
                                </div>
                                <h3 className="text-xl font-bold text-gray-800 dark:text-white">{doc.name}</h3>
                                <p className="text-indigo-600 dark:text-indigo-400 font-medium">{doc.role}</p>
                                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">{doc.clinic}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* Datasets Section */}
                <div className="mb-24">
                    <h2 className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-16 flex items-center justify-center gap-4">
                        <Database className="w-10 h-10 text-blue-600" />
                        Our Training Datasets
                    </h2>
                    <div className="grid md:grid-cols-2 gap-10">
                        <motion.div 
                            className="bg-gray-50 dark:bg-gray-800/50 p-8 rounded-2xl border border-gray-100 dark:border-gray-700"
                            initial={{ opacity: 0, x: -50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true }}
                        >
                            <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">Kaggle Oral Cancer Dataset</h3>
                            <p className="text-gray-600 dark:text-gray-300 mb-4">
                                A comprehensive collection of over 5,000 high-resolution images categorized into cancerous and non-cancerous oral cavity images. This dataset forms the foundational training ground for our CNN models.
                            </p>
                            <ul className="space-y-2 text-sm text-gray-500 dark:text-gray-400">
                                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-blue-500"></div> Total Images: 5,000+</li>
                                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-blue-500"></div> Classes: SCC, Normal, Benign</li>
                                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-blue-500"></div> Accuracy Achieved: 94.2%</li>
                            </ul>
                        </motion.div>
                        
                        <motion.div 
                            className="bg-gray-50 dark:bg-gray-800/50 p-8 rounded-2xl border border-gray-100 dark:border-gray-700"
                            initial={{ opacity: 0, x: 50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true }}
                        >
                            <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">Clinical Research Dataset (Karnataka)</h3>
                            <p className="text-gray-600 dark:text-gray-300 mb-4">
                                An exclusive dataset compiled through our partnerships with local clinics and hospitals in Karnataka, helping fine-tune our models to demographic-specific variations and real-world clinical noise.
                            </p>
                            <ul className="space-y-2 text-sm text-gray-500 dark:text-gray-400">
                                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-purple-500"></div> Total Images: 1,200+</li>
                                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-purple-500"></div> Sourced from: Regional Clinics</li>
                                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-purple-500"></div> Focus: Early-stage lesions</li>
                            </ul>
                        </motion.div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default About;