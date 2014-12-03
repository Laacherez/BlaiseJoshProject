'''
Simple quaternion object for use with quaternion integrators.
'''
import numpy as np

class Quaternion(object):
  
  def __init__(self, entries):
    ''' Constructor, takes 4 entries = s, p1, p2, p3 as a numpy array. '''
    self.entries = entries
    self.s = np.array(entries[0])
    self.p = np.array(entries[1:4])


  @classmethod
  def from_rotation(cls, phi):
    ''' Create a quaternion given an angle of rotation phi,
    which represents a rotation clockwise about the vector phi of magnitude 
    phi. This will be used with phi = omega*dt or similar in the integrator.'''
    phi_norm = np.linalg.norm(phi)
    s = np.array([np.cos(phi_norm/2.)])
    p = np.sin(phi_norm/2)*(phi/phi_norm)
    return cls(np.concatenate([s, p]))

    
  def __mul__(self, other):
    ''' 
    Quaternion multiplication.  In this case, other is the 
    right quaternion. 
    '''
    s = (self.s*other.s - 
         np.dot(self.p, other.p))
    p = (self.s*other.p + other.s*self.p
         + np.cross(self.p, other.p))
    return Quaternion(np.concatenate(([s], p)))


  def rotation_matrix(self):
    ''' 
    Return the rotation matrix representing rotation
    by this quaternion.
    '''
    # Cross product matrix for p
    P = np.array([[0., -1.*self.p[2], self.p[1]], 
                 [self.p[2], 0., -1.*self.p[0]],
                 [-1.*self.p[1], self.p[0], 0.]])
    # Put pieces together to get rotation matrix.
    R = 2.*(np.outer(self.p, self.p) + 
            (self.s**2 - 0.5)*np.identity(3)
            + self.s*P)
    return R

  def __str__(self):
    return '[ %f, %f, %f, %f ]' % (self.s, self.p[0], self.p[1], self.p[2])