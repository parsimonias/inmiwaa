#!/usr/bin/python

# http://stackoverflow.com/questions/29164661/monitoring-jdbc-connection-pools-on-webspere-7
# https://www.ibm.com/developerworks/websphere/techjournal/1112_guillemenot/1112_guillemenot.html?ca=drs-

def quetal(server,driver,datasource):
        perfStr = AdminControl.queryNames( 'type=Perf,process=' + server + ',*')
        if perfStr == "":
                print "Sorry I can't find server " + server
                sys.exit(1)
        perfObj = AdminControl.makeObjectName( perfStr)
        srvrStr = AdminControl.queryNames( 'type=Server,process=' + server + ',*')
        srvrObj = AdminControl.makeObjectName( srvrStr)
        stats = AdminControl.invoke_jmx( perfObj, 'getStatsObject', [ srvrObj, java.lang.Boolean('true')], ['javax.management.ObjectName', 'java.lang.Boolean'])
        try:
                waitingThreads=stats.getStats('connectionPoolModule').getStats(driver).getStats(datasource).getStatistic('WaitingThreadCount').getCurrent()
		print "stats: " + str(stats)
		print "stats.getStats('connectionPoolModule'): " + str(stats.getStats('connectionPoolModule'))
		print "stats.getStats('connectionPoolModule').getStats(driver): " + str(stats.getStats('connectionPoolModule').getStats(driver))
		print "stats.getStats('connectionPoolModule').getStats(driver).getStats(datasource): " + str(stats.getStats('connectionPoolModule').getStats(driver).getStats(datasource))
                poolSize=stats.getStats('connectionPoolModule').getStats(driver).getStats(datasource).getStatistic('PoolSize').getCurrent()
                freePoolSize=stats.getStats('connectionPoolModule').getStats(driver).getStats(datasource).getStatistic('FreePoolSize').getCurrent()
                percentUsed=stats.getStats('connectionPoolModule').getStats(driver).getStats(datasource).getStatistic('PercentUsed').getCurrent()
                print "WaitingThreadCount=" + str(waitingThreads) + ", PoolSize=" + str(poolSize) + ", FreePoolSize="  + str(freePoolSize) + ", PercentUsed=" + str(percentUsed)
        except:
                print "Ooops, something went wrong :("
                raise


def listServers():
        """List the servers Database Connection Pools"""
        servers = AdminControl.queryNames( 'type=Perf,*').split("\n")
        for i in range(0, len(servers)):
                srvName = servers[i].split(",")[1].split("=")[1]
                if srvName == "nodeagent":
                        continue
                print "Server: " + srvName
                perfStr = AdminControl.queryNames( 'type=Perf,process=' + srvName +',*')
                perfObj = AdminControl.makeObjectName( perfStr)
                srvrStr = AdminControl.queryNames( 'type=Server,process=' + srvName +',*')
                srvrObj = AdminControl.makeObjectName( srvrStr)
                stats = AdminControl.invoke_jmx( perfObj, 'getStatsObject', [ srvrObj, java.lang.Boolean('true')], ['javax.management.ObjectName', 'java.lang.Boolean'])
                for driver in stats.getStats('connectionPoolModule').subCollections():
                        print "\tDriver Name: " + driver.getName()
                        for datasource in stats.getStats('connectionPoolModule').getStats(driver.getName()).subCollections():
                                print "\t\tDatasource: " + datasource.getName()
				print quetal(srvName, driver.getName(), datasource.getName())

print listServers()
