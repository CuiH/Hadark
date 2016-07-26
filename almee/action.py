import sys
import os
import re
import time
import subprocess


class action:

    def __init__(self):
        """Constructor"""

    def killApplicationByID(applicationID):
        order = 'bash /usr/local/hadoop-2.7.2/bin/yarn application -kill ' + applicationID
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.readline()
        return feedback

    def getApplicationIDSet(arg='RUNNING'):
        order = 'bash /usr/local/hadoop-2.7.2/bin/yarn application -list -appStates ' + arg
        feedback = os.popen(order).read()
        regix = re.compile(r'application_\d+_\d+')
        IDset = regix.findall(feedback)
        IDset.sort()
        return IDset

    def submitJob(className, driverMemory, executorMemory, executorCores, jarPath, args=""):
        order = 'bash /usr/local/spark-1.6.2-bin-without-hadoop/bin/spark-submit --class ' + className + ' --master yarn --deploy-mode cluster --driver-memory ' + \
            driverMemory + ' --executor-memory ' + executorMemory + \
                ' --executor-cores ' + executorCores + ' --queue default ' \
                + jarPath + ' ' + args
        applicationIDSet = getApplicationIDSet('ALL')
        applicationNum = len(applicationIDSet)
        # feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        applicationIDSet = getApplicationIDSet('ALL')
        applicationNum2 = len(applicationIDSet)
        if applicationNum == applicationNum2:
        	result = feedback.stdout.readline()
        else:
	        if len(applicationIDSet) == 0:
	            time.sleep(2)
	        result = applicationIDSet[-1]
        # print '-------------------------------------------------------------------------------'
        # print result
        # print
        # '-------------------------------------------------------------------------------'
        return result

    def getStatus(applicationID):
        order = 'bash /usr/local/hadoop-2.7.2/bin/yarn application -status ' + applicationID
        feedback = os.popen(order).read()
        feedback = feedback.replace('\n', '')
        first = feedback.split('\t')
        report = {}
        for item in first:
            second = item.split(' : ')
            report[second[0]] = second[1]
        report['Application Report'] = applicationID
        return report

    def getLog(applicationID):
        order = 'bash /usr/local/hadoop-2.7.2/bin/yarn logs -applicationId  ' + applicationID
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

    def uploadFile(filePath, filePathHDFS):
        # order = 'hadoop fs -put ' + filePath + ' ' + filePathHDFS
        order = 'bash /usr/local/bash/hdfs-put.sh ' + filePath + ' ' + filePathHDFS
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.readline()
        return feedback

    def makeDirectory(filePathHDFS):
        order = 'bash /usr/local/bash/hdfs-mkdir.sh ' + filePathHDFS
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.readline()
        return feedback

    def downloadFIle(filePathHDFS, filePath):
        # order = 'hadoop fs -get ' + filePathHDFS + ' ' + filePath
        order = 'bash /usr/local/bash/hdfs-get.sh ' + filePathHDFS + ' ' + filePath
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.readline()
        return feedback

    def removeFile(filePathHDFS, document=False):
        if document is True:
            order = 'bash /usr/local/bash/hdfs-rmfile.sh ' + filePathHDFS
        else:
            order = 'bash /usr/local/bash/hdfs-rmdir.sh ' + filePathHDFS
        #feedback = os.popen(order).read()
        feedback = subprocess.Popen(order, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        feedback = feedback.stdout.readline()
        return feedback

