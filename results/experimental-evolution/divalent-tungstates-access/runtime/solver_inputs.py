"""Solver inputs for synthetic cases, in the form LAB.md gives for the lab's experimental inputs.

A recipe's `sample` object holds the solver-visible sample description (for example precursors and a
firing temperature). LAB.md's `solver_inputs` declares those fields, the columns of pattern.csv, and a
metadata.json template. Template strings "{sample.NAME}" take the recipe's value; {"per_session": [...]}
takes one listed value per measurement session. Solvers receive exactly pattern.csv and metadata.json.
"""
import hashlib
import json
import math

TYPES = {'formula', 'formula_list', 'number', 'string'}


def _elements(formula):
    from pymatgen.core import Composition
    return {str(e) for e in Composition(formula).elements}


def _check_field(name, spec, value):
    kind = spec.get('type')
    if kind not in TYPES or set(spec) - {'type', 'items', 'range', 'choices', 'nullable', 'note'}:
        raise ValueError('Invalid sample field definition in LAB.md: ' + name)
    if value is None:
        if not spec.get('nullable'):
            raise ValueError('sample.%s is required' % name)
        return None
    if kind in ('formula', 'formula_list'):
        values = value if kind == 'formula_list' else [value]
        if kind == 'formula_list':
            low, high = spec.get('items', [1, 16])
            if not isinstance(value, list) or not low <= len(value) <= high or len(set(value)) != len(value):
                raise ValueError('sample.%s must list %s distinct formulas' % (name, low if low == high else '%d-%d' % (low, high)))
        for v in values:
            if not isinstance(v, str) or not v.strip():
                raise ValueError('sample.%s must contain formula strings' % name)
            try:
                _elements(v)
            except Exception:
                raise ValueError('sample.%s: cannot parse formula %r' % (name, v))
        return list(value) if kind == 'formula_list' else value
    if kind == 'number':
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError('sample.%s must be a number' % name)
        if 'range' in spec and not spec['range'][0] <= value <= spec['range'][1]:
            raise ValueError('sample.%s must lie in %s' % (name, spec['range']))
        return float(value)
    if not isinstance(value, str) or ('choices' in spec and value not in spec['choices']):
        raise ValueError('sample.%s must be %s' % (name, ('one of ' + str(spec['choices'])) if 'choices' in spec else 'a string'))
    return value


def check_sample(recipe, rows, protocol):
    """Validate the stated sample and return the elements a submission may use."""
    spec = protocol['generation']['solver_inputs']
    fields, sample = spec['sample_fields'], recipe.get('sample')
    if not isinstance(sample, dict) or set(sample) - set(fields):
        raise ValueError('sample must be an object with fields from LAB.md: ' + ', '.join(fields))
    values = {name: _check_field(name, fields[name], sample.get(name)) for name in fields}
    sources = spec['element_sources']
    ambient = set(sources['ambient'])
    supplied = []
    for name in sources['fields']:
        value = values.get(name)
        formulas = value if isinstance(value, list) else [value] if value else []
        supplied += [(f, _elements(f)) for f in formulas]
    allowed = set().union(*(e for _, e in supplied)) | ambient
    present = set().union(*(set(r['composition']) for r in rows))
    if present - allowed:
        raise ValueError('Phases contain elements the stated sample does not supply: ' + ', '.join(sorted(present - allowed)))
    if sources.get('each_source_element_present'):
        unused = [f for f, e in supplied if not (e - ambient) <= present]
        if unused:
            raise ValueError('Every element of %s (other than %s) must appear in some phase: %s'
                             % ('/'.join(sources['fields']), ', '.join(sorted(ambient)), ', '.join(unused)))
    return values, sorted(allowed)


def _fill(template, values, session):
    if isinstance(template, dict):
        if set(template) == {'per_session'}:
            options = template['per_session']
            return options[int(hashlib.sha256(session.encode()).hexdigest(), 16) % len(options)]
        return {k: _fill(v, values, session) for k, v in template.items()}
    if isinstance(template, list):
        return [_fill(v, values, session) for v in template]
    if isinstance(template, str) and template.startswith('{sample.') and template.endswith('}'):
        return values[template[len('{sample.'):-1]]
    return template


def write_inputs(public, x, observed, recipe, values, protocol):
    spec = protocol['generation']['solver_inputs']
    newline = {'lf': '\n', 'crlf': '\r\n'}[spec['line_ending']]
    lines = [','.join(spec['pattern_columns'])] + [f'{round(float(a), 8)!r},{float(b)!r}' for a, b in zip(x, observed)]
    (public / 'pattern.csv').write_text(newline.join(lines) + newline)
    session = recipe.get('measurement_session') or recipe['id']
    metadata = _fill(spec['metadata'], values, session)
    (public / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
