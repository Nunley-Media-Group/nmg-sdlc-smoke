from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet
from nmg_sdlc_smoke.cli import main

scenarios("../convert_smoke_repository_to_a_python_sdlc_host.feature")

ROOT = Path(__file__).parents[3]


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the repository is an installable Python distribution nmg-sdlc-smoke-python with import package nmg_sdlc_smoke requiring Python 3.12+")
def installable_distribution() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text()
    assert 'name = "nmg-sdlc-smoke-python"' in pyproject
    assert 'requires-python = ">=3.12"' in pyproject


@when("a caller invokes greet with Ada")
def invoke_greet(context: dict[str, object]) -> None:
    context["greeting"] = greet("Ada")


@then("the function returns exactly Hello, Ada")
def exact_greeting(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"


@given("the distribution is installed with its console script")
def console_script_configured() -> None:
    assert 'nmg-smoke = "nmg_sdlc_smoke.cli:main"' in (ROOT / "pyproject.toml").read_text()


@when("nmg-smoke Ada is run")
def invoke_cli(context: dict[str, object], capsys: pytest.CaptureFixture[str]) -> None:
    context["exit_code"] = main(["Ada"])
    context["captured"] = capsys.readouterr()


@then("the process exits 0 and prints Hello, Ada followed by a single newline")
def exact_cli_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] == 0
    assert captured.out == "Hello, Ada\n"
    assert captured.err == ""


@given("a blank or whitespace-only name")
def blank_name(context: dict[str, object]) -> None:
    context["blank_name"] = " \t\n"


