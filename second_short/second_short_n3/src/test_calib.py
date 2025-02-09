dist_calib_data = [[0, 0, 0],
                    [250, 4.75, 0],
                    [375, 9.5, 0],
                    [500, 14.5, 0],
                    [625, 18.5, 0],
                    [750, 22.5, 0],
                    [875, 26, 0],
                    [1000, 29, 0],
                    [1125, 31.75, 0],
                    [1250, 34.25, 0]]

for i in range(0,len(dist_calib_data)-1):
    y1, x1, m1 = dist_calib_data[i+1]
    y0, x0, m0 = dist_calib_data[i]
    m0 = (y1-y0)/(x1-x0)
    dist_calib_data[i][2] = m0
dist_calib_data[len(dist_calib_data)-1][2] = dist_calib_data[len(dist_calib_data)-2][2]

def get_drive_time_for_distance(distance):
    drive_time = 0
    for y0, x0, m in dist_calib_data:
        if distance < x0:
            break
        else:
            drive_time = y0 + (distance-x0)*m
    return drive_time

distances = [16, 24]

for distance in distances:
    print(f"Drive time for {distance} inches is {get_drive_time_for_distance(distance)}")