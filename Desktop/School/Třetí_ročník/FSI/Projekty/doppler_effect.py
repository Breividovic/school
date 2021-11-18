import pandas as pd
import matplotlib.pyplot as plt


def simulate_doppler_effect(constant_frequency, initial_speed, acceleration,
                            speed_of_sound=343, track_length=1000, viewer_distance=500):
    print("Simulation of Doppler effect")
    print("Attributes:")
    print("\t Sound frequency:", constant_frequency, "Hz")
    print("\t Initial speed:  ", initial_speed, "m/s")
    print("\t Acceleration:   ", acceleration, "m/s^2")
    print("\t Speed of sound: ", speed_of_sound, "m/s")
    print("\t Track length:   ", track_length, "m")
    print("\t Viewer distance:", viewer_distance, "m")
    print()

    distance = 0
    speed = initial_speed
    t = 0
    frequency = 0
    track_ratio = track_length / viewer_distance

    distances = []
    frequencies = []



    print("+----------+--------------+----------------+")
    print("| Time (s) | Distance (m) | Frequency (Hz) |")
    print("+----------+--------------+----------------+")
    while distance < track_length:
        speed += acceleration
        distance += speed
        t += 1


        if distance < track_length / track_ratio:
            frequency = (constant_frequency * speed_of_sound /
                         (speed_of_sound - (((initial_speed ** 2) +
                                             (2 * acceleration * distance)) ** 0.5)))
        else:
            frequency = (constant_frequency * speed_of_sound /
                         (speed_of_sound + ((initial_speed ** 2) +
                                            (2 * acceleration * distance)) ** 0.5))

        distances.append(distance)
        frequencies.append(frequency)

        time = str(t) + (8 - len(str(t))) * " "
        dist = str(distance) + (12 - len(str(distance))) * " "
        freq = str(round(frequency, 2)) + (14 - len(str(round(frequency, 2)))) * " "
        print("|", time, "|", dist, "|", freq, "|")

    print("+----------+--------------+----------------+")

    df = pd.DataFrame({"distance": distances, "frequency": frequencies})

    df.plot(x="distance", y="frequency", xlabel="distance", ylabel="frequency", kind="line")
    plt.show()

simulate_doppler_effect(5000, 10, 5)

