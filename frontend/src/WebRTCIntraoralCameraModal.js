import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Camera, RefreshCw, X, CheckCircle2, AlertTriangle, VideoOff, Crosshair } from 'lucide-react';
import { computeClientLaplacian } from './clientBlurDetector';

const WebRTCIntraoralCameraModal = ({ isOpen, onClose, onCapture, targetSite = 'buccal_mucosa' }) => {
    const videoRef = useRef(null);
    const streamRef = useRef(null);
    const intervalRef = useRef(null);

    const [devices, setDevices] = useState([]);
    const [selectedDeviceId, setSelectedDeviceId] = useState('');
    const [liveSharpness, setLiveSharpness] = useState(0);
    const [isBlurry, setIsBlurry] = useState(true);
    const [isStreaming, setIsStreaming] = useState(false);
    const [errorMsg, setErrorMsg] = useState(null);

    // Stop current media stream
    const stopStream = useCallback(() => {
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
            streamRef.current = null;
        }
        setIsStreaming(false);
    }, []);

    // Start video stream with selected device
    const startStream = useCallback(async (deviceId = '') => {
        stopStream();
        setErrorMsg(null);

        try {
            const constraints = {
                video: {
                    width: { ideal: 1920, min: 640 },
                    height: { ideal: 1080, min: 480 },
                    deviceId: deviceId ? { exact: deviceId } : undefined,
                    facingMode: deviceId ? undefined : { ideal: "environment" }
                }
            };

            const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
            streamRef.current = mediaStream;

            if (videoRef.current) {
                videoRef.current.srcObject = mediaStream;
                await videoRef.current.play();
                setIsStreaming(true);

                // Start real-time optical Laplacian analyzer loop (every 200ms)
                intervalRef.current = setInterval(() => {
                    if (videoRef.current && videoRef.current.readyState >= 2) {
                        const { sharpness, isBlurry: blurry } = computeClientLaplacian(videoRef.current);
                        setLiveSharpness(sharpness);
                        setIsBlurry(blurry);
                    }
                }, 200);
            }
        } catch (err) {
            console.error("Camera acquisition error:", err);
            setErrorMsg(err.name === 'NotAllowedError' 
                ? "Camera permission denied. Please enable camera access in your browser settings."
                : `Hardware camera initialization failed: ${err.message}`
            );
            setIsStreaming(false);
        }
    }, [stopStream]);

    // Enumerate connected cameras (Intraoral USB wands, macro lenses, webcams)
    useEffect(() => {
        if (!isOpen) {
            stopStream();
            return;
        }

        const enumerateDevices = async () => {
            try {
                const devs = await navigator.mediaDevices.enumerateDevices();
                const videoDevs = devs.filter(d => d.kind === 'videoinput');
                setDevices(videoDevs);
                if (videoDevs.length > 0 && !selectedDeviceId) {
                    setSelectedDeviceId(videoDevs[0].deviceId);
                    startStream(videoDevs[0].deviceId);
                } else {
                    startStream(selectedDeviceId);
                }
            } catch {
                startStream();
            }
        };

        enumerateDevices();

        return () => {
            stopStream();
        };
    }, [isOpen, selectedDeviceId, startStream, stopStream]);

    // Capture current frame from high-resolution video
    const handleSnap = () => {
        if (!videoRef.current) return;
        const video = videoRef.current;
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth || 1280;
        canvas.height = video.videoHeight || 720;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            if (!blob) return;
            const filename = `intraoral_capture_${Date.now()}.jpg`;
            const file = new File([blob], filename, { type: 'image/jpeg' });
            stopStream();
            onCapture(file, liveSharpness);
            onClose();
        }, 'image/jpeg', 0.95);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-stone-950/85 backdrop-blur-xs p-4 animate-in fade-in duration-200">
            <div className="relative w-full max-w-3xl border border-stone-300 dark:border-stone-800 bg-white dark:bg-stone-900 shadow-2xl p-6 font-sans">
                {/* Header */}
                <div className="flex items-center justify-between border-b border-stone-200 dark:border-stone-800 pb-3 mb-4">
                    <div className="flex items-center gap-2">
                        <Camera className="w-5 h-5 text-clinical-teal" />
                        <h2 className="font-serif text-lg text-stone-900 dark:text-stone-100 font-semibold tracking-wide">
                            Intraoral Camera & Hardware Optical Stream
                        </h2>
                    </div>
                    <button
                        type="button"
                        onClick={() => { stopStream(); onClose(); }}
                        className="p-1.5 text-stone-400 hover:text-stone-900 dark:hover:text-stone-100 transition-colors"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Device Selector Toolbar */}
                <div className="flex flex-wrap items-center justify-between gap-3 mb-3 font-mono text-xs">
                    <div className="flex items-center gap-2">
                        <span className="text-stone-500 uppercase text-[10px]">VIDEO SENSOR:</span>
                        <select
                            value={selectedDeviceId}
                            onChange={(e) => {
                                setSelectedDeviceId(e.target.value);
                                startStream(e.target.value);
                            }}
                            className="bg-stone-50 dark:bg-stone-950 border border-stone-300 dark:border-stone-700 px-2 py-1 text-xs text-stone-800 dark:text-stone-200 focus:outline-none focus:border-clinical-teal"
                        >
                            {devices.length > 0 ? (
                                devices.map((d, i) => (
                                    <option key={d.deviceId || i} value={d.deviceId}>
                                        {d.label || `Optical Input Device ${i + 1}`}
                                    </option>
                                ))
                            ) : (
                                <option value="">Default Optical Camera</option>
                            )}
                        </select>
                    </div>

                    <div className="flex items-center gap-2">
                        <span className="text-stone-500 uppercase text-[10px]">TARGET SITE:</span>
                        <span className="px-2 py-0.5 border border-clinical-teal/40 bg-teal-500/10 text-clinical-teal font-semibold">
                            {targetSite.toUpperCase()}
                        </span>
                    </div>
                </div>

                {/* Viewfinder Display */}
                <div className="relative aspect-[16/10] bg-stone-950 border border-stone-800 overflow-hidden flex items-center justify-center">
                    {errorMsg ? (
                        <div className="text-center p-6 max-w-md">
                            <VideoOff className="w-10 h-10 text-rose-500 mx-auto mb-3" />
                            <p className="font-mono text-xs text-rose-400 leading-relaxed mb-4">{errorMsg}</p>
                            <button
                                type="button"
                                onClick={() => startStream(selectedDeviceId)}
                                className="px-3 py-1.5 bg-stone-800 text-stone-200 text-xs font-mono uppercase hover:bg-stone-700 transition-colors inline-flex items-center gap-1.5"
                            >
                                <RefreshCw className="w-3.5 h-3.5" /> Retry Stream
                            </button>
                        </div>
                    ) : (
                        <>
                            <video
                                ref={videoRef}
                                playsInline
                                muted
                                className="w-full h-full object-contain"
                            />

                            {/* Center Crosshair Overlay */}
                            <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
                                <div className="relative w-36 h-36 border border-dashed border-teal-400/40 rounded-full flex items-center justify-center">
                                    <Crosshair className="w-8 h-8 text-clinical-teal/70 animate-pulse" />
                                    <span className="absolute -top-3 font-mono text-[8px] text-teal-300 bg-stone-950/80 px-1">
                                        ANATOMICAL FOCUS
                                    </span>
                                </div>
                            </div>

                            {/* Real-Time Optical HUD Telemetry */}
                            <div className="absolute top-2 left-2 flex items-center gap-2 bg-stone-950/80 backdrop-blur-xs border border-stone-800 px-2.5 py-1 font-mono text-[10px]">
                                <span className={`w-2 h-2 rounded-full ${isBlurry ? 'bg-amber-500 animate-ping' : 'bg-clinical-teal'}`}></span>
                                <span className="text-stone-300">SHARPNESS σ²:</span>
                                <span className={`font-bold ${isBlurry ? 'text-amber-400' : 'text-teal-400'}`}>
                                    {liveSharpness.toFixed(1)}
                                </span>
                                <span className="text-stone-500">| THRESHOLD: 50.0</span>
                            </div>

                            {/* Status Banner */}
                            <div className={`absolute bottom-2 inset-x-2 py-1.5 px-3 flex items-center justify-between font-mono text-xs backdrop-blur-xs border ${
                                isBlurry 
                                    ? 'bg-amber-950/85 border-amber-600/60 text-amber-200' 
                                    : 'bg-teal-950/85 border-teal-600/60 text-teal-200'
                            }`}>
                                <div className="flex items-center gap-2">
                                    {isBlurry ? (
                                        <>
                                            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                                            <span className="text-[11px]">MOTION BLUR DETECTED // STABILIZE PROBE FOR AUTO-GATE</span>
                                        </>
                                    ) : (
                                        <>
                                            <CheckCircle2 className="w-4 h-4 text-clinical-teal shrink-0" />
                                            <span className="text-[11px]">OPTICAL FOCUS LOCKED // READY FOR SHUTTER RELEASE</span>
                                        </>
                                    )}
                                </div>
                                <span className="text-[10px] opacity-75">1080p UVC STREAM</span>
                            </div>
                        </>
                    )}
                </div>

                {/* Footer Controls */}
                <div className="flex items-center justify-between mt-4 pt-3 border-t border-stone-200 dark:border-stone-800">
                    <button
                        type="button"
                        onClick={() => { stopStream(); onClose(); }}
                        className="px-4 py-2 border border-stone-300 dark:border-stone-700 text-stone-700 dark:text-stone-300 font-mono text-xs uppercase hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
                    >
                        Cancel
                    </button>

                    <div className="flex items-center gap-3">
                        <button
                            type="button"
                            disabled={!isStreaming}
                            onClick={handleSnap}
                            className={`px-6 py-2.5 font-mono text-xs uppercase font-semibold tracking-wider flex items-center gap-2 transition-all ${
                                !isStreaming 
                                    ? 'bg-stone-400 text-stone-200 cursor-not-allowed'
                                    : isBlurry
                                        ? 'bg-amber-600 text-white hover:bg-amber-500 shadow-md'
                                        : 'bg-clinical-teal text-white hover:bg-teal-600 shadow-lg'
                            }`}
                        >
                            <Camera className="w-4 h-4" />
                            <span>Capture Mucosal Frame</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default WebRTCIntraoralCameraModal;
