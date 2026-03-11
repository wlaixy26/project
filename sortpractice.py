def ef(li,val):
    li.sort()
    left = 0
    right = len(li)-1
    while left <= right:
        mid = (left+right)//2
        if li[mid] < val:
            left = mid+1
        elif li[mid] > val:
            right = mid-1
        else:
          return True
    return False

def bubu(li):#冒泡
    for i in range(len(li)-1):
        for j in range(len(li)-1-i):
            if li[j] > li[j+1]:
                li[j], li[j+1] = li[j+1], li[j]
    return li

def xz(li):#选择
    ki=[]
    for i in range(len(li)):
        minl = min(li)
        ki.append(minl)
        li.remove(minl)
    return ki

def xza(li):   #选择plus
    for i in range(len(li)-1):
        minloc = i
        for j in range(i+1,len(li)):
            if li[j] < li[minloc]:
                minloc = j
        li[minloc], li[i] = li[i], li[minloc]
    return li

def charu(li):#插入
    for i in range(1,len(li)):#摸到的牌
        temp = li[i]
        j = i - 1#手里的牌
        while j >= 0 and li[j] > temp:
            li[j+1]=li[j]
            j=j-1
        li[j+1]=temp
    return li

def partition(li,left,right):
    tmp = li[left]
    while left < right:
        while left <right and li[right] >= tmp: #找比最左边小的
            right = right - 1#从右往左走
        li[left]=li[right]  #把右边的值写道左边
        while left <right and li[left] < tmp:
            left = left+1
        li[right]=li[left]
    li[left] = tmp         #tmp归位置
    return left

def fastsort(li,left,right):
    if left < right: #至少两个元素
     pi = partition(li,left,right)
     fastsort(li,left,pi-1)
     fastsort(li,pi+1,right)
    return li

l = [5,7,1,3,4,6]
fastsort(l, 0, len(l)-1)
print(l)
