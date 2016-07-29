import sys
import os
import re
import time
import subprocess
from random import choice


class action:

    def __init__(self):
        """Constructor"""

    def killApplicationById(self, applicationId):
        order = 'bash /usr/local/hadoop-2.7.2/bin/yarn application -kill ' + applicationId
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.read()
        return feedback

    def getApplicationName2IdSet(self, arg='RUNNING'):
        order = 'bash /usr/local/hadoop-2.7.2/bin/yarn application -list -appStates ' + arg
        feedback = os.popen(order).read()
        regix = re.compile(r'application_\d+_\d+\s+\d+')
        IdAndName = regix.findall(feedback)
        IdAndName.sort()
        Idset = {}
        for item in IdAndName:
            tmp = item.split('\t')
            Id = tmp[0].replace(' ', '')
            Name = tmp[1].replace(' ', '')
            Idset[Name] = Id
        return Idset

    def submitJob(self, className, driverMemory, executorMemory, executorCores, jarPath, args=""):
        name = ''.join([choice('0123456789') for i in range(24)])
        order = 'bash /usr/local/spark-1.6.2-bin-without-hadoop/bin/spark-submit --class ' + className + ' --master yarn --deploy-mode cluster --driver-memory ' + \
            driverMemory + ' --executor-memory ' + executorMemory + ' --name ' + name + \
                ' --executor-cores ' + executorCores + ' --queue default '\
                + jarPath + ' ' + args
        # feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while 1:
            applicationIdSet = self.getApplicationName2IdSet('ALL')
            if applicationIdSet.has_key(name):
                applicationId = applicationIdSet[name]
                break;
            else:
                time.sleep(2)
        return applicationId

    def getStatus(self, applicationId):
        order = 'bash /usr/local/hadoop-2.7.2/bin/yarn application -status ' + applicationId
        feedback = os.popen(order).read()
        feedback = feedback.replace('\n', '')
        first = feedback.split('\t')
        report = {}
        #for item in first:
        for index in range(0, 16):
            item = first[index]
            second = item.split(' : ')
            report[second[0]] = second[1]
        report['Application Report'] = applicationId
        return report

    def getLog(self, applicationId):
        order = 'bash /usr/local/hadoop-2.7.2/bin/yarn logs -applicationId  ' + applicationId
        feedback = os.popen(order).read()
        # bad response
        containers = feedback.split('Container: ')
        del containers[0]
        logs = {}
        for container in containers:
            tmpa = container.split('LogType:')
            name = tmpa[0].split('\n')[0]
            stderr = tmpa[1]
            stdout = tmpa[3]
            logs[name] = [stderr, stdout]
        # end
        return logs

    def uploadFile(self, filePath, filePathHDFS):
        # order = 'hadoop fs -put ' + filePath + ' ' + filePathHDFS
        order = 'bash /usr/local/bash/hdfs-put.sh ' + filePath + ' ' + filePathHDFS
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.read()
        return feedback

    def makeDirectory(self, filePathHDFS):
        order = 'bash /usr/local/bash/hdfs-mkdir.sh ' + filePathHDFS
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.read()
        return feedback

    def downloadFIle(self, filePathHDFS, filePath):
        # order = 'hadoop fs -get ' + filePathHDFS + ' ' + filePath
        order = 'bash /usr/local/bash/hdfs-get.sh ' + filePathHDFS + ' ' + filePath
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.read()
        return feedback

    def removeFile(self, filePathHDFS, document=False):
        if document is True:
            order = 'bash /usr/local/bash/hdfs-rmfile.sh ' + filePathHDFS
        else:
            order = 'bash /usr/local/bash/hdfs-rmdir.sh ' + filePathHDFS
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.read()
        return feedback

#if __name__ == '__main__':
#       ac = action()
#       ID = ac.submitJob('org.apache.spark.examples.SparkPi', '4g', '4g', '7', 'hdfs:///spark-examples-1.6.2-hadoop2.2.0.jar', '1000')
#       print '-------------------------------------------------'
#       print ID
#       print '-------------------------------------------------'