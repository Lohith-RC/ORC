import React, { useState } from 'react';
import { Crosshair, CheckCircle2 } from 'lucide-react';

export const ORAL_SITES = [
    {
        id: 'lateral_tongue',
        label: 'Lateral Tongue (Border)',
        shortLabel: 'Lateral Tongue',
        riskTier: 'HIGH ONCOLOGICAL RISK',
        riskColor: 'text-rose-600 dark:text-rose-400',
        badgeBg: 'bg-rose-500/15 border-rose-500/40 text-rose-700 dark:text-rose-300',
        pathologyNote: 'High incidence of early occult cervical lymph node metastasis. Aggressive submucosal infiltration.',
        coords: 'x: 35-65%, y: 52-68%'
    },
    {
        id: 'floor_of_mouth',
        label: 'Floor of Mouth (Sublingual)',
        shortLabel: 'Floor of Mouth',
        riskTier: 'HIGH ONCOLOGICAL RISK',
        riskColor: 'text-rose-600 dark:text-rose-400',
        badgeBg: 'bg-rose-500/15 border-rose-500/40 text-rose-700 dark:text-rose-300',
        pathologyNote: 'Thin non-keratinized epithelium permits rapid invasion into mylohyoid and deep submandibular spaces.',
        coords: 'x: 40-60%, y: 72-82%'
    },
    {
        id: 'buccal_mucosa',
        label: 'Buccal Mucosa (Cheek Lining)',
        shortLabel: 'Buccal Mucosa',
        riskTier: 'ELEVATED WITH BETEL/TOBACCO',
        riskColor: 'text-amber-600 dark:text-amber-400',
        badgeBg: 'bg-amber-500/15 border-amber-500/40 text-amber-700 dark:text-amber-300',
        pathologyNote: 'Primary site of Oral Submucous Fibrosis (OSF) and verrucous carcinoma in habit-associated regions.',
        coords: 'x: 10-25% & 75-90%, y: 40-70%'
    },
    {
        id: 'gingiva',
        label: 'Gingiva / Retromolar Trigone',
        shortLabel: 'Gingiva / Trigone',
        riskTier: 'ELEVATED (BONE INFILTRATION)',
        riskColor: 'text-amber-600 dark:text-amber-400',
        badgeBg: 'bg-amber-500/15 border-amber-500/40 text-amber-700 dark:text-amber-300',
        pathologyNote: 'Close proximity to cortical alveolar bone can lead to early osteolytic invasion requiring mandibulectomy.',
        coords: 'x: 20-80%, y: 78-90%'
    },
    {
        id: 'dorsal_tongue',
        label: 'Dorsal Tongue (Upper Surface)',
        shortLabel: 'Dorsal Tongue',
        riskTier: 'STANDARD RISK',
        riskColor: 'text-teal-600 dark:text-teal-400',
        badgeBg: 'bg-teal-500/15 border-teal-500/40 text-teal-700 dark:text-teal-300',
        pathologyNote: 'Thick keratinized filiform papillae provide mechanical barrier; lower primary carcinoma incidence.',
        coords: 'x: 42-58%, y: 45-62%'
    },
    {
        id: 'soft_palate',
        label: 'Soft Palate / Oropharyngeal Junction',
        shortLabel: 'Soft Palate',
        riskTier: 'HIGH RISK (HPV ASSOCIATION)',
        riskColor: 'text-rose-600 dark:text-rose-400',
        badgeBg: 'bg-rose-500/15 border-rose-500/40 text-rose-700 dark:text-rose-300',
        pathologyNote: 'Frequently linked to High-Risk Human Papillomavirus (HPV-16/18) with non-keratinizing basaloid morphology.',
        coords: 'x: 40-60%, y: 22-34%'
    },
    {
        id: 'hard_palate',
        label: 'Hard Palate (Vault)',
        shortLabel: 'Hard Palate',
        riskTier: 'STANDARD RISK',
        riskColor: 'text-teal-600 dark:text-teal-400',
        badgeBg: 'bg-teal-500/15 border-teal-500/40 text-teal-700 dark:text-teal-300',
        pathologyNote: 'Keratinized mucosa firmly bound to periosteum; uncommon site for primary OSCC except in reverse smokers.',
        coords: 'x: 35-65%, y: 12-25%'
    },
    {
        id: 'lip',
        label: 'Labial Mucosa / Vermilion Border',
        shortLabel: 'Labial / Lip',
        riskTier: 'SOLAR / UV ACTINIC RISK',
        riskColor: 'text-amber-600 dark:text-amber-400',
        badgeBg: 'bg-amber-500/15 border-amber-500/40 text-amber-700 dark:text-amber-300',
        pathologyNote: 'Actinic cheilitis predilection; lower lip SCC has high cure rate if caught prior to mental nerve infiltration.',
        coords: 'x: 30-70%, y: 2-10%'
    }
];

