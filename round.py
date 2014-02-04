from decimal import Decimal

def seperate_exponent(value,precision=1):
    if value >= 0:
        sign = 1
    else:
        sign = -1
    value=value*sign
    form1 = '%.*g' % (precision, value)
    if not form1.find('e') == -1:
        form2 = form1.split('e')
        val = float(form2[0])
        exp = int(form2[1])
        return (sign*val, exp)
    elif float(form1) < 1. and not float(form1) == 0.:
        i=0
        form1=float(form1)
        while form1 < 1:
            form1*=10
            i-=1
        return (sign*form1,i)
    else:
        return (sign*float(form1),0)

class ArgumentError():
    def __init__(self,argvs):
        self.argvs = argvs
    def __str__(self):
        print 'Argument array %s is too long.' % self.argvs

class figure(object):
    def __init__(self, argvs):
        if type(argvs) in (float,int,str):
            self.value = Decimal(repr(argvs))
            self.lowerr = 0
            self.uperr = 0
        elif type(argvs) is Decimal:
            self.value = argvs
            self.lowerr = 0
            self.uperr = 0
        elif isinstance(argvs, (list, tuple)):
            self.value = argvs[0]
            if len(argvs) == 2:
                self.lowerr = -1* argvs[1]
                self.uperr = argvs[1]
            elif len(argvs) == 3:
                self.lowerr = argvs[1]
                self.uperr = argvs[2]
            elif len(argvs) > 3:
                raise ArgumentError(argvs)
        else:
            raise TypeError
        FstFig, digit = seperate_exponent(self.value)
        if FstFig == 1.0 and FstFig * 10**digit > self.value:
            self.digit = digit - 1
        else:
            self.digit = digit
        lerr,lowerrdig = seperate_exponent(self.lowerr)
        uerr,uperrdig = seperate_exponent(self.uperr)
        self.lowerrdig = lowerrdig
        self.uperrdig = uperrdig
        self.lowerrNSD = max(lowerrdig - min(self.digit, lowerrdig, uperrdig), 0) + 1
        self.uperrNSD = max(uperrdig - min(self.digit, lowerrdig, uperrdig), 0) + 1
        self.NumSigDigit = max(self.digit - min(lowerrdig, uperrdig), 0) + 1
        val,dig=seperate_exponent(self.value,self.NumSigDigit)
        lerr,lowerrdig=seperate_exponent(self.lowerr,self.lowerrNSD)
        uerr,uperrdig=seperate_exponent(self.uperr,self.uperrNSD)
        self.val = val
        self.dig = dig
        self.ldig = lowerrdig
        self.udig = uperrdig
        #print 'dig lowerrdig, uperrdig: ', dig, lowerrdig, uperrdig
        #print 'digit NSD: ', self.digit, self.NumSigDigit
        if dig == 1 or dig == 2:
            self.lowerrNSD +=1
            self.uperrNSD +=1
            self.lowerrstr='%.*g' % (self.lowerrNSD,abs(self.lowerr))
            self.uperrstr='%.*g' % (self.uperrNSD,self.uperr)
            self.valuestr = r'%.*f' % (self.NumSigDigit-dig, self.value)
            lerr,lowerrdig=seperate_exponent(self.lowerr,self.lowerrNSD)
            uerr,uperrdig=seperate_exponent(self.uperr,self.uperrNSD)
            if lowerrdig > 0:
                lerr *= 10**lowerrdig
                lowerrdig = 0
                self.lowerrdig = 0
            if uperrdig > 0:
                uerr *= 10**uperrdig
                uperrdig = 0
                self.uperrdig = 0
        elif dig > 2 or dig < -3:
            self.valuestr = r'%.*f' % (self.NumSigDigit-1, self.value*10**(0-self.digit))
            self.lowerrstr='%.*g' % (self.lowerrNSD,abs(lerr*10**(lowerrdig - self.digit)))
            self.uperrstr='%.*g' % (self.uperrNSD,uerr*10**(uperrdig - self.digit))
        #elif min(lowerrdig, uperrdig) < -3:
            #self.valuestr = r'%.*f' % (self.NumSigDigit-1, self.value)
            #self.lowerrstr='%.*g' % (self.lowerrNSD,abs(self.lowerr))
            #self.uperrstr='%.*g' % (self.uperrNSD,self.uperr)
        else:
            if self.dig == 0:
                #print 'dig lowerrdig, uperrdig: ', dig, lowerrdig, uperrdig
                self.valuestr = r'%.*f' % (self.NumSigDigit - self.digit - 1, self.value)
            elif self.dig  > 0:
                self.valuestr = r'%.*f' % (self.NumSigDigit - self.dig - 1, self.val*10**self.dig)
            else:
                self.valuestr = r'%.*f' % (self.NumSigDigit - self.digit - 1, self.value)
            self.lowerrstr='%.*g' % (self.lowerrNSD,abs(self.lowerr))
            self.uperrstr='%.*g' % (self.uperrNSD,self.uperr)
        #print 'value, err, str: ', self.valuestr, self.lowerrstr, self.uperrstr
        if self.uperrdig > self.dig and not self.dig == 0:
            self.uperrstrshort='%.0f' % (uerr * 10**(self.uperrdig - self.dig))
        else:
            self.uperrstrshort='%.0f' % (uerr)

        if self.lowerrdig > self.dig and not self.dig == 0:
            self.lowerrstrshort='%.0f' % ( abs(lerr * 10**(self.uperrdig - self.dig)))
        else:
            self.lowerrstrshort='%.0f' % ( abs(lerr))

    def __repr__(self):
        return str((self.value, self.lowerr, self.uperr))

    def tex(self):
        #print self.dig
        #print self.lowerrstr, self.uperrstr
        if not (self.lowerrstr.find('e') == -1 and self.uperrstr.find('e') == -1):
            return str(self)
        if self.lowerrstr == self.uperrstr:
            FirstPart = r'%s\pm%s' % (self.valuestr, self.uperrstr)
            #if self.dig > 2 or min(self.ldig, self.udig) < -3:
            if self.dig > 2 or self.dig < -3:
                return r'$(%s)\times10^{%d}$' % (FirstPart, self.digit)
            else:
                return r'$%s$' % (FirstPart)
        else:
            FirstPart = r'%s^{+%s}_{-%s}' % (self.valuestr, self.uperrstr, self.lowerrstr)
            #if self.dig > 2 or min(self.ldig, self.udig) < -3:
            if self.dig > 2 or self.dig < -3:
                return r'$%s\times10^{%d}$' % (FirstPart, self.digit)
            else:
                return r'$%s$' % (FirstPart)
    def __str__(self):
        if abs(self.lowerr) == abs(self.uperr):
            if not self.uperrstrshort == '0':
                FirstPart = r'%s(%s)' % (self.valuestr, self.uperrstrshort)
            else:
                FirstPart = r'%s' % (self.valuestr)
        else:
            #print self.uperr, self.lowerr
            return str(figure((self.value, (self.uperr-self.lowerr)/2)))
        #if self.dig > 2 or min(self.ldig, self.udig) < -3:
        if self.dig > 2 or self.dig < -3:
            return r'%sE%d' % (FirstPart, self.digit)
        else:
            return r'%s' % (FirstPart)



        
