import os , json , csv
import result_parser
import combination_parser

class testRes():
    def __init__(self , workingDir , curCsv=None):
        self.workingDir = workingDir
        self.logsDir = workingDir + '/logs'
        self.failedLogsDir = workingDir + '/logs_failed'
        self.suite2casesDir = workingDir + '/suite2cases_out'
        self.testResult = []
        self.curCsv = None
        if curCsv is not None:
            if curCsv[0] != '/':
                curCsv = os.path.join('.' , curCsv)
            if os.path.exists(curCsv):
                self.csvtestResult = {}
                self.curCsv = curCsv
        self.totalCaseNum, self.totalPassedCaseNum, self.totalFailedCaseNum = 0, 0, 0

    def resPick(self):
        allSuites = os.listdir(self.logsDir)
        withFailedSuites = os.listdir(self.failedLogsDir)
        for suite in allSuites:
            if suite not in withFailedSuites:
                for case in os.listdir(self.logsDir+'/'+suite):
                    if self.csvtestResult.get(case , None) is not None and self.csvtestResult[case]['status'] == 'success':
                        self.testResult.append({'suite name':suite , 'case name':case , 'status':'success' , 'reason':self.csvtestResult[case]['reason']})
                    else:
                        self.testResult.append({'suite name':suite , 'case name':case , 'status':'success'})
    
    

    def csvRead(self):
        if self.curCsv is not None:
            with open(self.curCsv , 'r') as f:
                rows = csv.reader(f)
                rows = [row for row in rows]
                rows = rows[1:]
                keys = ['suite name' , 'case name' , 'status' , 'logFile' , 'reason']
                for row in rows:
                    self.csvtestResult[row[1]] = dict(zip(keys , row))

    def exprotToCsv(self, filename = 'failureCause.csv'):
        csvfile = open('./'+filename,'w')
        cw = csv.writer(csvfile,lineterminator = '\n')
        title = ['测试套/软件包名','测试用例名','状态','日志文件','原因']
        row = []
        row.append(title)
        ran = range(len(self.testResult))
        suite = ''
        for i in ran:
            if len(row) == 1 or suite != self.testResult[i]['suite name']:
                suiteName = self.testResult[i]['suite name']
            else:
                suiteName = ''
            if self.testResult[i]['suite name'] != '':
                suite = self.testResult[i]['suite name']
            if self.testResult[i].get('reason' , None) is not None:
                reason = self.testResult[i]['reason']
            elif self.testResult[i]['status'] == 'x86 fail':
                reason = 'x86 fail'
            elif self.testResult[i]['status'] == 'success':
                reason = 'None'
            else:
                reason = ''
            logfile = sorted(os.listdir(self.logsDir+'/'+suite+'/'+self.testResult[i]['case name']))[0]
            logPath = self.logsDir+'/'+suite+'/'+self.testResult[i]['case name']+'/'+logfile
            row.append([suiteName , self.testResult[i]['case name'] , self.testResult[i]['status'] , logPath , reason])
        cw.writerows(row)
        csvfile.close()

    def exportToMarkdown(self , filename = 'table.md'):
        with open(filename, "w") as md_file:
            title = ['测试套/软件包名','测试用例名','状态','日志文件','原因']
            md_file.write("| ")
            for header in title:
                md_file.write(header + " | ")
            md_file.write("\n")
            md_file.write("| ")
            for header in title:
                md_file.write(":---: | ")
            md_file.write("\n")
            ran = range(len(self.testResult))
            step = -1
            suite = ''
            for i in ran:
                if self.testResult[i]['suite name'] != '':
                    suite = self.testResult[i]['suite name']
                if (i+step < 0 or i+step >= len(self.testResult)) or self.testResult[i+step]['suite name'] != self.testResult[i]['suite name']:
                    suiteName = self.testResult[i]['suite name']
                else:
                    suiteName = ''
                if self.testResult[i].get('reason' , None) is not None:
                    reason = self.testResult[i]['reason']
                elif self.testResult[i]['status'] == 'success' :
                    reason = 'None'
                elif self.testResult[i]['status'] == 'x86 fail':
                    reason = 'x86 fail'
                else:
                    reason = ''
                logfile = sorted(os.listdir(self.logsDir+'/'+suite+'/'+self.testResult[i]['case name']))[0]
                logPath = self.logsDir+'/'+suite+'/'+self.testResult[i]['case name']+'/'+logfile
                md_file.write('| '+suiteName+' | '+self.testResult[i]['case name']+' | '+self.testResult[i]['status']+' | ['+logPath+']('+logPath+') | '+reason+' |\n')

    
    def statNum(self):
        self.totalCaseNum = len(self.testResult)
        for case in self.testResult:
            if case['status'] == 'success':
                self.totalPassedCaseNum += 1
        self.totalFailedCaseNum = self.totalCaseNum - self.totalPassedCaseNum

    


