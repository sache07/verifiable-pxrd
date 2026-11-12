# Matched P0 experimental baseline

45 fresh attempts: three on each of the same 15 experimental Precursor Genome scans. P0 is exactly the unlearned task prefix of frozen autonomous v6, including the final.gpx requirement. No learned guidance or helper scripts are supplied.

Identical Sol gpt-5.6-sol/high, raw CSV/metadata hashes, filtered COD 2024, scientific tools, isolation, 2 CPU quota / 5 GiB per worker, and no solver time limit. No references, prior outputs, or canonical solutions are visible to workers.

Wait until all 45 v6 attempts have launched, then fill the slots they release, keeping shared-host concurrency at most 16. This avoids waiting for the last v6 straggler before beginning P0. No existing attempt is restarted. Each attempt is unique and receives its own workspace/session. Preserve failures in the result table; do not silently replace them. Both panels are development evaluation.

The only intended scientific intervention is v6's learned guidance and seven helpers. Assess matched P0 versus v6 using all three outcomes per case, native-project replay with fitted calibration preserved, common original-data Rwp, phase inventories/fractions and geometry. Do not invent a synthetic score for experimental scans or treat every disagreement with Ceder as an error.

Monitoring and artifact copies run without model polling; detailed comparison begins once all 90 records are terminal.
