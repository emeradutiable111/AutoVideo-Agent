from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Scene:
    """One renderable scene from a Markdown script."""

    index: int
    title: str
    visual: str
    narration: str
    duration: float = 3.0
    color: str = "#172033"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Project:
    title: str
    scenes: tuple[Scene, ...]
    source: str

    @property
    def duration(self) -> float:
        return sum(scene.duration for scene in self.scenes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "source": self.source,
            "duration": self.duration,
            "scene_count": len(self.scenes),
            "scenes": [scene.to_dict() for scene in self.scenes],
        }
