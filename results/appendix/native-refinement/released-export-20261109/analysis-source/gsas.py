"""Pinned native recipes and independently recalculated exported-structure residuals."""
from __future__ import annotations

import ast
import copy
import importlib.util
import io
import os
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from scipy.optimize import lsq_linear
from scipy.signal import find_peaks, peak_widths

from common import write_json


def scriptable():
    sys.path.insert(0, os.environ.get("GSASII_PATH", "/opt/GSAS-II/GSASII"))
    import GSASIIscriptable as g2
    g2.SetPrintLevel("warn")
    return g2


def observation(task):
    method = task["method"]
    if method == "pxrdgen":
        y = np.loadtxt(io.StringIO(task["pattern_text"])) * task["intensity_multiplier"]
        return 5 + np.arange(len(y)) * .01, y
    if method in ("crystalyze", "ab-pxrd-solver"):
        return np.loadtxt(io.StringIO(task["pattern_text"]), delimiter=",", skiprows=1).T
    peaks = np.loadtxt(io.StringIO(task["pattern_text"]))
    x = 5 + np.arange(7501) * .01
    y = np.zeros(len(x))
    sigma = .1 / (2 * np.sqrt(2 * np.log(2)))
    for angle, intensity in peaks:
        y += intensity * np.exp(-.5 * ((x - angle) / sigma) ** 2)
    return x, y / max(y) * 100


def instrument(path, wavelength, u=0., w=18.0336880111, doublet=False):
    radiation = "Lam1:1.54056;Lam2:1.54433;I(L2)/I(L1):0.5" if doublet else f"Lam:{wavelength}"
    path.write_text("#GSAS-II fixed diagnostic instrument\nType:PXC;Bank:1\n" + radiation +
                    f";Zero:0;Polariz.:0.5;Azimuth:0\nU:{u};V:0;W:{w};X:0;Y:0;Z:0;SH/L:0\n")
    return path


@contextmanager
def precise_export():
    """Keep coordinates, rather than rounding them to their uncertainty."""
    import GSASIImath as math_module
    original = math_module.ValEsd
    math_module.ValEsd = lambda value, *args, **kwargs: f"{float(value):.12g}"
    try:
        yield
    finally:
        math_module.ValEsd = original


def export(phase, path):
    """Export at full precision before parsing; prevent special-position duplication."""
    with precise_export():
        phase.export_CIF(str(path))
    return path


def released_export(phase, path):
    """Export a fitted phase using unmodified GSAS-II formatting (Ab adapter)."""
    phase.export_CIF(str(path))
    return path


def stage(root, name):
    write_json(root / "refinement-stage.json", {"stage": name})


def recalculate(project):
    # Compute accepted parameter values without any further optimization. GSAS may
    # otherwise leave calculated arrays from a rejected LM trial step.
    cycles = project.data["Controls"]["data"]["max cyc"]
    project.data["Controls"]["data"]["max cyc"] = 0
    try:
        project.do_refinements([{}])
    finally:
        project.data["Controls"]["data"]["max cyc"] = cycles
    hist = project.histogram(0)
    arrays = hist.data["data"][1]
    obs, calc = np.asarray(arrays[1]), np.asarray(arrays[3])
    return float(100 * np.sqrt(np.sum((obs - calc) ** 2) / np.sum(obs ** 2)))


def project_from(cif, pattern, inst, filename, uniform=False):
    g2 = scriptable()
    project = g2.G2Project(newgpx=str(filename))
    hist = project.add_powder_histogram(str(pattern), str(inst))
    phase = project.add_phase(str(cif), phasename="candidate", histograms=[hist], fmthint="CIF")
    if uniform:
        hist.data["data"][1][2][:] = 1.
    return project, hist, phase


