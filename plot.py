import numpy as np
import matplotlib.pyplot as plt

x = np.arange(51)


coorXmanhattan=np.load("coorXmanhattan.npy")
coorYOpenCloseRatiomanhattan=np.load("coorYOpenCloseRatiomanhattan.npy")
sd_err_ratiomanhattan=np.load("sd_err_ratiomanhattan.npy")
coorYtimemanhattan=np.load("coorYtimemanhattan.npy")
sd_timemanhattan=np.load("sd_timemanhattan.npy")

coorXzero=np.load("coorXzero.npy")
coorYOpenCloseRatiozero=np.load("coorYOpenCloseRatiozero.npy")
sd_err_ratiozero=np.load("sd_err_ratiozero.npy")
coorYtimezero=np.load("coorYtimezero.npy")
sd_timezero=np.load("sd_timezero.npy")

n='\n'
# print(sd_timemanhattan, len)
# print(len(coorXzero),len(coorYOpenCloseRatiozero),len(sd_err_ratiozero),len(coorYtimezero),len(sd_timezero))
plt.xlabel('Buckets')
plt.ylabel('Open/Close ratio')
# plt.ylabel('Runtime/s')
plt.title('The ratio of Open/Close of lazy-A*')
# plt.title('Runtime of lazy-A*')
plt.xlim([0,512])
# plt.errorbar(coorXzero,coorYtimezero,sd_timezero, label="No heuristic")
# plt.errorbar(coorXmanhattan,coorYtimemanhattan,sd_timemanhattan,label="Manhattan Distance heuristic")
plt.errorbar(coorXmanhattan,coorYOpenCloseRatiomanhattan,sd_err_ratiomanhattan, label = 'Manhattan Distance heuristic')
plt.errorbar(coorXzero,coorYOpenCloseRatiozero,sd_err_ratiozero, label = "No heuristic")
plt.legend()
plt.show()



# plt.xlabel("Episode")
# plt.ylabel("Steps per Episode")
# plt.title("Dyna Maze - with Dyna-Q\n ")
# plt.plot(x,data0, label = "n = 0")
# plt.plot(x,data1, label = "n = 5")
# plt.plot(x,data2, label = "n = 50")
# plt.legend()
# plt.show()