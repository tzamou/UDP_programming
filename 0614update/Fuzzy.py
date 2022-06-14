import numpy as np
import matplotlib.pyplot as plt
#模糊化------------------------------------------------------------------------------------------------------------

#first
class FuzzyObs:
    def __init__(self,fuzzy,max_array,min_array):
        self.max_array = max_array
        self.min_array = min_array
        assert len(max_array)==len(min_array)
        self.length = len(max_array)
        self.fuzzy = fuzzy

    def transform_observation(self,obs,denominator):
        fuzzylist = np.zeros((self.length, 3))
        for i in range(len(obs)):
            self.fuzzy.transform(obs[i],self.min_array[i],self.max_array[i],fuzzylist[i],denominator)
        return fuzzylist.flatten()
        #print(fuzzylist.flatten(),len(fuzzylist.flatten()))
class Triangular_mf(FuzzyObs):
    def __init__(self,min_obs,max_obs,fuzlst,denominator):
        self.min_obs = min_obs
        self.max_obs = max_obs
        self.fuzlst = fuzlst
        self.denominator = denominator
    def triangular_mf(self,x,min_obs,max_obs,fuzlst,denominator):
        d1=min_obs+(max_obs-min_obs)*1/self.denominator
        d2=(max_obs+min_obs)*1/2
        d3=min_obs+(max_obs-min_obs)*(self.denominator-1)/self.denominator
        n=m=p=0
        if x<=d1:
            n = 1
            m = 0
            p = 0
        elif (x>d1 and x<=d2):
            n = (x - d2) / (d1 - d2)
            m = (x - d1) / (d2 - d1)
            p = 0
        elif (x>d2 and x<=d3):
            n = 0
            m = (x - d3) / (d2 - d3)
            p = (x - d2) / (d3 - d2)
        elif (x>d3):
            n = 0
            m = 0
            p = 1
        fuzlst[0]=n
        fuzlst[1]=m
        fuzlst[2]=p

    def membership_function_plot(self,maxnum=None,minnum=None,label='observation'):
        ax=plt.gca()
        if maxnum==None:
            maxnum=10
        else:
            maxnum=maxnum
        if minnum==None:
            minnum=0
        else:
            minnum=minnum
        D1=minnum+(maxnum-minnum)*1/4
        D2=(maxnum+minnum)*1/2
        D3=minnum+(maxnum-minnum)*3/4
        DELTA=0.001

        ax.spines['left'].set_position(('data', D2))
        ax.spines['bottom'].set_position(('data',0))
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        plt.yticks([0.5,1])
        plt.xticks([minnum,D1,D2,D3,maxnum])
        plt.ylabel('Probability',labelpad=150)
        plt.xlabel(label)
        plt.title('membership_function')

        xn0=np.arange(minnum,D1,DELTA,float)
        yn0=0*xn0+1
        xn1=np.arange(D1,D2,DELTA,float)
        yn1=(xn1-D2)/(D1-D2)
        plt.plot(xn0,yn0,'b',label='N')
        plt.plot(xn1,yn1,'b')

        xm0=np.arange(D1,D2,DELTA,float)
        ym0=(xm0-D1)/(D2-D1)
        xm1=np.arange(D2,D3,DELTA,float)
        ym1=(xm1-D3)/(D2-D3)
        plt.plot(xm0,ym0,'r',label='M')
        plt.plot(xm1,ym1,'r')

        xp0=np.arange(D2,D3,DELTA,float)
        yp0=(xp0-D2)/(D3-D2)
        xp1=np.arange(D3,maxnum,DELTA,float)
        yp1=xp1*0+1
        plt.plot(xp0,yp0,'g',label='P')
        plt.plot(xp1,yp1,'g')


        plt.legend(loc='center right')
        plt.show()
class Gaussian_mf:
    def __init__(self,sigma_denominator,a):
        """
        :param sigma_denominator: 高斯函數的寬數字越小越窄
        :param a: sigmoid 斜率
        """
        self.sigma_denominator = sigma_denominator
        self.a = a
    def gaussian_mf(self,obs,min_obs,max_obs,fuzlst):
        l = [min_obs,max_obs]

        sigma = np.std(l) / self.sigma_denominator
        u = b = sum(l) / 2
        c = (min_obs - max_obs) / 5
        x = obs

        n = 1 - (1 / (1 + np.e ** (self.a * (x - b - c))))
        m = np.e ** (-(x - u) ** 2 / (2 * sigma ** 2))
        p = (1 / (1 + np.e ** (self.a * (x - b + c))))

        fuzlst[0] = n
        fuzlst[1] = m
        fuzlst[2] = p


    def gaussian_mf_plot(obs_name,sigma_denominator,a,maximum,minimum):

        for i in range(len(maximum)):
            ax=plt.gca()
            l = [maximum[i], minimum[i]]

            sigma = np.std(l) / sigma_denominator
            u = b = sum(l) / 2
            c = (l[0] - l[1]) / 5
            x = np.arange(minimum[i],maximum[i],0.001,float)

            y = np.e ** (-(x - u) ** 2 / (2 * sigma ** 2))
            y2 = 1 - (1 / (1 + np.e ** (a * (x - b - c))))
            y3 = (1 / (1 + np.e ** (a * (x - b + c))))


            plt.title(obs_name[i])
            plt.plot(x, y)
            plt.plot(x, y2)
            plt.plot(x, y3)

            plt.xlabel('Observation value')

            plt.savefig(f'{obs_name[i]}.png')
if __name__=='__main__':
    pass
