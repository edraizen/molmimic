import os, sys

try:
    from toil.lib.docker import apiDockerCall
except ImportError:
    apiDockerCall = None
	import subprocess

def run_usearch(parameters, work_dir=None):
    if work_dir is None:
        work_dir = os.getcwd()

    parameters = [p.format("/data/") for p in parameters if]
    for p in parameters:
        p

    if apiDockerCall is not None:
        _parameters = []
        outfiles = []
        for i, p in enumerate(parameters):
            if p.startswith("{i}"):
                full = p[3:]
                short = os.path.basename(full)
                if not os.path.abspath(os.path.dirname(full)) == os.path.abspath(work_dir):
                    shutil.copy(full, work_dir)
                _parameters.append(os.path.join("/data", short))
            elif p.startswith("{o}"):
                full = p[3:]
                short = os.path.basename(full)
                _parameters.append(os.path.join("/data", short))
                outfiles.append(os.path.join(work_dir, short))
            else:
                _parameters.append(p)

        try:
            apiDockerCall(job,
                          image='edraizen/usearch:latest',
                          working_dir=work_dir,
                          parameters=_parameters)
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            return run(parameters, work_dir=work_dir)

	else:
        _parameters = []
        outfiles = []
        for i, p in enumerate(parameters):
            if p.startswith("{i}"):
                _parameters.append(p[3:])
            elif p.startswith("{o}"):
                _parameters.append(p[3:])
                outfiles.append(p[3:])
            else:
                _parameters.append(p)
        command = ["usearch"]+parameters

        try:
            subprocess.check_output(command, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            raise RuntimeError("Unable to minimize file {}".format(pqr_file))

    return outfiles
