from dataclasses import replace

import numpy as np

from desensitized_interface_response import Config, make_grid, run_trial


def _field_audit(result, cfg, grid):
    """Print non-scoring public hints about generic field structure.

    These checks intentionally avoid the hidden target trends.  They only tell
    the solver whether the returned arrays look like a resolved continuum
    evolution rather than constant placeholders or direct parameter echoes.
    """

    time = np.asarray(result["time"], dtype=float)
    rate = np.asarray(result["rate"], dtype=float)
    feedback = np.asarray(result["feedback_scalar"], dtype=float)
    surface = np.asarray(result["scalar_surface_mean"], dtype=float)
    scalar = np.asarray(result["scalar_samples"], dtype=float)

    start = max(0, time.size // 3)
    late_scalar = scalar[:, :, start:]
    spatial_scale = float(np.std(np.mean(late_scalar, axis=-1)))
    temporal_scale = float(np.mean(np.std(late_scalar, axis=-1)))
    rate_scale = float(np.std(rate[start:]))
    feedback_scale = float(np.std(feedback[start:]))
    surface_scale = float(np.std(surface[start:]))

    interface_depth = float(getattr(cfg, "interface_layer_depth", 2.0))
    interface_mask = np.asarray(grid.Z <= interface_depth)
    if np.any(interface_mask):
        interface_series = np.mean(scalar[interface_mask, :], axis=0)
        surface_mismatch = float(np.mean(np.abs(surface - interface_series)))
    else:
        surface_mismatch = float("inf")

    def label(value, floor):
        return "ok" if value > floor else "weak"

    print("PUBLIC_FIELD_AUDIT:")
    print(f"  spatial_resolution={label(spatial_scale, 1.0e-8)}")
    print(f"  temporal_evolution={label(temporal_scale + rate_scale + feedback_scale + surface_scale, 1.0e-8)}")
    print(f"  interface_local_diagnostic={'ok' if surface_mismatch < 0.5 else 'weak'}")
    print("  note=no score or hidden trend information is reported by this public check")


def test_public_api_shapes_and_finiteness():
    cfg = replace(Config(), t_total=8.0, nx=12, nz=8, history_window=4)
    grid = make_grid(cfg)
    rng = np.random.default_rng(123)
    result = run_trial(0.0, cfg, grid, rng, record_fields=True)

    time = np.asarray(result["time"], dtype=float)
    rate = np.asarray(result["rate"], dtype=float)
    feedback = np.asarray(result["feedback_scalar"], dtype=float)
    surface = np.asarray(result["scalar_surface_mean"], dtype=float)
    scalar = np.asarray(result["scalar_samples"], dtype=float)

    assert time.ndim == 1
    assert rate.shape == time.shape
    assert feedback.shape == time.shape
    assert surface.shape == time.shape
    assert scalar.shape == (cfg.nz, cfg.nx, time.size)

    assert np.all(np.isfinite(time))
    assert np.all(np.isfinite(rate))
    assert np.all(np.isfinite(feedback))
    assert np.all(np.isfinite(surface))
    assert np.all(np.isfinite(scalar))
    _field_audit(result, cfg, grid)


def test_config_is_replace_compatible():
    cfg = replace(Config(), num_trials=2, seed=99)
    assert cfg.num_trials == 2
    assert cfg.seed == 99


if __name__ == "__main__":
    test_public_api_shapes_and_finiteness()
    test_config_is_replace_compatible()
    print("public interface checks passed")
