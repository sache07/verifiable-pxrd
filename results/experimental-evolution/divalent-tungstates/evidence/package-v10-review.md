# v10 design

v10 is a guidance-only replacement for v9. It preserves the prospectively
successful CIF-health, fixed-balance, constructed-analogue scale-test,
two-family weak-phase, low-index March and output-schema mechanisms. Both
helpers are byte-identical to v9: `cif_health.py` SHA-256
`2e2d8abc4d563ba2011772b21714716557ead17663556eb2db2d1c0c4ca2da7f`
and `stoichiometric_analogues.py` SHA-256
`0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`.

The 506-word guidance has SHA-256
`0c78056945d4b5dae405247c9e1d83444d510623b6845713bf8a0a1de4ac7176`.
It addresses only mechanisms observed across the three v9 failures:

- a failed bound/collapsed branch must reload saved pre-trial values; turning
  off flags does not neutralize fixed active physics;
- a physically meaningful boundary is retested at the boundary with
  complementary broadening rather than automatically treated as absence;
- topology, polymorph and same-composition coexistence decisions require an
  adequate matched baseline and must survive source, broadening and texture
  challenges rather than split a poor parent model;
- isolated low/middle/high family checks drive correction, while size and
  strain are tested one phase at a time and may be combined with supported
  symmetry-compatible anisotropy;
- covariance alone neither validates nor rejects a term; independent angular
  or family evidence and fresh replay distinguish physical shared-intensity
  effects from scale/background surrogates.

No case identity, hidden value, source identifier or case-specific lookup is
present. The first prospective screen remains limited to unresolved
b001-c03/c05/c06. The successful c04 and b002 controls remain set aside until
those three mechanisms pass.