const OralCavityMap = ({ selectedSite = 'buccal_mucosa', onSelectSite }) => {
    const [hoveredSite, setHoveredSite] = useState(null);

    const activeSite = ORAL_SITES.find(s => s.id === (hoveredSite || selectedSite)) || ORAL_SITES[0];
    const currentSelection = ORAL_SITES.find(s => s.id === selectedSite) || ORAL_SITES[0];

    const isSelected = (id) => selectedSite === id;
    const isHovered = (id) => hoveredSite === id;

    return (
        <div className="border border-stone-300 dark:border-stone-800 bg-stone-50/70 dark:bg-stone-900/60 p-4 transition-all">
            {/* Header Telemetry */}
            <div className="flex items-center justify-between font-mono text-[10px] text-stone-500 uppercase pb-2 border-b border-stone-200 dark:border-stone-800 mb-3">
                <div className="flex items-center gap-1.5">
                    <Crosshair className="w-3.5 h-3.5 text-clinical-teal" />
                    <span>ANATOMICAL TARGETING // ORAL CAVITY TOPOLOGY</span>
                </div>
                <span className="text-[9px] text-stone-400">CLICK ZONE TO SPECIFY LESION SITE</span>
            </div>

            <div className="grid md:grid-cols-12 gap-4 items-center">
                {/* 2D Anatomical Vector Schematic */}
                <div className="md:col-span-6 flex flex-col items-center justify-center p-2 relative">
                    <div className="relative w-full max-w-[260px] aspect-[4/5] bg-stone-100 dark:bg-stone-950/80 border border-stone-200 dark:border-stone-800 rounded-sm p-3 shadow-inner">
                        {/* Anatomical SVG Diagram */}
                        <svg viewBox="0 0 300 360" className="w-full h-full select-none">
                            <defs>
                                <radialGradient id="oralCavityBg" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stopColor="#292524" stopOpacity="0.4" />
                                    <stop offset="100%" stopColor="#1c1917" stopOpacity="0.8" />
                                </radialGradient>
                                <pattern id="diagGrid" width="12" height="12" patternUnits="userSpaceOnUse">
                                    <path d="M 12 0 L 0 0 0 12" fill="none" stroke="currentColor" strokeWidth="0.5" className="text-stone-300/30 dark:text-stone-700/30" />
                                </pattern>
                            </defs>

                            <rect width="300" height="360" fill="url(#diagGrid)" />

                            {/* Maxillary / Mandibular Outer Contour */}
                            <path 
                                d="M 50 140 C 40 50, 260 50, 250 140 C 245 280, 220 330, 150 340 C 80 330, 55 280, 50 140 Z" 
                                fill="url(#oralCavityBg)" 
                                stroke="#78716c" 
                                strokeWidth="1.5" 
                                strokeDasharray="3 3"
                            />

                            {/* 1. Labial Mucosa / Lip (Top arch) */}
                            <path
                                d="M 80 40 C 120 20, 180 20, 220 40 C 200 50, 100 50, 80 40 Z"
                                onClick={() => onSelectSite('lip')}
                                onMouseEnter={() => setHoveredSite('lip')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('lip') ? 'fill-clinical-teal stroke-teal-300 stroke-2' : 
                                    isHovered('lip') ? 'fill-teal-600/50 stroke-white' : 'fill-stone-600/40 stroke-stone-500'
                                }`}
                            />

                            {/* 2. Hard Palate */}
                            <path
                                d="M 95 65 C 125 50, 175 50, 205 65 C 195 105, 105 105, 95 65 Z"
                                onClick={() => onSelectSite('hard_palate')}
                                onMouseEnter={() => setHoveredSite('hard_palate')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('hard_palate') ? 'fill-clinical-teal stroke-teal-300 stroke-2' : 
                                    isHovered('hard_palate') ? 'fill-teal-600/50 stroke-white' : 'fill-stone-600/30 stroke-stone-500'
                                }`}
                            />

                            {/* 3. Soft Palate & Uvula Junction */}
                            <path
                                d="M 110 108 C 130 100, 170 100, 190 108 C 175 140, 125 140, 110 108 Z"
                                onClick={() => onSelectSite('soft_palate')}
                                onMouseEnter={() => setHoveredSite('soft_palate')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('soft_palate') ? 'fill-rose-600 stroke-rose-300 stroke-2' : 
                                    isHovered('soft_palate') ? 'fill-rose-500/50 stroke-white' : 'fill-stone-700/50 stroke-stone-500'
                                }`}
                            />

                            {/* 4. Buccal Mucosa - Left Side (Cheek) */}
                            <path
                                d="M 45 120 C 35 180, 50 250, 75 285 C 80 250, 75 180, 65 120 Z"
                                onClick={() => onSelectSite('buccal_mucosa')}
                                onMouseEnter={() => setHoveredSite('buccal_mucosa')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('buccal_mucosa') ? 'fill-amber-500 stroke-amber-200 stroke-2' : 
                                    isHovered('buccal_mucosa') ? 'fill-amber-500/50 stroke-white' : 'fill-stone-700/40 stroke-stone-500'
                                }`}
                            />

                            {/* 4. Buccal Mucosa - Right Side (Cheek) */}
                            <path
                                d="M 255 120 C 265 180, 250 250, 225 285 C 220 250, 225 180, 235 120 Z"
                                onClick={() => onSelectSite('buccal_mucosa')}
                                onMouseEnter={() => setHoveredSite('buccal_mucosa')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('buccal_mucosa') ? 'fill-amber-500 stroke-amber-200 stroke-2' : 
                                    isHovered('buccal_mucosa') ? 'fill-amber-500/50 stroke-white' : 'fill-stone-700/40 stroke-stone-500'
                                }`}
                            />

                            {/* 5. Dorsal Tongue (Central surface) */}
                            <ellipse
                                cx="150"
                                cy="205"
                                rx="32"
                                ry="45"
                                onClick={() => onSelectSite('dorsal_tongue')}
                                onMouseEnter={() => setHoveredSite('dorsal_tongue')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('dorsal_tongue') ? 'fill-clinical-teal stroke-teal-300 stroke-2' : 
                                    isHovered('dorsal_tongue') ? 'fill-teal-600/50 stroke-white' : 'fill-stone-500/40 stroke-stone-400'
                                }`}
                            />

                            {/* 6. Lateral Tongue - Left Border (High Risk) */}
                            <path
                                d="M 115 170 C 105 200, 110 235, 128 250 C 122 230, 120 195, 124 170 Z"
                                onClick={() => onSelectSite('lateral_tongue')}
                                onMouseEnter={() => setHoveredSite('lateral_tongue')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('lateral_tongue') ? 'fill-rose-600 stroke-rose-200 stroke-2 animate-pulse' : 
                                    isHovered('lateral_tongue') ? 'fill-rose-500/70 stroke-white' : 'fill-rose-900/60 stroke-rose-600'
                                }`}
                            />

                            {/* 6. Lateral Tongue - Right Border (High Risk) */}
                            <path
                                d="M 185 170 C 195 200, 190 235, 172 250 C 178 230, 180 195, 176 170 Z"
                                onClick={() => onSelectSite('lateral_tongue')}
                                onMouseEnter={() => setHoveredSite('lateral_tongue')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('lateral_tongue') ? 'fill-rose-600 stroke-rose-200 stroke-2 animate-pulse' : 
                                    isHovered('lateral_tongue') ? 'fill-rose-500/70 stroke-white' : 'fill-rose-900/60 stroke-rose-600'
                                }`}
                            />

                            {/* 7. Floor of Mouth (Anterior Sublingual crescent) */}
                            <path
                                d="M 110 258 C 130 278, 170 278, 190 258 C 175 288, 125 288, 110 258 Z"
                                onClick={() => onSelectSite('floor_of_mouth')}
                                onMouseEnter={() => setHoveredSite('floor_of_mouth')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('floor_of_mouth') ? 'fill-rose-600 stroke-rose-200 stroke-2' : 
                                    isHovered('floor_of_mouth') ? 'fill-rose-500/70 stroke-white' : 'fill-rose-950/70 stroke-rose-700'
                                }`}
                            />

                            {/* 8. Lower Gingiva / Alveolar Ridge Arch */}
                            <path
                                d="M 85 295 C 120 325, 180 325, 215 295 C 200 310, 100 310, 85 295 Z"
                                onClick={() => onSelectSite('gingiva')}
                                onMouseEnter={() => setHoveredSite('gingiva')}
                                onMouseLeave={() => setHoveredSite(null)}
                                className={`cursor-pointer transition-all duration-200 ${
                                    isSelected('gingiva') ? 'fill-amber-500 stroke-amber-200 stroke-2' : 
                                    isHovered('gingiva') ? 'fill-amber-500/50 stroke-white' : 'fill-stone-600/30 stroke-stone-500'
                                }`}
                            />

                            {/* Crosshair Target on Selected */}
                            <circle cx="150" cy="180" r="1.5" fill="#14b8a6" />
                        </svg>

                        {/* Selected Indicator Chip */}
                        <div className="absolute bottom-1 right-2 font-mono text-[8px] text-stone-400">
                            ZONE: <span className="text-clinical-teal font-semibold uppercase">{currentSelection.shortLabel}</span>
                        </div>
                    </div>
                </div>

                {/* Quick Selection Buttons & Clinical Risk Telemetry */}
                <div className="md:col-span-6 flex flex-col justify-between space-y-3">
                    <div className="grid grid-cols-2 gap-1.5">
                        {ORAL_SITES.map((site) => {
                            const isCurrent = isSelected(site.id);
                            return (
                                <button
                                    key={site.id}
                                    type="button"
                                    onClick={() => onSelectSite(site.id)}
                                    onMouseEnter={() => setHoveredSite(site.id)}
                                    onMouseLeave={() => setHoveredSite(null)}
                                    className={`text-left px-2.5 py-1.5 border transition-all text-xs font-mono flex items-center justify-between ${
                                        isCurrent 
                                            ? 'border-clinical-teal bg-teal-50/80 dark:bg-teal-950/40 text-stone-900 dark:text-stone-100 font-semibold shadow-xs' 
                                            : 'border-stone-200 dark:border-stone-800 bg-white/40 dark:bg-stone-950/40 text-stone-600 dark:text-stone-400 hover:border-stone-300 dark:hover:border-stone-700'
                                    }`}
                                >
                                    <span className="truncate">{site.shortLabel}</span>
                                    {isCurrent && <CheckCircle2 className="w-3 h-3 text-clinical-teal flex-shrink-0" />}
                                </button>
                            );
                        })}
                    </div>

                    {/* Active Zone Clinical Dossier Card */}
                    <div className="p-3 border border-stone-200 dark:border-stone-800 bg-white/70 dark:bg-stone-950/70">
                        <div className="flex items-center justify-between mb-1.5">
                            <span className="font-serif text-sm text-stone-900 dark:text-stone-100 font-medium">
                                {activeSite.label}
                            </span>
                            <span className={`font-mono text-[9px] px-1.5 py-0.5 border font-semibold ${activeSite.badgeBg}`}>
                                {activeSite.riskTier}
                            </span>
                        </div>
                        <p className="font-sans text-[11px] text-stone-600 dark:text-stone-300 leading-snug">
                            {activeSite.pathologyNote}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OralCavityMap;
