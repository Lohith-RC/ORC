import React from 'react';

export const SectionHeader = ({ title, subtitle, icon: Icon, badge }) => (
    <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
            {Icon && (
                <div className="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400">
                    <Icon className="w-5 h-5" />
                </div>
            )}
            <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {title}
                </h3>
                {subtitle && (
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                        {subtitle}
                    </p>
                )}
            </div>
        </div>
        {badge && (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 dark:bg-indigo-900/60 text-indigo-800 dark:text-indigo-300">
                {badge}
            </span>
        )}
    </div>
);

export default SectionHeader;
