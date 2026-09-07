import React from 'react';

const BADGE_STYLES = {
    cancer: 'bg-rose-100 text-rose-800 border-rose-200 dark:bg-rose-950/60 dark:text-rose-300 dark:border-rose-800/50',
    non_cancer: 'bg-emerald-100 text-emerald-800 border-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800/50',
    uncertain: 'bg-amber-100 text-amber-800 border-amber-200 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800/50',
    high: 'bg-red-100 text-red-800 border-red-200 dark:bg-red-950/60 dark:text-red-300 dark:border-red-800/50',
    moderate: 'bg-amber-100 text-amber-800 border-amber-200 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800/50',
    low: 'bg-emerald-100 text-emerald-800 border-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800/50',
    default: 'bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700'
};

const LABELS = {
    cancer: 'High Risk / Malignant',
    non_cancer: 'Benign / Non-Cancerous',
    uncertain: 'Equivocal / Inconclusive',
    high: 'High Risk',
    moderate: 'Moderate Risk',
    low: 'Low Risk'
};

export const StatusBadge = ({ type, label, size = 'md' }) => {
    const key = (type || '').toLowerCase();
    const style = BADGE_STYLES[key] || BADGE_STYLES.default;
    const text = label || LABELS[key] || type;

    const sizeClasses = {
        sm: 'px-2 py-0.5 text-xs',
        md: 'px-2.5 py-1 text-xs',
        lg: 'px-3 py-1.5 text-sm'
    }[size] || 'px-2.5 py-1 text-xs';

    return (
        <span className={`inline-flex items-center font-semibold rounded-full border ${sizeClasses} ${style}`}>
            {text}
        </span>
    );
};

export default StatusBadge;
