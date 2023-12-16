#This program animates a 3d linear transform encoded in the matrix containted in the "Matrix Entries" xlsv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import sys
from copy import deepcopy
from math import ceil

#Defines the time of the animation in seconds, the fps, and the number of buffer frames added to the end of an animation
ANIMATION_LENGTH = 1.5
FPS = 60
TOT_FRAMES = ANIMATION_LENGTH * float(FPS)
BUFFER_FRAMES = 0.5 * float(FPS)

#Takes a list of lists lst and returns a list of the ith element of each sublist
def extract(lst, i):
    return [sub[i] for sub in lst]

#Defines the dimensions of the plot
def set_plot():
    ax.set_xlim([-absolute_max, absolute_max])
    ax.set_ylim([-absolute_max, absolute_max])
    ax.set_zlim([-absolute_max, absolute_max])

#Plots the given vectors
def plot (v_1, v_2, v_3):
    ax.cla()
    set_plot()
    ax.quiver(origin,origin,origin,v_1,v_2,v_3, color = ['r','g','b'])

#Runs the animation
def run_animation():
    #Bool for if the annimation is running
    anim_running = True

    #Changes the running state of the animation on spacebar press
    def on_key(event):
        #Guard clause for eliminating any non-spacebar presses
        if event.key != ' ':
            return
        
        #Switches the state of animation and the associated boolean
        nonlocal anim_running
        if anim_running:
            ani.event_source.stop()
            anim_running = False
        else:
            ani.event_source.start()
            anim_running = True
    
    #Function which defines each time step in the animation
    def update (frame):
        #If the animation hasn't completed, update each vector. Otherwise, set it to the final vector
        if frame <= TOT_FRAMES:
            v_1 = e_1 + dc_1 * frame
            v_2 = e_2 + dc_2 * frame
            v_3 = e_3 + dc_3 * frame
        else:
            v_1 = e_1_prime
            v_2 = e_2_prime
            v_3 = e_3_prime
        plot(v_1, v_2, v_3)

    #Checks for key press event and changes state of animation if detected
    fig.canvas.mpl_connect('key_press_event', on_key)
    ani = animation.FuncAnimation(fig=fig, func=update, frames=ceil(TOT_FRAMES + BUFFER_FRAMES), interval= (1/float(FPS)))
    plt.show()


#MAIN
#Creating a set of initial vectors in a matrix
origin = np.array([0.,0.,0.])
e_1 = np.array([1.,0.,0.])
e_2 = np.array([0.,1.,0.])
e_3 = np.array([0.,0.,1.])
initial_matrix = np.array([e_1, e_2, e_3])

#Prompt the user to enter the data into the excel sheet
#input("Please enter the desired 3x3 matrix entries into the spreadsheet. Then close the sheet. Press enter when complete.")

#Creates the matrix that will hold the matrix
transform_matrix = np.array([])

#Reads file to a dataframe
try:
    matrix_data = pd.read_excel('Matrix Entries.xlsx')
except PermissionError:
    print("Please close the excel file and try again.")
    sys.exit([-1])

#Converts matrix data dataframe to transform matrix np array
transform_matrix = matrix_data.to_numpy()

#Creates the final matrix by applying the transform on the initial matrix
try:
    final_matrix = np.matmul(transform_matrix, initial_matrix)
except ValueError:
    print("Check that the matrix in the excel file is 3x3 and that the top row is empty.")
    sys.exit([-1])

#Creates the vectors after the transformation
e_1_prime = extract(final_matrix, 0)
e_2_prime = extract(final_matrix, 1)
e_3_prime = extract(final_matrix, 2)

#Calculates the change vectors
c_1 = e_1_prime - e_1
c_2 = e_2_prime - e_2
c_3 = e_3_prime - e_3

#Calculates the per frame change vectors
dc_1 = c_1/(TOT_FRAMES)
dc_2 = c_2/(TOT_FRAMES)
dc_3 = c_3/(TOT_FRAMES)

#Finding the longest length of an axis to set up the right size of plot later
x_max = max(initial_matrix[0].max(), final_matrix[0].max())
y_max = max(initial_matrix[1].max(), final_matrix[1].max())
z_max = max(initial_matrix[2].max(), final_matrix[2].max())
absolute_max = max(x_max, y_max, z_max)

#Setting up the intial 3D plot
t = np.linspace(0, ANIMATION_LENGTH, FPS)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#Setting the boundaries of the plot
set_plot()

#Plotting the initial vectors
v_1 = deepcopy(e_1)
v_2 = deepcopy(e_2)
v_3 = deepcopy(e_3)
ax.quiver(origin, origin, origin, v_1, v_2, v_3)

#Setting up the animation
run_animation()
plt.show()