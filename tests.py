# int inverse_gcd(int y, int x){
# 	int t = 0, newt = 1;
# 	int r = x, newr = y;
# 	int temp;
# 	int quotient;
# 	while(newr!=0){
# 		quotient = r / newr;
# 		temp = newt;
# 		newt = t - quotient*newt;
# 		t = temp;
#
# 		temp = newr;
# 		newr = r - quotient*newr;
# 		r = temp;
# 	}
#
# 	if(r>1){ return -1213456; }
# 	if(t<0){
# 		t = t+x;
# 		return t;
# 		}
# 		if(t>0) return t;
# 		else return -1245455;
#
# }
def ass(y,x):
    if y>x:
        return ine(x, y)
    return ine(y, x)


def ine(y, x):
    t = 0
    newt = 1
    r = x
    newr = y
    while newr != 0:
        quotient = int(r / newr);
        temp = newt;
        newt = t - quotient * newt;
        t = temp;

        temp = newr;
        newr = r - quotient * newr;
        r = temp;
    if r > 1:
        return "no1"
    if t < 0:
        t = t+x;
        return t;
    if t>0:
        return t;
    return "no2"

print(ass(26,15))
