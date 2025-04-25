import numpy as np

def euler_to_rotation_matrix(roll, pitch, yaw):
    """
    Convert Euler angles (roll, pitch, yaw) to a rotation matrix.
    Args:
    - roll (float): rotation around x-axis in radians
    - pitch (float): rotation around y-axis in radians
    - yaw (float): rotation around z-axis in radians
    
    Returns:
    - rotation_matrix (np.array): 3x3 rotation matrix
    """
    # Rotation matrix for roll (x-axis)
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])
    
    # Rotation matrix for pitch (y-axis)
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    
    # Rotation matrix for yaw (z-axis)
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])
    
    # Combined rotation matrix (yaw -> pitch -> roll)
    rotation_matrix = R_z @ R_y @ R_x
    return rotation_matrix

def euler_to_vector(roll, pitch, yaw):
    """
    Convert Euler angles (roll, pitch, yaw) to a unit vector in the global coordinate system.
    Args:
    - roll (float): rotation around x-axis in degrees
    - pitch (float): rotation around y-axis in degrees
    - yaw (float): rotation around z-axis in degrees
    
    Returns:
    - unit_vector (np.array): resulting unit vector in global coordinates
    """
    # Convert degrees to radians
    roll_rad = np.radians(roll)
    pitch_rad = np.radians(pitch)
    yaw_rad = np.radians(yaw)
    
    # Get the rotation matrix from the Euler angles
    rotation_matrix = euler_to_rotation_matrix(roll_rad, pitch_rad, yaw_rad)
    
    # Apply rotation to the unit vector along x-axis [1, 0, 0]
    initial_vector = np.array([1, 0, 0])
    unit_vector = rotation_matrix @ initial_vector
    
    return unit_vector

def calculate_angle_with_x_axis(vector):
    """
    计算给定向量与x轴正方向[1,0,0]的夹角（度数）
    
    Args:
    - vector (np.array): 输入向量
    
    Returns:
    - angle (float): 与x轴正方向的夹角（度数）
    """
    # 单位化输入向量
    unit_vector = vector / np.linalg.norm(vector)
    
    # x轴正方向的单位向量
    x_axis = np.array([1, 0, 0])
    
    # 计算点积
    dot_product = np.dot(unit_vector, x_axis)
    
    # 计算夹角（弧度）
    angle_rad = np.arccos(np.clip(dot_product, -1.0, 1.0))
    
    # 转换为度数
    angle_deg = np.degrees(angle_rad)
    
    return angle_deg

def calculate_90_minus_angle(vector):
    """
    计算90度减去向量与x轴正方向夹角的结果
    
    Args:
    - vector (np.array): 输入向量
    
    Returns:
    - result (float): 90度减去夹角的结果（度数）
    """
    angle = calculate_angle_with_x_axis(vector)
    return 90 - angle

# Example usage:
roll = 34  # degrees
pitch = 82  # degrees
yaw = -74  # degrees

unit_vector = euler_to_vector(roll, pitch, yaw)
print("单位向量:", unit_vector)

angle = calculate_angle_with_x_axis(unit_vector)
print(f"与x轴夹角: {angle:.2f}度")

result = calculate_90_minus_angle(unit_vector)
print(f"90度减去夹角: {result:.2f}度")
