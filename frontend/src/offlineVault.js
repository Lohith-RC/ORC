/**
 * OFFLINE CLINICAL VAULT (IndexedDB)
 * High-assurance client-side offline storage for rural outreach camps
 * Allows clinicians to capture, triage, and store patient specimens with zero network connectivity.
 */

const DB_NAME = 'ORC_ClinicalVault_v1';
const STORE_NAME = 'pending_screenings';

export const openVaultDB = () => {
    return new Promise((resolve, reject) => {
        if (!window.indexedDB) {
            reject(new Error("IndexedDB is not supported in this browser environment."));
            return;
        }
        const request = window.indexedDB.open(DB_NAME, 1);
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains(STORE_NAME)) {
                const store = db.createObjectStore(STORE_NAME, { keyPath: 'id', autoIncrement: true });
                store.createIndex('patient_identifier', 'patient_identifier', { unique: false });
                store.createIndex('timestamp', 'timestamp', { unique: false });
            }
        };
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
};

export const saveOfflineSpecimen = async (specimenData) => {
    const db = await openVaultDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite');
        const store = tx.objectStore(STORE_NAME);
        const record = {
            ...specimenData,
            timestamp: new Date().toISOString(),
            status: 'QUEUED_OFFLINE'
        };
        const req = store.add(record);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
    });
};

export const getOfflineSpecimens = async () => {
    try {
        const db = await openVaultDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_NAME, 'readonly');
            const store = tx.objectStore(STORE_NAME);
            const req = store.getAll();
            req.onsuccess = () => resolve(req.result || []);
            req.onerror = () => reject(req.error);
        });
    } catch (err) {
        console.warn("Vault read note:", err);
        return [];
    }
};

export const deleteOfflineSpecimen = async (id) => {
    const db = await openVaultDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite');
        const store = tx.objectStore(STORE_NAME);
        const req = store.delete(id);
        req.onsuccess = () => resolve();
        req.onerror = () => reject(req.error);
    });
};

export const clearSyncedSpecimens = async () => {
    const db = await openVaultDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite');
        const store = tx.objectStore(STORE_NAME);
        const req = store.clear();
        req.onsuccess = () => resolve();
        req.onerror = () => reject(req.error);
    });
};
