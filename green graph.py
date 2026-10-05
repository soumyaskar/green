import subprocess
import sys
import os
import random
from datetime import datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Realistic developer commit messages
REALISTIC_MESSAGES = [
    "Fix minor bug in API response handler",
    "Refactor utility functions for better readability",
    "Update project documentation and comments",
    "Optimize rendering performance in core loop",
    "Add unit tests for edge case scenarios",
    "Improve styling and responsive UI layout",
    "Clean up redundant imports and unused variables",
    "Update dependency configurations",
    "Fix typo in error logging messages",
    "Enhance validation logic for user input",
    "Implement helper methods for data processing",
    "Format code according to project style guide",
    "Patch potential memory leak in listener hook",
    "Add fallback handling for network timeout",
    "Improve state management logic",
    "Update environment variables schema",
    "Adjust theme colors and contrast ratio",
    "Refactor component structure for reusability",
    "Fix issue with date parsing in edge cases",
    "Optimize assets and reduce bundle size",
    "Add type definitions and interface declarations",
    "Improve accessibility tags and aria labels",
    "Tweak animation duration and easing curves",
    "Add error boundary wrapper for resilience",
    "Sync config files with latest specs",
    "Update test coverage and assertions",
    "Minor tweak to logging format",
    "Cache computation results for faster lookup",
    "Fix edge case in pagination logic",
    "Clean up temporary debug statements",
    "Standardize error codes across modules",
    "Improve form validation feedback",
    "Refactor constants into separate module",
    "Fix race condition in async handler",
    "Update README with latest setup instructions"
]

def generate_random_time(date_obj, commit_index, total_commits):
    """Generate realistic, sequentially ordered times throughout the day."""
    start_hour = 9   # 9:00 AM
    end_hour = 23    # 11:00 PM
    
    slot_hours = (end_hour - start_hour) / max(total_commits, 1)
    hour = int(start_hour + (commit_index * slot_hours) + random.uniform(0, slot_hours * 0.8))
    hour = min(max(hour, 9), 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    return date_obj.strftime(f"%Y-%m-%dT{hour:02d}:{minute:02d}:{second:02d}")

def get_random_commit_count():
    """
    Randomized natural distribution (kabhi 1, 2, 3, 4, 5):
    - 1 commit: 35%
    - 2 commits: 35%
    - 3 commits: 18%
    - 4 commits: 8%
    - 5 commits: 4%
    """
    choices = [1, 2, 3, 4, 5]
    weights = [35, 35, 18, 8, 4]
    return random.choices(choices, weights=weights)[0]

def rebuild_clean_history(start_date, end_date):
    total_days = (end_date.date() - start_date.date()).days + 1
    print(f"\n{CYAN}⚡ Building clean randomized commits from {YELLOW}{start_date.strftime('%Y-%m-%d')}{CYAN} to {YELLOW}{end_date.strftime('%Y-%m-%d')}{CYAN} ({total_days} days)...{RESET}\n")

    # Save current files content
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()
    with open("green_graph.py", "r", encoding="utf-8") as f:
        script_content = f.read()

    # Update git remote to new repository
    subprocess.run(["git", "remote", "set-url", "origin", "https://github.com/soumyaskarl/green.git"], check=False)

    # Create fresh orphan branch
    subprocess.run(["git", "checkout", "--orphan", "clean-streak-gre"], check=True)
    subprocess.run(["git", "rm", "-rf", "."], check=True)

    # Restore files
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    with open("green_graph.py", "w", encoding="utf-8") as f:
        f.write(script_content)

    subprocess.run(["git", "add", "README.md", "green_graph.py"], check=True)

    env = os.environ.copy()
    first_date_str = start_date.strftime("%Y-%m-%dT09:15:00")
    env["GIT_COMMITTER_DATE"] = first_date_str
    env["GIT_AUTHOR_DATE"] = first_date_str
    subprocess.run(["git", "commit", "-m", "Initial commit: Set up repository tooling and documentation"], env=env, check=True)

    total_commits = 1

    for i in range(total_days):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        
        num_commits = get_random_commit_count()
        total_commits += num_commits
        
        daily_messages = random.sample(REALISTIC_MESSAGES, min(num_commits, len(REALISTIC_MESSAGES)))

        for c_idx in range(num_commits):
            formatted_date = generate_random_time(current_date, c_idx, num_commits)
            env["GIT_COMMITTER_DATE"] = formatted_date
            env["GIT_AUTHOR_DATE"] = formatted_date
            
            msg = daily_messages[c_idx]
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", msg],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    # Replace main branch
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    print(f"\n{GREEN}🎉 Created {YELLOW}{total_commits}{GREEN} natural randomized commits across {YELLOW}{total_days}{GREEN} days ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})!{RESET}")
    print(f"{CYAN}Pushing to https://github.com/soumyaskar/green_graph.git...{RESET}")

    push_result = subprocess.run(["git", "push", "--force", "-u", "origin", "main"])
    if push_result.returncode == 0:
        print(f"\n{GREEN}✔ Successfully pushed to green_graph repository!{RESET}\n")
    else:
        print(f"\n{RED}Push failed with code {push_result.returncode}.{RESET}\n")

if __name__ == "__main__":
    start_date = datetime(2026, 1, 1)
    end_date = datetime.now()
    rebuild_clean_history(start_date, end_date)
