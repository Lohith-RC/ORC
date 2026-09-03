import React, { useCallback, useState, useRef, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, FileImage, XCircle, AlertTriangle, CheckCircle, BarChart, Percent, Download } from 'lucide-react';
import axios from 'axios';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

const Upload = ({ token }) => {
  const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
    const [user, setUser] = useState(null);
    const reportRef = useRef();
    // Fault 5: Clinical risk factors
    const [riskForm, setRiskForm] = useState({ age: 30, tobacco_use: false, alcohol_use: false, betel_nut: false, prior_lesions: false });

    useEffect(() => {
        if (token) {
            axios.get('http://localhost:8000/me', {
                headers: { 'Authorization': `Bearer ${token}` }
            }).then(response => {
                setUser(response.data);
            }).catch(err => {
                console.error("Failed to fetch user data for report", err);
            });
        }
    }, [token]);

    const onDrop = useCallback(acceptedFiles => {
        setResult(null);
    setError('');
        const selectedFile = acceptedFiles[0];
        if (selectedFile) {
            setFile(selectedFile);
            const reader = new FileReader();
            reader.onload = () => {
                setPreview(reader.result);
            };
            reader.readAsDataURL(selectedFile);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'image/*': ['.jpeg', '.jpg', '.png'] },
        multiple: false
    });

    const handleUpload = async () => {
    if (!file) {
            setError('Please select a file first.');
      return;
    }
    setLoading(true);
    setError('');
        setResult(null);
    const formData = new FormData();
    formData.append('file', file);
    // Append clinical risk factors as query params via URL
    const params = new URLSearchParams({
        age: riskForm.age,
        tobacco_use: riskForm.tobacco_use,
        alcohol_use: riskForm.alcohol_use,
        betel_nut: riskForm.betel_nut,
        prior_lesions: riskForm.prior_lesions,
    });

    try {
            const response = await axios.post(`http://localhost:8000/predict?${params.toString()}`, formData, {
        headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${token}`
                }
            });
            console.log("Received from backend:", response.data);
            setResult(response.data);
    } catch (err) {
            setError(err.response?.data?.detail || err.response?.data?.error || 'An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };
    
    const removeFile = () => {
        setFile(null);
        setPreview(null);
        setResult(null);
        setError('');
    };

    const handleDownload = () => {
        const input = reportRef.current;
        if (input) {
            html2canvas(input, { scale: 2, useCORS: true }).then((canvas) => {
                const imgData = canvas.toDataURL('image/png');
                const pdf = new jsPDF('p', 'mm', 'a4');
                const pdfWidth = pdf.internal.pageSize.getWidth();
                const pdfHeight = pdf.internal.pageSize.getHeight();
                const canvasWidth = canvas.width;
                const canvasHeight = canvas.height;
                const ratio = canvasWidth / canvasHeight;
                let newWidth = pdfWidth;
                let newHeight = newWidth / ratio;
                if (newHeight > pdfHeight) {
                    newHeight = pdfHeight;
                    newWidth = newHeight * ratio;
                }
                const xOffset = (pdfWidth - newWidth) / 2;

                pdf.addImage(imgData, 'PNG', xOffset, 0, newWidth, newHeight);
                pdf.save('OralCancer_Report.pdf');
            });
        }
    };

    const dropzoneVariants = {
        initial: { y: -20, opacity: 0 },
        animate: { y: 0, opacity: 1, transition: { duration: 0.5 } },
        exit: { y: 20, opacity: 0, transition: { duration: 0.3 } }
    };

    const isCancer = result?.prediction?.toLowerCase() === 'cancer';
    const isUncertain = result?.prediction?.toLowerCase() === 'uncertain';
    const resultColor = isUncertain ? 'text-yellow-500' : (isCancer ? 'text-red-500' : 'text-green-500');
    const resultBg = isUncertain ? 'bg-yellow-500/10' : (isCancer ? 'bg-red-500/10' : 'bg-green-500/10');

  return (
        <div className="bg-gray-50 dark:bg-gray-900/95 min-h-screen py-16 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-12"
                >
                    <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white">Upload Your Image</h1>
                    <p className="mt-4 text-xl text-gray-600 dark:text-gray-300">Get an instant AI-powered analysis of your oral image.</p>
                </motion.div>

                <div className="grid md:grid-cols-2 gap-8 items-start">
                    {/* Main Upload Area */}
                    <div className="space-y-6">
                        <AnimatePresence mode="wait">
                            {!preview ? (
                                <motion.div
                                    key="dropzone"
                                    variants={dropzoneVariants}
                                    initial="initial"
                                    animate="animate"
                                    exit="exit"
                                    {...getRootProps()}
                                    className={`p-10 border-4 border-dashed rounded-2xl cursor-pointer text-center transition-colors duration-300 ${isDragActive ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500 bg-white dark:bg-gray-800'}`}
                                >
                                    <input {...getInputProps()} />
                                    <UploadCloud className="w-16 h-16 mx-auto text-gray-400 dark:text-gray-500 mb-4" />
                                    <p className="text-lg font-semibold text-gray-700 dark:text-gray-200">
                                        {isDragActive ? 'Drop the image here ...' : "Drag 'n' drop an image here, or click to select"}
                                    </p>
                                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Supports: *.jpeg, *.jpg, *.png</p>
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="preview"
                                    variants={dropzoneVariants}
                                    initial="initial"
                                    animate="animate"
                                    exit="exit"
                                    className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg relative"
                                >
                                    <div className="flex items-center space-x-4">
                                        <FileImage className="w-12 h-12 text-blue-500" />
                                        <div>
                                            <h3 className="font-semibold text-gray-800 dark:text-gray-100">{file.name}</h3>
                                            <p className="text-sm text-gray-500 dark:text-gray-400">{(file.size / 1024).toFixed(2)} KB</p>
                                        </div>
                                    </div>
                                    <div className="mt-4 aspect-video overflow-hidden rounded-lg">
                                        <img src={preview} alt="Preview" className="w-full h-full object-cover" />
                                    </div>
                                    <button onClick={removeFile} className="absolute -top-3 -right-3 bg-red-500 text-white rounded-full p-1.5 shadow-md hover:bg-red-600 transition">
                                        <XCircle className="w-6 h-6" />
                                    </button>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        {/* Clinical Risk Factors — Fault 5 */}
                        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg">
                            <h3 className="text-base font-bold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
                                <span className="text-amber-500">⚕</span> Patient Risk Factors <span className="text-xs font-normal text-gray-400 ml-1">(optional — improves accuracy)</span>
                            </h3>
                            <div className="grid grid-cols-2 gap-3">
                                <div className="col-span-2">
                                    <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">Age</label>
                                    <input type="number" min="5" max="110" value={riskForm.age}
                                        onChange={e => setRiskForm(p => ({...p, age: parseInt(e.target.value) || 30}))}
                                        className="w-full px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white text-sm border border-gray-200 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-teal-500"
                                    />
                                </div>
                                {[
                                    { key: 'tobacco_use', label: 'Tobacco Use' },
                                    { key: 'alcohol_use', label: 'Alcohol Use' },
                                    { key: 'betel_nut', label: 'Betel Nut Use' },
                                    { key: 'prior_lesions', label: 'Prior Oral Lesions' },
                                ].map(({ key, label }) => (
                                    <label key={key} className="flex items-center gap-2 cursor-pointer select-none bg-gray-50 dark:bg-gray-700/50 rounded-lg px-3 py-2">
                                        <input type="checkbox" checked={riskForm[key]}
                                            onChange={e => setRiskForm(p => ({...p, [key]: e.target.checked}))}
                                            className="accent-teal-500 w-4 h-4"
                                        />
                                        <span className="text-sm text-gray-700 dark:text-gray-200">{label}</span>
                                    </label>
                                ))}
                            </div>
                        </div>

                        {file && !loading && (
                            <motion.button
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={handleUpload}
                                className="w-full bg-gradient-to-r from-teal-500 to-emerald-500 text-white font-bold py-4 px-4 rounded-xl text-lg shadow-lg hover:shadow-xl transition-shadow duration-300"
                            >
                                Analyze Image
                            </motion.button>
                        )}
                    </div>
                    
                    {/* Sidebar */}
                    <div className="space-y-6">
                        {/* Result/Loading Area */}
                        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg h-full min-h-[15rem] flex flex-col justify-center">
                            <AnimatePresence mode="wait">
                                {loading ? (
                                    <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-center">
                                        <div className="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 dark:border-gray-600 h-12 w-12 mb-4 mx-auto" style={{ borderTopColor: '#3498db' }}></div>
                                        <p className="text-lg font-semibold text-gray-700 dark:text-gray-200">Analyzing...</p>
                                        <p className="text-sm text-gray-500 dark:text-gray-400">This may take a moment.</p>
                                    </motion.div>
                                ) : error ? (
                                    <motion.div key="error" initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.8 }} className="flex flex-col items-center text-center text-red-500">
                                        <AlertTriangle className="w-12 h-12 mb-3" />
                                        <p className="font-bold">An Error Occurred</p>
                                        <p className="text-sm">{error}</p>
                                    </motion.div>
                                ) : result ? (
                                    <motion.div key="result" initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} className="text-center">
                                        <div className={`mx-auto w-16 h-16 rounded-full flex items-center justify-center ${resultBg}`}>
                                            {isUncertain ? <AlertTriangle className={`w-8 h-8 ${resultColor}`} /> : (isCancer ? <AlertTriangle className={`w-8 h-8 ${resultColor}`} /> : <CheckCircle className={`w-8 h-8 ${resultColor}`} />)}
                                        </div>
                                        <p className="text-sm font-semibold text-gray-500 dark:text-gray-400 mt-4">Result</p>
                                        <p className={`text-4xl font-bold mt-1 capitalize ${resultColor}`}>{result.prediction}</p>

                                        {/* Status badges */}
                                        <div className="flex flex-wrap justify-center gap-2 mt-3">
                                            {result.image_quality === 'low_quality' && (
                                                <span className="text-xs font-semibold px-2 py-1 rounded-full bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300">⚠ Low Image Quality</span>
                                            )}
                                            {result.clinical_alert && (
                                                <span className="text-xs font-semibold px-2 py-1 rounded-full bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300">🔴 High Clinical Risk</span>
                                            )}
                                            {result.tta_passes && (
                                                <span className="text-xs font-semibold px-2 py-1 rounded-full bg-teal-100 text-teal-700 dark:bg-teal-900/40 dark:text-teal-300">✓ TTA Enhanced</span>
                                            )}
                                        </div>

                                        {/* Metrics row */}
                                        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 grid grid-cols-3 gap-2 text-center">
                                            <div>
                                                <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Confidence</p>
                                                <p className={`text-xl font-bold ${resultColor} flex items-center justify-center`}>
                                                    <Percent className="w-4 h-4 mr-1" />
                                                    {typeof result.confidence === 'number' ? (result.confidence * 100).toFixed(1) : 'N/A'}
                                                </p>
                                            </div>
                                            <div>
                                                <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Uncertainty</p>
                                                <p className={`text-xl font-bold ${result.uncertainty > 0.015 ? 'text-yellow-500' : 'text-green-500'}`}>
                                                    {typeof result.uncertainty === 'number' ? (result.uncertainty * 1000).toFixed(2) + '‱' : 'N/A'}
                                                </p>
                                            </div>
                                            <div>
                                                <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Risk Score</p>
                                                <p className={`text-xl font-bold ${result.clinical_risk_score >= 0.6 ? 'text-red-500' : result.clinical_risk_score >= 0.3 ? 'text-yellow-500' : 'text-green-500'}`}>
                                                    {typeof result.clinical_risk_score === 'number' ? (result.clinical_risk_score * 100).toFixed(0) + '%' : 'N/A'}
                                                </p>
                                            </div>
                                        </div>

                                        <div className="mt-6">
                                            <h4 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">AI Focus Heatmap (XAI)</h4>
                                            <div className="relative aspect-video overflow-hidden rounded-lg shadow-inner ring-1 ring-black/5 dark:ring-white/10">
                                                <img src={preview} alt="Base" className="absolute inset-0 w-full h-full object-cover grayscale opacity-90" />
                                                {isCancer && (
                                                    <div className="absolute inset-0 mix-blend-color-burn opacity-80 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-red-600 via-transparent to-transparent scale-150 animate-pulse"></div>
                                                )}
                                                {!isCancer && (
                                                    <div className="absolute inset-0 mix-blend-color-burn opacity-40 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-green-500 via-transparent to-transparent scale-150"></div>
                                                )}
                                                <div className="absolute bottom-2 right-2 bg-black/50 backdrop-blur-md px-2 py-1 rounded text-[10px] text-white uppercase tracking-wider">
                                                    Simulated Grad-CAM
                                                </div>
                                            </div>
                                        </div>

                                        <div className="mt-6 text-left p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                                            <h4 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-3">
                                                {isUncertain ? "Uncertain Result - Action Required" : (isCancer ? "Precautions & Next Steps" : "Recommendations")}
                                            </h4>
                                            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                                                {isUncertain ? (
                                                    <>
                                                        <li className="flex items-start"><AlertTriangle className="w-4 h-4 mr-2 mt-0.5 text-yellow-500 flex-shrink-0" /><span>The AI is uncertain about this image due to artifacts, blur, or complex pathology.</span></li>
                                                        <li className="flex items-start"><AlertTriangle className="w-4 h-4 mr-2 mt-0.5 text-yellow-500 flex-shrink-0" /><span>Please capture a clearer image and re-upload.</span></li>
                                                        <li className="flex items-start"><AlertTriangle className="w-4 h-4 mr-2 mt-0.5 text-yellow-500 flex-shrink-0" /><span>If uncertainty persists, refer immediately to a clinical specialist for manual biopsy.</span></li>
                                                    </>
                                                ) : isCancer ? (
                                                    <>
                                                        <li className="flex items-start"><AlertTriangle className="w-4 h-4 mr-2 mt-0.5 text-red-500 flex-shrink-0" /><span>Visit a nearby hospital for a professional diagnosis.</span></li>
                                                        <li className="flex items-start"><AlertTriangle className="w-4 h-4 mr-2 mt-0.5 text-red-500 flex-shrink-0" /><span>Prepare for weekly checkups as advised by your doctor.</span></li>
                                                        <li className="flex items-start"><AlertTriangle className="w-4 h-4 mr-2 mt-0.5 text-red-500 flex-shrink-0" /><span>Follow the prescribed medication and treatment plan strictly.</span></li>
                                                        <li className="flex items-start"><AlertTriangle className="w-4 h-4 mr-2 mt-0.5 text-red-500 flex-shrink-0" /><span>Take all necessary care as advised by your healthcare provider.</span></li>
                                                    </>
                                                ) : (
                                                    <>
                                                        <li className="flex items-start"><CheckCircle className="w-4 h-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" /><span>You appear to be healthy, so there's no need to panic.</span></li>
                                                        <li className="flex items-start"><CheckCircle className="w-4 h-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" /><span>Continue with monthly doctor visits for routine checkups.</span></li>
                                                        <li className="flex items-start"><CheckCircle className="w-4 h-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" /><span>Maintain a healthy diet and lifestyle.</span></li>
                                                    </>
                                                )}
                                            </ul>
                                             <p className="text-xs text-gray-400 dark:text-gray-500 mt-4 italic">
                                                *This is an AI-generated analysis and not a substitute for professional medical advice.
                                            </p>
                                        </div>

                                        <div className="mt-6">
                                            <button
                                                onClick={handleDownload}
                                                className="w-full flex items-center justify-center bg-blue-600 text-white font-bold py-3 px-4 rounded-xl text-lg shadow-lg hover:bg-blue-700 transition-shadow duration-300"
                                            >
                                                <Download className="w-5 h-5 mr-2" />
                                                Download Report
        </button>
                                        </div>
                                    </motion.div>
                                ) : (
                                    <motion.div key="placeholder" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center text-gray-500 dark:text-gray-400">
                                        <BarChart className="w-12 h-12 mx-auto mb-3" />
                                        <p className="font-semibold">Your results will appear here.</p>
                                        <p className="text-sm mt-1">Upload an image to start the analysis.</p>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </div>
                        {/* Guidelines */}
                         <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg">
                            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-3">Image Guidelines</h3>
                            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                                <li className="flex items-start"><CheckCircle className="w-4 h-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" /> Clear, in-focus image.</li>
                                <li className="flex items-start"><CheckCircle className="w-4 h-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" /> Good, direct lighting.</li>
                                <li className="flex items-start"><CheckCircle className="w-4 h-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" /> Image taken from a close distance.</li>
                                <li className="flex items-start"><XCircle className="w-4 h-4 mr-2 mt-0.5 text-red-500 flex-shrink-0" /> Avoid blurry or dark photos.</li>
                            </ul>
                        </div>
                    </div>
                </div>

                {result && user && (
                     <div style={{ position: 'absolute', left: '-9999px', top: 'auto' }}>
                        <div ref={reportRef} className="p-10 bg-white text-black w-[800px]">
                            <h1 className="text-4xl font-bold text-center mb-2">Oral Cancer AI</h1>
                            <p className="text-center text-gray-600 mb-8">Analysis Report</p>
                            
                            <div className="grid grid-cols-2 gap-8 mb-8">
                                <div>
                                    <h2 className="text-xl font-bold border-b pb-2 mb-2">Patient Details</h2>
                                    <p><strong>Name:</strong> {user.full_name}</p>
                                    <p><strong>Email:</strong> {user.email}</p>
                                    <p><strong>Report Date:</strong> {new Date().toLocaleDateString()}</p>
                                </div>
                                 <div>
                                    <h2 className="text-xl font-bold border-b pb-2 mb-2">Analysis Result</h2>
                                    <p><strong>Prediction:</strong> <span className={isCancer ? 'font-bold text-red-600' : 'font-bold text-green-600'}>{result.prediction}</span></p>
                                    <p><strong>Confidence:</strong> {typeof result.confidence === 'number' ? (result.confidence * 100).toFixed(1) + '%' : 'N/A'}</p>
                                </div>
                            </div>

                            <h2 className="text-xl font-bold border-b pb-2 mb-4">Uploaded Image</h2>
                            <img src={preview} alt="Uploaded for analysis" className="max-w-md mx-auto rounded-lg shadow-md mb-8" />
                            
                            <h2 className="text-xl font-bold border-b pb-2 mb-4">
                                {isCancer ? "Precautions & Next Steps" : "Recommendations"}
                            </h2>
                            <ul className="list-disc list-inside space-y-2 text-sm mb-8">
                                {isCancer ? (
                                    <>
                                        <li>Visit a nearby hospital for a professional diagnosis.</li>
                                        <li>Prepare for weekly checkups as advised by your doctor.</li>
                                        <li>Follow the prescribed medication and treatment plan strictly.</li>
                                        <li>Take all necessary care as advised by your healthcare provider.</li>
                                    </>
                                ) : (
                                    <>
                                        <li>You appear to be healthy, so there's no need to panic.</li>
                                        <li>Continue with monthly doctor visits for routine checkups.</li>
                                        <li>Maintain a healthy diet and lifestyle.</li>
                                    </>
                                )}
                            </ul>

                            <p className="text-xs text-gray-500 mt-12 pt-4 border-t text-center">
                                *This is an AI-generated analysis and not a substitute for professional medical advice. Always consult a qualified healthcare provider for any health concerns.
                            </p>
                        </div>
        </div>
      )}
            </div>
    </div>
  );
};

export default Upload; 