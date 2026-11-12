import numpy as np


def linear_stepping(x:float, y:float, x0:float, y0:float, boxSize:float):
    """
    Returns potential values based on input locations,
    Potential is linearly proportional to the difference between the points,
    x = particle x position
    y = particle y position
    x_0 = destination x position
    y_0 = destination y position.
    """
    
    return [max(0,(x-x0)/boxSize),
            max(0,(x0-x)/boxSize),
            max(0,(y-y0)/boxSize),
            max(0,(y0-y)/boxSize)]



def exponential_stepping(x:float, y:float, x0:float, y0:float, boxSize:float):
    """
    Returns potential values based on input locations,
    Potential is exponentially proportional to the difference between the points,
    x = particle x position
    y = particle y position
    x_0 = destination x position
    y_0 = destination y position.
    """
    
    return [max(0,(1-(np.e**((x0-x))))),
            max(0,(1-(np.e**((x-x0))))),
            max(0,(1-(np.e**((y0-y))))),
            max(0,(1-(np.e**((y-y0)))))]
