import React from 'react';

export const RiskFactorToggle = ({ label, weight, active, onChange, note }) => {
    return (
        <div 
            onClick={() => onChange(!active)}
            className={`cursor-pointer select-none border p-3 flex items-center justify-between transition-all ${
                active 
                    ? 'border-clinical-teal bg-teal-50/50 dark:bg-teal-950/20 dark:border-teal-700' 
                    : 'border-stone-200 dark:border-stone-800 bg-stone-50/50 dark:bg-stone-900/30 hover:border-stone-300 dark:hover:border-stone-700'
            }`}
        >
            <div className="flex flex-col">
                <span className="text-xs font-mono font-medium text-stone-900 dark:text-stone-100">{label}</span>
                <span className="text-[10px] text-stone-400 font-mono mt-0.5">{note}</span>
            </div>
            <div className="flex items-center gap-2">
                <span className="font-mono text-[10px] text-clinical-teal dark:text-teal-400">{weight}</span>
                <div className={`w-9 h-5 rounded-full p-0.5 transition-colors ${active ? 'bg-clinical-teal' : 'bg-stone-300 dark:bg-stone-700'}`}>
                    <div className={`w-4 h-4 rounded-full bg-white transition-transform ${active ? 'translate-x-4' : 'translate-x-0'}`}></div>
                </div>
            </div>
        </div>
    );
};

export default RiskFactorToggle;
