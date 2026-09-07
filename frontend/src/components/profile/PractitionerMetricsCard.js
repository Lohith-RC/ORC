import React from 'react';
import { Activity, ShieldAlert, ShieldCheck, HelpCircle, BarChart3 } from 'lucide-react';

export const PractitionerMetricsCard = ({
    totalAnalyses,
    cancerCases,
    benignCases,
    uncertainCases,
    avgConfidence,
    flywheelMetrics
}) => {
    return (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-900/60 p-4">
                <div className="flex items-center justify-between text-stone-400 mb-2">
                    <span className="font-mono text-[10px] uppercase">TOTAL TRIAGED</span>
                    <Activity className="w-4 h-4 text-clinical-teal" />
                </div>
                <div className="text-2xl font-mono font-bold text-stone-900 dark:text-stone-100">{totalAnalyses}</div>
                <div className="text-[10px] text-stone-400 mt-1">Evaluated Specimens</div>
            </div>

            <div className="border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-900/60 p-4">
                <div className="flex items-center justify-between text-stone-400 mb-2">
                    <span className="font-mono text-[10px] uppercase">HIGH RISK (OSCC)</span>
                    <ShieldAlert className="w-4 h-4 text-red-500" />
                </div>
                <div className="text-2xl font-mono font-bold text-red-600 dark:text-red-400">{cancerCases}</div>
                <div className="text-[10px] text-stone-400 mt-1">Carcinoma Identified</div>
            </div>

            <div className="border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-900/60 p-4">
                <div className="flex items-center justify-between text-stone-400 mb-2">
                    <span className="font-mono text-[10px] uppercase">BENIGN / HEALTHY</span>
                    <ShieldCheck className="w-4 h-4 text-teal-600" />
                </div>
                <div className="text-2xl font-mono font-bold text-teal-600 dark:text-teal-400">{benignCases}</div>
                <div className="text-[10px] text-stone-400 mt-1">Non-Dysplastic Tissue</div>
            </div>

            <div className="border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-900/60 p-4">
                <div className="flex items-center justify-between text-stone-400 mb-2">
                    <span className="font-mono text-[10px] uppercase">EQUIVOCAL / UNCERTAIN</span>
                    <HelpCircle className="w-4 h-4 text-amber-500" />
                </div>
                <div className="text-2xl font-mono font-bold text-amber-600 dark:text-amber-400">{uncertainCases}</div>
                <div className="text-[10px] text-stone-400 mt-1">High Epistemic Variance</div>
            </div>

            <div className="col-span-2 md:col-span-1 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-900/60 p-4">
                <div className="flex items-center justify-between text-stone-400 mb-2">
                    <span className="font-mono text-[10px] uppercase">AVG CONFIDENCE</span>
                    <BarChart3 className="w-4 h-4 text-clinical-teal" />
                </div>
                <div className="text-2xl font-mono font-bold text-clinical-teal dark:text-teal-400">{avgConfidence}%</div>
                <div className="text-[10px] text-stone-400 mt-1">Ensemble Consensus</div>
            </div>
        </div>
    );
};

export default PractitionerMetricsCard;
