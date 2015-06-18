#!/usr/bin/python

# get line separator
import  java.lang.System  as sys
lineSeparator = sys.getProperty('line.separator')

fCSV = open("hostname.csv", "w")
fCSV.write('cell;node;server;app;lib\n')

cells = AdminConfig.list('Cell').split()
for cell in cells:
    cname = AdminConfig.showAttribute(cell, 'name')

    nodes = AdminConfig.list('Node', cell).split()
    for node in nodes:
        nname = AdminConfig.showAttribute(node, 'name')

        servs = AdminControl.queryNames('type=Server,cell=' + cname + ',node=' + nname + ',*').split()
        print "Número de servidores en ejecución en el nodo %s: %s" % (nname, len(servs))
        for server in servs:
            sname = AdminControl.getAttribute(server, 'name')

            ptype = AdminControl.getAttribute(server, 'processType')
            pid   = AdminControl.getAttribute(server, 'pid')
            state = AdminControl.getAttribute(server, 'state')
            jvm = AdminControl.queryNames('type=JVM,cell=' + cname + ',node=' + nname + ',process=' + sname + ',*')
            osname = AdminControl.invoke(jvm, 'getProperty', 'os.name')
            print " %s %s has pid %s; state: %s; on %s" % (sname, ptype, pid, state, osname)
            if ptype == 'ManagedProcess':
                # running apps
                apps = AdminControl.queryNames('type=Application,cell=' + cname + ',node=' + nname + ',process=' + sname + ',*').splitlines()
                print "  Número de aplicaciones en ejecución en %s: %s" % (sname, len(apps))
                for app in apps:
                    aname = AdminControl.getAttribute(app, 'name')
                    print "   " + aname
                    deployment = AdminConfig.getid('/Deployment:' + aname + '/')
                    sharedLibs = AdminConfig.showall(deployment).splitlines()
                    for slib in sharedLibs:
                        if slib.find('libraryName') >= 0:
                            slibClean = slib.split()[3].split(']')[0]

                            fCSV.write(cname + ";" +
                                       nname + ";" +
                                       sname + ";" +
                                       aname + ";" +
                                       slibClean + "\n")

                            print("    lib: " + slibClean)
        print "----------------------------------------------------"
        print "\n"

fCSV.close()