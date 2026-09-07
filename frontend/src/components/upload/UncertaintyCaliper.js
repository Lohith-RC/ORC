import React from 'react';

export const UncertaintyCaliper = ({ confidence, uncertainty, prediction }) => {
    const confPct = Math.min(100, Math.max(0, confidence * 100));
    const bandWidth = Math.min(25, Math.max(4, Math.sqrt(uncertainty) * 100));
    const leftBound = Math.max(0, confPct - bandWidth / 2);
    const rightBound = Math.min(100, confPct + bandWidth / 2);
    const isUncertain = uncertainty > 0.015;

    return (
        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50 dark:bg-stone-900/70 p-5 rounded-none my-4">
            <div className="flex items-center justify-between font-mono text-[11px] mb-2 uppercase text-stone-500">
                <span>EPISTEMIC UNCERTAINTY CALIPER</span>
                <span className={isUncertain ? 'text-amber-500 font-bold' : 'text-clinical-teal dark:text-teal-400'}>
                    σ² = {uncertainty.toFixed(5)} ({isUncertain ? 'HIGH VARIANCE' : 'STABLE CONSENSUS'})
                </span>
            </div>

            {/* Ruler Scale */}
            <div className="relative h-9 bg-stone-200/80 dark:bg-stone-800/80 rounded-none overflow-hidden my-3 border border-stone-300/80 dark:border-stone-700">
                <div className="absolute inset-0 flex justify-between px-2 items-end pb-1 pointer-events-none opacity-40 font-mono text-[8px]">
                    <span>0%</span>
                    <span>25%</span>
                    <span>50%</span>
                    <span>75%</span>
                    <span>100%</span>
                </div>

                {/* Uncertainty Range Band */}
                <div 
                    style={{ left: `${leftBound}%`, width: `${bandWidth}%` }}
                    className={`absolute top-0 bottom-0 ${isUncertain ? 'bg-amber-400/30 dark:bg-amber-400/20' : 'bg-clinical-teal/25 dark:bg-teal-400/20'} border-x-2 ${isUncertain ? 'border-amber-500' : 'border-clinical-teal'}`}
                />

                {/* Mean Confidence Indicator Point */}
                <div 
                    style={{ left: `${confPct}%` }}
                    className="absolute top-0 bottom-0 w-1 bg-stone-900 dark:bg-white z-10 -ml-0.5"
                >
                    <div className="w-2.5 h-2.5 bg-stone-900 dark:bg-white rounded-full -ml-[3px] -mt-1 shadow-sm"></div>
                </div>
            </div>

            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 pt-1">
                <span>LOWER BOUND: {leftBound.toFixed(1)}%</span>
                <span className="font-semibold text-stone-800 dark:text-stone-200">POINT ESTIMATE: {confPct.toFixed(1)}%</span>
                <span>UPPER BOUND: {rightBound.toFixed(1)}%</span>
            </div>
        </div>
    );
};

export default UncertaintyCaliper;
