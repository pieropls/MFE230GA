# Team inspection repository

Goal: give the team a private, bounded review copy of both completed 230GA studies and the original project documents.

Current state: package complete and validated; publication in progress. Contains the original briefing/specification, both studies’ exact source and numeric results, portable reports, 24 study figures, candidate/judge/audit evidence, bounded call journals and 28 offline tests. Raw archives, vendor downloads, intermediate panels, credentials and abandoned technical-run directories are excluded. See package_manifest.json for source/export hashes and omissions.

Validation: tools/verify_review_package.py passed 3,058 export hashes, both source inventories, 40 saved strategy ledgers, exact human labels and 106 links. All 28 tests pass. One exported mapping test now uses synthetic ZIP fixtures instead of omitted local archives; assertions unchanged. Both original local freezes still pass. No experimental source, results or selection changed. No experiment or model call rerun.

Interpretation: both studies conclude Do not implement. Opus is exploratory after the original test was seen; it changes model/effort and disclosed preflight instructions/screens together. Human review remains yes for items 5/11/15, no for the rest, with 10/17 machine agreement.

Next: publish to the authorized private repository, verify remote commit and visibility, then give the team access when usernames are supplied. Team critique and final course-submission review remain for the students. Do not retune or rerun the frozen experiments.
