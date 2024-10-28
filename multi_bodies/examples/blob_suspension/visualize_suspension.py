import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
# Function to read particle positions from a file
def read_positions(file_path):
    positions = []
    with open(file_path, 'r') as file:
        k=0
        step = 0
        for line in file:
            k+=1
            line = line.split()
            if k==1:
              Np = int(line[0]) 
            else:	
              if line[0]!=str(Np):             
                positions.append(line[0:3])
              else:
                step+=1
    print(Np)       
    return Np,positions

# Function to plot particles in 3D
def plot_particles(positions):
    
    xs, ys, zs = zip(*positions)
    
    ax.scatter(xs, ys, zs)
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    
    plt.show()

# Main function
if __name__ == "__main__":
    file_path = 'run_blobs.sphere_array.config'  # Path to the file with positions
    Np,positions = read_positions(file_path)
    Nstep = int(len(positions)/Np)
    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    for i in range(Nstep):
     pos = np.array(positions[i*Np:(i+1)*Np],dtype = float)

     xs, ys, zs = zip(*pos)    
     #ax.scatter(xs, ys, zs)
     ax1.scatter(xs, zs, c=zs, vmin = 0, vmax = 25, cmap = 'viridis', alpha = 0.5)
     ax2.scatter(xs, ys, c=zs, vmin = 0, vmax = 25, cmap = 'viridis', alpha = 0.5)
    
     ax1.set_xlabel('X')
     ax1.set_ylabel('Z')
     ax1.set_xlim([-5,65])
     ax1.set_ylim([0,25])

     ax2.set_xlabel('X')
     ax2.set_ylabel('Y')
     ax2.set_xlim([-5,65])
     ax2.set_ylim([-5,25])
     #plt.ylim([-5,25])
     #ax.set_zlim(0,25)
     filename = file_path + str(i).zfill(3) + '.png'
     plt.savefig(filename)
     ax1.cla() 
     ax2.cla() 
