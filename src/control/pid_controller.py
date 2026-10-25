"""
control/pid_controller.py — Dinamik PID Kontrolcü (Anti-Windup İyileştirmeli)
Tek Sorumluluk: Mesafeye bağlı agresyonlu PID hesaplaması yapmak.
Mesafe azaldıkça refleksler sertleşir (x2.5'e kadar).
Derivative Kick önlenir: Derivative on Measurement kullanılır.
"""

import numpy as np
from typing import Tuple
from core.config import CONFIG


class PIDController:
    """
    Pilotun lövye reflekslerini mesafeye göre sertleştiren PID kontrolcü.
    Derivative on Measurement ile derivative kick önlenir.
    
    Parametreler:
        kp:      Oransal kazanç (P)
        ki:      İntegral kazanç (I)
        kd:      Türevsel kazanç (D)
        output_range: Çıkış sınırları (min, max)
    """
    def __init__(self, kp: float, ki: float, kd: float, output_range: Tuple[float, float]):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min_out, self.max_out = output_range
        self.integral = 0.0
        self.prev_measurement = 0.0
        self.prev_error = 0.0
        
    def compute(self, setpoint: float, measurement: float, dt: float, distance: float) -> float:
        """
        PID çıkışını hesaplar.
        DİNAMİK AGRESYON: Mesafe 100 metrenin altına düştüğünde
        P ve D kazançları x2.5 katına kadar artırılır.
        Derivative on Measurement kullanılır (derivative kick yok).
        """
        if dt <= 0.0:
            return 0.0
        
        # Mesafeye bağlı agresyon çarpanı
        aggression_multiplier = np.clip(
            CONFIG.pid.aggression_min_distance / max(distance, CONFIG.pid.aggression_min_distance),
            1.0,
            CONFIG.pid.aggression_max_multiplier
        )
        
        kp = self.kp * aggression_multiplier
        kd = self.kd * aggression_multiplier
        ki = self.ki
        
        # Hata hesapla
        error = setpoint - measurement
        
        # Anti-Windup: İntegral limitini çıkış limitlerine göre dinamik ayarla
        integral_limit = max(abs(self.max_out), abs(self.min_out)) * 0.5
        self.integral = np.clip(self.integral + error * dt, -integral_limit, integral_limit)
        
        # Derivative on Measurement (derivative kick yok!)
        # Ölçümün değişim hızı üzerinden türev alınır, hata üzerinden değil
        derivative = -(measurement - self.prev_measurement) / dt
        self.prev_measurement = measurement
        self.prev_error = error
        
        # PID çıkışı
        output = (kp * error) + (ki * self.integral) + (kd * derivative)
        
        return float(np.clip(output, self.min_out, self.max_out))
    
    def reset(self):
        """PID'yi sıfırla."""
        self.integral = 0.0
        self.prev_measurement = 0.0
        self.prev_error = 0.0


class DynamicPIDController:
    """
    Eksen bazlı PID kontrolcü.
    PID_X, PID_Y, PID_Z şeklinde çalışır.
    """
    def __init__(self):
        # X ekseni (Yatay - Roll/Pitch)
        self.pid_x = PIDController(
            CONFIG.pid.kp_x, 
            CONFIG.pid.ki_x, 
            CONFIG.pid.kd_x, 
            CONFIG.pid.output_limit
        )
        # Y ekseni (Dikey - Altitude)
        self.pid_y = PIDController(
            CONFIG.pid.kp_y, 
            CONFIG.pid.ki_y, 
            CONFIG.pid.kd_y, 
            CONFIG.pid.output_limit
        )
        # Z ekseni (Yatay - Yaw)
        self.pid_z = PIDController(
            CONFIG.pid.kp_z, 
            CONFIG.pid.ki_z, 
            CONFIG.pid.kd_z, 
            CONFIG.pid.output_limit
        )
        
    def compute(
        self, 
        setpoint_x: float, 
        measurement_x: float, 
        setpoint_y: float, 
        measurement_y: float, 
        setpoint_z: float, 
        measurement_z: float, 
        dt: float, 
        distance: float
    ) -> tuple[float, float, float]:
        """
        Üç eksen için PID çıkışlarını hesaplar.
        Döndürür: (cmd_x, cmd_y, cmd_z)
        """
        cmd_x = self.pid_x.compute(setpoint_x, measurement_x, dt, distance)
        cmd_y = self.pid_y.compute(setpoint_y, measurement_y, dt, distance)
        cmd_z = self.pid_z.compute(setpoint_z, measurement_z, dt, distance)
        
        return cmd_x, cmd_y, cmd_z
    
    def reset(self):
        """Tüm PID'leri sıfırla."""
        self.pid_x.reset()
        self.pid_y.reset()
        self.pid_z.reset()