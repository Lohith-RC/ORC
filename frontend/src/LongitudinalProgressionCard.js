import React from 'react';
import { 
    Clock, 
    TrendingUp, 
    TrendingDown, 
    Minus, 
    AlertOctagon, 
    CheckCircle, 
    ShieldAlert,
    Calendar,
    Layers
} from 'lucide-react';

/**
 * LongitudinalProgressionCard
 * Displays serial growth velocity (mm²/day), elapsed interval, and overlaid
 * dual-contour comparison (baseline vs current) for longitudinal dysplasia surveillance.
 */
const LongitudinalProgressionCard = ({ trajectory }) => {
    if (!trajectory || !trajectory.has_prior) {
        return null;
    }

    const {
        prior_analysis_id,
        prior_timestamp,
        elapsed_days = 0,
        prior_diameter_mm = 0,
        current_diameter_mm = 0,
        delta_diameter_mm = 0,
        prior_surface_area_mm2 = 0,
        current_surface_area_mm2 = 0,
        delta_surface_area_mm2 = 0,
        percentage_change_area = 0,
        growth_velocity_mm2_per_day = 0,
        prior_border_irregularity = 1.0,
        current_border_irregularity = 1.0,
        delta_irregularity = 0,
        prior_contour_points = [],
        current_contour_points = [],
        trajectory_status,
        trajectory_status_display,
        clinical_directive
    } = trajectory;

    const isRapid = trajectory_status === 'RAPID_EXPANSION_CRITICAL';
    const isRegression = trajectory_status === 'REGRESSION_RESOLVING';
    const isIndolent = trajectory_status === 'INDOLENT_EXPANSION';

    const priorSvgPoints = (prior_contour_points || []).map(([x, y]) => `${x},${y}`).join(' ');
    const currentSvgPoints = (current_contour_points || []).map(([x, y]) => `${x},${y}`).join(' ');

    return (
        <div className={`border p-6 my-5 ${
            isRapid 
                ? 'border-rose-500/60 bg-rose-50/40 dark:bg-rose-950/20' 
                : isRegression 
                    ? 'border-teal-500/60 bg-teal-50/40 dark:bg-teal-950/20'
                    : 'border-stone-300 dark:border-stone-800 bg-stone-50/90 dark:bg-stone-900/60'
        }`}>
            {/* Header / Trajectory Ribbon */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-stone-200 dark:border-stone-800 font-mono text-xs">
                <div className="flex items-center gap-2">
                    {isRapid ? (
                        <AlertOctagon className="w-4 h-4 text-rose-600 animate-pulse" />
                    ) : isRegression ? (
                        <CheckCircle className="w-4 h-4 text-teal-600" />
                    ) : (
                        <Clock className="w-4 h-4 text-stone-500" />
                    )}
                    <span className="font-semibold uppercase tracking-wider text-stone-900 dark:text-stone-100">
                        LONGITUDINAL LESION GROWTH CALIBRATION
                    </span>
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-[10px] text-stone-400">INTERVAL:</span>
                    <span className="px-2 py-0.5 bg-stone-900 text-stone-100 text-[10px] font-bold">
                        {elapsed_days} DAYS ELAPSED
                    </span>
                </div>
            </div>

            {/* Trajectory Status Banner */}
            <div className="my-4">
                <span className={`inline-block font-mono text-[11px] px-3 py-1 font-bold uppercase tracking-wider ${
                    isRapid 
                        ? 'bg-rose-600 text-white' 
                        : isRegression 
                            ? 'bg-teal-700 text-white'
                            : isIndolent
                                ? 'bg-amber-600 text-white'
                                : 'bg-stone-800 text-stone-200'
                }`}>
                    {trajectory_status_display}
                </span>
                <p className="font-sans text-xs text-stone-700 dark:text-stone-300 mt-2 leading-relaxed">
                    {clinical_directive}
                </p>
            </div>

            {/* Serial Metrics Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 my-4 font-mono">
                {/* Delta Area */}
                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950/60">
                    <span className="text-[9px] text-stone-400 block uppercase">AREA DELTA (Δ)</span>
                    <div className="flex items-baseline gap-1 mt-0.5">
                        <span className={`text-base font-bold ${delta_surface_area_mm2 > 0 ? (isRapid ? 'text-rose-600' : 'text-amber-600') : 'text-teal-600'}`}>
                            {delta_surface_area_mm2 > 0 ? `+${delta_surface_area_mm2}` : delta_surface_area_mm2}
                        </span>
                        <span className="text-[10px] text-stone-500">mm²</span>
                    </div>
                    <span className="text-[10px] text-stone-500 block mt-0.5 font-sans">
                        {percentage_change_area > 0 ? `+${percentage_change_area}%` : `${percentage_change_area}%`}
                    </span>
                </div>

                {/* Growth Velocity */}
                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950/60">
                    <span className="text-[9px] text-stone-400 block uppercase">GROWTH VELOCITY</span>
                    <div className="flex items-baseline gap-1 mt-0.5">
                        <span className={`text-base font-bold ${growth_velocity_mm2_per_day > 0.35 ? 'text-rose-600' : 'text-stone-800 dark:text-stone-200'}`}>
                            {growth_velocity_mm2_per_day > 0 ? `+${growth_velocity_mm2_per_day}` : growth_velocity_mm2_per_day}
                        </span>
                        <span className="text-[10px] text-stone-500">mm²/day</span>
                    </div>
                    <span className="text-[9px] text-stone-400 block mt-0.5 font-sans">
                        Expansion rate
                    </span>
                </div>

                {/* Diameter Delta */}
                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950/60">
                    <span className="text-[9px] text-stone-400 block uppercase">DIAMETER DELTA</span>
                    <div className="flex items-baseline gap-1 mt-0.5">
                        <span className={`text-base font-bold ${delta_diameter_mm > 0 ? 'text-amber-600' : 'text-teal-600'}`}>
                            {delta_diameter_mm > 0 ? `+${delta_diameter_mm}` : delta_diameter_mm}
                        </span>
                        <span className="text-[10px] text-stone-500">mm</span>
                    </div>
                    <span className="text-[9px] text-stone-400 block mt-0.5 font-sans">
                        {prior_diameter_mm} → {current_diameter_mm} mm
                    </span>
                </div>

                {/* Border Compactness Delta */}
                <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950/60">
                    <span className="text-[9px] text-stone-400 block uppercase">IRREGULARITY DELTA</span>
                    <div className="flex items-baseline gap-1 mt-0.5">
                        <span className={`text-base font-bold ${delta_irregularity > 0.2 ? 'text-rose-600' : 'text-stone-800 dark:text-stone-200'}`}>
                            {delta_irregularity > 0 ? `+${delta_irregularity}` : delta_irregularity}
                        </span>
                    </div>
                    <span className="text-[9px] text-stone-400 block mt-0.5 font-sans">
                        {prior_border_irregularity} → {current_border_irregularity}
                    </span>
                </div>
            </div>

            {/* Overlaid Dual Contour Visualizer */}
            {prior_contour_points.length > 2 && current_contour_points.length > 2 && (
                <div className="mt-4 p-4 bg-stone-950 border border-stone-800 select-none">
                    <div className="flex items-center justify-between font-mono text-[10px] text-stone-400 pb-2 border-b border-stone-800 mb-2">
                        <span className="flex items-center gap-1.5 text-stone-200">
                            <Layers className="w-3.5 h-3.5 text-clinical-teal" />
                            DUAL-CONTOUR SPATIAL PROGRESSION OVERLAY
                        </span>
                        <div className="flex items-center gap-3">
                            <span className="flex items-center gap-1 text-amber-400">
                                <span className="w-3 h-0.5 border-b border-dashed border-amber-400 inline-block"></span>
                                Prior Baseline Margin
                            </span>
                            <span className="flex items-center gap-1 text-teal-400">
                                <span className="w-3 h-0.5 bg-teal-400 inline-block"></span>
                                Current Follow-up Margin
                            </span>
                        </div>
                    </div>

                    <div className="relative aspect-[21/9] w-full bg-stone-900 overflow-hidden flex items-center justify-center">
                        <svg viewBox="0 0 100 100" className="w-full h-full">
                            {/* Prior Contour (Dashed Amber) */}
                            <polygon
                                points={priorSvgPoints}
                                fill="rgba(245, 158, 11, 0.15)"
                                stroke="#f59e0b"
                                strokeWidth="0.8"
                                strokeDasharray="2 1.5"
                            />
                            {/* Current Contour (Solid Cyan/Teal) */}
                            <polygon
                                points={currentSvgPoints}
                                fill="rgba(20, 184, 166, 0.25)"
                                stroke="#14b8a6"
                                strokeWidth="1.0"
                            />
                        </svg>
                        <div className="absolute bottom-2 left-2 font-mono text-[9px] text-stone-500">
                            Prior: {prior_timestamp}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default LongitudinalProgressionCard;
