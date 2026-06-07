from dataclasses import replace

import numpy as np

from desensitized_interface_response import Config, make_grid, run_trial


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


def test_config_is_replace_compatible():
    cfg = replace(Config(), num_trials=2, seed=99)
    assert cfg.num_trials == 2
    assert cfg.seed == 99


if __name__ == "__main__":
    test_public_api_shapes_and_finiteness()
    test_config_is_replace_compatible()
    print("public interface checks passed")