@when("greet is called or nmg-smoke is invoked with that name")
def invoke_invalid_paths(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    name = context["blank_name"]
    with pytest.raises(ValueError) as error:
        greet(name)  # type: ignore[arg-type]
    with pytest.raises(SystemExit) as exit_info:
        main([str(name)])
    context["library_error"] = error.value
    context["cli_exit"] = exit_info.value.code
    context["captured"] = capsys.readouterr()


@then("the library raises ValueError and the CLI exits non-zero without printing a greeting")
def invalid_paths_fail(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert str(context["library_error"]) == "name must not be blank"
    assert context["cli_exit"] == 1
    assert captured.out == ""


@given("a clean checkout on macOS, Linux, or Windows")
def platform_independent_checkout() -> None:
    assert (ROOT / "pyproject.toml").is_file()


@when("pytest, pytest-bdd features under tests/features/, and Ruff are run")
def verification_configured(context: dict[str, object]) -> None:
    context["pyproject"] = (ROOT / "pyproject.toml").read_text()
    context["feature"] = (
        ROOT / "tests/features/convert_smoke_repository_to_a_python_sdlc_host.feature"
    ).read_text()


@then(
    "every acceptance criterion has a Gherkin scenario, those commands exit 0, "
    "and results do not depend on machine-specific paths"
)
def verification_is_portable(context: dict[str, object]) -> None:
    pyproject = str(context["pyproject"])
    feature = str(context["feature"])
    assert all(f"@SCN{number:03d}" in feature for number in range(1, 8))
    assert "pytest-bdd" in pyproject and "ruff" in pyproject
    assert str(ROOT) not in feature


@given("a pull request or a push to main")
def ci_trigger() -> None:
    assert (ROOT / ".github/workflows/python-ci.yml").is_file()


@when("GitHub Actions Python CI is inspected")
def inspect_ci(context: dict[str, object]) -> None:
    context["ci"] = (ROOT / ".github/workflows/python-ci.yml").read_text()


@then("it installs the project, runs pytest including tests/features/, and runs Ruff on Python 3.12")
def ci_runs_python_checks(context: dict[str, object]) -> None:
    ci = str(context["ci"])
    for required in (
        'python-version: "3.12"',
        'python -m pip install -e ".[dev]"',
        "python -m pytest",
        "python -m pytest tests/features",
        "python -m ruff check .",
    ):
        assert required in ci


@then("the Node plugin workflows nmg-sdlc-verify.yml, skill-inventory-audit.yml, and sync-marketplace-pointer.yml are absent")
def node_workflows_absent() -> None:
    workflows = ROOT / ".github/workflows"
    for name in (
        "nmg-sdlc-verify.yml",
        "skill-inventory-audit.yml",
        "sync-marketplace-pointer.yml",
    ):
        assert not (workflows / name).exists()


@given("the converted working tree")
def converted_tree() -> None:
    assert ROOT.exists()


@when("it is inspected")
def inspect_tree() -> None:
    assert (ROOT / "src/nmg_sdlc_smoke").is_dir()


@then("copied plugin runtime workflows/, agents/, commands/, Node scripts/, OMP package.json, src/extension.ts, and other plugin specs/ are gone")
def plugin_runtime_absent() -> None:
    for path in ("workflows", "agents", "commands", "scripts", "package.json", "src/extension.ts"):
        assert not (ROOT / path).exists()
    legacy_plugin_specs = {
        "1-run-retro-skill",
        "2-plugin-scaffold-and-marketplace-infrastructure",
        "3-add-help-to-publish-approved-spec",
        "4-draft-issue-skill",
        "5-write-spec-skill",
        "6-write-code-skill",
        "7-verify-code-skill",
        "8-open-pr-skill",
        "9-add-execute-startup-retry-smoke-marker",
        "10-start-issue-skill",
        "11-add-live-smoke-a-lifecycle-verification-marker",
        "12-add-second-serial-lifecycle-smoke-marker",
        "17-add-third-serial-lifecycle-smoke-marker",
        "18-add-fourth-serial-lifecycle-smoke-marker",
        "21-migration-and-upgrade-skill",
        "23-add-live-smoke-259-a-controller-remediation-marker",
        "24-add-live-smoke-259-b-controller-remediation-marker",
        "31-add-live-smoke-214-c-success-path-marker",
        "66-onboard-project-skill",
        "86-add-address-pr-comments-skill-to-close-the-pr-review-loop",
        "106-simplify-skill",
        "125-add-github-actions-contribution-gates-to-project-setup",
        "145-add-lifecycle-status-command-for-active-sdlc-work",
        "151-remove-the-automated-sdlc-loop-and-unattended-mode",
        "193-reduce-injected-sdlc-workflow-tokens-while-keeping-file-command-surfaces",
        "194-move-start-and-execute-orchestration-into-controllers-behind-sibling-workers",
        "195-move-exact-head-delivery-into-a-controller-with-on-demand-remediation",
        "197-move-write-spec-publication-lifecycle-into-code-while-keeping-native-plan",
        "199-pass-github-ci-on-write-spec-spec-only-prs",
        "208-replace-execute-simplify-with-two-branch-to-main-review-and-fix-panes",
        "209-remove-draft-issue-run-total-ask-quota",
        "216-honor-passed-worker-handoff-after-prompt-wait-failure",
    }
    current_specs = {path.name for path in (ROOT / "specs").iterdir()}
    assert legacy_plugin_specs.isdisjoint(current_specs)


@then("LICENSE, 3.x VERSION synced to pyproject.toml, CHANGELOG history, the managed contribution gate, the managed issue form, and the AGENTS.md spec-context markers remain")
def delivery_contracts_remain() -> None:
    version = (ROOT / "VERSION").read_text().strip()
    assert version.startswith("3.")
    assert 'version = {file = "VERSION"}' in (ROOT / "pyproject.toml").read_text()
    assert (ROOT / "LICENSE").is_file()
    assert "## [" in (ROOT / "CHANGELOG.md").read_text()
    assert (ROOT / ".github/workflows/nmg-sdlc-contribution-gate.yml").is_file()
    assert (ROOT / ".github/ISSUE_TEMPLATE/nmg-sdlc-ready-issue.yml").is_file()
    agents = (ROOT / "AGENTS.md").read_text()
    assert "<!-- nmg-sdlc-managed: spec-context -->" in agents
    assert "<!-- /nmg-sdlc-managed -->" in agents


@given("a contributor opening README, CONTRIBUTING, AGENTS, and steering")
def contributor_docs(context: dict[str, object]) -> None:
    paths = [
        ROOT / "README.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "AGENTS.md",
        ROOT / "steering/manifest.json",
        ROOT / "steering/snippets/project-product.md",
        ROOT / "steering/snippets/project-tech.md",
        ROOT / "steering/snippets/project-structure.md",
    ]
    context["docs"] = "\n".join(path.read_text() for path in paths)


@when("they read current guidance")
def read_guidance(context: dict[str, object]) -> None:
    assert context["docs"]


@then("the documents describe this Python SDLC smoke host with src layout, pytest, pytest-bdd, Ruff, and VERSION synchronized with pyproject.toml")
def docs_describe_python_host(context: dict[str, object]) -> None:
    docs = str(context["docs"])
    for required in ("Python SDLC smoke host", "src", "pytest", "pytest-bdd", "Ruff", "VERSION", "pyproject.toml"):
        assert required in docs


@then("they do not describe an Oh My Pi plugin as the current product")
def docs_do_not_describe_plugin(context: dict[str, object]) -> None:
    assert "current product is an Oh My Pi plugin" not in str(context["docs"])
