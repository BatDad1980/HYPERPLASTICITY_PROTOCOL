# hpp_secret_engine.py
# Layer A: The Secret Engine (Core Math & Models)
# Proprietary Hyperplasticity Protocol (HPP) V5 Node Routing and Plasticity Logic

from __future__ import annotations
import torch
from torch import nn
from torch.nn import functional as F
from dataclasses import dataclass

def make_clean_patterns(classes: int, dim: int, device: torch.device) -> torch.Tensor:
    """Generates the synthetic clean attractor representation vectors."""
    clean = F.normalize(torch.randn(classes, dim, device=device), dim=1)
    return clean * 2.5

def sample_batch(
    clean: torch.Tensor,
    *,
    batch: int,
    noise: float,
    distractor_scale: float,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Generates a batch of noisy input vectors, target attractors, and class labels."""
    labels = torch.randint(0, clean.shape[0], (batch,), device=device)
    targets = clean[labels]
    distractors = clean[torch.randint(0, clean.shape[0], (batch,), device=device)]
    inputs = targets + torch.randn_like(targets) * noise + distractors * distractor_scale
    return inputs, targets, labels

@dataclass
class HPPDevelopmentalMemory:
    """HPP V5 Developmental Memory with Staged Plasticity and Habit-14 Locking."""
    prototypes: torch.Tensor
    exposures: torch.Tensor
    threshold: int = 14
    learning_rate: float = 0.36
    distractor_learning_rate: float = 0.03

    def observe(self, x: torch.Tensor, labels: torch.Tensor, *, trusted: bool) -> None:
        """Plasticity updates based on exposure trust levels."""
        rate = self.learning_rate if trusted else self.distractor_learning_rate
        for label in labels.unique():
            mask = labels == label
            batch_mean = x[mask].mean(dim=0)
            index = int(label.detach().cpu())
            self.prototypes[index] = (1.0 - rate) * self.prototypes[index] + rate * batch_mean.detach()
            if trusted:
                self.exposures[index] += int(mask.sum().detach().cpu())

    def recall(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Node routing and protection using maturity-gated interpolation."""
        distances = torch.cdist(x, self.prototypes)
        labels = torch.argmin(distances, dim=1)
        selected = self.prototypes[labels]
        exposure = self.exposures[labels].float().to(x.device)
        maturity = torch.clamp((exposure - self.threshold) / max(self.threshold, 1), 0.0, 1.0)
        protection = (0.55 + 0.43 * maturity).unsqueeze(1)
        return x * (1.0 - protection) + selected * protection, labels

class NearestCentroidBaseline:
    """Standard Nearest Centroid prototype memory baseline."""
    def __init__(self, classes: int, dim: int, device: torch.device):
        self.prototypes = torch.zeros(classes, dim, device=device)
        self.counts = torch.zeros(classes, device=device)

    def observe(self, x: torch.Tensor, labels: torch.Tensor) -> None:
        for label in labels.unique():
            mask = labels == label
            index = int(label.detach().cpu())
            count = float(mask.sum().detach().cpu())
            batch_mean = x[mask].mean(dim=0)
            old_count = self.counts[index]
            total = old_count + count
            self.prototypes[index] = (self.prototypes[index] * old_count + batch_mean.detach() * count) / total
            self.counts[index] = total

    def recall(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        distances = torch.cdist(x, self.prototypes)
        labels = torch.argmin(distances, dim=1)
        return self.prototypes[labels], labels

class OnePassMLPDenoiser(nn.Module):
    """Conventional multi-layer perceptron denoiser baseline."""
    def __init__(self, dim: int, hidden: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, hidden),
            nn.GELU(),
            nn.Linear(hidden, hidden),
            nn.GELU(),
            nn.Linear(hidden, dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

class GRURefiner(nn.Module):
    """Conventional recurrent GRU refiner baseline."""
    def __init__(self, dim: int, hidden: int):
        super().__init__()
        self.in_proj = nn.Linear(dim, hidden)
        self.gru = nn.GRUCell(dim, hidden)
        self.out = nn.Linear(hidden, dim)

    def forward(self, x: torch.Tensor, passes: int = 4) -> torch.Tensor:
        hidden = torch.tanh(self.in_proj(x))
        state = x
        for _ in range(passes):
            hidden = self.gru(state, hidden)
            state = self.out(hidden)
        return state

def train_model(
    model: nn.Module,
    clean: torch.Tensor,
    *,
    steps: int,
    batch: int,
    noise: float,
    distractor_scale: float,
    lr: float,
    device: torch.device,
) -> list[float]:
    """Optimizes standard gradient-based baselines on the attractor targets."""
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    losses = []
    model.train()
    for _ in range(steps):
        x, target, _ = sample_batch(
            clean,
            batch=batch,
            noise=noise,
            distractor_scale=distractor_scale,
            device=device,
        )
        output = model(x)
        loss = F.mse_loss(output, target)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    model.eval()
    return losses

def train_memories(
    clean: torch.Tensor,
    *,
    classes: int,
    dim: int,
    exposures_per_class: int,
    batch: int,
    noise: float,
    distractor_scale: float,
    device: torch.device,
) -> tuple[HPPDevelopmentalMemory, NearestCentroidBaseline]:
    """Trains the prototype memory matrices (HPP and Nearest Centroid)."""
    hpp = HPPDevelopmentalMemory(
        prototypes=torch.zeros(classes, dim, device=device),
        exposures=torch.zeros(classes, device=device, dtype=torch.long),
    )
    nearest = NearestCentroidBaseline(classes, dim, device)
    total_observations = classes * exposures_per_class
    steps = max(1, total_observations // batch)

    for index in range(steps):
        trusted = index >= max(1, steps // 4)
        current_noise = noise * (1.25 if not trusted else 0.85)
        current_distractor = distractor_scale * (1.35 if not trusted else 0.65)
        x, target, labels = sample_batch(
            clean,
            batch=batch,
            noise=current_noise,
            distractor_scale=current_distractor,
            device=device,
        )
        hpp_signal = target if trusted else x
        hpp.observe(hpp_signal, labels, trusted=trusted)
        nearest.observe(x, labels)

    return hpp, nearest

def count_parameters(model: nn.Module) -> int:
    """Helper to count trainable parameters of a PyTorch Module."""
    return sum(p.numel() for p in model.parameters())
