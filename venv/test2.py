import test
import Prof
p = Prof.Prof(1, 'sads', 'asd')
l = [p]
print(p.time_preferred)
p.time_preferred.append(34)
print(p.time_preferred)
print(test.d(l).time_preferred)
