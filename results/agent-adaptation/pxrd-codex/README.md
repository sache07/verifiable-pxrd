# pxrd-codex

This completed condition uses the same coding-agent benchmark contract as
`matsci-codex`, adding native GSAS-II and bare DICVOL14 while withholding learned skills
and workflow policy. One `gpt-5.6-sol` high API rollout with a one-hour cap per case
completed all 200 cases.

| Corpus | Selected only | Selected or declared alternative |
| --- | ---: | ---: |
| pXRD-100 | 58/100 | 59/100 |
| pXRD-ood | 56/100 | 58/100 |
| Combined | **114/200** | **117/200** |

`full-200-api-sol-high-r1/` retains the run contract and, for every case, the submitted
CIFs, exact verifier result, final response, and compressed chronological event trace.
