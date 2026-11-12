# Lab

## Application

The lab studies solid-state reactions between tungsten trioxide and a divalent-metal source. Each sample is made from exactly two precursors: WO₃ plus one source of Mg, Ca, Sr, Ba, Pb, Zn, Cu, Co, Ni or Mn. The source is an oxide (including mixed-valence Mn and Co oxides), a carbonate, or a peroxide. Precursors are dosed robotically at a 1:1 metal ratio (about 2 g), fired once for 60 minutes in a box furnace at 200–900 °C without regrinding, and the recovered powder is measured directly.

Depending on the reactivity, a sample may be an unreacted precursor mixture, a partially reacted mixture, or mostly product. It may contain residual precursors, their decomposition products, the target tungstate, intermediate or off-stoichiometric phases, polymorphs, and phases absent from the reference library. The task is to determine the crystalline phases, defensible atomic structures and mass fractions. 

## Learning priorities 
Since this lab works with different precursors (divalent-metal source) and temperatures, the main priorities are improving capabilities on complex multiphase patterns, the type that may arise during these synthesis experiments. This includes better ability to carry out complex refinement, understand and persist when a solution is incomplete, and recover intermediate, off-stoichiometric phases outside the provided database through chemical-intuition guided reference adaptation, especially where the phases are secondary, overlap significantly, or have convincing decoys in the library. Ab initio structure solution for hidden phases with no structural relative in the library is not a priority, as teaching effective general procedures that expand this capability is difficult through the evolution framework.

## Measurement and solver inputs

Measurements are laboratory Cu Kα Bragg–Brentano reflection scans, 10–100° 2θ, with a PIXcel1D detector. Solvers receive the two precursor formulas, the reported firing temperature, the radiation settings and the raw counts. The product composition, number of phases, instrument profile, polarization and calibration are unknown, and specimen height, surface condition, crystallite size, microstrain and texture are uncalibrated.

## Generator settings

The generator reads the block below. It describes this lab's measurements: the scan grid and count levels, the uncertainty of the instrument profile and angular zero, the background, the ranges of specimen effects, and the exact form of the solver inputs. Distributions are deliberately broad, so they describe what this kind of laboratory measurement can look like rather than any particular sample.

```json lab-settings
{
  "schema": "pxrd-lab-settings/1",
  "lab_id": "divalent-tungstates",
  "measurement": {
    "geometry": "bragg_brentano",
    "goniometer_radius_mm": 200.0,
    "radiation": {"wavelength_ka1_A": 1.540598, "wavelength_ka2_A": 1.544426, "ka2_ka1_ratio": 0.5},
    "grid_deg": {"min": 9.90343322, "max": 100.09455322, "step": 0.0108664},
    "peak_counts": [5000, 15000, 40000],
    "zero_offset_deg": {"distribution": "uniform", "range": [-0.25, 0.25]},
    "instrument_profile": {
      "U": {"distribution": "uniform", "range": [0.0, 40.0]},
      "W": {"distribution": "uniform", "range": [2.0, 40.0]},
      "X": {"distribution": "log_uniform", "range": [0.1, 6.0]},
      "SH_L": {"distribution": "log_uniform", "range": [0.005, 0.10]},
      "polarization": {"distribution": "uniform", "range": [0.5, 1.0]}
    },
    "background": {
      "mode": "sampled_families_v1",
      "family_weights": {"simple": 0.1, "exponential": 0.6, "power_law": 0.3},
      "floor_counts": [200.0, 1200.0],
      "high_floor_probability": 0.15,
      "high_floor_counts": [2500.0, 3500.0],
      "tail_counts": [1000.0, 3000.0],
      "high_floor_tail_counts": [0.0, 700.0],
      "decay_length_deg": [5.0, 20.0],
      "power_exponent": [1.0, 3.0]
    }
  },
  "specimen": {
    "displacement_um": {"distribution": "uniform", "range": [-800.0, 800.0], "probability": 1.0},
    "surface_roughness": {"probability": 0.5, "A_range": [0.05, 0.6], "B_range": [0.02, 0.5], "B_distribution": "log_uniform",
                          "max_low_angle_deficit": 0.5, "deficit_reference_2theta_deg": 20.0},
    "crystallite_size_um": {"distribution": "log_uniform", "range": [0.04, 1.5]},
    "microstrain_ppm": {"distribution": "log_uniform", "range": [300.0, 8000.0], "probability": 0.6,
                        "anisotropy": {"probability": 0.4, "axial_ratio": {"distribution": "log_uniform", "range": [0.25, 4.0]},
                                       "axes": [[0, 0, 1], [1, 0, 0], [0, 1, 0]]}},
    "preferred_orientation": {"model": "march_dollase", "distribution": "log_uniform", "range": [0.7, 1.4], "probability": 0.35,
                              "axes": [[0, 0, 1], [1, 0, 0], [0, 1, 0], [1, 1, 0], [1, 1, 1]]},
    "uiso_A2": {"distribution": "log_uniform", "range": [0.003, 0.02]},
    "reference_mismatch": {"cell_strain": {"distribution": "log_uniform", "range": [0.0002, 0.005]},
                           "position_rms_A": {"distribution": "log_uniform", "range": [0.01, 0.04]},
                           "position_rms_A_by_element": {"O": {"distribution": "log_uniform", "range": [0.01, 0.05]}},
                           "probability": 1.0},
    "control_size_um": [0.3, 1.0]
  },
  "solver_inputs": {
    "pattern_columns": ["two_theta_deg", "intensity"],
    "line_ending": "crlf",
    "sample_fields": {
      "precursors": {"type": "formula_list", "items": [2, 2]},
      "reported_heating_temperature_C": {"type": "number", "range": [200, 900]}
    },
    "element_sources": {"fields": ["precursors"], "ambient": ["O", "H", "C"], "each_source_element_present": true},
    "metadata": {
      "precursors": "{sample.precursors}",
      "reported_heating_temperature_C": "{sample.reported_heating_temperature_C}",
      "product_composition": null,
      "number_of_phases": null,
      "instrument": {
        "sample_mode": "Reflection",
        "detector": "PIXcel1D-Medipix3 detector",
        "used_wavelength_intended": "K-Alpha 1",
        "radiation": "Cu K-alpha",
        "wavelength_Kalpha1_angstrom": 1.540598,
        "wavelength_Kalpha2_angstrom": 1.544426,
        "reported_Kalpha2_to_Kalpha1_ratio": 0.5,
        "common_counting_time_seconds": {"per_session": [12.495, 13.77, 18.249]},
        "effective_polarization": null,
        "calibrated_instrument_profile": null
      },
      "data": {
        "x": "two_theta_deg",
        "y": "intensity",
        "intensity_unit": "counts",
        "processing": "Original measured intensities; no smoothing, background subtraction, normalization, or resampling.",
        "pointwise_standard_uncertainties": "Not supplied."
      }
    }
  }
}
```