def TexStyle(value, NumSigDigit=None):
    if isinstance(value,str):
        try:
            return '%.3g' % float(value)
        except:
            return value
    elif isinstance(value,int):
        return value
    elif isinstance(value,list):
        res=[]
        for eachone in value:
            res.append(TexStyle(eachone))
        return res
    elif isinstance(value,dict):
        res={}
        for key in value.keys():
            res[key]=TexStyle(value[key])
        return res
    elif isinstance(value,tuple):
        if len(value) == 3 and all([isinstance(value[i],(float, int)) for i in range(3)]):
            return figure(value).tex()
        elif len(value) == 2 and all([isinstance(value[0],(float, int)),isinstance(value[1],(float, int))]):
            return figure((value[0], -1.* value[1], value[1])).tex()
        elif len(value) == 2 and any([isinstance(value[0],str),isinstance(value[1],str)]):
            try:
                return TexStyle((float(value[0]),float(value[1])))
            except:
                return '%s %s' % (TexStyle(value[0]),TexStyle(value[1]))
        else:
            res=[]
            for eachone in value:
                res.append(TexStyle(eachone))
            return tuple(res)
    elif isinstance(value, (float,int)):
        if NumSigDigit == None or not isinstance(NumSigDigit, int):
            form1 = '%.3g' % (value)
            if not form1.find('e') == -1:
                form2 = form1.split('e')
                val = form2[0]
                exp = form2[1]
                return r'$%.2f\times10^{%d}$' % (float(val),int(exp))
            else: 
                val,exp = seperate_exponent(value)
                if exp < -2:
                    return '%.*f' % (abs(exp),float(form1))
                else: return '%.2f' % float(form1)
        else:
            FstFig, digit = seperate_exponent(value)
            if FstFig == 1.0 and FstFig * 10**digit > value:
                digit = digit - 1
            val,dig=seperate_exponent(value,NumSigDigit)
            if dig == 1 or dig == 2:
                valuestr = r'%.*f' % (NumSigDigit-dig, value)
            elif dig > 2 or dig < -3:
                valuestr = r'%.*f' % (NumSigDigit-1, value*10**(0-digit))
                if valuestr.find('.') == -1 and valuestr[-1] == '0':
                    valuestr = valuestr[:-1]
                    digit += 1
            else:
                if dig == 0:
                    valuestr = r'%.*f' % (NumSigDigit - digit - 1, value)
                elif dig  > 0:
                    valuestr = r'%.*f' % (NumSigDigit - dig - 1, val*10**dig)
                else:
                    valuestr = r'%.*f' % (NumSigDigit - digit - 1, value)
            if dig > 2 or dig < -3:
                return '$'+valuestr+(r'\times10^{%i}' % (digit))+'$'
            else:
                return '$'+valuestr+'$'


