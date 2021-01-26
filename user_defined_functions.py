import os
import glob


def createDirectories(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def deleteFiles(file_path):
    for file_path in glob.glob(file_path):
        os.remove(file_path)


def interpolate(mass1, mass2, y1, y2, medial_mass):
    value = y1 + ((y2 - y1) / (mass2 - mass1)) * (medial_mass - mass1)
    return value
