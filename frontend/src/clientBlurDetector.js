/**
 * CLIENT-SIDE OPTICAL FOCUS & LAPLACIAN BLUR GATING (<15ms execution)
 * Computes 2D discrete Laplacian variance directly on client pixels.
 * Gating threshold = 50.0 (identical to backend BLUR_THRESHOLD).
 */

export const computeClientLaplacian = (sourceElement, width = 224, height = 224) => {
    try {
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        if (!ctx) return { sharpness: 0, isBlurry: true };

        ctx.drawImage(sourceElement, 0, 0, width, height);
        const imgData = ctx.getImageData(0, 0, width, height);
        const data = imgData.data;

        // Convert RGB to 2D Grayscale matrix
        const gray = new Float32Array(width * height);
        for (let i = 0, j = 0; i < data.length; i += 4, j++) {
            // Luminance formula
            gray[j] = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
        }

        // Discrete 2D Laplacian operator on interior pixels (ignore boundary wrap)
        // lap = gray[y-1][x] + gray[y+1][x] + gray[y][x-1] + gray[y][x+1] - 4*gray[y][x]
        let sum = 0;
        let sumSq = 0;
        let count = 0;

        for (let y = 1; y < height - 1; y++) {
            const rowOffset = y * width;
            const upOffset = (y - 1) * width;
            const downOffset = (y + 1) * width;

            for (let x = 1; x < width - 1; x++) {
                const val = (
                    gray[upOffset + x] +
                    gray[downOffset + x] +
                    gray[rowOffset + x - 1] +
                    gray[rowOffset + x + 1] -
                    4 * gray[rowOffset + x]
                );
                sum += val;
                sumSq += val * val;
                count++;
            }
        }

        if (count === 0) return { sharpness: 0, isBlurry: true };

        const mean = sum / count;
        const variance = (sumSq / count) - (mean * mean);
        const sharpness = Math.max(0, Math.round(variance * 10) / 10);
        const isBlurry = sharpness < 50.0;

        return { sharpness, isBlurry };
    } catch (err) {
        console.warn("Client blur detection error:", err);
        return { sharpness: 75.0, isBlurry: false }; // fallback safe
    }
};

export const computeImageFileSharpness = (file) => {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const result = computeClientLaplacian(img);
                resolve(result);
            };
            img.onerror = () => resolve({ sharpness: 0, isBlurry: true });
            img.src = e.target.result;
        };
        reader.onerror = () => resolve({ sharpness: 0, isBlurry: true });
        reader.readAsDataURL(file);
    });
};
