### This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from sos.plugins import Plugin, RedHatPlugin
import os
import time
import re
import xml.etree.ElementTree as ET


class abiquo_sos(Plugin, RedHatPlugin):
    """Abiquo servers related information
    """

    option_list = [
        ("days", "Number of days to collect (tomcat logs)", "slow", 7),
    ]

    #add copy file/path only if the resource exists
    def copy_if_exists(self, path):
        if os.path.exists(path):
            self.add_copy_spec(path)
        return

    #choose only files from provided path which were modified < days
    def abiquo_log_filter(self, path, days):
        now = time.time()
        file_list = [os.path.join(path,i) for i in os.listdir(path)]
        collect_list = []
        for i in file_list:
            modification_time = os.path.getmtime(i)
            if (now - modification_time) // (24*3600) < days:
                collect_list.append(i)
        return collect_list

    #find substrings
    def find_between(self, s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def setup(self):

        # Abiquo tomcat logs, default 7 days
        if os.path.exists("/opt/abiquo/tomcat/logs"):
            filestocollect = self.abiquo_log_filter("/opt/abiquo/tomcat/logs/", self.get_option("days"))
            for a in filestocollect:
                self.add_copy_spec(a)

        # Abiquo config files
        self.copy_if_exists("/opt/abiquo/tomcat/conf")
        self.copy_if_exists("/opt/abiquo/config")

        # Abiquo remote service redis dump
        self.copy_if_exists("/var/lib/redis")

        # History
        self.copy_if_exists("/root/.bash_history")
 
        # MySQL dump
        if os.path.exists("/opt/abiquo/tomcat/conf/Catalina/localhost/api.xml"):
                tree = ET.parse("/opt/abiquo/tomcat/conf/Catalina/localhost/api.xml")
                root = tree.getroot()
                xml_params = {}
                for params in root.findall('Resource'):
                    xml_params = params.attrib
                    dbUsername = xml_params['username']
                    dbPassword = xml_params['password']
                    dbHost = self.find_between(xml_params['url'], 'mysql://', ':')
                    dbPort = self.find_between(xml_params['url'], dbHost + ':', '/')
                    dbSchema = 'kinton'
                self.add_cmd_output("mysqldump --routines --triggers -h " + dbHost + " -P " + dbPort + " -u " + dbUsername + " --password=" + dbPassword + " " + dbSchema, suggest_filename="kinton_dump.sql")
                self.add_cmd_output("mysqldump --routines --triggers -h " + dbHost + " -P " + dbPort + " -u " + dbUsername + " --password=" + dbPassword + " kinton_accounting --ignore-table=kinton_accounting.accounting_event_detail", suggest_filename="kinton_dump_ignore_accounting_event_detail.sql")

        # rabbitmq queues status
        if self.is_installed("rabbitmq-server"):
            self.add_cmd_output("rabbitmqctl list_queues")
            self.add_cmd_output("rabbitmqctl list_queues name consumers messages_ready messages_unacknowledged messages")

        # get jinfo sysprops
        if os.path.exists("/opt/abiquo/tomcat"):
            self.add_cmd_output("sudo -u tomcat sh -c '/usr/java/default/bin/jinfo -sysprops $(pgrep java)'")

        # vm_repository find -ls
        if os.path.exists("/opt/abiquo/config/abiquo.properties"):
            propsFile = open("/opt/abiquo/config/abiquo.properties").read()
            vmRepo = re.search(r'abiquo.appliancemanager.localRepositoryPath(.?=)(.*)', propsFile)
            if vmRepo:
                self.add_cmd_output("find " +vmRepo.group(2)+ " -ls")
            else:
                if os.path.exists("/opt/vm_repository/"):
                    self.add_cmd_output("find /opt/vm_repository -ls")

        # /opt/abiquo/ find -ls
        if os.path.exists("/opt/abiquo"):
            self.add_cmd_output("find /opt/abiquo -ls")
 
        # logback files
        self.copy_if_exists("/opt/abiquo/tomcat/webapps/am/WEB-INF/classes/logback.xml")
        self.copy_if_exists("/opt/abiquo/tomcat/webapps/m/WEB-INF/classes/logback.xml")
        self.copy_if_exists("/opt/abiquo/tomcat/webapps/api/WEB-INF/classes/logback.xml")
        self.copy_if_exists("/opt/abiquo/tomcat/webapps/nodecollector/WEB-INF/classes/logback.xml")
        self.copy_if_exists("/opt/abiquo/tomcat/webapps/cpp/WEB-INF/classes/logback.xml")
        self.copy_if_exists("/opt/abiquo/tomcat/webapps/ssm/WEB-INF/classes/logback.xml")
        self.copy_if_exists("/opt/abiquo/tomcat/webapps/vsm/WEB-INF/classes/logback.xml")
        self.copy_if_exists("/opt/abiquo/tomcat/webapps/bpm-async/WEB-INF/classes/logback.xml")
        self.copy_if_exists("/opt/abiquo/tomcat/webapps/virtualfactory/WEB-INF/classes/logback.xml")

        # monitoring conf, logs, default 7 days
        self.copy_if_exists("/etc/abiquo/watchtower/")
        self.copy_if_exists("/etc/cassandra/")
        self.copy_if_exists("/opt/kairosdb/conf/")
        self.copy_if_exists("/opt/kairosdb/log/")
        self.copy_if_exists("/var/log/emmett.log")
        self.copy_if_exists("/var/log/delorean.log")
        self.copy_if_exists("/var/log/emmett-metrics.log")
        self.copy_if_exists("/var/log/delorean-metrics.log")
        self.copy_if_exists("/var/log/cassandra/")

        # Sysstat logs
        self.copy_if_exists("/var/log/sa/")
 
        # dhcp leases
        self.copy_if_exists("/var/lib/dhcpd/")

        # Abiquo lvm tomcat logs, default 7 days
        if os.path.exists("/opt/abiquo/lvmiscsi/"):
            self.add_copy_spec("/opt/abiquo/lvmiscsi/tomcat/conf")
            filestocollect = abiquo_log_filter("/opt/abiquo/lvmiscsi/tomcat/logs", self.get_option("days"))
            for a in filestocollect:
                self.add_copy_spec(a)

        # Abiquo nodes
        self.copy_if_exists("/var/log/libvirt/")
        self.copy_if_exists("/etc/abiquo-aim.ini")
        if os.path.exists("/etc/libvirt"):
            self.add_copy_spec("/etc/libvirt/")
            self.add_cmd_output("virsh capabilities")
            self.add_cmd_output("virsh list --all")
        self.copy_if_exists("/var/log/xen/")
        self.copy_if_exists("/etc/xen/")

        return
