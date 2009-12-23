#! /usr/bin/env python

usageText = """

This command will help you to distribute your Panda application,
consisting of a .p3d package, into a standalone executable, graphical
installer or an HTML webpage. It will attempt to create packages
for every platform, if possible.

Usage:

  %(prog)s [opts] app.p3d standalone|installer|html

Modes:

  standalone
    A standalone executable will be created that embeds the given
    p3d file. The resulting executable will require an
    internet connection in order to run properly.

  installer
    In this mode, installable packages will be created for as many
    platforms as possible. To create Windows installers on
    non-Windows platforms, you need to have the "makensis" utility
    on your system PATH environment variable.

  html
    An HTML webpage will be generated that can be used to view
    the provided p3d file in a browser.

Options:

  -n your_app
     Short, lowercase name of the application or game. Can only
     contain alphanumeric characters, underscore or dash. This
     name will also define the output file(s) of the process.
     If omitted, the basename of the p3d file is used.

  -N "Your Application"
     Full name of the application or game. This value will
     be used to display to the end-user.
     If omitted, the short name is used.

  -v version_number
     This should define the version number of your application
     or game. In some deploy modes, this argument is required.
     This should only contain alphanumeric characters, dots and
     dashes, as otherwise the result of the deployment may be
     invalid on some platforms.

  -o output_dir
     Indicates the directory where the output will be stored.
     Within this directory, subdirectories will be created
     for every platform, unless -t is provided.
     If omitted, the current working directory is assumed.

  -t token=value
     Defines a web token or parameter to pass to the application.
     Use this to configure how the application will be run.
     You can pass as many -t options as you need. Examples of
     tokens are width, height, log_basename, auto_start, hidden.

  -P platform
     If this option is provided, it should specify a comma-
     separated list of platforms that the p3d package will be
     deployed for. If omitted, it will be built for all platforms.
     This option may be specified multiple times.
     Examples of valid platforms are win32, linux_amd64 and osx_ppc.

  -c
     If this option is provided, the -p option is ignored and
     the p3d package is only deployed for the current platform.
     Furthermore, no per-platform subdirectories will be created
     inside the output dirctory.

  -l "License Name"
     Specifies the name of the software license that the game
     or application is licensed under.
     Only relevant when generating a graphical installer.

  -L licensefile.txt
     This should point to a file that contains the full text
     describing the software license that the game or application
     is licensed under.
     Only relevant when generating a graphical installer.

  -h
     Display this help

"""

DEPLOY_MODES = ["standalone", "installer", "html"]

import sys
import os
import getopt
from DeploymentTools import Standalone, Installer
from pandac.PandaModules import Filename, PandaSystem

def usage(code, msg = ''):
    print >> sys.stderr, usageText % {'prog' : os.path.split(sys.argv[0])[1]}
    print >> sys.stderr, msg
    sys.exit(code)

shortname = ""
fullname = ""
version = ""
outputDir = Filename("./")
tokens = {}
platforms = []
currentPlatform = False
licensename = ""
licensefile = Filename()

try:
    opts, args = getopt.getopt(sys.argv[1:], 'n:N:v:o:t:P:cl:L:h')
except getopt.error, msg:
    usage(1, msg)

for opt, arg in opts:
    if opt == '-n':
        shortname = arg.strip()
    elif opt == '-N':
        fullname = arg.strip()
    elif opt == '-v':
        version = arg.strip()
    elif opt == '-o':
        outputDir = Filename.fromOsSpecific(arg)
    elif opt == '-t':
        token = arg.strip().split("=", 1)
        tokens[token[0]] = token[1]
    elif opt == '-P':
        platforms.append(arg)
    elif opt == '-c':
        currentPlatform = True
    elif opt == '-l':
        licensename = arg.strip()
    elif opt == '-L':
        licensefile = Filename.fromOsSpecific(arg)
        
    elif opt == '-h':
        usage(0)
    else:
        print 'illegal option: ' + flag
        sys.exit(1)

if not args or len(args) != 2:
    usage(1)

appFilename = Filename.fromOsSpecific(args[0])
if appFilename.getExtension().lower() != 'p3d':
    print 'Application filename must end in ".p3d".'
    sys.exit(1)
deploy_mode = args[1].lower()

if not appFilename.exists():
    print 'Application filename does not exist!'
    sys.exit(1)

if shortname.lower() != shortname or ' ' in shortname:
    print '\nProvided short name should be lowercase, and may not contain spaces!\n'

if shortname == '':
    shortname = appFilename.getBasenameWoExtension()

if fullname == '':
    fullname = shortname

if version == '' and deploy_mode == 'installer':
    print '\nA version number is required in "installer" mode.\n'
    sys.exit(1)

if not outputDir:
    print '\nYou must name the output directory with the -o parameter.\n'
    sys.exit(1)

if deploy_mode == 'standalone':
    s = Standalone(appFilename, tokens)
    s.basename = shortname
    
    if currentPlatform:
        platform = PandaSystem.getPlatform()
        if platform.startswith("win"):
            s.build(Filename(outputDir, shortname + ".exe"), platform)
        else:
            s.build(Filename(outputDir, shortname), platform)
    elif len(platforms) == 0:
        s.buildAll(outputDir)
    else:
        for platform in platforms:
            if platform.startswith("win"):
                s.build(Filename(outputDir, platform + "/" + shortname + ".exe"), platform)
            else:
                s.build(Filename(outputDir, platform + "/" + shortname), platform)

elif deploy_mode == 'installer':
    i = Installer(shortname, fullname, appFilename, version, tokens = tokens)
    i.licensename = licensename
    i.licensefile = licensefile
    
    if currentPlatform:
        platform = PandaSystem.getPlatform()
        if platform.startswith("win"):
            i.build(outputDir, platform)
        else:
            i.build(outputDir, platform)
    elif len(platforms) == 0:
        i.buildAll(outputDir)
    else:
        for platform in platforms:
            if platform.startswith("win"):
                i.build(Filename(outputDir, platform + "/"), platform)
            else:
                i.build(Filename(outputDir, platform + "/"), platform)
elif deploy_mode == 'html':
    print "Creating %s.html..." % shortname
    html = open(shortname + ".html", "w")
    html.write("<html>\n")
    html.write("  <head>\n")
    html.write("    <title>%s</title>\n" % fullname)
    html.write("  </head>\n")
    html.write("  <body>\n")
    html.write("    <object data=\"%s\" type=\"application/x-panda3d\"></object>\n" % appFilename.getBasename())
    html.write("  </body>\n")
    html.write("</html>\n")
    html.close()
else:
    usage(1, 'Invalid deployment mode!')

# An explicit call to exit() is required to exit the program, when
# this module is packaged in a p3d file.
sys.exit(0)
