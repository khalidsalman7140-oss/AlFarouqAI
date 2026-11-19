# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""AlFarouq AI: explicit, lightweight, local-first AI orchestration."""
from .core import (Config, Result, Capability, Registry, AlFarouqError,
                   ValidationError, MissingDependency, ConsentRequired,
                   UnsupportedTask, __version__)
from .client import AI, Client
from .agents import AgentTeam, Step, Ref
from .documents import KnowledgeBase, SemanticIndex
__all__ = ['AI', 'Client', 'Config', 'Result', 'Capability', 'Registry',
           'AgentTeam', 'Step', 'Ref', 'KnowledgeBase', 'SemanticIndex',
           'AlFarouqError', 'ValidationError', 'MissingDependency',
           'ConsentRequired', 'UnsupportedTask', '__version__']

# Additive 0.2 interfaces; heavy engines remain lazily imported.
from .retrieval import VectorStore
from .automation import Scheduler, LLMAgent
from .learning import NeuralModel
from .models import prepare as prepare_model, inventory as model_inventory
__all__ += ['VectorStore', 'Scheduler', 'LLMAgent', 'NeuralModel', 'prepare_model', 'model_inventory']

from .arabic import TextModel
__all__ += ['TextModel']
from .shortcut import Model
__all__ += ['Model']

from .resources import environment, model_plan
__all__ += ['environment', 'model_plan']
