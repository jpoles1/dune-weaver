"""
Spirograph pattern generator for creating THR files.

This module generates parametric spirograph patterns including:
- Hypotrochoids (small circle rolling inside a larger circle)
- Epitrochoids (small circle rolling outside a larger circle)
- Custom parametric curves

The output is in THR format (theta-rho polar coordinates).
"""

import math
import numpy as np
from enum import Enum
from typing import List, Tuple, Optional
import os
import logging

logger = logging.getLogger(__name__)


class SpirographType(str, Enum):
    """Types of spirograph patterns."""
    HYPOTROCHOID = "hypotrochoid"  # Inner spirograph (classic Spirograph toy)
    EPITROCHOID = "epitrochoid"    # Outer spirograph
    ROSE = "rose"                   # Rose curve (special case)
    LISSAJOUS = "lissajous"         # Lissajous figure


class SpirographGenerator:
    """
    Generate spirograph patterns in polar coordinates for sand tables.
    
    Spirographs are created by tracing a point on a circle as it rolls
    around another circle. The mathematical formulas are:
    
    Hypotrochoid (inner):
        x = (R - r) * cos(t) + d * cos((R - r) / r * t)
        y = (R - r) * sin(t) - d * sin((R - r) / r * t)
    
    Epitrochoid (outer):
        x = (R + r) * cos(t) - d * cos((R + r) / r * t)
        y = (R + r) * sin(t) - d * sin((R + r) / r * t)
    
    Where:
        R = radius of fixed circle
        r = radius of rolling circle
        d = distance from center of rolling circle to tracing point
        t = parameter (angle)
    """
    
    def __init__(self, output_dir: str = './patterns'):
        """
        Initialize the spirograph generator.
        
        Args:
            output_dir: Directory where THR files will be saved
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    @staticmethod
    def _normalize_rho(rho: float, max_rho: float = 1.0) -> float:
        """
        Normalize rho values to be within [0, max_rho].
        
        Args:
            rho: Raw rho value
            max_rho: Maximum rho value (default 1.0 for normalized)
        
        Returns:
            Normalized rho value
        """
        return max(0.0, min(max_rho, rho))
    
    def generate_hypotrochoid(
        self,
        R: float,
        r: float,
        d: float,
        num_points: int = 2000,
        scale: float = 0.95,
        center_offset: float = 0.0
    ) -> List[Tuple[float, float]]:
        """
        Generate a hypotrochoid pattern (small circle inside large circle).
        
        Args:
            R: Radius of fixed circle (typically 1.0 for normalized)
            r: Radius of rolling circle (try values like 0.25, 0.33, 0.5)
            d: Distance from center of rolling circle to pen (try 0.5 to 1.5 * r)
            num_points: Number of points to generate
            scale: Scale factor to keep pattern within table bounds (0.0 to 1.0)
            center_offset: Offset from center (0.0 to 1.0)
        
        Returns:
            List of (theta, rho) tuples in polar coordinates
        """
        # Calculate number of rotations needed for pattern to close
        # LCM(R, r) / r gives the period
        gcd = math.gcd(int(R * 1000), int(r * 1000))
        lcm = (int(R * 1000) * int(r * 1000)) // gcd
        num_rotations = lcm / (r * 1000)
        
        # Generate parameter values
        t_max = 2 * math.pi * num_rotations
        t_values = np.linspace(0, t_max, num_points)
        
        coordinates = []
        prev_theta = 0
        
        for t in t_values:
            # Hypotrochoid parametric equations
            x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
            y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
            
            # Convert to polar coordinates
            rho = math.sqrt(x*x + y*y)
            theta = math.atan2(y, x)
            
            # Handle theta wrapping for continuous motion
            # Adjust theta to be continuous (no jumps)
            while theta - prev_theta > math.pi:
                theta -= 2 * math.pi
            while theta - prev_theta < -math.pi:
                theta += 2 * math.pi
            prev_theta = theta
            
            # Normalize and scale rho
            max_possible_rho = R + d  # Maximum extent of the pattern
            rho_normalized = (rho / max_possible_rho) * scale + center_offset
            rho_normalized = self._normalize_rho(rho_normalized, max_rho=1.0)
            
            coordinates.append((theta, rho_normalized))
        
        return coordinates
    
    def generate_epitrochoid(
        self,
        R: float,
        r: float,
        d: float,
        num_points: int = 2000,
        scale: float = 0.95,
        center_offset: float = 0.0
    ) -> List[Tuple[float, float]]:
        """
        Generate an epitrochoid pattern (small circle outside large circle).
        
        Args:
            R: Radius of fixed circle (typically 1.0 for normalized)
            r: Radius of rolling circle (try values like 0.1, 0.15, 0.2)
            d: Distance from center of rolling circle to pen (try 0.5 to 2.0 * r)
            num_points: Number of points to generate
            scale: Scale factor to keep pattern within table bounds (0.0 to 1.0)
            center_offset: Offset from center (0.0 to 1.0)
        
        Returns:
            List of (theta, rho) tuples in polar coordinates
        """
        # Calculate number of rotations needed for pattern to close
        gcd = math.gcd(int(R * 1000), int(r * 1000))
        lcm = (int(R * 1000) * int(r * 1000)) // gcd
        num_rotations = lcm / (r * 1000)
        
        # Generate parameter values
        t_max = 2 * math.pi * num_rotations
        t_values = np.linspace(0, t_max, num_points)
        
        coordinates = []
        prev_theta = 0
        
        for t in t_values:
            # Epitrochoid parametric equations
            x = (R + r) * math.cos(t) - d * math.cos((R + r) / r * t)
            y = (R + r) * math.sin(t) - d * math.sin((R + r) / r * t)
            
            # Convert to polar coordinates
            rho = math.sqrt(x*x + y*y)
            theta = math.atan2(y, x)
            
            # Handle theta wrapping for continuous motion
            while theta - prev_theta > math.pi:
                theta -= 2 * math.pi
            while theta - prev_theta < -math.pi:
                theta += 2 * math.pi
            prev_theta = theta
            
            # Normalize and scale rho
            max_possible_rho = R + r + d  # Maximum extent
            rho_normalized = (rho / max_possible_rho) * scale + center_offset
            rho_normalized = self._normalize_rho(rho_normalized, max_rho=1.0)
            
            coordinates.append((theta, rho_normalized))
        
        return coordinates
    
    def generate_rose(
        self,
        n: int,
        d: int = 1,
        num_points: int = 2000,
        scale: float = 0.95,
        center_offset: float = 0.0
    ) -> List[Tuple[float, float]]:
        """
        Generate a rose curve pattern.
        
        Rose curve equation: r = cos(n/d * theta)
        
        Args:
            n: Numerator of the frequency ratio (number of petals)
            d: Denominator of the frequency ratio (default 1)
            num_points: Number of points to generate
            scale: Scale factor (0.0 to 1.0)
            center_offset: Offset from center (0.0 to 1.0)
        
        Returns:
            List of (theta, rho) tuples
        """
        # Calculate number of rotations for complete pattern
        gcd = math.gcd(n, d)
        if d % 2 == 0 or n % 2 == 0:
            t_max = 2 * math.pi * d // gcd
        else:
            t_max = math.pi * d // gcd
        
        t_values = np.linspace(0, t_max, num_points)
        
        coordinates = []
        for t in t_values:
            # Rose curve equation
            k = n / d
            rho_raw = abs(math.cos(k * t))  # abs to keep rho positive
            
            # Scale and offset
            rho_normalized = rho_raw * scale + center_offset
            rho_normalized = self._normalize_rho(rho_normalized, max_rho=1.0)
            
            coordinates.append((t, rho_normalized))
        
        return coordinates
    
    def generate_lissajous(
        self,
        a: float,
        b: float,
        delta: float = 0.0,
        num_points: int = 2000,
        scale: float = 0.95,
        center_offset: float = 0.0
    ) -> List[Tuple[float, float]]:
        """
        Generate a Lissajous figure.
        
        Lissajous equations:
            x = sin(a * t + delta)
            y = sin(b * t)
        
        Args:
            a: Frequency ratio for x (try 2, 3, 5)
            b: Frequency ratio for y (try 3, 4, 7)
            delta: Phase shift in radians (try 0, pi/2, pi)
            num_points: Number of points to generate
            scale: Scale factor (0.0 to 1.0)
            center_offset: Offset from center (0.0 to 1.0)
        
        Returns:
            List of (theta, rho) tuples
        """
        # Calculate period
        gcd = math.gcd(int(a * 1000), int(b * 1000))
        lcm = (int(a * 1000) * int(b * 1000)) // gcd
        period = 2 * math.pi * lcm / 1000
        
        t_values = np.linspace(0, period, num_points)
        
        coordinates = []
        prev_theta = 0
        
        for t in t_values:
            # Lissajous equations
            x = math.sin(a * t + delta)
            y = math.sin(b * t)
            
            # Convert to polar coordinates
            rho = math.sqrt(x*x + y*y)
            theta = math.atan2(y, x)
            
            # Handle theta wrapping
            while theta - prev_theta > math.pi:
                theta -= 2 * math.pi
            while theta - prev_theta < -math.pi:
                theta += 2 * math.pi
            prev_theta = theta
            
            # Normalize rho (max is sqrt(2))
            rho_normalized = (rho / math.sqrt(2)) * scale + center_offset
            rho_normalized = self._normalize_rho(rho_normalized, max_rho=1.0)
            
            coordinates.append((theta, rho_normalized))
        
        return coordinates
    
    def generate_custom_parametric(
        self,
        x_func,
        y_func,
        t_start: float = 0.0,
        t_end: float = 2 * math.pi,
        num_points: int = 2000,
        scale: float = 0.95,
        center_offset: float = 0.0,
        auto_scale: bool = True
    ) -> List[Tuple[float, float]]:
        """
        Generate a pattern from custom parametric equations.
        
        Args:
            x_func: Function that takes t and returns x coordinate
            y_func: Function that takes t and returns y coordinate
            t_start: Starting parameter value
            t_end: Ending parameter value
            num_points: Number of points to generate
            scale: Scale factor (0.0 to 1.0)
            center_offset: Offset from center (0.0 to 1.0)
            auto_scale: Automatically scale to fit within bounds
        
        Returns:
            List of (theta, rho) tuples
        """
        t_values = np.linspace(t_start, t_end, num_points)
        
        # First pass: calculate all cartesian coordinates
        cartesian_coords = []
        for t in t_values:
            x = x_func(t)
            y = y_func(t)
            cartesian_coords.append((x, y))
        
        # Find max radius if auto-scaling
        max_r = 1.0
        if auto_scale:
            max_r = max(math.sqrt(x*x + y*y) for x, y in cartesian_coords)
            if max_r == 0:
                max_r = 1.0
        
        # Second pass: convert to polar with continuous theta
        coordinates = []
        prev_theta = 0
        
        for x, y in cartesian_coords:
            rho = math.sqrt(x*x + y*y)
            theta = math.atan2(y, x)
            
            # Handle theta wrapping
            while theta - prev_theta > math.pi:
                theta -= 2 * math.pi
            while theta - prev_theta < -math.pi:
                theta += 2 * math.pi
            prev_theta = theta
            
            # Normalize and scale
            rho_normalized = (rho / max_r) * scale + center_offset
            rho_normalized = self._normalize_rho(rho_normalized, max_rho=1.0)
            
            coordinates.append((theta, rho_normalized))
        
        return coordinates
    
    def save_to_thr(
        self,
        coordinates: List[Tuple[float, float]],
        filename: str
    ) -> str:
        """
        Save coordinates to a THR file.
        
        Args:
            coordinates: List of (theta, rho) tuples
            filename: Name of the output file (without .thr extension)
        
        Returns:
            Full path to the saved file
        """
        if not filename.endswith('.thr'):
            filename += '.thr'
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for theta, rho in coordinates:
                    # Format: "theta rho" with 5 decimal places
                    f.write(f"{theta:.5f} {rho:.5f}\n")
            
            logger.info(f"Saved spirograph pattern to {filepath} ({len(coordinates)} points)")
            return filepath
        
        except Exception as e:
            logger.error(f"Failed to save THR file {filepath}: {e}")
            raise
    
    def generate_and_save(
        self,
        pattern_type: SpirographType,
        filename: str,
        **kwargs
    ) -> str:
        """
        Generate a spirograph pattern and save it to a THR file.
        
        Args:
            pattern_type: Type of spirograph to generate
            filename: Name for the output file
            **kwargs: Parameters specific to the pattern type
        
        Returns:
            Full path to the saved file
        
        Examples:
            generator.generate_and_save(
                SpirographType.HYPOTROCHOID,
                "my_spiro",
                R=1.0, r=0.25, d=0.5
            )
        """
        if pattern_type == SpirographType.HYPOTROCHOID:
            coordinates = self.generate_hypotrochoid(**kwargs)
        elif pattern_type == SpirographType.EPITROCHOID:
            coordinates = self.generate_epitrochoid(**kwargs)
        elif pattern_type == SpirographType.ROSE:
            coordinates = self.generate_rose(**kwargs)
        elif pattern_type == SpirographType.LISSAJOUS:
            coordinates = self.generate_lissajous(**kwargs)
        else:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
        
        return self.save_to_thr(coordinates, filename)


# Preset spirograph configurations
SPIROGRAPH_PRESETS = {
    "classic_5_petal": {
        "type": SpirographType.HYPOTROCHOID,
        "params": {"R": 1.0, "r": 0.2, "d": 0.4, "num_points": 2000}
    },
    "classic_7_petal": {
        "type": SpirographType.HYPOTROCHOID,
        "params": {"R": 1.0, "r": 0.142857, "d": 0.3, "num_points": 2000}
    },
    "flower_small": {
        "type": SpirographType.HYPOTROCHOID,
        "params": {"R": 1.0, "r": 0.33, "d": 0.66, "num_points": 3000}
    },
    "flower_large": {
        "type": SpirographType.HYPOTROCHOID,
        "params": {"R": 1.0, "r": 0.25, "d": 1.0, "num_points": 2000}
    },
    "star_burst": {
        "type": SpirographType.EPITROCHOID,
        "params": {"R": 1.0, "r": 0.1, "d": 0.3, "num_points": 2000}
    },
    "rose_5": {
        "type": SpirographType.ROSE,
        "params": {"n": 5, "d": 1, "num_points": 2000}
    },
    "rose_7": {
        "type": SpirographType.ROSE,
        "params": {"n": 7, "d": 1, "num_points": 2000}
    },
    "lissajous_3_4": {
        "type": SpirographType.LISSAJOUS,
        "params": {"a": 3, "b": 4, "delta": 0, "num_points": 2000}
    },
    "lissajous_5_6": {
        "type": SpirographType.LISSAJOUS,
        "params": {"a": 5, "b": 6, "delta": math.pi/2, "num_points": 3000}
    }
}
