"""Operator launcher for this version only. Starts no researcher or solver itself."""
from pathlib import Path
import json
import subprocess
import sys
from common import ROOT, CORE, read, remote, frozen_code_ok

frozen_code_ok()
settings=read(ROOT/'control/settings.json')
prefix=settings['service_prefix'];session=settings['tmux_session']
tmux=['tmux','-L',settings['tmux_socket']]
# A separate shared authentication path is configured on EC2 by the operator;
# credential contents never enter this project or the research sandbox.
remote('test','-f',ROOT/'control/auth/auth.json')
remote(CORE,'-c',"from pathlib import Path; import sys; sys.path.insert(0,"+repr(str(ROOT/'control'))+"); from common import frozen_code_ok; frozen_code_ok()")
exists=remote(*tmux,'has-session','-t',session,check=False,timeout=10)
if exists.returncode:
    remote(*tmux,'new-session','-d','-s',session,'-n','overview',
           CORE+' '+str(ROOT/'control/view.py'),timeout=10)
unit=Path.home()/'.config/systemd/user'/(prefix+'-controller.service')
unit.parent.mkdir(parents=True,exist_ok=True)
unit.write_text('[Unit]\nDescription=PXRD evolution request controller ('+prefix+')\nAfter=network-online.target\n\n'
    '[Service]\nType=simple\nWorkingDirectory='+str(ROOT)+'\nExecStart='+CORE+' '+str(ROOT/'control/broker.py')+
    '\nRestart=on-failure\nRestartSec=10\nEnvironment=PYTHONDONTWRITEBYTECODE=1\n\n[Install]\nWantedBy=default.target\n')
monitor_unit = unit.parent / (prefix + '-monitor.service')
monitor_unit.write_text('[Unit]\nDescription=PXRD process monitor\nPartOf='+prefix+'-controller.service\n'
    'After='+prefix+'-controller.service\n\n[Service]\nType=oneshot\nWorkingDirectory='+str(ROOT)+
    '\nExecStart='+CORE+' '+str(ROOT/'control/process_monitor.py')+
    '\nTimeoutStartSec=360\nKillMode=control-group\nCPUQuota=100%\nMemoryMax=2G\nTasksMax=128\n'
    'Environment=PYTHONDONTWRITEBYTECODE=1\n')
timer = unit.parent / (prefix + '-monitor.timer')
timer.write_text('[Unit]\nDescription=Review PXRD research progress every 30 minutes\nPartOf='+prefix+'-controller.service\n'
    '\n[Timer]\nOnActiveSec=30min\nOnUnitActiveSec=30min\nAccuracySec=30s\nUnit='+prefix+'-monitor.service\n'
    '\n[Install]\nWantedBy=timers.target\n')
subprocess.run(['systemctl','--user','daemon-reload'],check=True)
subprocess.run(['systemctl','--user','enable','--now',prefix+'-controller'],check=True)
subprocess.run(['systemctl','--user','enable','--now',prefix+'-monitor.timer'],check=True)
print(json.dumps({'controller':prefix+'-controller','tmux':session,
                  'researcher_launched':False,'monitor_interval_minutes':30,
                  'scope':'Only this version; existing controllers untouched.'}))
