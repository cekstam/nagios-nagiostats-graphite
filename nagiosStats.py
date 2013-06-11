#!/usr/bin/python
from subprocess import Popen, PIPE
import time
import socket
import datetime
import pickle
import struct

hostname = socket.gethostname()
hostname = hostname.replace('.', '_')

stats = {
  "AVGACTSVCLAT": ["AvgActiveServiceCheck-Latency", "AVG active service check latency (ms)."],
  "AVGACTSVCPSC": ["AvgActiveServiceCheck-PercentChange", "AVG active service check % state change."],
  "AVGACTSVCEXT": ["AvgActiveServiceCheck-ExecTime", "AVG active service check execution time (ms)."],
  "AVGSVCPSC": ["AvgServiceCheck-PercentChange", "AVG service check % state change."],
  "AVGHSTPSC": ["AvgHostCheck-PercentChange", "AVG host check % state change."],
  "AVGACTHSTLAT": ["AvgActiveHostCheck-Latency", "AVG active host check latency (ms)."],
  "AVGACTHSTPSC": ["AvgActiveHostCheck-PercentChange", "AVG active host check % state change."],
  "AVGACTHSTEXT": ["AvgActiveHostCheck-ExecTime", "AVG active host check execution time (ms)."],
  "AVGPSVHSTLAT": ["AvgPassiveHostCheck-Latency", "AVG passive host check latency (ms)."],
  "AVGPSVHSTPSC": ["AvgPassiveHostCheck-PercentChange", "AVG passive host check % state change."],
  "AVGPSVSVCLAT": ["AvgPassiveServiceCheck-Latency", "AVG passive service check latency (ms)."],
  "AVGPSVSVCPSC": ["AvgPassiveServiceCheck-PercentChange", "AVG passive service check % state change."],
  "NUMHSTACTCHK5M": ["HostsActivelyChecked-5Min", "number of hosts actively checked in last 5 minutes."],
  "NUMHSTACTCHK15M": ["HostsActivelyChecked-15Min", "number of hosts actively checked in last 15 minutes."],
  "NUMSVCACTCHK5M": ["ServicesActivelyChecked-5Min", "number of services actively checked in last 5 minutes."],
  "NUMSVCACTCHK15M": ["ServicesActivelyChecked-15Min", "number of services actively checked in last 15 minutes."],
  "NUMHSTPSVCHK5M": ["HostsPassivelyChecked-5Min", "number of hosts passively checked in last 5 minutes."],
  "NUMHSTPSVCHK15M": ["HostsPassivelyChecked-15Min", "number of hosts passively checked in last 15 minutes."],
  "NUMSVCPSVCHK5M": ["ServicesPassivelyChecked-5Min", "number of services passively checked in last 5 minutes."],
  "NUMSVCPSVCHK15M": ["ServicesPassivelyChecked-15Min", "number of services passively checked in last 15 minutes."],
  "NUMEXTCMDS5M": ["ExternalCommands-5Min", "number of external commands processed in last 5 minutes."],
  "NUMEXTCMDS15M": ["ExternalCommands-15Min", "number of external commands processed in last 15 minutes."],
  "NUMACTHSTCHECKS5M": ["ActiveHostChecks-5Min", "number of total active host checks occurring in last 5 minutes."],
  "NUMACTHSTCHECKS15M": ["ActiveHostChecks-15Min", "number of total active host checks occurring in last 15 minutes."],
  "NUMACTSVCCHECKS5M": ["ActiveServiceChecks-5Min", "number of total active service checks occurring in last 5 minutes."],
  "NUMACTSVCCHECKS15M": ["ActiveServiceChecks-15Min", "number of total active service checks occurring in last 15 minutes."],
  "NUMPSVHSTCHECKS5M": ["PassiveHostChecks-5Min", "number of passive host checks occurring in last 5 minutes."],
  "NUMPSVHSTCHECKS15M": ["PassiveHostChecks-15Min", "number of passive host checks occurring in last 15 minutes."],
  "NUMPSVSVCCHECKS5M": ["PassiveServiceChecks-5Min", "number of passive service checks occurring in last 5 minutes."],
  "NUMPSVSVCCHECKS15M": ["PassiveServiceChecks-15Min", "number of passive service checks occurring in last 15 minutes."],
  "NUMOACTSVCCHECKS5M": ["ActiveOnDemandServiceChecks-5Min", "number of on-demand active service checks occurring in last 5 minutes."],
  "NUMOACTSVCCHECKS15M": ["ActiveOnDemandServiceChecks-15Min", "number of on-demand active service checks occurring in last 15 minutes."],
  "NUMOACTHSTCHECKS5M": ["HostsOnDemandChecked-5Min", "number of on-demand active host checks occurring in last 5 minutes."],
  "NUMOACTHSTCHECKS15M": ["HostsOnDemandChecked-15Min", "number of on-demand active host checks occurring in last 15 minutes."],
  "NUMCACHEDSVCCHECKS5M": ["CachedServiceChecks-5Min", "number of cached service checks occurring in last 5 minutes."],
  "NUMCACHEDSVCCHECKS15M": ["CachedServiceChecks-15Min", "number of cached service checks occurring in last 15 minutes."],
  "NUMCACHEDHSTCHECKS5M": ["CachedHostChecks-5Min", "number of cached host checks occurring in last 5 minutes."],
  "NUMCACHEDHSTCHECKS15M": ["CachedHostChecks-15Min", "number of cached host checks occurring in last 15 minutes."],
  "NUMSACTSVCCHECKS5M": ["ScheduledActiveServiceChecks-5Min", "number of scheduled active service checks occurring in last 5 minutes."],
  "NUMSACTSVCCHECKS15M": ["ScheduledActiveServiceChecks-15Min", "number of scheduled active service checks occurring in last 15 minutes."],
  "NUMSACTHSTCHECKS5M": ["ScheduledHostChecks-5Min", "number of scheduled active host checks occurring in last 5 minutes."],
  "NUMSACTHSTCHECKS15M": ["ScheduledHostChecks-15Min", "number of scheduled active host checks occurring in last 15 minutes."],
  "NUMSERHSTCHECKS5M": ["SerialHostChecks-5Min", "number of serial host checks occurring in last 5 minutes."],
  "NUMSERHSTCHECKS15M": ["SerialHostChecks-15Min", "number of serial host checks occurring in last 15 minutes."],
  "NUMPARHSTCHECKS5M": ["ParallelHostChecks-5Min", "number of parallel host checks occurring in last 5 minutes."],
  "NUMPARHSTCHECKS15M": ["ParallelHostChecks-15Min", "number of parallel host checks occurring in last 15 minutes."],
  "NUMHSTPROB": ["HostProblems", "number of host problems (DOWN or UNREACHABLE)."],
  "NUMSVCPROB": ["ServiceProblems", "number of service problems (WARNING, UNKNOWN or CRITICAL)."],
  "NUMHSTUP": ["HostsUp", "number of hosts UP."],
  "NUMHSTDOWN": ["HostsDown", "number of hosts DOWN."],
  "NUMHSTUNR": ["HostsUnreachable", "number of hosts UNREACHABLE."],
  "NUMSVCOK": ["ServicesOK", "number of services OK."],
  "NUMSVCWARN": ["ServicesWarning", "number of services WARNING."],
  "NUMSVCCRIT": ["ServicesCritical", "number of services CRITICAL."],
  "NUMSVCUNKN": ["ServicesUnknown", "number of services UNKNOWN."],
  "NUMSVCFLAPPING": ["ServicesFlapping", "number of services that are currently flapping."],
  "NUMHSTFLAPPING": ["HostsFlapping", "number of hosts that are currently flapping."],
  "NUMHOSTS": ["TotalHosts", "total number of hosts."],
  "NUMSERVICES": ["TotalServices", "total number of services."],
  "NUMHSTDOWNTIME": ["HostsInDowntime", "number of hosts that are currently in downtime."],
  "NUMSVCDOWNTIME": ["ServicesInDowntime", "number of services that are currently in downtime."],
  "NUMHSTSCHEDULED": ["HostsSchedulesForChecks", "number of hosts that are currently scheduled to be checked."],
  "NUMSVCSCHEDULED": ["ServicesScheduledForChecks", "number of services that are currently scheduled to be checked."],
  "NUMHSTCHECKED": ["HostsCheckedSinceStart", "number of hosts that have been checked since start."],
  "NUMSVCCHECKED": ["ServicesCheckedSinceStart", "number of services that have been checked since start."],
  "TOTCMDBUF": ["ExternalBufferSlotsAvailable", "total number of external command buffer slots available."],
  "USEDCMDBUF": ["ExternalBufferSlotsInUse", "number of external command buffer slots currently in use."],
  "HIGHCMDBUF": ["ExternalBufferSlotsAlltimeMax", "highest number of external command buffer slots ever in use."],
}

def collectStats():
    carbonServer = "localhost"
    carbonPort = 2004
    sock = socket.socket()
    sock.connect((carbonServer, carbonPort))
    tuples = ([])
    binary = "/usr/local/nagios/bin/nagiostats"
    for stat, metaData in stats.items():
        metricName, descr = metaData
        command = binary + " --mrtg --data=" + stat
        nagprocess = Popen(command, shell=True, stderr=PIPE, stdout=PIPE, universal_newlines=True)
        stdout, stderr = nagprocess.communicate()
        stdout = stdout.splitlines()
        metricValue = stdout[0]
        tuples.append(('nagios.%s.%s' % (hostname, metricName), (int(time.time()), metricValue)))
    package = pickle.dumps(tuples, 1)
    size = struct.pack('!L', len(package))
    sock.sendall(size)
    sock.sendall(package)



if __name__ == "__main__":
    collectStats()
