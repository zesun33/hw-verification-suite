"""poisson.py — Biological Poisson Spike Stream & Sparsity Generators."""

import random
from typing import List


class PoissonSpikeGenerator:
    """Generates independent Bernoulli/Poisson spike vectors across N channels."""

    def __init__(self, num_channels: int = 8, seed: int = 42):
        self.num_channels = num_channels
        self.rng = random.Random(seed)

    def generate_vector(self, rate_lambda: float) -> int:
        """Generates an integer bitmask of spikes with probability rate_lambda per channel."""
        vector = 0
        for ch in range(self.num_channels):
            if self.rng.random() < rate_lambda:
                vector |= (1 << ch)
        return vector

    def generate_sweep(self, num_timesteps: int, min_rate: float = 0.10, max_rate: float = 0.90) -> List[int]:
        """Generates a list of spike vectors sweeping from min_rate to max_rate."""
        vectors = []
        for t in range(num_timesteps):
            rate = min_rate + (max_rate - min_rate) * (t / max(1, num_timesteps - 1))
            vectors.append(self.generate_vector(rate))
        return vectors
