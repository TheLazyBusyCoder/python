
def fun(a, fn):
  ans = fn(a)
  return ans


def square(a):
  return a * a


x = square

print(fun(5, x))
