import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm

# data
sale_price = np.array([6625,3936.272,8000,3192.84,10350])
land_square_feet = np.array([1633,2272,2369,1750,3717])

# scatter plot
plt.plot(land_square_feet,sale_price,'.r')
plt.xlabel('land square feet')
plt.ylabel('sale price')
plt.show()

# h functions matrix
h_mat_1 = np.array([[0,1],[1,0],[1000,1]]).T

# examples matrix
exp_mat = np.vstack([land_square_feet,sale_price]).T

# cost function
mat1 = np.hstack([np.ones([land_square_feet.shape[0],1]),land_square_feet.T[:,np.newaxis]])
h_x_1 = np.dot(mat1,h_mat_1)

temp = np.dot(sale_price[:,np.newaxis],np.ones([1,h_x_1.shape[1]]))
cost_mat = 1/(2*exp_mat.shape[0])*(sum((h_x_1-temp)**2))

#
land_square_feet_2 = np.array([1000,2000,3000])
mat1 = np.hstack([np.ones([land_square_feet_2.shape[0],1]),land_square_feet_2.T[:,np.newaxis]])
h_x_2 = np.dot(mat1,h_mat_1)

#
theta1 = np.arange(1,6)
theta0 = np.zeros([5])

h_mat_3 = np.vstack([theta0,theta1])

# cost function
mat1 = np.hstack([np.ones([land_square_feet.shape[0],1]),land_square_feet.T[:,np.newaxis]])
h_x_3 = np.dot(mat1,h_mat_3)

temp = np.dot(sale_price[:,np.newaxis],np.ones([1,h_x_3.shape[1]]))
cost_mat = 1/(2*exp_mat.shape[0])*(sum((h_x_3-temp)**2))