def pxrdgen(task, root, pattern):
    """Execute the two released functions, with paths fixed and no reference code."""
    from pymatgen.core import Structure
    from pymatgen.io.cif import CifWriter
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    source = Path(os.environ["REFINEMENT_SOURCES"]) / "PXRDGen"
    # Extract only released function definitions: the example's module-level
    # code reads truth and must never execute inside a benchmark worker.
    tree = ast.parse((source / "GSAS_rietveld.py").read_text())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in
                 {"HistStats", "Rietveld_wo_spacegroup", "Rietveld_constrained_with_spacegroup"}]
    namespace = {"G2sc": scriptable(), "os": os, "np": np, "work_dir": str(root),
                 "save_dir": str(root), "prmfile": str(source / "INST_XRY_Cu.PRM")}
    if len(functions) != 3:
        raise ValueError("Unexpected PXRDGen source functions")
    exec(compile(ast.Module(body=functions, type_ignores=[]), "pinned-PXRDGen", "exec"), namespace)
    (root / "candidate_pre.cif").write_bytes((root / "input.cif").read_bytes())
    stage(root, "native-first-pass")
    namespace["Rietveld_wo_spacegroup"]("candidate", str(pattern))
    # Keep the released export, even if uncertainty rounding makes it unreadable.
    (root / "stage-1.cif").write_bytes((root / "candidate_refine.cif").read_bytes())
    stage(root, "read-first-pass-export")
    structure = Structure.from_file(root / "candidate_refine.cif")
    stage(root, "conventional-cell-conversion")
    conventional = SpacegroupAnalyzer(structure).get_conventional_standard_structure()
    stage(root, "symmetry-cif-export")
    CifWriter(conventional, symprec=.5).write_file(root / "candidate_refine_con.cif")
    (root / "stage-2.cif").write_bytes((root / "candidate_refine_con.cif").read_bytes())
    stage(root, "native-second-pass")
    namespace["Rietveld_constrained_with_spacegroup"]("candidate", str(pattern))
    (root / "refined.cif").write_bytes((root / "candidate_refine_con_last.cif").read_bytes())
    stage(root, "final-export-validation")
    # Check before running independent diagnostics, so errors are classified correctly.
    Structure.from_file(root / "refined.cif")
    return {"recipe": "released two-pass PXRDGen example; corrected paths; unmodified GSAS-II CIF formatting",
            "export_policy": "released GSAS-II uncertainty-based formatting"}


