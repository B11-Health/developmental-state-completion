import math

def two_point_minimax():
    # Common decoder output y on antipodal unit points: midpoint y=0 attains radius 1.
    x=(1.0,0.0)
    y=(0.0,0.0)
    e1=math.dist(x,y); e2=math.dist((-1.0,0.0),y)
    assert max(e1,e2)==1.0

def noise_threshold():
    a=(0.0,); b=(2.0,)
    Delta=math.dist(a,b)
    eta=1.0
    z=(1.0,)
    assert 2*eta==Delta
    assert math.dist(z,a)<=eta and math.dist(z,b)<=eta

def noncompact_infimum():
    vals=[1/(1+abs(t)) for t in [0,10,100,10000]]
    assert vals[-1] < 1e-3 and all(v>0 for v in vals)

if __name__=='__main__':
    two_point_minimax(); noise_threshold(); noncompact_infimum()
    print('PASS T7A illustrative checks')
