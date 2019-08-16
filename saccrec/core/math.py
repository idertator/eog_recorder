from math import radians, tan


def distance_to_subject(distance: float, angle: float) -> float:
    """Calcula la distancia al sujeto para lograr un ángulo
    
    Args:
        distance (float): Distancia entre los puntos en la pantalla
        angle (float): Ángulo que se desea lograr
    
    Returns:
        float: Distancia al paciente
    """
    return (distance / 2.0) / tan(radians(angle / 2.0))


def points_distance(distance: float, angle: float) -> float:
    """Calcula la distancia entre los puntos de estimulación
    
    Args:
        distance (float): Distancia al sujeto
        angle (float): Ángulo que se desea lograr
    
    Returns:
        float: Distancia entre los puntos
    """
    return (tan(radians(angle / 2.0)) * distance) * 2
