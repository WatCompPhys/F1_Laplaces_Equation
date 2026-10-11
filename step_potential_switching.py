from boundary_class import boundaries

def step_switching(x: float, y: float, x_0: float, y_0: float) -> list:
    """
    Returns potential values based on input locations,
    x = particle x position
    y = particle y position
    x_0 = destination x position
    y_0 = destination y position.
    """

    disp_x = x - x_0
    disp_y = y - y_0

    # Go Left
    if disp_x > 0:
        # Go Down
        if disp_y > 0:
            R = 1
            L = 0
            T = 1
            B = 0
        # Go Up
        elif disp_y < 0:
            R = 1
            L = 0
            T = 0
            B = 1
        # Stop
        else:
            R = 1
            L = 0
            T = 0
            B = 0

    # Go Right
    elif disp_x < 0:
        # Go Down
        if disp_y > 0:
            R = 0
            L = 1
            T = 1
            B = 0
        # Go Up
        elif disp_y < 0:
            R = 0
            L = 1
            T = 0
            B = 1
        # Stop
        else:
            R = 0
            L = 1
            T = 0
            B = 0

    # Stop
    else:
        # Go Down
        if disp_y > 0:
            R = 0
            L = 0
            T = 1
            B = 0
        # Go Up
        elif disp_y < 0:
            R = 0
            L = 0
            T = 0
            B = 1
        # Stop
        else:
            R = 0
            L = 0
            T = 0
            B = 0

    new_values = [R, L, T, B]

    return new_values