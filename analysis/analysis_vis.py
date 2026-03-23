from main_analysis import de_r, Ve_r, Fe_r, alpha_aero, Cl, Cd, alpha_trim,            Cl_alpha, Cl0, alpha0 
from matplotlib import pyplot as plt
import numpy as np
import sys
import matplotlib



font = {'family' : "Times New Roman",
        'size'   : 14}

matplotlib.rc('font', **font)



def plot_fit(x, y, names):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    

    coeffs = np.polyfit(x, y, 1)
    fit = np.poly1d(coeffs)
    
    y_pred = fit(x)
    
    #compute R2
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    
   
    x_u = np.unique(x)
    sign = '+' if coeffs[1] >= 0 else '-'
   
    plt.scatter(x, y, color='black', marker='x')  # raw data
    plt.plot(x_u, fit(x_u), ls='--', color='blue',         
             label = f'Fit: y={coeffs[0]:.3g}x {sign} {abs(coeffs[1]):.4g}, $R^2$={r2:.4g}')
    
    plt.xlabel(names[0])
    plt.ylabel(names[1])
    plt.legend()
    
    # save and show
    plt.tight_layout()
    plt.savefig('analysis/outputs_vis/' + names[2] + '_vs_' + names[3] + '.png', dpi=300)
    plt.show()




def plot(x,y,names):
    plt.scatter(x, y, color='black', marker = "x")  # raw data

    plt.xlabel(names[0])
    plt.ylabel(names[1])
    plt.savefig('analysis/outputs_vis/'+ names[2] + '_vs_'+ names[3] +'.png', dpi=300)
    plt.show()


de_r = de_r.to_numpy(dtype=float)
Ve_r = np.asarray(Ve_r, dtype=float)
Fe_r = Fe_r.to_numpy(dtype=float)
alpha_aero = np.asarray(alpha_aero, dtype=float)
alpha_trim = np.asarray(alpha_trim, dtype=float)
Cl = np.asarray(Cl, dtype=float)
Cd = np.asarray(Cd, dtype=float)



plot_fit(Ve_r, de_r, ["Reduced equivalent velocity [m/s]", "Reduced elevator deflection [rad]", "Ve_r", "de_r"])
plot_fit(Ve_r, Fe_r, ["Reduced equivalent velocity [m/s]", "Reduced stick force [N]", "Ve_r", "Fe_r"])
plot_fit(alpha_trim, de_r, [r"$\alpha$"+" [rad]", "Reduced elevator deflection [rad]", "alpha", "de_r"])
plot_fit(alpha_aero, Cl,  [r"$\alpha$"+" [rad]", "Coefficient of lift [-]","alpha", "Cl"]) 
plot(Cd, Cl,  ["Coefficient of lift [-]", "Drag coefficient[-]", "Cl", "Cd"])
plot_fit(Cl**2, Cd,  ["Coefficient of lift suqared [-]", "Drag coefficient[-]", "Cl^2", "Cd"])






'''
der / Ve_r
Fe_r / Ve_r
de_r / alpha

Cl/ alpha

Cl2 / Cd

best fit for the datatpoints
'''