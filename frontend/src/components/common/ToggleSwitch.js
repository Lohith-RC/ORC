import React from 'react';

export const ToggleSwitch = ({ id, label, description, checked, onChange, disabled = false }) => (
    <div className="flex items-center justify-between py-2">
        <div className="flex flex-col pr-4">
            <label htmlFor={id} className="text-sm font-medium text-gray-700 dark:text-gray-300 cursor-pointer">
                {label}
            </label>
            {description && (
                <span className="text-xs text-gray-500 dark:text-gray-400">
                    {description}
                </span>
            )}
        </div>
        <button
            id={id}
            type="button"
            role="switch"
            aria-checked={checked}
            disabled={disabled}
            onClick={() => !disabled && onChange(!checked)}
            className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 ${
                checked ? 'bg-indigo-600' : 'bg-gray-200 dark:bg-gray-700'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
            <span
                aria-hidden="true"
                className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    checked ? 'translate-x-5' : 'translate-x-0'
                }`}
            />
        </button>
    </div>
);

export default ToggleSwitch;
