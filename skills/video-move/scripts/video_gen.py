#!/usr/bin/env python3
"""
video_move/scripts/video_gen.py — provider-agnostischer Clip-Generator.

EIN Interface für Higgsfield / fal.ai / Replicate: submit -> poll -> download.
Provider-Tausch = eine Env-Var (VIDEO_PROVIDER) oder ein Funktions-Argument.

Kosten-Disziplin eingebaut:
  - Prompt-Hash-Cache: derselbe (provider, model, prompt, params) wird NIE zweimal bezahlt.
  - Dry-Run: GenSpec(resolution="480p") für billige Previews vor dem Final in 1080p.
  - Budget-Guard: optionales budget.json stoppt den Batch, bevor Credits trocken laufen.

Secrets NUR aus env (HF_KEY / FAL_KEY / REPLICATE_API_TOKEN). Nie hier hardcoden, nie committen.

Hinweis: Die exakten `arguments`-Keys je Modell-Endpoint (image_url vs. start_image,
duration int vs. str, ...) variieren. Sie sind in `_submit` gekapselt und über
`GenSpec.extra` überschreibbar. Beim ersten Einsatz eines neuen Modells das JSON-Schema
der Modell-Seite (fal/Replicate zeigen es direkt) prüfen — nicht raten.
"""
from __future__ import annotations

import abc
import hashlib
import json
import os
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path


# --------------------------------------------------------------------------- #
# Gemeinsame Spezifikation
# --------------------------------------------------------------------------- #
@dataclass
class GenSpec:
    prompt: str
    image: Path | None = None            # image-to-video Startframe (optional)
    duration: int = 5                    # 5 oder 10 s
    resolution: str = "720p"             # 480p (Dry-Run) / 720p / 1080p (Final)
    aspect_ratio: str = "16:9"           # 16:9 / 9:16 / 1:1
    negative_prompt: str = ""
    seed: int | None = None
    extra: dict = field(default_factory=dict)  # provider-spezifische Extras


# --------------------------------------------------------------------------- #
# Provider-Vertrag (Strategy-Pattern)
# --------------------------------------------------------------------------- #
class Provider(abc.ABC):
    name: str = "base"
    MODEL: str = ""

    @abc.abstractmethod
    def _submit(self, spec: GenSpec) -> str: ...      # -> job/request id

    @abc.abstractmethod
    def _poll(self, job_id: str) -> str: ...          # -> finale download-URL

    def _download(self, url: str, dest: Path) -> Path:
        dest.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest)
        return dest

    def generate(self, spec: GenSpec, dest: Path) -> Path:
        job = self._submit(spec)
        url = self._poll(job)
        return self._download(url, dest)


# --------------------------------------------------------------------------- #
# Higgsfield
# --------------------------------------------------------------------------- #
class HiggsfieldProvider(Provider):
    name = "higgsfield"
    MODEL = os.getenv("HF_VIDEO_MODEL", "higgsfield/dop/image-to-video")

    def __init__(self):
        import higgsfield_client as hf          # nutzt HF_KEY / HF_API_KEY+SECRET aus env
        self.hf = hf
        self._ctrls: dict[str, object] = {}

    def _submit(self, spec: GenSpec) -> str:
        args = {
            "prompt": spec.prompt,
            "duration": spec.duration,
            "resolution": spec.resolution,
            "aspect_ratio": spec.aspect_ratio,
            **spec.extra,
        }
        if spec.negative_prompt:
            args["negative_prompt"] = spec.negative_prompt
        if spec.seed is not None:
            args["seed"] = spec.seed
        if spec.image:
            args["image_url"] = self.hf.upload(str(spec.image))
        ctrl = self.hf.submit(self.MODEL, arguments=args)
        jid = getattr(ctrl, "request_id", str(id(ctrl)))
        self._ctrls[jid] = ctrl
        return jid

    def _poll(self, job_id: str) -> str:
        ctrl = self._ctrls[job_id]
        for status in ctrl.poll_request_status():
            if isinstance(status, self.hf.Completed):
                break
            if isinstance(status, (self.hf.Failed, self.hf.Cancelled, self.hf.NSFW)):
                raise RuntimeError(f"higgsfield {type(status).__name__}")
            time.sleep(3)
        res = ctrl.get()
        node = res.get("videos") or res.get("video") or res.get("output")
        if isinstance(node, list):
            return node[0]["url"] if isinstance(node[0], dict) else node[0]
        return node["url"] if isinstance(node, dict) else node


# --------------------------------------------------------------------------- #
# fal.ai
# --------------------------------------------------------------------------- #
class FalProvider(Provider):
    name = "fal"
    MODEL = os.getenv("FAL_VIDEO_MODEL", "fal-ai/kling-video/v2/master/image-to-video")

    def __init__(self):
        import fal_client                        # nutzt FAL_KEY aus env
        self.fal = fal_client

    def _submit(self, spec: GenSpec) -> str:
        args = {
            "prompt": spec.prompt,
            "duration": str(spec.duration),
            "aspect_ratio": spec.aspect_ratio,
            **spec.extra,
        }
        if spec.negative_prompt:
            args["negative_prompt"] = spec.negative_prompt
        if spec.seed is not None:
            args["seed"] = spec.seed
        if spec.image:
            args["image_url"] = self.fal.upload_file(str(spec.image))
        handler = self.fal.submit(self.MODEL, arguments=args)
        return handler.request_id

    def _poll(self, job_id: str) -> str:
        while True:
            st = self.fal.status(self.MODEL, job_id, with_logs=False)
            cls = type(st).__name__
            if cls == "Completed":
                break
            if cls in ("Failed", "Error"):
                raise RuntimeError("fal generation failed")
            time.sleep(3)
        res = self.fal.result(self.MODEL, job_id)
        return res["video"]["url"]


