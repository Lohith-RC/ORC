import React, { useState } from 'react';
import { Eye, EyeOff, Crosshair, Sparkles, Ruler, AlertCircle } from 'lucide-react';

/**
 * LesionSegmentationViewer
 * Renders the specimen image with SVG spatial lesion contours,
 * center of mass reticle, and clinical morphology metrics (area mm², diameter mm, margin irregularity).
 */
const LesionSegmentationViewer = ({ imageSrc, telemetry, stagingReport }) => {
    const [showOverlay, setShowOverlay] = useState(true);

    if (!telemetry) return null;

    const {
        mask_detected,
        center_pct = [50, 50],
        diameter_mm = 0,
        surface_area_mm2 = 0,
        border_irregularity_score = 1.0,
        contour_points = [],
        optical_cross_polarized = false,
        vital_stain_present = false,
        vital_stain_abnormal = false
    } = telemetry;

    // Format SVG polygon points from percentage coordinates [x%, y%]
    const svgPoints = contour_points.map(([x, y]) => `${x},${y}`).join(' ');

    const isHighIrregularity = border_irregularity_score >= 1.45;

    return (
        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900/60 p-5 my-5">
            {/* Header / Protocol Status */}
            <div className="flex items-center justify-between font-mono text-[11px] pb-3 border-b border-stone-200 dark:border-stone-800 mb-4">
                <div className="flex items-center gap-2">
                    <span className="w-2 h-2 bg-clinical-teal dark:bg-teal-400 rounded-full animate-pulse"></span>
                    <span className="font-semibold text-stone-900 dark:text-stone-100 uppercase tracking-wider">
                        STAGE I // LESION SPATIAL SEGMENTATION
                    </span>
                </div>
                <button
                    onClick={() => setShowOverlay(!showOverlay)}
                    className="flex items-center gap-1.5 px-2.5 py-1 border border-stone-300 dark:border-stone-700 bg-white dark:bg-stone-800 text-stone-700 dark:text-stone-300 hover:text-clinical-teal text-[10px] uppercase font-mono transition-colors"
                >
                    {showOverlay ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                    <span>{showOverlay ? 'Hide Margin Overlay' : 'Show Margin Overlay'}</span>
                </button>
            </div>

            {/* Visual Viewport with SVG Contour Overlay */}
            <div className="relative aspect-video w-full overflow-hidden bg-stone-950 border border-stone-300 dark:border-stone-700 select-none">
                {imageSrc && (
                    <img
                        src={imageSrc}
                        alt="Clinical Specimen"
                        className="w-full h-full object-contain"
                    />
                )}

                {/* SVG Margin Annotation Overlay */}
                {showOverlay && (
                    <svg
                        viewBox="0 0 100 100"
                        preserveAspectRatio="none"
                        className="absolute inset-0 w-full h-full pointer-events-none"
                    >
                        <defs>
                            {/* Glow filter for active margin */}
                            <filter id="tealGlow" x="-20%" y="-20%" width="140%" height="140%">
                                <feDropShadow dx="0" dy="0" stdDeviation="0.8" floodColor="#0d9488" floodOpacity="0.8" />
                            </filter>
                        </defs>

                        {/* Segmented Lesion Boundary */}
                        {contour_points.length > 2 && (
                            <polygon
                                points={svgPoints}
                                fill="rgba(13, 148, 136, 0.22)"
                                stroke="#14b8a6"
                                strokeWidth="0.8"
                                strokeDasharray={mask_detected ? 'none' : '1.5 1.5'}
                                filter="url(#tealGlow)"
                            />
                        )}

                        {/* Center of Mass Reticle */}
                        <g transform={`translate(${center_pct[0]}, ${center_pct[1]})`}>
                            <circle r="1.5" fill="none" stroke="#2dd4bf" strokeWidth="0.5" />
                            <circle r="0.5" fill="#f43f5e" />
                            <line x1="-3" y1="0" x2="3" y2="0" stroke="#2dd4bf" strokeWidth="0.4" />
                            <line x1="0" y1="-3" x2="0" y2="3" stroke="#2dd4bf" strokeWidth="0.4" />
                        </g>
                    </svg>
                )}

                {/* Viewport Floating Badges */}
                <div className="absolute top-2 left-2 flex flex-col gap-1 pointer-events-none">
                    <span className="px-2 py-0.5 bg-stone-900/80 backdrop-blur-md text-[9px] font-mono text-teal-300 border border-teal-500/30">
                        {mask_detected ? 'MARGIN: DELINEATED' : 'MARGIN: SYNTHETIC ROI'}
                    </span>
                    {optical_cross_polarized && (
                        <span className="px-2 py-0.5 bg-stone-900/80 backdrop-blur-md text-[9px] font-mono text-indigo-300 border border-indigo-500/30">
                            OPTICAL: CROSS-POLARIZED
                        </span>
                    )}
                </div>

                <div className="absolute bottom-2 right-2 px-2 py-1 bg-stone-900/85 backdrop-blur-md text-[9px] font-mono text-stone-300 flex items-center gap-2 pointer-events-none">
                    <Ruler className="w-3 h-3 text-clinical-teal" />
                    <span>CALIBRATED SCALE (50MM SPACER)</span>
                </div>
            </div>

            {/* Spatial Morphology Metric Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950/60 font-mono">
                    <div className="text-[9px] text-stone-400 uppercase">CALIBRATED DIAMETER</div>
                    <div className="text-base font-bold text-stone-900 dark:text-stone-100 mt-0.5">
                        {diameter_mm.toFixed(1)} <span className="text-[10px] text-stone-500 font-normal">mm</span>
                    </div>
                    <div className="text-[9px] text-clinical-teal mt-0.5 font-sans">
                        {diameter_mm <= 20 ? 'AJCC cT1 (≤20mm)' : diameter_mm <= 40 ? 'AJCC cT2 (20-40mm)' : 'AJCC cT3 (>40mm)'}
                    </div>
                </div>

                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950/60 font-mono">
                    <div className="text-[9px] text-stone-400 uppercase">SURFACE AREA</div>
                    <div className="text-base font-bold text-stone-900 dark:text-stone-100 mt-0.5">
                        {surface_area_mm2.toFixed(1)} <span className="text-[10px] text-stone-500 font-normal">mm²</span>
                    </div>
                    <div className="text-[9px] text-stone-500 mt-0.5 font-sans">
                        Mucosal coverage
                    </div>
                </div>

                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950/60 font-mono">
                    <div className="text-[9px] text-stone-400 uppercase">BORDER IRREGULARITY</div>
                    <div className={`text-base font-bold mt-0.5 ${isHighIrregularity ? 'text-amber-500' : 'text-emerald-500'}`}>
                        {border_irregularity_score.toFixed(2)}
                    </div>
                    <div className="text-[9px] text-stone-500 mt-0.5 font-sans">
                        {isHighIrregularity ? 'Infiltrative / Jagged' : 'Regular / Circumscribed'}
                    </div>
                </div>

                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950/60 font-mono">
                    <div className="text-[9px] text-stone-400 uppercase">VITAL STAIN RETENTION</div>
                    <div className={`text-base font-bold mt-0.5 ${vital_stain_present ? (vital_stain_abnormal ? 'text-rose-500' : 'text-emerald-500') : 'text-stone-400'}`}>
                        {!vital_stain_present ? 'N/A' : (vital_stain_abnormal ? 'POSITIVE' : 'NEGATIVE')}
                    </div>
                    <div className="text-[9px] text-stone-500 mt-0.5 font-sans">
                        {!vital_stain_present ? 'No dye channel' : (vital_stain_abnormal ? 'Dysplastic uptake' : 'Normal clearance')}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LesionSegmentationViewer;
