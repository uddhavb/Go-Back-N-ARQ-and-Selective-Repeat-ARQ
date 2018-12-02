import matplotlib.pyplot as plt
plt.plot([100,200,300,400,500,600,700,800,900,1000], \
[294.94026222229,147.3446613311768, 94.92234601974488, 74.45712990760804, 54.89262681007385 \
, 44.00137395858765, 40.41090669631958, 35.527920150756835, 32.257616949081424, 27.258062744140624], \
'ro')
plt.axis([0, 1000, 0, 300])
plt.ylabel('average RTT')
# plt.label("MSS = 500, p = 0.05")
plt.xlabel('MSS')
plt.show()