def shortform(value, NumSigDigit=None):
    if isinstance(value,str):
        try:
            return '%.3g' % float(value)
        except:
            return value
    elif isinstance(value,int):
        return value
    elif isinstance(value,list):
        res=[]
        for eachone in value:
            res.append(shortform(eachone))
        return res
    elif isinstance(value,dict):
        res={}
        for key in value.keys():
            res[key]=shortform(value[key])
        return res
    elif isinstance(value,tuple):
        if len(value) == 3 and all([type(v) in (float, int, Decimal) for v in value]):
            return str(figure(value))
        elif len(value) == 2 and all([type(v) in (float, int, Decimal) for v in value]):
            return str(figure(value))
        else:
            res=[]
            for eachone in value:
                res.append(shortform(eachone))
            return tuple(res)
    elif isinstance(value, (float,int,Decimal)):
        if NumSigDigit == None or not isinstance(NumSigDigit, int):
            form1 = '%.3g' % (value)
            if not form1.find('e') == -1:
                form2 = form1.split('e')
                val = form2[0]
                exp = form2[1]
                return r'%.2fE%i' % (float(val),int(exp))
            else: 
                val,exp = seperate_exponent(value)
                if exp < -2:
                    return '%.*f' % (abs(exp),float(form1))
                else: return '%.2f' % float(form1)
        else:
            FstFig, digit = seperate_exponent(value)
            if FstFig == 1.0 and FstFig * 10**digit > value:
                digit = digit - 1
            val,dig=seperate_exponent(value,NumSigDigit)
            if dig == 1 or dig == 2:
                valuestr = r'%.*f' % (NumSigDigit-dig, value)
            elif dig > 2 or dig < -3:
                valuestr = r'%.*f' % (NumSigDigit-1, value*10**(0-digit))
                if valuestr.find('.') == -1 and valuestr[-1] == '0':
                    valuestr = valuestr[:-1]
                    digit += 1
            else:
                if dig == 0:
                    valuestr = r'%.*f' % (NumSigDigit - digit - 1, value)
                elif dig  > 0:
                    valuestr = r'%.*f' % (NumSigDigit - dig - 1, val*10**dig)
                else:
                    valuestr = r'%.*f' % (NumSigDigit - digit - 1, value)
            if dig > 2 or dig < -3:
                return valuestr+(r'E%i' % (digit))
            else:
                return valuestr
    else:
        return shortform(str(value))
