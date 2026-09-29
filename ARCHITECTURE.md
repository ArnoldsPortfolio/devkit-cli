CLI, POST /scans, and the GitHub Action all call ScanRepoUseCase (scan_repo).
Rules: no_todo, no_secret_like, trailing_space (safe fix).
Exit codes: 0 clean, 1 findings, 2 error.
