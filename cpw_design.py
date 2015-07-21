from scipy.constants import c, epsilon_0, mu_0
from scipy.special import ellipk, ellipkm1
from numpy import *

class cpw:
    def __init__(self, w=10., s=6., t=.1, h=500., l=1000., e1=11.6, material="nb", tgdelta=1e-8):
        self.w = w*1e-6
        self.s = s*1e-6
        self.t = t*1e-6
        self.h = h*1e-6
        self.l = l*1e-6
        self.e1 = e1
        self.tgdelta = tgdelta
        self.material = material
        
        if material == "al":
            self.Tc = 1.23
            self.rho = 4e-9
        elif material == 'nb':
            self.Tc = 8
            self.rho = 4e-9
        
        self.l0 = 1.05e-3*sqrt(self.rho/self.Tc)
    
#     Effective Dielectric Constant from Silicon-Air Interface
    
    def k0(self):
        return self.w/(self.w+2*self.s)
    
    def kp0(self):
        return sqrt(1-self.k0()**2)
    
    def k1(self):
        return sinh(pi*self.w/(4*self.h))/sinh(pi*(2*self.s+self.w)/(4*self.h))
    
    def kp1(self):
        return sqrt(1-self.k1()**2)
    
    def Eeff(self):
        return 1 + ((self.e1-1)*ellipk(self.k1())*ellipk(self.kp0()))/(2*ellipk(self.kp1())*ellipk(self.k0()))
    
#     Kinetic Inductance Calculation

    def g(self):
        a = -log(self.t/(4*self.w))
        b = -self.w/(self.w+2*self.s)*log(self.t/(4*(self.w+2*self.s)))
        c = 2*(self.w+self.s)/(self.w+2*self.s)*log(self.s/(self.w+self.s))
        return 1/(1*self.k0()**2*ellipk(self.k0())**2) * (a+b+c)
    
    def Llk(self):
        return mu_0*self.l0**2/(self.w*self.t)*self.g()
    
#     Circuit Parameters
    
    def Ll(self):
        return mu_0*ellipk(self.kp0())/(4*ellipk(self.k0())) + self.Llk()
    
    def Cl(self):
        return 4*epsilon_0*self.Eeff()*ellipk(self.k0())/ellipk(self.kp0())
    
    def vph(self):
        return 1/sqrt(self.Ll()*self.Cl())
    
    def f0(self):
        return c/(sqrt(self.Eeff())*2*self.l)
    
    def z0(self):
        return sqrt(self.Ll()/self.Cl())
    
#     Loss
    def k(self):
        return 2*pi*self.f0()*sqrt(self.Eeff())/c
    
    def alpha_d(self):
        return self.e1/sqrt(self.Eeff())*(self.Eeff()-1)/(self.e1-1)*self.tgdelta*self.k()/2
    
#     Circuit Parameters with Loss
    
    def L(self):
        return 2*self.Ll()*self.l/(pi**2)
    
    def C(self):
        return self.Cl()*self.l/2
    
    def R(self):
        return self.z0()/(self.alpha_d()*self.l)
    
    def Qint(self):
        return self.R()*self.C()/sqrt(self.L()*self.C())
    
    def wn(self):
        return self.Qint()/(self.R()*self.C())
    def fn(self):
        return self.wn()/(2*pi)