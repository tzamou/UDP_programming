import numpy as np
import matplotlib.pyplot as plt
#模糊化------------------------------------------------------------------------------------------------------------

#first
class Observation:
    def __init__(self,max_array,min_array):
        self.max_array = max_array
        self.min_array = min_array
        assert len(max_array)==len(min_array)
        self.length = len(max_array)
# class
def transform_observation(obs,denominator):
    fuzzylist = np.zeros((8, 3))
    maximum = [0.243836122382149, 0.26096066466958034, 0.5429821429983187, 0.24733888311207228, 0.28781175260419184,
               0.5219398954427787, 0.19009299698100937, 0.3193822980298661]
    minimum = [0.1376097596035281, 0.03909854459337937, 0.3602279178851564, 0.1576450126829109, 0.0469565299996373,
               0.3485320661780878, 0.008999067465086353, 0.08198913776795991]
    for i in range(len(obs)):
        membership_func(obs[i],minimum[i],maximum[i],fuzzylist[i],denominator)
    return fuzzylist.flatten()
    #print(fuzzylist.flatten(),len(fuzzylist.flatten()))

def membership_func(x,minx,maxx,fuzlst,denominator):
    d1=minx+(maxx-minx)*1/denominator
    d2=(maxx+minx)*1/2
    d3=minx+(maxx-minx)*(denominator-1)/denominator
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

def membership_function_plot(maxnum=None,minnum=None,label='observation'):
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

def gaussian_mf(obs,sigma_denominator,a,envstep):
    if envstep == 0:
        fuzzylist = np.zeros((8, 3))
        maximum = [0.243836122382149, 0.26096066466958034, 0.5429821429983187, 0.24733888311207228, 0.28781175260419184,
                   0.5219398954427787, 0.19009299698100937, 0.3193822980298661]
        minimum = [0.1376097596035281, 0.03909854459337937, 0.3602279178851564, 0.1576450126829109, 0.0469565299996373,
                   0.3485320661780878, 0.008999067465086353, 0.08198913776795991]
    if envstep == 1:
        fuzzylist = np.zeros((7, 3))
        maximum = [0.243836122382149, 0.26096066466958034, 0.5429821429983187, 0.24733888311207228, 0.28781175260419184,
                   0.5219398954427787, 0.19009299698100937]
        minimum = [0.1376097596035281, 0.03909854459337937, 0.3602279178851564, 0.1576450126829109, 0.0469565299996373,
                   0.3485320661780878, 0.008999067465086353]
    if envstep == 2:
        fuzzylist = np.zeros((4, 3))
        maximum = [0.243836122382149, 0.26096066466958034, 0.5429821429983187, 0.3193822980298661]
        minimum = [0.1376097596035281, 0.03909854459337937, 0.3602279178851564, 0.08198913776795991]
    for i in range(len(maximum)):
        l = [maximum[i], minimum[i]]

        sigma = np.std(l) / sigma_denominator
        u = b = sum(l) / 2
        c = (l[0] - l[1]) / 5
        x = obs[i]

        m = np.e ** (-(x - u) ** 2 / (2 * sigma ** 2))
        n = 1 - (1 / (1 + np.e ** (a * (x - b - c))))
        p = (1 / (1 + np.e ** (a * (x - b + c))))
        fuzzylist[i][0] = m
        fuzzylist[i][1] = n
        fuzzylist[i][2] = p
    return fuzzylist.flatten()

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
    obs1 = ['The x-axis of the palm', 'The y-axis of the palm', 'The z-axis of the palm',
            'The x-axis of the object', 'The y-axis of the object', 'The z-axis of the object',
            'The distance from the palm to the object']

    obs2 = ['The x-axis of the object (palm)', 'The y-axis of the object (palm)', 'The z-axis of the object (palm)',
            'The distance from the object (palm) to above the target']
    # for i in range(8):
    #     membership_function_plot(maxnum=maximum[i],minnum=minimum[i],label=obs[i])
    gaussian_mf_plot(obs1, 4, 183, maximum1, minimum1)
    gaussian_mf_plot(obs2, 2, 57, maximum2, minimum2)