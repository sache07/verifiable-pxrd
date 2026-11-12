"""Run one researcher procedure on one copied solver project. Executes inside the evaluator sandbox.

python procedure_host.py SCRIPT_NAME
The procedure is called exactly as a solver would call a package helper:
    python SCRIPT /work/input.gpx /work/output.gpx /inputs
/procedure holds the snapshot (sibling .py files are importable), /inputs the case's public inputs,
and /work is the only writable directory. There is no network and no hidden truth in the sandbox.
"""
import pickle
import runpy
import sys


class InvalidProject(ValueError):
    pass


class ProjectUnpickler(pickle.Unpickler):
    """GSAS stores data as pickle; permit data constructors, never arbitrary code (the scorer's list)."""
    allowed = {('GSASII.GSASIIobj', 'G2VarObj'), ('GSASIIobj', 'G2VarObj'),
               ('builtins', 'object'), ('__builtin__', 'object'), ('builtins', 'set'), ('__builtin__', 'set'),
               ('builtins', 'frozenset'), ('__builtin__', 'frozenset'), ('builtins', 'complex'), ('__builtin__', 'complex'),
               ('_codecs', 'encode'), ('copyreg', '_reconstructor'), ('copy_reg', '_reconstructor'),
               ('collections', 'OrderedDict'), ('numpy', 'dtype'), ('numpy', 'ndarray'),
               ('numpy.core.multiarray', '_reconstruct'), ('numpy.core.multiarray', 'scalar'),
               ('numpy._core.multiarray', '_reconstruct'), ('numpy._core.multiarray', 'scalar'),
               ('numpy.core.numeric', '_frombuffer'), ('numpy._core.numeric', '_frombuffer'),
               ('numpy.ma.core', 'MaskedArray'), ('numpy.ma.core', '_mareconstruct')}

    def find_class(self, module, name):
        if (module, name) not in self.allowed:
            raise InvalidProject('Disallowed executable object in GSAS project: ' + module + '.' + name)
        return super().find_class(module, name)


def restricted_load(file, **kwargs):
    return ProjectUnpickler(file, **kwargs).load()


# Solver projects are untrusted input; install the guard before any GSAS-II import.
pickle.load = restricted_load

if __name__ == '__main__':
    script = '/procedure/' + sys.argv[1]
    sys.path.insert(0, '/procedure')
    sys.argv = [script, '/work/input.gpx', '/work/output.gpx', '/inputs']
    runpy.run_path(script, run_name='__main__')
