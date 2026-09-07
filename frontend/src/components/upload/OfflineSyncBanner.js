import React from 'react';
import { HardDrive, CloudUpload, CheckCircle2 } from 'lucide-react';

export const OfflineSyncBanner = ({
    offlineVaultCount,
    isOffline,
    isSyncingVault,
    onSyncVault,
    offlineSuccessMsg
}) => {
    return (
        <>
            {offlineVaultCount > 0 && (
                <div className="mb-4 p-3 border border-amber-500/40 bg-amber-50/70 dark:bg-amber-950/30 flex items-center justify-between font-mono text-xs">
                    <div className="flex items-center gap-2 text-amber-800 dark:text-amber-300">
                        <HardDrive className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                        <span>OFFLINE VAULT: <strong>{offlineVaultCount}</strong> queued</span>
                    </div>
                    <button
                        type="button"
                        disabled={isOffline || isSyncingVault}
                        onClick={onSyncVault}
                        className={`px-3 py-1 text-[10px] font-semibold uppercase border transition-all flex items-center gap-1.5 ${
                            isOffline 
                                ? 'border-stone-300 dark:border-stone-700 text-stone-400 cursor-not-allowed'
                                : 'border-amber-600 bg-amber-600 text-white hover:bg-amber-700 shadow-xs'
                        }`}
                    >
                        <CloudUpload className="w-3 h-3" />
                        <span>{isSyncingVault ? 'SYNCING...' : 'SYNC TO CLOUD'}</span>
                    </button>
                </div>
            )}

            {offlineSuccessMsg && (
                <div className="mb-4 p-2.5 border border-teal-500/40 bg-teal-50 dark:bg-teal-950/30 text-teal-800 dark:text-teal-300 font-mono text-xs flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-teal-600 shrink-0" />
                    <span>{offlineSuccessMsg}</span>
                </div>
            )}
        </>
    );
};

export default OfflineSyncBanner;
