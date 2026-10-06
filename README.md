# Green

A clean and reliable Git utility & repository diagnostics tool.

## Overview
This repository provides helper utilities and diagnostics to verify Git author configurations, remote origin endpoints, branch status, and to ensure commits are properly attributed to your GitHub profile.

## Features
- **Git Identity Verification**: Checks if `user.name` and `user.email` are properly set.
- **Remote & Branch Diagnostics**: Verifies the active branch and origin remotes.
- **Attribution Checklist**: Validates prerequisites for GitHub contribution graph activity.
- **Safe Operations**: Avoids history alteration, forced pushes, or synthetic commit loops.

## Usage

Run the diagnostics script with Python 3:

```bash
python "green graph.py"
```

## GitHub Contribution Graph Troubleshooting
If your commits are not appearing on your GitHub contribution graph, check:
1. **Email Verification**: Ensure your local Git email (`git config user.email`) is added and verified in your [GitHub Email Settings](https://github.com/settings/emails).
2. **Default Branch**: Ensure commits are pushed to the default branch (usually `main`).
3. **Private Contributions**: If your repository is private, enable "Include private contributions on my profile" under your GitHub profile settings.
