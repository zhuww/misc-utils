import unittest
from round import TexStyle as TS
from round import shortform as SF

def double_check(f): 
    def func(*args,**kwargs):
        try:
            f(*args,**kwargs)
        except AssertionError:
            raise AssertionError
    func.__name__ = f.__name__
    func.__dict__ = f.__dict__
    func.__doc__ = f.__doc__
    func.__module__ = f.__module__
    return func

class TestPublishStyleModule(unittest.TestCase):
    def setUp(self):
        self.float=19973.79
        self.floatres='$2.00\\times10^{4}$'
        self.float1=0.0000091741
        self.float1res='$9.17\\times10^{-6}$'
        self.float2=0.0034
        self.float2res='0.003'
        self.float3=0.00046
        self.float3res='0.0005'
        self.string='123456.78e9'
        self.stringres='1.23e+14'
        self.tuple2=(1.2345678e9,1.234567e8)
        self.tuple2res='$(1.2\\pm0.1)\\times10^{9}$'
        self.tuple2s=(0.3,0.01)
        self.tuple2sres='$0.30\\pm0.01$'
        self.tuple2a=(54550.8,0.01)
        self.tuple2ares='$54550.80\\pm0.01$'
        self.tuple2b=(54550.8,100.)
        self.tuple2bres='$(5.46\\pm0.01)\\times10^{4}$'
        self.tuple2c=(150., 75.)
        self.tuple2cres='$150\pm75$'
        self.tuple3=(2.0312700000000001, -0.21791000000000005, 0.19948999999999995)
        self.tuple3res='$2.0\\pm0.2$'
        self.tuple3s=(0.03,-0.001,0.002)
        self.tuple3sres='$0.030^{+0.002}_{-0.001}$'
        self.tuple3a=(54550.8,-0.02,0.01)
        self.tuple3ares='$54550.80^{+0.01}_{-0.02}$'
        self.tuple3b=(0.18826599999999999, -0.028073999999999988, 0.032406000000000018)
        self.tuple3bres='$0.19\\pm0.03$'
        self.tuple3c=(0.018826599999999999, -0.0028073999999999988, 0.0042406000000000018)
        self.tuple3cres='$0.019^{+0.004}_{-0.003}$'
        self.tuple3d=(0.0977, -0.07, 0.038)
        self.tuple3dres='$0.10^{+0.04}_{-0.07}$'
        self.tuple3e=(130.0, -50, 100.)
        self.tuple3eres='$130^{+100}_{-50}$'
        self.tuple3f=(999., -50.,50.)
        self.tuple3fres='$(10.0\\pm0.5)\\times10^{2}$'
        self.tuplewithstring=(3.2738499999999999, 'abcd')
        self.tuplewithstringres='3.27 abcd'
        self.tuple3jinwei=(0.095826599999999999, -0.0028073999999999988, 0.0042406000000000018)
        self.tuple3jinweires='$0.096^{+0.004}_{-0.003}$'
        self.lists1=[(0.59509999999999996, -0.014440999999999926, 0.0079680000000000861), (0.0, 0.0, 0.056300099999999999)]
        self.lists1res=['$0.595^{+0.008}_{-0.014}$', '$0.00^{+0.06}_{-0}$'] 
        self.lists2=[(9.2931399999999993e-12, -2.2368999999999942e-13, 1.3144000000000131e-13), (9.1609100000000008e-12, -1.8142000000000025e-13, 1.5091999999999871e-13), (1.0769499999999999e-11, -1.186939999999999e-12, 6.4620000000000102e-13), (1.0637200000000001e-11, -1.1917100000000012e-12, 6.106999999999986e-13), (1.15354e-11, -1.2310000000000007e-12, 5.9049999999999915e-13), (1.15354e-11, -1.2310000000000007e-12, 5.9049999999999915e-13), (1.11705e-11, -1.5039700000000005e-12, 7.347000000000009e-13), (1.11705e-11, -1.5039700000000005e-12, 7.347000000000009e-13), (1.26726e-11, -1.3597000000000004e-12, 4.8010000000000075e-13), (1.26726e-11, -1.3597000000000004e-12, 4.8010000000000075e-13), (1.25313e-11, -1.4328000000000009e-12, 5.8029999999999986e-13)]
        self.lists2res=['$9.3^{+0.1}_{-0.2}\\times10^{-12}$', '$(9.2\\pm0.2)\\times10^{-12}$', '$1.08^{+0.06}_{-0.12}\\times10^{-11}$', '$1.06^{+0.06}_{-0.12}\\times10^{-11}$', '$1.15^{+0.06}_{-0.12}\\times10^{-11}$', '$1.15^{+0.06}_{-0.12}\\times10^{-11}$', '$1.12^{+0.07}_{-0.15}\\times10^{-11}$', '$1.12^{+0.07}_{-0.15}\\times10^{-11}$', '$1.27^{+0.05}_{-0.14}\\times10^{-11}$', '$1.27^{+0.05}_{-0.14}\\times10^{-11}$', '$1.25^{+0.06}_{-0.14}\\times10^{-11}$']
        self.tentotheone=(94., -23., 11.)
        self.tentotheoneres='$94^{+11}_{-23}$'
        self.verysmallerr = (259.123456789,-0.0000001234,0.0000002341)
        self.verysmallerrres = '259.1234568(2)'
        self.numsigdigittest=984.3
        self.numsigdigittestres='$1\\times10^{3}$'
        self.numsigdigittest1=99.4
        self.numsigdigittestres1='$99$'
        self.numsigdigittest2=217.19
        self.numsigdigittestres2='$217$'

    def testTS(self):
        self.assertEqual(TS(self.string),self.stringres)
        self.assertEqual(TS(self.float),self.floatres)
        self.assertEqual(TS(self.float1),self.float1res)
        self.assertEqual(TS(self.float2),self.float2res)
        self.assertEqual(TS(self.float3),self.float3res)
        self.assertEqual(TS(self.tuple2),self.tuple2res)
        self.assertEqual(TS(self.tuple2s),self.tuple2sres)
        self.assertEqual(TS(self.tuple2a),self.tuple2ares)
        self.assertEqual(TS(self.tuple2b),self.tuple2bres)
        self.assertEqual(TS(self.tuple2c),self.tuple2cres)
        self.assertEqual(TS(self.tuple3),self.tuple3res)
        self.assertEqual(TS(self.tuple3s),self.tuple3sres)
        self.assertEqual(TS(self.tuple3a),self.tuple3ares)
        self.assertEqual(TS(self.tuple3b),self.tuple3bres)
        self.assertEqual(TS(self.tuple3c),self.tuple3cres)
        self.assertEqual(TS(self.tuple3d),self.tuple3dres)
        self.assertEqual(TS(self.tuple3e),self.tuple3eres)
        self.assertEqual(TS(self.tuple3f),self.tuple3fres)
        self.assertEqual(TS(self.tuplewithstring),self.tuplewithstringres)
        self.assertEqual(TS(self.tuple3jinwei),self.tuple3jinweires)
        self.assertEqual(TS(self.lists1),self.lists1res)
        self.assertEqual(TS(self.lists2),self.lists2res)
        self.assertEqual(TS(self.tentotheone),self.tentotheoneres)
        self.assertEqual(TS(self.verysmallerr),self.verysmallerrres)
        self.assertEqual(TS(self.numsigdigittest, NumSigDigit=1),self.numsigdigittestres)
        self.assertEqual(TS(self.numsigdigittest1, NumSigDigit=1),self.numsigdigittestres1)
        self.assertEqual(TS(self.numsigdigittest2, NumSigDigit=1),self.numsigdigittestres2)

        self.show(self.string,self.stringres)
        self.show(self.float,self.floatres)
        self.show(self.float1,self.float1res)
        self.show(self.float2,self.float2res)
        self.show(self.float3,self.float3res)
        self.show(self.tuple2,self.tuple2res)
        self.show(self.tuple2s,self.tuple2sres)
        self.show(self.tuple2a,self.tuple2ares)
        self.show(self.tuple2b,self.tuple2bres)
        self.show(self.tuple2c,self.tuple2cres)
        self.show(self.tuple3,self.tuple3res)
        self.show(self.tuple3s,self.tuple3sres)
        self.show(self.tuple3a,self.tuple3ares)
        self.show(self.tuple3b,self.tuple3bres)
        self.show(self.tuple3c,self.tuple3cres)
        self.show(self.tuple3d,self.tuple3dres)
        self.show(self.tuple3e,self.tuple3eres)
        self.show(self.tuple3f,self.tuple3fres)
        self.show(self.tuplewithstring,self.tuplewithstringres)
        self.show(self.tuple3jinwei,self.tuple3jinweires)
        self.show(self.lists1,self.lists1res)
        self.show(self.lists2,self.lists2res)
        self.show(TS(self.tentotheone),self.tentotheoneres)
        self.show(TS(self.verysmallerr),self.verysmallerrres)
        self.show(TS(self.numsigdigittest, NumSigDigit=1),self.numsigdigittestres)
        self.show(TS(self.numsigdigittest1, NumSigDigit=1),self.numsigdigittestres1)
        self.show(TS(self.numsigdigittest2, NumSigDigit=1),self.numsigdigittestres2)

    def show(self, first, second):
        print 'TexStyle(%s) -> %s' % (first, second)


def suite():
    suite = unittest.makeSuite(TestPublishStyleModule, 'test')
    return suite

if __name__ == '__main__':
        unittest.main(defaultTest='suite')

