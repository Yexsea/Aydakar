"""
core/types.py — Veri tipleri (dataclass)
"""

from dataclasses import dataclass, field
import numpy as np
from typing import Optional
from core.constants import LockStatus, MissionMode


@dataclass
class Vector3:
    """3D vektör."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z], dtype=np.float32)

    @classmethod
    def from_numpy(cls, arr: np.ndarray):
        return cls(float(arr[0]), float(arr[1]), float(arr[2]))


@dataclass
class BBox:
    """Bounding box: merkez (cx, cy), genişlik (w), yükseklik (h)."""
    cx: float
    cy: float
    w: float
    h: float

    def to_xywh(self) -> np.ndarray:
        return np.array([self.cx, self.cy, self.w, self.h], dtype=np.float32)


@dataclass
class Detection:
    """Tek bir algılama sonucu."""
    id: int
    bbox: BBox
    pos_m: Vector3
    confidence: Optional[float] = None


@dataclass
class TrackedEntity:
    """Takip edilen varlık."""
    id: int
    bbox: BBox
    pos: Vector3
    vel: Vector3
    acc: Vector3
    track_age: float = 0.0
    time_since_update: float = 0.0
    is_ghost: bool = False
    is_biological: bool = False
    prediction_probability: float = 1.0


@dataclass
class FlightState:
    """Sistemin tek state'i."""
    frame: Optional[np.ndarray] = None
    tracked_entities: dict[int, TrackedEntity] = field(default_factory=dict)
    locked_target_id: Optional[int] = None
    lock_status: LockStatus = LockStatus.SEARCHING
    lock_progress_percent: float = 0.0
    mission_mode: MissionMode = MissionMode.BOOT
    own_altitude: float = 100.0
    own_velocity: Vector3 = field(default_factory=Vector3)
    cmd_velocity: Vector3 = field(default_factory=Vector3)
    av_box_coords: tuple = (0, 0, 0, 0)