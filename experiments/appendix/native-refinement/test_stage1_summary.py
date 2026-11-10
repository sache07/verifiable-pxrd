"""Keep paired stage-1 reporting separate from final-stage and oracle scores."""
import pytest

from summarize_structsnap_stage1 import summarize


def rows():
    return [dict(corpus=corpus, case=corpus + '-case', slot=slot,
                 before_exact=slot == 2, stage1_exact=slot == 1,
                 stage2_exact=False, before_cosine=.2, stage1_cosine=.4,
                 stage1_seconds=120., before_rwp=90., after_rwp=80.)
            for corpus in ('pxrd-100', 'pxrd-ood') for slot in range(1, 9)]


def test_first_candidate_not_oracle_or_stage2():
    result = summarize(rows())[-1]
    assert result['recovery']['pass_at_1'] == dict(n=2, before=0, after=2)
    assert result['recovery']['pass_at_8'] == dict(n=2, before=2, after=2)
    assert result['exact_candidates'] == dict(before=2, after=2, gained=2, lost=2)
    assert result['stage2_subset']['stage2'] == 0
    assert result['first_candidate_diagnostic_rwp'] == dict(
        n=2, mean_before=90., median_before=90., mean_after=80., median_after=80.)
    assert result['native_cosine']['all_candidates']['n'] == 16
    assert result['native_cosine']['first_candidates']['n'] == 2


def test_missing_candidate_is_not_a_failure():
    with pytest.raises(ValueError, match='Incomplete candidate set'):
        summarize(rows()[:-1])
