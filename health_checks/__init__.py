"""Health check detector registry."""

from typing import List, Type
from .base import BaseDetector

# Registry of all detector classes
_detectors: List[Type[BaseDetector]] = []


def register(detector_class: Type[BaseDetector]) -> Type[BaseDetector]:
    """Decorator to register a health check detector."""
    _detectors.append(detector_class)
    return detector_class


def get_all_detectors() -> List[BaseDetector]:
    """Return instances of all registered detectors."""
    return [cls() for cls in _detectors]


# Import all detectors to trigger registration
# Critical detectors
from .critical.bloated_claude_md import BloatedClaudeMdDetector
from .critical.secrets_exposed import SecretsExposedDetector
from .critical.mcp_overload import McpOverloadDetector
from .critical.no_gitignore import NoGitignoreDetector

# Warning detectors
from .warning.no_skills_dir import NoSkillsDirDetector
from .warning.no_commands_dir import NoCommandsDirDetector
from .warning.no_status_md import NoStatusMdDetector
from .warning.no_changelog_md import NoChangelogMdDetector
from .warning.no_planning_docs import NoPlanningDocsDetector
from .warning.no_architecture_md import NoArchitectureMdDetector
from .warning.model_not_set import ModelNotSetDetector
from .warning.thinking_not_enabled import ThinkingNotEnabledDetector
from .warning.no_agents_dir import NoAgentsDirDetector
from .warning.no_hooks import NoHooksDetector
from .warning.invalid_hook_keys import InvalidHookKeysDetector
from .warning.large_files import LargeFilesDetector
from .warning.no_tests_dir import NoTestsDirDetector
from .warning.no_readme import NoReadmeDetector

# Info detectors
from .info.no_init_command import NoInitCommandDetector
from .info.no_commit_command import NoCommitCommandDetector
from .info.no_worktrees import NoWorktreesDetector
from .info.no_github_actions import NoGithubActionsDetector
from .info.missing_env_example import MissingEnvExampleDetector

__all__ = [
    "BaseDetector",
    "register",
    "get_all_detectors",
    # Critical
    "BloatedClaudeMdDetector",
    "SecretsExposedDetector",
    "McpOverloadDetector",
    "NoGitignoreDetector",
    # Warning
    "NoSkillsDirDetector",
    "NoCommandsDirDetector",
    "NoStatusMdDetector",
    "NoChangelogMdDetector",
    "NoPlanningDocsDetector",
    "NoArchitectureMdDetector",
    "ModelNotSetDetector",
    "ThinkingNotEnabledDetector",
    "NoAgentsDirDetector",
    "NoHooksDetector",
    "InvalidHookKeysDetector",
    "LargeFilesDetector",
    "NoTestsDirDetector",
    "NoReadmeDetector",
    # Info
    "NoInitCommandDetector",
    "NoCommitCommandDetector",
    "NoWorktreesDetector",
    "NoGithubActionsDetector",
    "MissingEnvExampleDetector",
]
