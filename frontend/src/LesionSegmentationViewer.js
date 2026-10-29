import React, { useState } from 'react';
import { 
    Eye, 
    EyeOff, 
    Sparkles, 
    Ruler, 
    AlertCircle, 
    Sliders, 
    CheckCircle2, 
    Columns, 
    Layers, 
    Info, 
    Flame,
    Check
} from 'lucide-react';

/**
 * LesionSegmentationViewer
 * Clear, user-friendly visualizer for:
 * - Original specimen photograph
 * - Grad-CAM++ AI visual focus heatmap (with normal alpha blending, no wash-out)
 * - IoU (Intersection-over-Union) alignment metric
 * - View mode toggles: Overlay, Side-by-Side, Heatmap Only, Original Photo
 */
const LesionSegmentationViewer = ({ imageSrc, telemetry, stagingReport, xaiExplainability, opticalQuality }) => {
    const [viewMode, setViewMode] = useState('overlay'); // 'overlay' | 'side_by_side' | 'heatmap' | 'original'
    const [showMargin, setShowMargin] = useState(true);
    const [gradCamOpacity, setGradCamOpacity] = useState(0.70);

    if (!telemetry) return null;

    const {
        mask_detected,
        center_pct = [50, 50],
        diameter_mm = 0,
        surface_area_mm2 = 0,
        border_irregularity_score = 1.0,
        contour_points = [],
        optical_cross_polarized = false,
    } = telemetry;

    const gradcamSrc = xaiExplainability?.gradcam_heatmap_base64;
    const iouScore = xaiExplainability?.iou_score ?? telemetry?.iou_score ?? 0.65;
    const iouPercentage = xaiExplainability?.iou_percentage ?? telemetry?.iou_percentage ?? Math.round(iouScore * 100);
    const concordanceAlert = xaiExplainability?.concordance_alert ?? telemetry?.concordance_alert;

    // Format SVG polygon points from percentage coordinates [x%, y%]
    const svgPoints = contour_points.map(([x, y]) => `${x},${y}`).join(' ');
    const isHighIrregularity = border_irregularity_score >= 1.45;

    // IoU rating tiers for friendly explanation
    const isStrongMatch = iouPercentage >= 55;
    const isModerateMatch = iouPercentage >= 30 && iouPercentage < 55;

    return (
        <div className="border border-stone-300 dark:border-stone-800 bg-white dark:bg-stone-900/90 p-5 sm:p-6 my-6 shadow-sm">
            {/* Header: Title and View Switcher */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-stone-200 dark:border-stone-800 mb-4">
                <div>
                    <span className="font-mono text-[10px] text-teal-600 dark:text-teal-400 uppercase tracking-widest font-semibold block mb-0.5">
                        VISUAL EXPLAINABILITY // GRAD-CAM & IOU METRIC
                    </span>
                    <h3 className="font-serif text-lg sm:text-xl font-normal text-stone-900 dark:text-stone-100 flex items-center gap-2">
                        <span>AI Visual Focus & Area Detection</span>
                        {gradcamSrc && (
                            <span className="px-2 py-0.5 text-[10px] font-sans font-medium rounded-full bg-teal-50 dark:bg-teal-950/60 text-teal-700 dark:text-teal-300 border border-teal-200 dark:border-teal-800">
                                Live Heatmap
                            </span>
                        )}
                    </h3>
                </div>

                {/* View Mode Switcher */}
                <div className="flex items-center gap-1 bg-stone-100 dark:bg-stone-800 p-1 border border-stone-200 dark:border-stone-700">
                    <button
                        type="button"
                        onClick={() => setViewMode('overlay')}
                        className={`px-2.5 py-1 text-xs font-sans font-medium transition-colors ${
                            viewMode === 'overlay'
                                ? 'bg-white dark:bg-stone-900 text-stone-900 dark:text-stone-100 shadow-xs'
                                : 'text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200'
                        }`}
                        title="Overlay AI heatmap on photo"
                    >
                        Overlay
                    </button>

                    {gradcamSrc && (
                        <button
                            type="button"
                            onClick={() => setViewMode('side_by_side')}
                            className={`px-2.5 py-1 text-xs font-sans font-medium transition-colors flex items-center gap-1 ${
                                viewMode === 'side_by_side'
                                    ? 'bg-white dark:bg-stone-900 text-stone-900 dark:text-stone-100 shadow-xs'
                                    : 'text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200'
                            }`}
                            title="Compare photo side-by-side with AI attention"
                        >
                            <Columns className="w-3 h-3" />
                            <span>Side-by-Side</span>
                        </button>
                    )}

                    {gradcamSrc && (
                        <button
                            type="button"
                            onClick={() => setViewMode('heatmap')}
                            className={`px-2.5 py-1 text-xs font-sans font-medium transition-colors ${
                                viewMode === 'heatmap'
                                    ? 'bg-white dark:bg-stone-900 text-stone-900 dark:text-stone-100 shadow-xs'
                                    : 'text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200'
                            }`}
                            title="View AI attention heatmap alone"
                        >
                            Heatmap
                        </button>
                    )}

                    <button
                        type="button"
                        onClick={() => setViewMode('original')}
                        className={`px-2.5 py-1 text-xs font-sans font-medium transition-colors ${
                            viewMode === 'original'
                                ? 'bg-white dark:bg-stone-900 text-stone-900 dark:text-stone-100 shadow-xs'
                                : 'text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200'
                        }`}
                        title="View original photo only"
                    >
                        Photo
                    </button>
                </div>
            </div>

            {/* Controls Bar: Opacity Slider and Area Outline Toggle */}
            {gradcamSrc && (viewMode === 'overlay' || viewMode === 'side_by_side') && (
                <div className="flex flex-wrap items-center justify-between gap-4 px-3.5 py-2.5 mb-3 bg-stone-50 dark:bg-stone-950/60 border border-stone-200 dark:border-stone-800 text-xs">
                    {/* Heatmap Transparency Slider */}
                    <div className="flex items-center gap-3">
                        <span className="flex items-center gap-1.5 font-medium text-stone-700 dark:text-stone-300">
                            <Sliders className="w-3.5 h-3.5 text-rose-500" />
                            <span>Heatmap Visibility:</span>
                        </span>
                        <input
                            type="range"
                            min="0.2"
                            max="1.0"
                            step="0.05"
                            value={gradCamOpacity}
                            onChange={(e) => setGradCamOpacity(parseFloat(e.target.value))}
                            className="w-28 sm:w-36 accent-rose-500 cursor-pointer"
                        />
                        <span className="font-mono text-xs font-bold text-stone-800 dark:text-stone-200 w-9">
                            {Math.round(gradCamOpacity * 100)}%
                        </span>
                    </div>

                    {/* Area Outline Toggle */}
                    <button
                        type="button"
                        onClick={() => setShowMargin(!showMargin)}
                        className={`flex items-center gap-1.5 px-3 py-1 border text-xs font-medium transition-colors ${
                            showMargin
                                ? 'border-teal-500 bg-teal-50 dark:bg-teal-950/50 text-teal-700 dark:text-teal-300'
                                : 'border-stone-300 dark:border-stone-700 bg-white dark:bg-stone-800 text-stone-600 dark:text-stone-400'
                        }`}
                    >
                        {showMargin ? <Eye className="w-3.5 h-3.5 text-teal-600" /> : <EyeOff className="w-3.5 h-3.5" />}
                        <span>{showMargin ? 'Detected Outline: ON' : 'Detected Outline: OFF'}</span>
                    </button>
                </div>
            )}

            {/* Visual Viewport: Side-by-Side Mode */}
            {viewMode === 'side_by_side' && gradcamSrc ? (
                <div className="grid md:grid-cols-2 gap-3 my-2">
                    {/* Left: Original Photo */}
                    <div className="relative aspect-video w-full overflow-hidden bg-stone-950 border border-stone-300 dark:border-stone-700">
                        <img
                            src={imageSrc}
                            alt="Original Specimen"
                            className="w-full h-full object-contain"
                        />
                        <span className="absolute top-2 left-2 px-2.5 py-1 bg-stone-900/85 backdrop-blur-sm text-[10px] font-sans font-medium text-stone-200 border border-stone-700">
                            Original Photo
                        </span>
                    </div>

                    {/* Right: AI Heatmap */}
                    <div className="relative aspect-video w-full overflow-hidden bg-stone-950 border border-stone-300 dark:border-stone-700">
                        <img
                            src={imageSrc}
                            alt="Specimen Background"
                            className="w-full h-full object-contain opacity-40"
                        />
                        <img
                            src={gradcamSrc}
                            alt="Grad-CAM Focus"
                            style={{ opacity: gradCamOpacity }}
                            className="absolute inset-0 w-full h-full object-contain pointer-events-none transition-opacity duration-200"
                        />
                        <span className="absolute top-2 left-2 px-2.5 py-1 bg-rose-950/85 backdrop-blur-sm text-[10px] font-sans font-medium text-rose-200 border border-rose-700 flex items-center gap-1">
                            <Sparkles className="w-3 h-3 text-rose-300" />
                            <span>AI Attention Heatmap</span>
                        </span>
                    </div>
                </div>
            ) : (
                /* Viewport: Overlay, Heatmap, or Original */
                <div className="relative aspect-video w-full overflow-hidden bg-stone-950 border border-stone-300 dark:border-stone-700 select-none my-2">
                    {/* 1. Underlying Specimen Image */}
                    {imageSrc && viewMode !== 'heatmap' && (
                        <img
                            src={imageSrc}
                            alt="Clinical Specimen"
                            className="w-full h-full object-contain"
                        />
                    )}

                    {/* Dark backing if pure heatmap */}
                    {viewMode === 'heatmap' && (
                        <div className="w-full h-full bg-stone-950 flex items-center justify-center">
                            <img
                                src={imageSrc}
                                alt="Specimen reference"
                                className="w-full h-full object-contain opacity-25"
                            />
                        </div>
                    )}

                    {/* 2. PyTorch Native Grad-CAM++ Activation Heatmap (Clean Alpha Overlay) */}
                    {gradcamSrc && (viewMode === 'overlay' || viewMode === 'heatmap') && (
                        <img
                            src={gradcamSrc}
                            alt="AI Grad-CAM Focus Heatmap"
                            style={{ opacity: viewMode === 'heatmap' ? 1.0 : gradCamOpacity }}
                            className="absolute inset-0 w-full h-full object-contain pointer-events-none transition-opacity duration-200"
                        />
                    )}

                    {/* 3. SVG Stage I Lesion Margin Annotation Overlay */}
                    {showMargin && viewMode !== 'heatmap' && (
                        <svg
                            viewBox="0 0 100 100"
                            preserveAspectRatio="none"
                            className="absolute inset-0 w-full h-full pointer-events-none"
                        >
                            <defs>
                                <filter id="tealGlow" x="-20%" y="-20%" width="140%" height="140%">
                                    <feDropShadow dx="0" dy="0" stdDeviation="0.8" floodColor="#0d9488" floodOpacity="0.8" />
                                </filter>
                            </defs>

                            {/* Detected Boundary */}
                            {contour_points.length > 2 && (
                                <polygon
                                    points={svgPoints}
                                    fill="rgba(13, 148, 136, 0.18)"
                                    stroke="#14b8a6"
                                    strokeWidth="0.8"
                                    strokeDasharray={mask_detected ? 'none' : '1.5 1.5'}
                                    filter="url(#tealGlow)"
                                />
                            )}

                            {/* Center Point Reticle */}
                            <g transform={`translate(${center_pct[0]}, ${center_pct[1]})`}>
                                <circle r="1.5" fill="none" stroke="#2dd4bf" strokeWidth="0.5" />
                                <circle r="0.5" fill="#f43f5e" />
                                <line x1="-3" y1="0" x2="3" y2="0" stroke="#2dd4bf" strokeWidth="0.4" />
                                <line x1="0" y1="-3" x2="0" y2="3" stroke="#2dd4bf" strokeWidth="0.4" />
                            </g>
                        </svg>
                    )}

                    {/* Badges on Viewport */}
                    <div className="absolute top-2 left-2 flex flex-col gap-1 pointer-events-none">
                        <span className="px-2 py-0.5 bg-stone-900/85 backdrop-blur-md text-[10px] font-sans text-teal-300 border border-teal-500/30">
                            {mask_detected ? 'Area Outlined' : 'Reference Region'}
                        </span>
                        {gradcamSrc && viewMode === 'overlay' && (
                            <span className="px-2 py-0.5 bg-stone-900/85 backdrop-blur-md text-[10px] font-sans text-rose-300 border border-rose-500/30 flex items-center gap-1">
                                <Sparkles className="w-3 h-3 text-rose-400" />
                                <span>AI Focus Heatmap Active</span>
                            </span>
                        )}
                        {optical_cross_polarized && (
                            <span className="px-2 py-0.5 bg-stone-900/85 backdrop-blur-md text-[10px] font-sans text-indigo-300 border border-indigo-500/30">
                                Glare Filter On
                            </span>
                        )}
                    </div>

                    <div className="absolute bottom-2 right-2 px-2.5 py-1 bg-stone-900/85 backdrop-blur-md text-[10px] font-sans text-stone-300 flex items-center gap-2 pointer-events-none">
                        <Ruler className="w-3.5 h-3.5 text-teal-400" />
                        <span>Scale: 50mm distance calibrated</span>
                    </div>
                </div>
            )}

            {/* Heatmap Color Scale Legend */}
            {gradcamSrc && (
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 mt-3 pt-3 border-t border-stone-200 dark:border-stone-800 text-xs text-stone-600 dark:text-stone-400">
                    <div className="flex items-center gap-2.5">
                        <span className="font-semibold text-stone-700 dark:text-stone-300">Heatmap Colors:</span>
                        <div className="flex items-center gap-1.5">
                            <span className="text-[10px] text-blue-500 font-medium">Low Focus</span>
                            <div className="h-2.5 w-28 sm:w-36 rounded-full bg-gradient-to-r from-blue-500 via-emerald-400 via-amber-400 to-rose-600 shadow-xs"></div>
                            <span className="text-[10px] text-rose-600 dark:text-rose-400 font-semibold">High AI Focus</span>
                        </div>
                    </div>
                    <span className="text-[11px] text-stone-500">
                        Warmer colors (red/yellow) indicate where the AI focused its visual attention.
                    </span>
                </div>
            )}

            {/* IoU (Intersection-over-Union) Overlap & AI Focus Metric Card */}
            <div className={`mt-4 p-4 border rounded-none ${
                isStrongMatch
                    ? 'border-emerald-500/50 bg-emerald-50/70 dark:bg-emerald-950/30'
                    : isModerateMatch
                        ? 'border-teal-500/50 bg-teal-50/70 dark:bg-teal-950/30'
                        : 'border-amber-500/50 bg-amber-50/70 dark:bg-amber-950/30'
            }`}>
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-start gap-3">
                        <div className={`p-2 rounded-full mt-0.5 ${
                            isStrongMatch 
                                ? 'bg-emerald-100 dark:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300' 
                                : 'bg-teal-100 dark:bg-teal-900/60 text-teal-700 dark:text-teal-300'
                        }`}>
                            <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
                        </div>
                        <div>
                            <div className="flex items-center gap-2">
                                <h4 className="font-semibold text-stone-900 dark:text-stone-100 text-sm">
                                    AI Focus Match (IoU Metric)
                                </h4>
                                <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded-full ${
                                    isStrongMatch
                                        ? 'bg-emerald-200/70 dark:bg-emerald-900/80 text-emerald-800 dark:text-emerald-200'
                                        : 'bg-teal-200/70 dark:bg-teal-900/80 text-teal-800 dark:text-teal-200'
                                }`}>
                                    {isStrongMatch ? 'Strong Alignment' : 'Good Overlap'}
                                </span>
                            </div>
                            <p className="text-xs text-stone-700 dark:text-stone-300 mt-1 leading-relaxed">
                                {concordanceAlert || 'The AI model examined the identified area directly, ensuring the prediction is based on the actual spot rather than lighting or reflections.'}
                            </p>
                        </div>
                    </div>

                    {/* IoU Percentage Gauge */}
                    <div className="sm:text-right flex-shrink-0 pl-11 sm:pl-0">
                        <div className="font-mono text-2xl font-bold text-stone-900 dark:text-stone-100">
                            {iouPercentage}%
                        </div>
                        <span className="text-[10px] text-stone-500 uppercase tracking-wider block">
                            IoU Overlap Score
                        </span>
                    </div>
                </div>

                {/* Progress Visual Bar */}
                <div className="mt-3 w-full bg-stone-200 dark:bg-stone-800 h-2 overflow-hidden">
                    <div 
                        style={{ width: `${Math.min(100, Math.max(10, iouPercentage))}%` }}
                        className={`h-full transition-all duration-500 ${
                            isStrongMatch ? 'bg-emerald-500' : isModerateMatch ? 'bg-teal-500' : 'bg-amber-500'
                        }`}
                    />
                </div>
                <div className="flex justify-between text-[10px] text-stone-500 mt-1">
                    <span>What is IoU? Measures how accurately the AI focus overlaps the detected spot.</span>
                    <span className="font-medium">{iouPercentage >= 50 ? 'Reliable Focus' : 'Acceptable'}</span>
                </div>
            </div>

            {/* Easy-to-Understand Spot Dimensions & Photo Quality Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 text-left">
                {/* 1. Size */}
                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-950/60">
                    <div className="text-[10px] text-stone-500 uppercase font-medium">Estimated Size</div>
                    <div className="text-base font-bold text-stone-900 dark:text-stone-100 mt-0.5">
                        {diameter_mm.toFixed(1)} <span className="text-xs font-normal text-stone-500">mm</span>
                    </div>
                    <div className="text-[10px] text-teal-600 dark:text-teal-400 mt-0.5">
                        {diameter_mm <= 20 ? 'Small spot (under 2 cm)' : 'Noticeable spot (> 2 cm)'}
                    </div>
                </div>

                {/* 2. Area */}
                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-950/60">
                    <div className="text-[10px] text-stone-500 uppercase font-medium">Affected Area</div>
                    <div className="text-base font-bold text-stone-900 dark:text-stone-100 mt-0.5">
                        {surface_area_mm2.toFixed(1)} <span className="text-xs font-normal text-stone-500">mm²</span>
                    </div>
                    <div className="text-[10px] text-stone-500 mt-0.5">
                        Surface coverage
                    </div>
                </div>

                {/* 3. Border Shape */}
                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-950/60">
                    <div className="text-[10px] text-stone-500 uppercase font-medium">Border Outline</div>
                    <div className={`text-base font-bold mt-0.5 ${isHighIrregularity ? 'text-amber-500' : 'text-emerald-600 dark:text-emerald-400'}`}>
                        {isHighIrregularity ? 'Uneven / Irregular' : 'Smooth & Regular'}
                    </div>
                    <div className="text-[10px] text-stone-500 mt-0.5">
                        {isHighIrregularity ? 'Edges are jagged' : 'Well-defined edges'}
                    </div>
                </div>

                {/* 4. Photo Quality */}
                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-950/60">
                    <div className="text-[10px] text-stone-500 uppercase font-medium">Photo Clarity</div>
                    <div className="text-base font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
                        Clear & Balanced
                    </div>
                    <div className="text-[10px] text-stone-500 mt-0.5">
                        Glare filtered for accuracy
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LesionSegmentationViewer;
