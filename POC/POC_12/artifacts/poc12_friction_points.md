# POC-12 Friction Notes and Fixes

| Friction point | Impact | Fix |
|---|---|---|
| Using `python` failed on systems without alias | New users hit command-not-found | Standardized commands on `./venv/bin/python` |
| Missing workspace folder before `trestle init` | Initialization failed | Added explicit `mkdir -p` step |
| Users unsure what "success" looks like | Hard to self-verify | Added clear PASS/FAIL expectations in tutorial |
| Evidence files location unclear | Hard to prepare proposal appendix | Added explicit artifact paths section |
