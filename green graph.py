#!/usr/bin/env python3
"""
Green Repository Utility & Git Diagnostic Tool

A safe, reliable Git management script that:
- Verifies local Git configuration (name, email) for proper GitHub attribution.
- Checks origin remote and branch alignment.
- Performs repository health checks and provides contribution graph diagnostics.
- Avoids fake commit generation, history rewriting, or forced pushes.
"""

import os
import subprocess
import sys
from typing import List, Optional, Tuple

# Terminal color formatting
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run_git_command(args: List[str], cwd: Optional[str] = None) -> Tuple[int, str, str]:
    """
    Executes a Git command safely using raw argument lists without shell injection.
    
    Args:
        args: List of command arguments (e.g. ['git', 'status'])
        cwd: Directory where the command should be run
        
    Returns:
        Tuple of (returncode, stdout_str, stderr_str)
    """
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except FileNotFoundError:
        return 127, "", "Error: 'git' command not found. Please ensure Git is installed and in PATH."
    except Exception as exc:
        return 1, "", f"Unexpected execution error: {exc}"


def get_git_config(key: str) -> Optional[str]:
    """Retrieve a Git configuration value."""
    code, stdout, _ = run_git_command(["git", "config", "--get", key])
    return stdout if code == 0 and stdout else None


def check_git_status() -> bool:
    """Check and display repository diagnostics and contribution graph prerequisites."""
    print(f"\n{BOLD}{CYAN}=== Git Repository Diagnostics & Configuration ==={RESET}\n")

    # 1. Author and Email Configuration
    user_name = get_git_config("user.name")
    user_email = get_git_config("user.email")

    print(f"{BOLD}1. Git Identity:{RESET}")
    if user_name:
        print(f"   - User Name : {GREEN}{user_name}{RESET}")
    else:
        print(f"   - User Name : {RED}Not configured! Set via `git config user.name <name>`{RESET}")

    if user_email:
        print(f"   - User Email: {GREEN}{user_email}{RESET}")
    else:
        print(f"   - User Email: {RED}Not configured! Set via `git config user.email <email>`{RESET}")

    # 2. Remote Origin Configuration
    code, remote_out, _ = run_git_command(["git", "remote", "-v"])
    print(f"\n{BOLD}2. Remotes:{RESET}")
    if code == 0 and remote_out:
        for line in remote_out.splitlines():
            print(f"   - {line}")
    else:
        print(f"   - {YELLOW}No remotes configured.{RESET}")

    # 3. Current Branch
    code, branch_out, _ = run_git_command(["git", "branch", "--show-current"])
    current_branch = branch_out if code == 0 and branch_out else "unknown"
    print(f"\n{BOLD}3. Active Branch:{RESET}")
    print(f"   - Branch: {GREEN}{current_branch}{RESET}")

    # 4. Working Tree Status
    code, status_out, _ = run_git_command(["git", "status", "--short"])
    print(f"\n{BOLD}4. Working Tree Status:{RESET}")
    if code == 0:
        if status_out:
            print(f"   - Uncommitted changes detected:\n{YELLOW}{status_out}{RESET}")
        else:
            print(f"   - {GREEN}Working tree is clean.{RESET}")
    else:
        print(f"   - {RED}Failed to get git status.{RESET}")

    # 5. Contribution Graph Attribution Guide
    print(f"\n{BOLD}{CYAN}=== GitHub Contribution Graph Attribution Checklist ==={RESET}")
    print("For commits to turn green on your GitHub contribution graph:")
    print(" 1. The email used to author the commits must match an email verified in your GitHub account.")
    print("    (Check: https://github.com/settings/emails)")
    print(" 2. Commits must be made in the repository's default branch (usually 'main') or gh-pages.")
    print(" 3. Commits must be pushed to a repository owned by you or a repository you have contributed to.")
    print(" 4. If the repository is private, enable 'Private contributions' in your GitHub profile settings.")
    print(" 5. Avoid fake timestamps or rewriting history; GitHub evaluates real pushed commits.\n")

    return True


def stage_and_commit(message: str) -> bool:
    """
    Safely stage tracked/modified files and create a genuine commit.
    
    Args:
        message: Descriptive commit message
    """
    if not message.strip():
        print(f"{RED}Error: Commit message cannot be empty.{RESET}")
        return False

    code, _, err = run_git_command(["git", "add", "-A"])
    if code != 0:
        print(f"{RED}Failed to stage changes: {err}{RESET}")
        return False

    code, out, err = run_git_command(["git", "commit", "-m", message])
    if code == 0:
        print(f"{GREEN}✔ Commit successful:{RESET}\n{out}")
        return True
    elif "nothing to commit" in out or "nothing to commit" in err:
        print(f"{YELLOW}Notice: No changes to commit.{RESET}")
        return True
    else:
        print(f"{RED}Commit failed: {err or out}{RESET}")
        return False


def push_to_origin(branch: str = "main") -> bool:
    """
    Safely push commits to origin on the specified branch without force-pushing.
    
    Args:
        branch: Target branch name (default 'main')
    """
    print(f"\n{CYAN}Pushing changes to origin/{branch}...{RESET}")
    code, out, err = run_git_command(["git", "push", "origin", branch])
    if code == 0:
        print(f"{GREEN}✔ Successfully pushed to origin/{branch}!{RESET}")
        if out:
            print(out)
        return True
    else:
        print(f"{RED}Push failed with return code {code}.{RESET}")
        if err:
            print(f"{RED}Error: {err}{RESET}")
        return False


if __name__ == "__main__":
    check_git_status()