# --------------------------------------------------------------------------- #
# Replicate
# --------------------------------------------------------------------------- #
class ReplicateProvider(Provider):
    name = "replicate"
    # "owner/model:versionhash" — Version pinnen fuer Reproduzierbarkeit
    MODEL = os.getenv("REPLICATE_VIDEO_MODEL", "kwaivgi/kling-v2.1:PIN_VERSION_HASH")

    def __init__(self):
        import replicate                         # nutzt REPLICATE_API_TOKEN aus env
        self.rep = replicate
        self._preds: dict[str, object] = {}

    def _submit(self, spec: GenSpec) -> str:
        inp = {
            "prompt": spec.prompt,
            "duration": spec.duration,
            "aspect_ratio": spec.aspect_ratio,
            **spec.extra,
        }
        if spec.negative_prompt:
            inp["negative_prompt"] = spec.negative_prompt
        if spec.seed is not None:
            inp["seed"] = spec.seed
        if spec.image:
            inp["start_image"] = open(spec.image, "rb")
        _, _, ver = self.MODEL.partition(":")
        pred = self.rep.predictions.create(version=ver, input=inp)
        self._preds[pred.id] = pred
        return pred.id

    def _poll(self, job_id: str) -> str:
        pred = self._preds[job_id]
        pred.wait()                               # blockt bis terminal
        if pred.status != "succeeded":
            raise RuntimeError(f"replicate {pred.status}: {pred.error}")
        out = pred.output
        return out[0] if isinstance(out, list) else str(out)


PROVIDERS = {p.name: p for p in (HiggsfieldProvider, FalProvider, ReplicateProvider)}


def get_provider(name: str | None = None) -> Provider:
    name = name or os.getenv("VIDEO_PROVIDER", "fal")
    if name not in PROVIDERS:
        raise ValueError(f"unknown provider '{name}' (have: {list(PROVIDERS)})")
    return PROVIDERS[name]()          # instanziiert lazy -> prueft SDK/Auth erst hier


# --------------------------------------------------------------------------- #
# Kosten-Disziplin: Cache + Budget-Guard
# --------------------------------------------------------------------------- #
def cache_key(provider: str, model: str, spec: GenSpec) -> str:
    blob = json.dumps(
        {
            "prov": provider, "model": model, "prompt": spec.prompt,
            "neg": spec.negative_prompt, "dur": spec.duration,
            "res": spec.resolution, "ar": spec.aspect_ratio,
            "seed": spec.seed, "img": str(spec.image) if spec.image else None,
            "extra": spec.extra,
        },
        sort_keys=True,
    )
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def generate_cached(prov: Provider, spec: GenSpec, cache_dir: Path) -> Path:
    """Cache-Hit = 0 Credits. Key deckt Provider+Model+Prompt+alle Params ab."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = cache_key(prov.name, prov.MODEL, spec)
    dest = cache_dir / f"{prov.name}_{spec.resolution}_{key}.mp4"
    if dest.exists():
        return dest
    return prov.generate(spec, dest)


class BudgetGuard:
    """
    Stoppt einen Batch, BEVOR Credits trocken laufen. budget.json Beispiel:
      {"credits_remaining": 40.0, "cost_per_shot": 0.45, "spent": 0.0}
    Higgsfield-Credits sind verfallbar -> vor jedem Batch pruefen, nicht mittendrin scheitern.
    """
    def __init__(self, budget_file: Path):
        self.file = budget_file
        self.data = json.loads(budget_file.read_text()) if budget_file.exists() else {
            "credits_remaining": 0.0, "cost_per_shot": 0.0, "spent": 0.0
        }

    def can_afford(self, shots: int) -> bool:
        return self.data["cost_per_shot"] * shots <= self.data["credits_remaining"]

    def charge(self, shots: int = 1) -> None:
        cost = self.data["cost_per_shot"] * shots
        self.data["credits_remaining"] -= cost
        self.data["spent"] = self.data.get("spent", 0.0) + cost
        self.file.write_text(json.dumps(self.data, indent=2))


# --------------------------------------------------------------------------- #
# CLI (Smoke-Test / Einzel-Clip)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="video_move — Einzel-Clip generieren")
    ap.add_argument("prompt")
    ap.add_argument("-o", "--out", default="shot.mp4")
    ap.add_argument("-p", "--provider", default=None, help="higgsfield|fal|replicate")
    ap.add_argument("-r", "--resolution", default="480p", help="Dry-Run default 480p")
    ap.add_argument("-d", "--duration", type=int, default=5)
    ap.add_argument("-a", "--aspect", default="16:9")
    ap.add_argument("--image", default=None, help="Startframe fuer image-to-video")
    ap.add_argument("--cache", default="cache", help="Cache-Verzeichnis")
    args = ap.parse_args()

    spec = GenSpec(
        prompt=args.prompt,
        image=Path(args.image) if args.image else None,
        duration=args.duration,
        resolution=args.resolution,
        aspect_ratio=args.aspect,
    )
    prov = get_provider(args.provider)
    print(f"[video_move] provider={prov.name} model={prov.MODEL} res={spec.resolution}")
    path = generate_cached(prov, spec, Path(args.cache))
    # Final an Zielort kopieren (Cache bleibt als Wiederverwendung erhalten)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_bytes(path.read_bytes())
    print(f"[video_move] fertig -> {args.out}  (cache: {path})")
