'''
Class to look at samples on a sphere and verify that they are a uniform
distribution.
'''
import numpy as np
from matplotlib import pyplot
from quaternion import Quaternion

class UniformAnalyzer(object):
  ''' 
  This object just takes samples on a sphere and analyzes their 
  distribution to determine if they are uniformly distributed.
  '''
  def __init__(self, samples, name):
    ''' 
    Just copy the reference to the list of samples.
    Each sample should be of the same length, and represent
    a point on the sphere.
    '''
    self.dim = len(samples[0])
    if isinstance(samples[0][0], Quaternion):
      if self.dim == 1:
        self.samples = [q[0].entries for q in samples]
        self.dim = 4
      else:
        raise NotImplementedError('Cannot handle distribution of '
                                  'multiple quaternions')
    else:
      self.samples = samples

    # Name used for plotting, etc.
    self.name = name

  def analyze_samples(self):
    ''' Analyze samples by calculating means of spherical harmonics. '''
    # Here 10 is the number of L's we will look at.
    statistics = [[] for _ in range(10)]  
    n_xi_eta_pairs = 1
    for k in range(n_xi_eta_pairs):
      xi, eta = self.generate_xi_eta()
      for L in range(1, len(statistics) + 1):
        harmonics = []
        for sample in self.samples:
          u = np.inner(xi, sample)
          v = np.inner(eta, sample)
          # Numpy arctan is always between -pi/2 and pi/2.
          theta = np.arctan(v/u)  + (u < 0)*np.pi
          harmonics.append(np.cos(L*theta))
        statistics[L-1].append(np.mean(harmonics))
    L_means = []
    for L in range(1, len(statistics) + 1):
      L_means.append(np.mean(statistics[L-1]))
      print ('Mean at L = %d is: %f +/- %f' % 
             (L, L_means[-1], 
              np.std(statistics[L-1])))

    return L_means

  def generate_xi_eta(self):
    ''' Generate a random pair of orthonormal vectors. '''
    xi = np.random.normal(0., 1., self.dim)
    xi = xi/np.linalg.norm(xi)
    
    eta = np.random.normal(0., 1., self.dim)
    eta = eta - np.inner(eta, xi)*xi
    
    eta = eta/np.linalg.norm(eta)

    return xi, eta
    
    
def compare_distributions(uniform_analyzer_list):
  ''' 
  Takes a list of UniformAnalyzer objects, and plots their average L values over
  the xi eta pairs generated for each.
  '''
  for ua in uniform_analyzer_list:
    pyplot.plot(ua.analyze_samples(), label=ua.name)
  
    
  pyplot.legend(loc="best", prop={'size': 9})
  pyplot.title('Comparison of distributions on the sphere, N = %d' % len(ua.samples))
  pyplot.xlabel('L')
  pyplot.savefig("./CompareDistributions.pdf")
  
  
    
    
