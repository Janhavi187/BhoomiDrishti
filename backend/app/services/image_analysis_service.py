"""Image analysis service — extracts visual features from uploaded soil/field images.
Uses lightweight CV heuristics (PIL-based) so no heavy ML dependencies are needed.
Architected so a real CNN/ViT model can later replace the feature extraction."""

from PIL import Image, ImageStat, ImageFilter
import numpy as np
from io import BytesIO
from pathlib import Path


class ImageAnalysisService:
    """Extract visual features from soil/crop images using PIL heuristics."""

    def analyze(self, image_path: str) -> dict:
        """
        Analyze image and return feature dict.
        Features: brightness, contrast, green_ratio, brown_ratio,
                  texture_score, patchiness, dryness_cue, color_uniformity,
                  vegetation_index, image_quality
        """
        try:
            img = Image.open(image_path).convert("RGB")
            img_resized = img.resize((256, 256))
            pixels = np.array(img_resized, dtype=np.float32)

            features = {}
            features["brightness"] = self._compute_brightness(pixels)
            features["contrast"] = self._compute_contrast(pixels)
            features["green_ratio"] = self._compute_green_ratio(pixels)
            features["brown_ratio"] = self._compute_brown_ratio(pixels)
            features["texture_score"] = self._compute_texture(img_resized)
            features["patchiness"] = self._compute_patchiness(pixels)
            features["dryness_cue"] = self._compute_dryness(pixels)
            features["color_uniformity"] = self._compute_uniformity(pixels)
            features["vegetation_index"] = self._compute_vegetation_index(pixels)
            features["image_quality"] = self._compute_quality(img_resized, pixels)

            # Round all values
            features = {k: round(float(v), 3) for k, v in features.items()}
            return features

        except Exception as e:
            # Return neutral features on error
            return self._default_features(str(e))

    def _compute_brightness(self, pixels: np.ndarray) -> float:
        """Average brightness 0-1."""
        return float(np.mean(pixels) / 255.0)

    def _compute_contrast(self, pixels: np.ndarray) -> float:
        """Standard deviation of pixel values normalized 0-1."""
        return float(np.std(pixels) / 128.0)

    def _compute_green_ratio(self, pixels: np.ndarray) -> float:
        """Ratio of green channel dominance — indicates vegetation."""
        r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        total = r + g + b + 1e-6
        green_dominant = np.mean(g / total)
        # Vegetation tends to have g > r and g > b
        veg_mask = (g > r * 1.05) & (g > b * 1.05)
        veg_ratio = np.mean(veg_mask.astype(float))
        return float((green_dominant + veg_ratio) / 2)

    def _compute_brown_ratio(self, pixels: np.ndarray) -> float:
        """Ratio of brown/earth tones — indicates dry soil."""
        r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        # Brown: r > g > b, with r in mid-range
        brown_mask = (r > 80) & (r < 200) & (g > 50) & (g < 180) & (b < g) & (r > g)
        return float(np.mean(brown_mask.astype(float)))

    def _compute_texture(self, img: Image.Image) -> float:
        """Texture complexity via edge detection 0-1."""
        gray = img.convert("L")
        edges = gray.filter(ImageFilter.FIND_EDGES)
        stat = ImageStat.Stat(edges)
        return min(1.0, stat.mean[0] / 60.0)

    def _compute_patchiness(self, pixels: np.ndarray) -> float:
        """Spatial variance — high means uneven coverage."""
        h, w = pixels.shape[:2]
        quadrants = [
            pixels[:h//2, :w//2],
            pixels[:h//2, w//2:],
            pixels[h//2:, :w//2],
            pixels[h//2:, w//2:],
        ]
        means = [np.mean(q) for q in quadrants]
        return float(np.std(means) / 128.0)

    def _compute_dryness(self, pixels: np.ndarray) -> float:
        """Dryness cue — lighter, low-saturation, low-green pixels."""
        r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        brightness = (r + g + b) / 3.0
        saturation = np.max(pixels, axis=2) - np.min(pixels, axis=2)
        dry_mask = (brightness > 140) & (saturation < 60) & (g < r)
        return float(np.mean(dry_mask.astype(float)))

    def _compute_uniformity(self, pixels: np.ndarray) -> float:
        """Color uniformity — how homogeneous the image is."""
        std = np.std(pixels.reshape(-1, 3), axis=0)
        uniformity = 1.0 - (np.mean(std) / 80.0)
        return max(0.0, min(1.0, uniformity))

    def _compute_vegetation_index(self, pixels: np.ndarray) -> float:
        """Simplified VARI-like vegetation index."""
        r, g, b = (
            pixels[:, :, 0].astype(float),
            pixels[:, :, 1].astype(float),
            pixels[:, :, 2].astype(float),
        )
        denom = r + g + b + 1e-6
        vari = (g - r) / denom
        vari_norm = (np.mean(vari) + 0.5)  # Shift to 0-1 range
        return max(0.0, min(1.0, vari_norm))

    def _compute_quality(self, img: Image.Image, pixels: np.ndarray) -> float:
        """Estimate image quality 0-1."""
        brightness = np.mean(pixels) / 255.0
        contrast = np.std(pixels) / 128.0
        # Penalize too dark or too bright
        bright_penalty = 1.0 - abs(brightness - 0.45) * 1.5
        quality = (bright_penalty * 0.5 + min(1.0, contrast) * 0.5)
        return max(0.1, min(1.0, quality))

    def _default_features(self, error: str = "") -> dict:
        """Return neutral features when image analysis fails."""
        return {
            "brightness": 0.5,
            "contrast": 0.5,
            "green_ratio": 0.3,
            "brown_ratio": 0.3,
            "texture_score": 0.4,
            "patchiness": 0.3,
            "dryness_cue": 0.3,
            "color_uniformity": 0.5,
            "vegetation_index": 0.4,
            "image_quality": 0.5,
            "_error": error,
        }


image_analysis_service = ImageAnalysisService()