def ab(task, root, pattern):
    source = Path(os.environ["REFINEMENT_SOURCES"]) / "Ab"
    spec = importlib.util.spec_from_file_location("pinned_ab_gsas", source / "gsas.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    os.environ["PXRD_TMP_ROOT"] = str(root / "tmp")
    os.environ["GSAS_MAX_CYC"] = "20"
    os.environ["GSAS_EARLY_EXIT_WR"] = "50"
    stage(root, "native-ab-refinement-and-export")
    values = module._refine_pxrd_impl(str(pattern), str(root / "input.cif"),
                                    str(source / "INST_XRY.PRM"),
                                    gpx_name=str(root / "ab.gpx"), gsas_log=str(root / "ab.log"))
    if values[0] is None or not values[3]:
        raise RuntimeError("Released Ab refinement failed")
    (root / "refined.cif").write_bytes(Path(values[3]).read_bytes())
    stage(root, "final-export-validation")
    from pymatgen.core import Structure
    Structure.from_file(root / "refined.cif")
    return {"recipe": "released Ab staged refinement; fitted-CIF export repair",
            "export_policy": "released GSAS-II uncertainty-based formatting",
            "native_reported_rwp": float(values[0])}


def real(task, root, pattern):
    from pymatgen.core import Structure
    from pymatgen.io.cif import CifWriter
    stage(root, "read-original-cif")
    original = Structure.from_file(root / "input.cif")
    # Normalize equivalent cell representation only, preserving all sites.
    CifWriter(original, symprec=None, significant_figures=12).write_file(root / "p1.cif")
    inst = instrument(root / "real.instprm", task["wavelength"])
    stage(root, "initialize-real-project")
    project, hist, phase = project_from(root / "p1.cif", pattern, inst, root / "real.gpx", True)
    project.data["Controls"]["data"]["max cyc"] = 20
    # GSAS atom pointers: coordinates/refinement flag/type/thermal marker.
    cx, ct, cs, cia = phase.data["General"]["AtomPtrs"]
    for atom in phase.data["Atoms"]:
        atom[cia] = "I"
        atom[cia + 1] = .01
    from pymatgen.core import Element
    held = max(range(len(phase.data["Atoms"])), key=lambda i: Element(phase.data["Atoms"][i][ct].strip()).Z)
    hist.set_refinements({"Background": {"type": "chebyschev-1", "no. coeffs": 4,
                                        "refine": False, "coeffs": [0., 0., 0., 0.]}})
    stage(root, "initial-profile-calculation")
    recalculate(project)
    arrays = hist.data["data"][1]
    scale, background, _ = linear_fit(np.asarray(arrays[0]), np.asarray(arrays[1]), np.asarray(arrays[3]) - np.asarray(arrays[4]))
    hist.data["Sample Parameters"]["Scale"][0] *= scale
    hist.data["Background"][0][3:7] = background.tolist()
    previous = recalculate(project)
    stage_records = []
    recipes = [
        ("background", {"set": {"Background": {"refine": True}}}),
        ("scale", {"set": {"Sample Parameters": ["Scale"]}}),
        ("profile", {"set": {"Instrument Parameters": ["U", "V", "W"]}}),
        ("cell", {"set": {"Cell": True}}),
        ("zero", {"set": {"Instrument Parameters": ["Zero"]}}),
        ("coordinates", {}), ("joint", {}),
    ]
    for number, (name, recipe) in enumerate(recipes, 1):
        stage(root, "real-" + name)
        snapshot = copy.deepcopy(project.data)
        record = {"stage": name, "before_rwp": previous, "accepted": False}
        try:
            if name == "coordinates":
                phase.set_refinements({"Atoms": {"all": "X"}})
                phase.data["Atoms"][held][cx - 1] = ""
            project.do_refinements([recipe])
            current = recalculate(project)
            hist, phase = project.histogram(0), project.phase(0)
            if not np.all(hist.data["data"][1][2] == 1):
                raise ValueError("GSAS changed uniform weights")
            out = export(phase, root / f"trial-{number}.cif")
            structure = Structure.from_file(out)
            distances = structure.distance_matrix + np.eye(len(structure)) * 1e6
            params = hist.data["Instrument Parameters"][0]
            u, v, w, zero = (params[k][1] for k in ("U", "V", "W", "Zero"))
            tangent = np.tan(np.radians(np.linspace(5, 80, 151) / 2))
            fwhm2 = (2.355 / 100) ** 2 * (u * tangent ** 2 + v * tangent + w)
            if (not np.isfinite(current) or current > previous + 1e-5 or
                not .75 <= structure.volume / original.volume <= 4 / 3 or
                distances.min() < .5 or abs(zero) > .15 or
                np.any(fwhm2 < .02 ** 2) or np.any(fwhm2 > .5 ** 2) or
                not structure.composition.fractional_composition.almost_equals(original.composition.fractional_composition)):
                raise ValueError("Residual, geometry, composition, or profile bound failed")
            record.update(accepted=True, after_rwp=current)
            previous = current
        except Exception as error:
            record["error"] = f"{type(error).__name__}: {error}"
            project.data = snapshot
            hist, phase = project.histogram(0), project.phase(0)
            project.save()
        export(phase, root / f"stage-{number}.cif")
        stage_records.append(record)
        write_json(root / "stages.json", stage_records)
    export(phase, root / "refined.cif")
    stage(root, "final-export-validation")
    return {"recipe": "paper-guided RealPXRD adapter (not released author refinement code)",
            "stages": stage_records, "native_after_rwp": previous,
            "scale_initialization": scale, "peak_fwhm_deg": .1}


def linear_fit(x, observed, calculated):
    calculated = np.asarray(calculated, dtype=float)
    maximum = float(np.max(np.abs(calculated)))
    if maximum <= 0 or not np.isfinite(maximum):
        raise ValueError("Empty simulated profile")
    background = np.polynomial.chebyshev.chebvander(np.linspace(-1, 1, len(x)), 3)
    design = np.column_stack((calculated / maximum, background))
    fit = lsq_linear(design, observed, bounds=([0., -np.inf, -np.inf, -np.inf, -np.inf], np.inf), tol=1e-12)
    if not fit.success:
        raise ValueError(f"Linear scale/background fit failed: {fit.message}")
    residual = 100 * np.sqrt(np.sum((observed - design @ fit.x) ** 2) / np.sum(observed ** 2))
    return float(fit.x[0] / maximum), fit.x[1:], float(residual)


def profile_start(x, y):
    """Observed-width initializer matching the repo's blind selector convention."""
    step = np.median(np.diff(x))
    diff = np.diff(y)
    noise = np.median(np.abs(diff - np.median(diff))) / .6744897501960817 / np.sqrt(2)
    prominence = max(6 * noise, .02 * (np.percentile(y, 99.9) - np.percentile(y, 10)), np.finfo(float).eps)
    peaks, properties = find_peaks(y, prominence=prominence, distance=max(2, round(.04 / step)))
    widths = peak_widths(y, peaks, rel_height=.5)[0] * step
    keep = (widths >= 1.5 * step) & (widths <= .5) & (x[peaks] >= x[0]+.5) & (x[peaks] <= x[-1]-.5)
    peaks, widths, prom = peaks[keep], widths[keep], properties["prominences"][keep]
    if len(peaks) > 30:
        selected = np.argsort(prom)[-30:]
        peaks, widths = peaks[selected], widths[selected]
    if len(peaks) < 3:
        return 5., float(np.clip((100 * max(6 * step, .08) / 2.355) ** 2, .25, 200))
    u, w = np.linalg.lstsq(np.column_stack((np.tan(np.radians(x[peaks]/2))**2, np.ones(len(peaks)))),
                          (100 * widths / 2.355) ** 2, rcond=None)[0]
    return float(np.clip(u, .1, 100)), float(np.clip(w, .25, 200))


def simulate(cif, x, inst, root, name, uiso=0.):
    from pymatgen.core import Structure
    from pymatgen.io.cif import CifWriter
    root.mkdir(exist_ok=True, parents=True)
    p1 = root / f"{name}.cif"
    CifWriter(Structure.from_file(cif), symprec=None, significant_figures=12).write_file(p1)
    project = scriptable().G2Project(newgpx=str(root / f"{name}.gpx"))
    phase = project.add_phase(str(p1), phasename="candidate", fmthint="CIF")
    cia = phase.data["General"]["AtomPtrs"][3]
    for atom in phase.data["Atoms"]:
        atom[cia] = "I"
        atom[cia+1] = uiso
    hist = project.add_simulated_powder_histogram(name, str(inst), float(x[0]), float(x[-1]),
            float(np.median(np.diff(x))), phases=[phase], scale=1.)
    project.data["Controls"]["data"]["max cyc"] = 0
    project.do_refinements([{}])
    xs, _, _, calc, bg, _ = hist.data["data"][1]
    return np.interp(x, np.asarray(xs), np.asarray(calc) - np.asarray(bg))


def diagnostic(task, root, x, y):
    u, w = (0., 18.0336880111) if task["method"] == "realpxrd-solver" else profile_start(x, y)
    inst = instrument(root / "diagnostic.instprm", task["wavelength"], u, w, task["method"] == "pxrdgen")
    output = {"profile_u": u, "profile_w": w, "weighting": "unit", "fitted": "nonnegative scale + four Chebyshev coefficients"}
    profiles = {"two_theta": x, "observed": y}
    for side, filename in (("before", "input.cif"), ("after", "refined.cif")):
        calc = simulate(root / filename, x, inst, root / "diagnostic", side, .01 if task["method"] == "realpxrd-solver" else 0.)
        scale, bg, residual = linear_fit(x, y, calc)
        output[side] = {"rwp_percent": residual, "scale": scale, "background": bg.tolist()}
        profiles[side] = calc * scale + np.polynomial.chebyshev.chebvander(np.linspace(-1, 1, len(x)), 3) @ bg
    np.savez_compressed(root / "paired-profiles.npz", **profiles)
    write_json(root / "paired-profile.json", output)
    return output


def run(task, root):
    x, y = observation(task)
    # Preserve native import/weighting for PXRDGen and Ab. Real uses explicit unit weights.
    pattern = root / ("observation.csv" if task["method"] == "ab-pxrd-solver" else "observation.xye")
    if task.get("self_target"):
        source = Path(os.environ["REFINEMENT_SOURCES"])
        if task["method"] == "realpxrd-solver":
            inst = instrument(root / "self.instprm", task["wavelength"])
        else:
            inst = source / ("PXRDGen/INST_XRY_Cu.PRM" if task["method"] == "pxrdgen" else "Ab/INST_XRY.PRM")
        y = simulate(root / "input.cif", x, inst, root / "self-target", "self", .01 if task["method"] == "realpxrd-solver" else 0.)
    if task["method"] == "ab-pxrd-solver":
        np.savetxt(pattern, np.column_stack((x, y)), delimiter=",", header="2theta,intensity", comments="")
    elif task["method"] == "pxrdgen":
        pattern = root / "observation.dat"
        np.savetxt(pattern, np.column_stack((x, y)), fmt="%.12g")
    else:
        np.savetxt(pattern, np.column_stack((x, y, np.ones_like(y))), fmt="%.12g")
    from common import time_limit
    with time_limit(task["timeout_seconds"]):
        result = {"pxrdgen": pxrdgen, "ab-pxrd-solver": ab, "realpxrd-solver": real}[task["method"]](task, root, pattern)
    # A diagnostic failure must not erase a successful structural refinement.
    try:
        result["paired_profile"] = diagnostic(task, root, x, y)
    except Exception as error:
        result["paired_profile_error"] = f"{type(error).__name__}: {error}"
    return result
