"""Root conftest: configure matplotlib to use a non-interactive backend."""

import matplotlib

matplotlib.use("Agg")