def findRealFail(riscv:testRes):
    riscvFailedSuite = os.listdir(riscv.failedLogsDir)
    module = testRes('mugen-riscv')
    command = testRes('mugen-riscv')
    suite = ''
    retest = combination_parser.combination()
    for suite in riscvFailedSuite:
        for case in os.listdir(riscv.logsDir+'/'+suite):
            if case not in os.listdir(riscv.failedLogsDir+'/'+suite):
                if riscv.csvtestResult.get(case , None) is not None and riscv.csvtestResult[case]['status'] == 'success':
                    riscv.testResult.append({'suite name':suite , 'case name':case , 'status':'success' , 'reason':riscv.csvtestResult[case]['reason']})
                else:
                    riscv.testResult.append({'suite name':suite , 'case name':case , 'status':'success'})
        
            else: 
                if riscv.csvtestResult.get(case , None) is not None:
                    riscv.testResult.append({'suite name':suite , 'case name':case , 'status':'fail' , 'reason':riscv.csvtestResult[case]['reason']})
                else:
                    riscv.testResult.append({'suite name':suite , 'case name':case , 'status':'fail'})
            for case in os.listdir(riscv.failedLogsDir+'/'+suite):
                if case not in os.listdir(riscv.failedLogsDir+'/'+suite):
                    reason = None
                    fileData = None
                    fliter = result_parser.classifier('catalog.json')
                    logfile = sorted(os.listdir(riscv.logsDir+'/'+suite+'/'+case))[0]
                    with open(riscv.logsDir+'/'+suite+'/'+case+'/'+logfile , 'r' , encoding="ISO-8859-1") as f:
                        fileData = f.read().split('\n')
                    if riscv.csvtestResult.get(case , None) is not None:
                        riscv.testResult.append({'suite name':suite , 'case name':case , 'status':'fail' , 'reason':riscv.csvtestResult[case]['reason']})
                        reason = riscv.csvtestResult[case].get('reason' , [])
                    else:
                        reason = fliter.checkErrorType(fileData)
                        riscv.testResult.append({'suite name':suite , 'case name':case , 'status':'fail' , 'reason':'/'.join(reason)})
                    if 'timeout' in reason:
                        retest.add_case(suite , case)
                    if 'kernel module absent' in reason:
                        for line in fileData:
                            if line.find('Module') != -1:
                                module.testResult.append({'suite name':suite , 'case name':case , 'status':'fail' , 'reason':line})
                                break
                    if 'file missing' in reason or 'preinstall absent' in reason :
                        retest.add_case(suite , case)
                        for line in fileData:
                            if line.find('command not found') != -1 or line.find('.service not found') != -1 or line.find('No such file or directory') != -1:
                                command.testResult.append({'suite name':suite , 'case name':case , 'status':'fail' , 'reason':line})
                                
                    
    module.exprotToCsv('module_failure.csv')
    command.exprotToCsv('command.csv')
    retest.export_every_json()



if __name__ == '__main__':
    riscv = testRes('./mugen-riscv' , 'failureCause.csv')
    riscv.resPick()
    riscv.csvRead()
    findRealFail(riscv)
    riscv.exprotToCsv()
    riscv.exportToMarkdown()