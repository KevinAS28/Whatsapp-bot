import random
import re
import time

class Error(Exception):
    pass

class InvalidPrefix(Error):
    pass

class InvalidIpAddressFormat(Error):
    pass

class InvalidInput(Error):
    pass

class InvalidOktet(Error):
    pass

def validIp(ip):
    if len(ip) <= 18 and len(ip) >= 7:
        if ip.count('.') == 3:
            if '/' in ip:
                ip = re.split('[./]', ip)
                try :
                    if int(ip[-1]) <= 32 and int(ip[-1]) >= 8:
                        try:
                            for i in ip[:4]:
                                if int(i) <= 255 and int(i) > 0:
                                    return True
                                else:
                                    raise InvalidOktet
                        except ValueError:
                            raise InvalidOktet
                    else:
                        raise InvalidPrefix
                except ValueError:
                    raise InvalidPrefix
            else:
                ip = ip.split('.')
                try:
                    for i in ip[:4]:
                        if int(i) <= 255 and int(i) > 0:
                            return True
                        else:
                            raise InvalidOktet
                except ValueError:
                    raise InvalidOktet
        else:
            raise InvalidIpAddressFormat
    else:
        raise InvalidInput



class ipv4(object):

    def __init__(self, ip):
        if "/" in ip:
            oktet1, oktet2, oktet3, oktet4, pre = re.split('[./]',ip)
        else :
            oktet1, oktet2, oktet3, oktet4 = ip.split('.')
            pre = None
        self.oktet1 = oktet1
        self.oktet2 = oktet2
        self.oktet3 = oktet3
        self.oktet4 = oktet4
        self.prefix = pre

    def getClassPrefix(self):
        try :
            pre = int(self.prefix)
            if pre <= 15:
                classPre = "A"
            elif pre <= 23:
                classPre = "B"
            else :
                classPre = "C"
        except TypeError:
            classPre = None
        return classPre

    def getClassIp(self):
        x = int(self.oktet1)
        if x <= 126:
            classIp = "A"
        elif x <= 191:
            classIp = "B"
        elif x <= 223:
            classIp = "C"
        elif x <= 239:
            classIp = "D"
        else :
            classIp = "E"
        return classIp
    def get_class_IP_short(self):
        octat = int(self.oktet1)
        boundaries = {126: "A", 191: "B", 223: "C", 239: "D"}
        for bound in boundaries:
            #bound itu otomatis dapet key dari dari boundaries. key = 126, 191, 223, ..., value = "A", "B", ...
            if octat <= bound:
                return boundaries[bound]
        return "E"



    def getType(self):
        type = None
        pass

class subnetting(ipv4):

    def __init__(self, fix):
        self.fix = super().getClassPrefix()

    def getRange(self):
        pass

    def getBroadcast(self):
        return self.fix

    def getNetwork(self):
        global fix
        fix = int(self.prefix)
        ok1, ok2, ok3, ok4 = int(self.oktet1), int(self.oktet2), int(self.oktet3), int(self.oktet4)
        global net

        if (super(subnetting, self).getClassPrefix()) == "A":
            fix = 2**(32-(fix+16))
            if fix == ok2:
                net = ok2 - fix
            elif fix > ok2:
                net = 0
            elif fix < ok2:
                net = 0
                while x < ok2:
                    net += fix
                net -= fix
            return (f'{ok1}.{net}.0.0')

        elif (super(subnetting, self).getClassPrefix()) == "B":
            fix = 2**(32-(fix+8))
            if fix == ok3:
                net = ok3 - fix
            elif fix > ok3:
                net = 0
            elif fix < ok3:
                net = 0
                while x < ok3:
                    x += fix
                net -= fix
            return (f'{ok1}.{ok2}.{net}.0')

        elif (super(subnetting, self).getClassPrefix()) == "C":
            fix = 2**(32-fix)
            if fix == ok4:
                net = ok4 - fix
            elif fix > ok4:
                net = 0
            elif fix < ok4:
                net = 0
                while x < ok4:
                    net += fix
                net -= fix
            return (f'{ok1}.{ok2}.{ok3}.{net}')

    def getSubnetmask(self):
        return net, fix
# check
def main():
    while True:
        var = input("type 'stop' to end this program : ")
        if var == 'stop':
            break
        else:
            try :
                if validIp(var):
                    varIp = subnetting(var)
                    print("Class prefix :", varIp.getClassPrefix())
                    print("Class Ip     :", varIp.getClassIp())
                    print("Network Address :", varIp.getNetwork())
                    print(varIp.getBroadcast())
            except InvalidIpAddressFormat:
                print("Error : InvalidIpAddressFormat")
                break
            except InvalidPrefix:
                print("Error : InvalidPrefix")
                break
            except InvalidInput:
                print("Error : InvalidInput")
                break
            except InvalidOktet:
                print("Error : InvalidOktet")
                break

    print("=========")
    print("Thank you")
    print("=========")

main()
