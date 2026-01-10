"""
Tech Stack Analyzer Service

Analyzes a directory to detect programming languages, package managers,
and project characteristics. Used by the Setup Wizard to determine what
kind of Claude Code configuration to generate.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class TechStackInfo:
    """Result of tech stack analysis"""
    languages: List[str] = field(default_factory=list)
    package_managers: List[str] = field(default_factory=list)
    has_git: bool = False
    has_env_file: bool = False
    file_count: int = 0
    primary_language: Optional[str] = None
    confidence: str = "low"  # 'high', 'medium', 'low'


class TechStackAnalyzer:
    """Analyzes directory structure to detect tech stack"""

    # Directories to exclude from analysis
    EXCLUDE_DIRS = {
        "node_modules", "venv", ".venv", "venv_312", ".git",
        "__pycache__", "dist", "build", ".next", ".nuxt",
        "site-packages", ".pytest_cache", "target", "bin", "obj"
    }

    def analyze_directory(self, path: Path) -> TechStackInfo:
        """
        Analyze a directory to detect tech stack

        Args:
            path: Directory to analyze

        Returns:
            TechStackInfo with detected languages and tools
        """
        if not path.exists() or not path.is_dir():
            return TechStackInfo()

        info = TechStackInfo()

        # Detect each language
        info.has_git = self._has_git(path)
        info.has_env_file = (path / ".env").exists()

        # Language detection
        python_detected, python_pm = self._detect_python(path)
        js_detected, js_pm = self._detect_javascript(path)
        go_detected = self._detect_go(path)
        rust_detected = self._detect_rust(path)

        # Build languages list
        if python_detected:
            info.languages.append("python")
            if python_pm:
                info.package_managers.extend(python_pm)

        if js_detected:
            info.languages.append("javascript")
            if js_pm:
                info.package_managers.extend(js_pm)

        if go_detected:
            info.languages.append("go")
            info.package_managers.append("go mod")

        if rust_detected:
            info.languages.append("rust")
            info.package_managers.append("cargo")

        # Count code files
        info.file_count = self._count_code_files(path, info.languages)

        # Determine primary language (most code files)
        info.primary_language = self._determine_primary_language(path, info.languages)

        # Calculate confidence
        info.confidence = self._calculate_confidence(info)

        return info

    def is_valid_code_project(self, info: TechStackInfo) -> Tuple[bool, str]:
        """
        Determine if analyzed directory is a valid code project

        Args:
            info: TechStackInfo from analyze_directory

        Returns:
            (is_valid, reason_string)
        """
        # Has git repo
        if info.has_git and info.file_count > 0:
            return True, "Git repository with code files detected"

        # Has package manager files
        if info.package_managers:
            return True, f"Package manager detected: {', '.join(info.package_managers)}"

        # Has significant code files
        if info.file_count >= 3:
            return True, f"Found {info.file_count} code files"

        # Has at least one language detected
        if info.languages:
            return True, f"Code detected: {', '.join(info.languages)}"

        # Otherwise invalid
        if info.file_count == 0:
            return False, "No code files found in directory"

        return False, "Directory doesn't appear to be a code project"

    def _has_git(self, path: Path) -> bool:
        """Check if directory is a git repository"""
        return (path / ".git").exists()

    def _detect_python(self, path: Path) -> Tuple[bool, List[str]]:
        """
        Detect Python project

        Returns:
            (is_python, package_managers_list)
        """
        package_managers = []

        # Check for Python package manager files
        if (path / "requirements.txt").exists():
            package_managers.append("pip")

        if (path / "pyproject.toml").exists():
            package_managers.append("poetry/pip")

        if (path / "setup.py").exists() or (path / "setup.cfg").exists():
            package_managers.append("setuptools")

        if (path / "Pipfile").exists():
            package_managers.append("pipenv")

        # Check for .py files
        has_py_files = any(path.rglob("*.py"))

        # Python detected if has package manager files OR .py files
        is_python = bool(package_managers) or has_py_files

        return is_python, package_managers

    def _detect_javascript(self, path: Path) -> Tuple[bool, List[str]]:
        """
        Detect JavaScript/Node project

        Returns:
            (is_javascript, package_managers_list)
        """
        package_managers = []

        # Check for package manager files
        if (path / "package.json").exists():
            # Determine which package manager
            if (path / "package-lock.json").exists():
                package_managers.append("npm")
            elif (path / "yarn.lock").exists():
                package_managers.append("yarn")
            elif (path / "pnpm-lock.yaml").exists():
                package_managers.append("pnpm")
            else:
                package_managers.append("npm")  # Default to npm

        # Check for JS/TS files
        has_js_files = any(path.rglob("*.js")) or any(path.rglob("*.ts"))
        has_jsx_files = any(path.rglob("*.jsx")) or any(path.rglob("*.tsx"))

        # JavaScript detected if has package.json OR .js/.ts files
        is_javascript = bool(package_managers) or has_js_files or has_jsx_files

        return is_javascript, package_managers

    def _detect_go(self, path: Path) -> bool:
        """Detect Go project"""
        return (path / "go.mod").exists() or any(path.rglob("*.go"))

    def _detect_rust(self, path: Path) -> bool:
        """Detect Rust project"""
        return (path / "Cargo.toml").exists() or any(path.rglob("*.rs"))

    def _count_code_files(self, path: Path, languages: List[str]) -> int:
        """Count code files excluding common build/dependency directories"""
        extensions = []

        if "python" in languages:
            extensions.extend(["*.py"])
        if "javascript" in languages:
            extensions.extend(["*.js", "*.ts", "*.jsx", "*.tsx"])
        if "go" in languages:
            extensions.extend(["*.go"])
        if "rust" in languages:
            extensions.extend(["*.rs"])

        # If no specific languages, count common extensions
        if not extensions:
            extensions = ["*.py", "*.js", "*.ts", "*.jsx", "*.tsx", "*.go", "*.rs"]

        count = 0
        for ext in extensions:
            for file_path in path.rglob(ext):
                # Skip excluded directories
                if any(excluded in file_path.parts for excluded in self.EXCLUDE_DIRS):
                    continue
                count += 1

        return count

    def _determine_primary_language(self, path: Path, languages: List[str]) -> Optional[str]:
        """Determine primary language based on file count"""
        if not languages:
            return None

        if len(languages) == 1:
            return languages[0]

        # Count files for each language
        counts = {}
        for lang in languages:
            if lang == "python":
                counts[lang] = sum(1 for _ in path.rglob("*.py")
                                  if not any(ex in str(_) for ex in self.EXCLUDE_DIRS))
            elif lang == "javascript":
                js_count = sum(1 for _ in path.rglob("*.js")
                              if not any(ex in str(_) for ex in self.EXCLUDE_DIRS))
                ts_count = sum(1 for _ in path.rglob("*.ts")
                              if not any(ex in str(_) for ex in self.EXCLUDE_DIRS))
                counts[lang] = js_count + ts_count
            elif lang == "go":
                counts[lang] = sum(1 for _ in path.rglob("*.go")
                                  if not any(ex in str(_) for ex in self.EXCLUDE_DIRS))
            elif lang == "rust":
                counts[lang] = sum(1 for _ in path.rglob("*.rs")
                                  if not any(ex in str(_) for ex in self.EXCLUDE_DIRS))

        # Return language with most files
        if counts:
            return max(counts.items(), key=lambda x: x[1])[0]

        return languages[0]

    def _calculate_confidence(self, info: TechStackInfo) -> str:
        """Calculate confidence level in detection"""
        # High confidence: package manager + significant files
        if info.package_managers and info.file_count >= 5:
            return "high"

        # Medium confidence: package manager OR many files
        if info.package_managers or info.file_count >= 10:
            return "medium"

        # Low confidence: few indicators
        return "low"


# Singleton instance
_tech_stack_analyzer = None


def get_tech_stack_analyzer() -> TechStackAnalyzer:
    """Get singleton instance of TechStackAnalyzer"""
    global _tech_stack_analyzer
    if _tech_stack_analyzer is None:
        _tech_stack_analyzer = TechStackAnalyzer()
    return _tech_stack_analyzer
