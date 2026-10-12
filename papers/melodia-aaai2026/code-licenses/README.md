# Melodia: Training-Free Music Editing Guided by Attention Probing in Diffusion Models (AAAI 2026)

[![arXiv](https://img.shields.io/badge/arXiv-2511.08252-b31b1b.svg)](https://arxiv.org/abs/2511.08252)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776ab.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[[🎵Demo Page]](https://melodia-edit.github.io/)** | **[[📄Paper]](https://arxiv.org/abs/2511.08252)**

---
## Overview

<p align="center">
  <img src="assets/framework.png" width="100%">
</p>

**Our method consists of two main stages:** (1) Partial DDIM Inversion with Attention Repository that stores self-attention features for structure preservation; (2) Reverse Process with Attention-based Structure Retention (ASR) that manipulates self-attention maps during denoising to achieve music editing while maintaining the original temporal structure.
