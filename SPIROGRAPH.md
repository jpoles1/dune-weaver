# Spirograph Pattern Generator

The Dune Weaver now includes a built-in spirograph pattern generator that creates mathematical patterns using parametric equations.

## Features

### Pattern Types

1. **Hypotrochoid** - Classic spirograph where a small circle rolls inside a larger circle
2. **Epitrochoid** - Small circle rolls outside a larger circle
3. **Rose Curve** - Beautiful petal patterns using polar equations
4. **Lissajous Figure** - Complex harmonic patterns from oscillations

### Access

Navigate to `/spirograph` in your browser or access via the web interface.

## Usage

### Web Interface

1. Open the spirograph generator at `http://your-dune-weaver-ip/spirograph`
2. Choose between:
   - **Presets Tab**: Quick access to pre-configured beautiful patterns
   - **Custom Tab**: Fine-tune all parameters for unique designs

#### Preset Patterns

Available presets include:
- `classic_5_petal`: Traditional 5-petal spirograph
- `classic_7_petal`: Traditional 7-petal spirograph
- `flower_small` & `flower_large`: Flower-like patterns
- `star_burst`: Radiating star pattern
- `rose_5` & `rose_7`: Rose curves with different petal counts
- `lissajous_3_4` & `lissajous_5_6`: Complex Lissajous figures

#### Custom Patterns

**Hypotrochoid/Epitrochoid Parameters:**
- `R`: Radius of fixed circle (typically 1.0)
- `r`: Radius of rolling circle (0.1-0.5 for good results)
- `d`: Distance from rolling circle center to pen point (0.5-1.5 × r)

**Rose Curve Parameters:**
- `n`: Number of petals
- `d`: Denominator (usually 1)

**Lissajous Parameters:**
- `a`: X-axis frequency (try 2-7)
- `b`: Y-axis frequency (try 2-7)
- `δ` (delta): Phase shift in radians (0 to 2π)

**Common Parameters:**
- `Points`: Number of coordinates (more = smoother, 1000-5000 recommended)
- `Scale`: Pattern size (0.1-1.0, use <1.0 to stay within table bounds)
- `Center Offset`: Move pattern away from center (0-0.5)

### API Usage

#### Get Available Presets

```bash
curl http://your-dune-weaver-ip/api/spirograph/presets
```

#### Generate from Preset

```bash
curl -X POST http://your-dune-weaver-ip/api/spirograph/generate-preset \
  -H "Content-Type: application/json" \
  -d '{
    "preset_name": "classic_5_petal",
    "filename": "my-pattern"
  }'
```

#### Generate Custom Pattern

```bash
# Hypotrochoid
curl -X POST http://your-dune-weaver-ip/api/spirograph/generate \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_type": "hypotrochoid",
    "filename": "custom-spiro",
    "R": 1.0,
    "r": 0.25,
    "d": 0.5,
    "num_points": 2000,
    "scale": 0.95,
    "center_offset": 0.0
  }'

# Rose Curve
curl -X POST http://your-dune-weaver-ip/api/spirograph/generate \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_type": "rose",
    "filename": "rose-7-petal",
    "n": 7,
    "rose_d": 1,
    "num_points": 2000,
    "scale": 0.95
  }'
```

### Python Module Usage

```python
from modules.spiro import SpirographGenerator, SpirographType

# Initialize generator
generator = SpirographGenerator(output_dir='./patterns')

# Generate a hypotrochoid
coordinates = generator.generate_hypotrochoid(
    R=1.0,      # Fixed circle radius
    r=0.25,     # Rolling circle radius
    d=0.5,      # Pen distance
    num_points=2000,
    scale=0.95
)

# Save to THR file
filepath = generator.save_to_thr(coordinates, "my_pattern")

# Or do it in one step
filepath = generator.generate_and_save(
    SpirographType.HYPOTROCHOID,
    "my_pattern",
    R=1.0, r=0.25, d=0.5
)
```

## Mathematical Background

### Hypotrochoid

A hypotrochoid is traced by a point on a circle rolling inside a fixed circle:

```
x = (R - r) × cos(t) + d × cos((R - r) / r × t)
y = (R - r) × sin(t) - d × sin((R - r) / r × t)
```

Where:
- `R` = radius of fixed circle
- `r` = radius of rolling circle
- `d` = distance from center of rolling circle to tracing point
- `t` = parameter (angle)

### Epitrochoid

Similar to hypotrochoid but the circle rolls outside:

```
x = (R + r) × cos(t) - d × cos((R + r) / r × t)
y = (R + r) × sin(t) - d × sin((R + r) / r × t)
```

### Rose Curve

Polar equation producing petal patterns:

```
r = cos(n/d × θ)
```

Where `n` determines the number of petals.

### Lissajous Figure

Parametric curves from harmonic oscillations:

```
x = sin(a × t + δ)
y = sin(b × t)
```

The ratio `a/b` determines the pattern complexity.

## Tips for Great Patterns

1. **Start with presets** to understand parameter effects
2. **Smaller r values** create more detailed, petal-like patterns
3. **Adjust d** to change petal shapes (try 0.5-1.5 times r)
4. **Use scale < 1.0** to ensure patterns stay within table bounds
5. **More points** create smoother paths but take longer to execute
6. **Experiment!** Small parameter changes create dramatically different patterns

## File Output

Generated patterns are saved as `.thr` files in `patterns/spirographs/` with the format:

```
theta rho
theta rho
...
```

Where:
- `theta`: Angle in radians (continuous, can exceed 2π for multi-revolution patterns)
- `rho`: Radius from center (0.0 to 1.0, normalized)

## Troubleshooting

**Pattern doesn't close properly:**
- Increase `num_points` for smoother curves
- Adjust r to values that create nice factors with R (e.g., R=1.0, r=0.2, 0.25, 0.33)

**Pattern extends beyond table:**
- Reduce `scale` parameter (try 0.9 or 0.8)
- Decrease `d` parameter for hypotrochoids/epitrochoids

**Pattern too simple:**
- For hypotrochoids: decrease `r` or increase `d`
- For rose curves: increase `n`
- For Lissajous: try coprime values for `a` and `b`

## Credits

Spirograph patterns are based on classical mathematical curves studied by mathematicians including:
- Albrecht Dürer (epitrochoids, 1525)
- Jules Antoine Lissajous (Lissajous figures, 1857)
- Guido Grandi (rose curves, 1728)

The modern Spirograph toy was invented by Denys Fisher in 1965.
