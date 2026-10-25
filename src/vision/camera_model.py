"""
vision/camera_model.py — Pinhole kamera modeli
Piksel koordinatları ile uzaysal (metrik) koordinatlar arasında dönüşüm yapar.
"""

import numpy as np
from core.types import Vector3
from core.config import CONFIG


class CameraModel:
    """
    Pinhole kamera modeli ile piksel ↔ uzaysal dönüşüm.
    """
    def __init__(self):
        self.width = CONFIG.camera.width
        self.height = CONFIG.camera.height
        self.cx = self.width / 2.0
        self.cy = self.height / 2.0
        fov_rad = np.radians(CONFIG.camera.fov_degrees)
        self.fx = self.fy = (self.width / 2.0) / np.tan(fov_rad / 2.0)
        
    def pixel_to_spatial(self, bbox_xywh: np.ndarray, target_width_m: float = 1.5) -> Vector3:
        """
        Bounding box'tan 3D pozisyon (metre) hesaplar.
        bbox_xywh: [cx, cy, w, h] formatında
        """
        cx, cy, bw, bh = bbox_xywh
        bw = max(bw, 1.0)  # Sıfıra bölmeyi önle
        z_m = (self.fx * target_width_m) / bw
        x_m = (cx - self.cx) * z_m / self.fx
        y_m = (cy - self.cy) * z_m / self.fy
        return Vector3(x_m, y_m, z_m)
    
    def spatial_to_pixel(self, pos: Vector3) -> tuple[int, int]:
        """
        3D pozisyondan piksel koordinatı hesaplar.
        """
        z_m = max(pos.z, 0.1)
        px = (pos.x * self.fx / z_m) + self.cx
        py = (pos.y * self.fy / z_m) + self.cy
        return int(px), int(py)