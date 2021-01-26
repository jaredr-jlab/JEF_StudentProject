from user_defined_functions import interpolate


# Set the final the parameter values for fixed masses
mainDict = {}

mainDict['mean'] = [0.0101, 0.0251, 0.05004,
                    0.0750, 0.0999, 0.1499,
                    0.1999, 0.2498, 0.2999,
                    0.3499, 0.3999, 0.4099]

mainDict['mean_min'] = [0.009, 0.024, 0.049,
                        0.074, 0.098, 0.148,
                        0.198, 0.248, 0.298,
                        0.348, 0.398, 0.408]

mainDict['mean_max'] = [0.011, 0.026, 0.051,
                        0.076, 0.101, 0.151,
                        0.201, 0.251, 0.301,
                        0.351, 0.401, 0.411]

mainDict['aL'] = [1.0, 1.0, 1.0,
                  1.5511, 1.2209, 1.1965,
                  1.3140, 1.2924, 1.3842,
                  1.7685, 1.0, 1.0]

mainDict['aL_min'] = [-3.0, -3.0, -3.0,
                      1.1117, 1.1117, 1.1117,
                      1.1117, 1.1117, 1.1117,
                      1.1117, -3.0, -3.0]

mainDict['aL_max'] = [2.0, 2.0, 2.0,
                      1.7371, 1.7371, 1.7371,
                      1.7371, 1.7371, 1.7371,
                      1.7371, 2.0, 2.0]

mainDict['aR'] = [-1.3, -1.3, -1.3,
                  -1.6966, -1.5868, -1.3621,
                  -1.3897, -1.1740, -1.6044,
                  -1.5839, -1.3, -1.3]

mainDict['aR_min'] = [-3.0, -3.0, -3.0,
                      -1.8567, -1.8567, -1.8567,
                      -1.8567, -1.8567, -1.8567,
                      -1.8567, -3.0, -3.0]

mainDict['aR_max'] = [3.0, 3.0, 3.0,
                      -1.1883, -1.1883, -1.1883,
                      -1.1883, -1.1883, -1.1883,
                      -1.1883, 3.0, 3.0]

mainDict['sigmaL'] = [0.0011, 0.0014, 0.0019,
                      0.00216, 0.00231, 0.00281,
                      0.00281, 0.00281, 0.00201,
                      0.00178, 0.0008, 0.0005]

mainDict['sigmaL_min'] = [0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0]

mainDict['sigmaL_max'] = [0.002, 0.002, 0.00274,
                          0.00274, 0.00274, 0.00274,
                          0.00274, 0.00274, 0.00274,
                          0.00274, 0.00274, 0.00274]

mainDict['sigmaR'] = [0.0012, 0.0023, 0.0027,
                      0.00303, 0.00284, 0.00315,
                      0.00358, 0.00331, 0.00323,
                      0.00277, 0.0015, 0.00085]

mainDict['sigmaR_min'] = [0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0]

mainDict['sigmaR_max'] = [0.00360, 0.00360, 0.00360,
                          0.00360, 0.00360, 0.00360,
                          0.00360, 0.00360, 0.00360,
                          0.00360, 0.00360, 0.00360]

mainDict['fracL'] = [0.5, 0.5, 0.5,
                     0.8677, 0.5790, 0.6085,
                     0.4914, 0.4417, 0.3247,
                     0.5188, 0.5, 0.57]

mainDict['fracL_min'] = [0.4, 0.1, 0.1,
                         0.1368, 0.1368, 0.1368,
                         0.1368, 0.1368, 0.1368,
                         0.1368, 0.1, 0.1]

mainDict['fracL_max'] = [1.0, 1.0, 1.0,
                         1.09481, 1.09481, 1.09481,
                         1.09481, 1.09481, 1.09481,
                         1.09481, 1.0, 1.0]

mainDict['nL'] = [6.0, 6.0, 6.0,
                  3.0743, 3.2069, 3.2069,
                  3.2069, 2.1432, 1.2828,
                  1.2828, 6.0, 6.0]

mainDict['nL_min'] = [1.1, 1.1, 1.1,
                      1.2431, 1.2431, 1.2431,
                      1.2431, 1.2431, 1.2431,
                      1.2431, 1.1, 1.1]

mainDict['nL_max'] = [6.0, 6.0, 6.0,
                      3.1078, 3.1078, 3.1078,
                      3.1078, 3.1078, 3.1078,
                      3.1078, 6.0, 6.0]

mainDict['nR'] = [6.0, 6.0, 6.0,
                  2.3963, 5.9907, 5.9907,
                  4.8832, 3.9238, 2.3966,
                  3.1914, 6.0, 6.0]

mainDict['nR_min'] = [0.0, 0.0, 0.0,
                      2.0552, 2.0552, 2.0552,
                      2.0552, 2.0552, 2.0552,
                      2.0552, 0.0, 0.0]

mainDict['nR_max'] = [6.0, 6.0, 6.0,
                      5.1380, 5.1380, 5.1380,
                      5.1380, 5.1380, 5.1380,
                      5.1380, 6.0, 6.0]

# Set the final the parameter values for intermediate masses
medialDict = {}

medialDict['mean'] = [interpolate(0.01, 0.025, mainDict['mean'][0], mainDict['mean'][1], 0.02),
                      interpolate(0.025, 0.05, mainDict['mean'][1], mainDict['mean'][2], 0.03),
                      interpolate(0.025, 0.05, mainDict['mean'][1], mainDict['mean'][2], 0.0375),
                      interpolate(0.025, 0.05, mainDict['mean'][1], mainDict['mean'][2], 0.04),
                      interpolate(0.05, 0.075, mainDict['mean'][2], mainDict['mean'][3], 0.06),
                      interpolate(0.05, 0.075, mainDict['mean'][2], mainDict['mean'][3], 0.07),
                      interpolate(0.1, 0.15, mainDict['mean'][4], mainDict['mean'][5], 0.125),
                      interpolate(0.15, 0.2, mainDict['mean'][5], mainDict['mean'][6], 0.175),
                      interpolate(0.4, 0.41, mainDict['mean'][10], mainDict['mean'][11], 0.405)]

medialDict['mean_min'] = [0.019, 0.029, 0.036,
                          0.039, 0.058, 0.068,
                          0.123, 0.173, 0.404]

medialDict['mean_max'] = [0.021, 0.031, 0.038,
                          0.041, 0.061, 0.071,
                          0.126, 0.176, 0.406]

medialDict['aL'] = [interpolate(0.01, 0.025, mainDict['aL'][0], mainDict['aL'][1], 0.02),
                    interpolate(0.025, 0.05, mainDict['aL'][1], mainDict['aL'][2], 0.03),
                    interpolate(0.025, 0.05, mainDict['aL'][1], mainDict['aL'][2], 0.0375),
                    interpolate(0.025, 0.05, mainDict['aL'][1], mainDict['aL'][2], 0.04),
                    interpolate(0.05, 0.075, mainDict['aL'][2], mainDict['aL'][3], 0.06),
                    interpolate(0.05, 0.075, mainDict['aL'][2], mainDict['aL'][3], 0.07),
                    interpolate(0.1, 0.15, mainDict['aL'][4], mainDict['aL'][5], 0.125),
                    interpolate(0.15, 0.2, mainDict['aL'][5], mainDict['aL'][6], 0.175),
                    interpolate(0.4, 0.41, mainDict['aL'][10], mainDict['aL'][11], 0.405)]

medialDict['aL_min'] = [-3.0, -3.0, -3.0,
                        -3.0, 1.1117, 1.1117,
                        1.1117, 1.1117, -3.0]

medialDict['aL_max'] = [2.0, 2.0, 2.0,
                        2.0, 1.7371, 1.7371,
                        1.7371, 1.7371, 2.0]

medialDict['aR'] = [interpolate(0.01, 0.025, mainDict['aR'][0], mainDict['aR'][1], 0.02),
                    interpolate(0.025, 0.05, mainDict['aR'][1], mainDict['aR'][2], 0.03),
                    interpolate(0.025, 0.05, mainDict['aR'][1], mainDict['aR'][2], 0.0375),
                    interpolate(0.025, 0.05, mainDict['aR'][1], mainDict['aR'][2], 0.04),
                    interpolate(0.05, 0.075, mainDict['aR'][2], mainDict['aR'][3], 0.06),
                    interpolate(0.05, 0.075, mainDict['aR'][2], mainDict['aR'][3], 0.07),
                    interpolate(0.1, 0.15, mainDict['aR'][4], mainDict['aR'][5], 0.125),
                    interpolate(0.15, 0.2, mainDict['aR'][5], mainDict['aR'][6], 0.175),
                    interpolate(0.4, 0.41, mainDict['aR'][10], mainDict['aR'][11], 0.405)]

medialDict['aR_min'] = [-3.0, -3.0, -3.0,
                        -3.0, -1.8567, -1.8567,
                        -1.8567, -1.8567, -3.0]

medialDict['aR_max'] = [3.0, 3.0, 3.0,
                        3.0, -1.1883, -1.1883,
                        -1.1883, -1.1883, 3.0]

medialDict['sigmaL'] = [interpolate(0.01, 0.025, mainDict['sigmaL'][0], mainDict['sigmaL'][1], 0.02),
                        interpolate(0.025, 0.05, mainDict['sigmaL'][1], mainDict['sigmaL'][2], 0.03),
                        interpolate(0.025, 0.05, mainDict['sigmaL'][1], mainDict['sigmaL'][2], 0.0375),
                        interpolate(0.025, 0.05, mainDict['sigmaL'][1], mainDict['sigmaL'][2], 0.04),
                        interpolate(0.05, 0.075, mainDict['sigmaL'][2], mainDict['sigmaL'][3], 0.06),
                        interpolate(0.05, 0.075, mainDict['sigmaL'][2], mainDict['sigmaL'][3], 0.07),
                        interpolate(0.1, 0.15, mainDict['sigmaL'][4], mainDict['sigmaL'][5], 0.125),
                        interpolate(0.15, 0.2, mainDict['sigmaL'][5], mainDict['sigmaL'][6], 0.175),
                        interpolate(0.4, 0.41, mainDict['sigmaL'][10], mainDict['sigmaL'][11], 0.405)]

medialDict['sigmaL_min'] = [0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0]

medialDict['sigmaL_max'] = [0.001, 0.0035, 0.0035,
                            0.0035, 0.00274, 0.00274,
                            0.00274, 0.00274, 0.0035]

medialDict['sigmaR'] = [interpolate(0.01, 0.025, mainDict['sigmaR'][0], mainDict['sigmaR'][1], 0.02),
                        interpolate(0.025, 0.05, mainDict['sigmaR'][1], mainDict['sigmaR'][2], 0.03),
                        interpolate(0.025, 0.05, mainDict['sigmaR'][1], mainDict['sigmaR'][2], 0.0375),
                        interpolate(0.025, 0.05, mainDict['sigmaR'][1], mainDict['sigmaR'][2], 0.04),
                        interpolate(0.05, 0.075, mainDict['sigmaR'][2], mainDict['sigmaR'][3], 0.06),
                        interpolate(0.05, 0.075, mainDict['sigmaR'][2], mainDict['sigmaR'][3], 0.07),
                        interpolate(0.1, 0.15, mainDict['sigmaR'][4], mainDict['sigmaR'][5], 0.125),
                        interpolate(0.15, 0.2, mainDict['sigmaR'][5], mainDict['sigmaR'][6], 0.175),
                        interpolate(0.4, 0.41, mainDict['sigmaR'][10], mainDict['sigmaR'][11], 0.405)]

medialDict['sigmaR_min'] = [0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0]

medialDict['sigmaR_max'] = [0.00360, 0.005, 0.005,
                            0.005, 0.00360, 0.00360,
                            0.00360, 0.00360, 0.005]

medialDict['fracL'] = [interpolate(0.01, 0.025, mainDict['fracL'][0], mainDict['fracL'][1], 0.02),
                       interpolate(0.025, 0.05, mainDict['fracL'][1], mainDict['fracL'][2], 0.03),
                       interpolate(0.025, 0.05, mainDict['fracL'][1], mainDict['fracL'][2], 0.0375),
                       interpolate(0.025, 0.05, mainDict['fracL'][1], mainDict['fracL'][2], 0.04),
                       interpolate(0.05, 0.075, mainDict['fracL'][2], mainDict['fracL'][3], 0.06),
                       interpolate(0.05, 0.075, mainDict['fracL'][2], mainDict['fracL'][3], 0.07),
                       interpolate(0.1, 0.15, mainDict['fracL'][4], mainDict['fracL'][5], 0.125),
                       interpolate(0.15, 0.2, mainDict['fracL'][5], mainDict['fracL'][6], 0.175),
                       interpolate(0.4, 0.41, mainDict['fracL'][10], mainDict['fracL'][11], 0.405)]

medialDict['fracL_min'] = [0.4, 0.1, 0.1,
                           0.1, 0.1368, 0.1368,
                           0.1368, 0.1368, 0.1]

medialDict['fracL_max'] = [1.0, 1.0, 1.0,
                           1.0, 1.09481, 1.09481,
                           1.09481, 0.9, 1.0]

medialDict['nL'] = [interpolate(0.01, 0.025, mainDict['nL'][0], mainDict['nL'][1], 0.02),
                    interpolate(0.025, 0.05, mainDict['nL'][1], mainDict['nL'][2], 0.03),
                    interpolate(0.025, 0.05, mainDict['nL'][1], mainDict['nL'][2], 0.0375),
                    interpolate(0.025, 0.05, mainDict['nL'][1], mainDict['nL'][2], 0.04),
                    interpolate(0.05, 0.075, mainDict['nL'][2], mainDict['nL'][3], 0.06),
                    interpolate(0.05, 0.075, mainDict['nL'][2], mainDict['nL'][3], 0.07),
                    interpolate(0.1, 0.15, mainDict['nL'][4], mainDict['nL'][5], 0.125),
                    interpolate(0.15, 0.2, mainDict['nL'][5], mainDict['nL'][6], 0.175),
                    interpolate(0.4, 0.41, mainDict['nL'][10], mainDict['nL'][11], 0.405)]

medialDict['nL_min'] = [1.1, 1.1, 1.1,
                        1.1, 1.2431, 1.2431,
                        1.2431, 1.2431, 1.1]

medialDict['nL_max'] = [30.0, 30.0, 30.0,
                        30.0, 3.1078, 3.1078,
                        3.1078, 3.1078, 30.0]

medialDict['nR'] = [interpolate(0.01, 0.025, mainDict['nR'][0], mainDict['nR'][1], 0.02),
                    interpolate(0.025, 0.05, mainDict['nR'][1], mainDict['nR'][2], 0.03),
                    interpolate(0.025, 0.05, mainDict['nR'][1], mainDict['nR'][2], 0.0375),
                    interpolate(0.025, 0.05, mainDict['nR'][1], mainDict['nR'][2], 0.04),
                    interpolate(0.05, 0.075, mainDict['nR'][2], mainDict['nR'][3], 0.06),
                    interpolate(0.05, 0.075, mainDict['nR'][2], mainDict['nR'][3], 0.07),
                    interpolate(0.1, 0.15, mainDict['nR'][4], mainDict['nR'][5], 0.125),
                    interpolate(0.15, 0.2, mainDict['nR'][5], mainDict['nR'][6], 0.175),
                    interpolate(0.4, 0.41, mainDict['nR'][10], mainDict['nR'][11], 0.405)]

medialDict['nR_min'] = [0.0, 0.0, 0.0,
                        0.0, 2.0552, 2.0552,
                        2.0552, 2.0552, 0.0]

medialDict['nR_max'] = [25.0, 25.0, 25.0,
                        25.0, 5.1380, 5.1380,
                        5.1380, 5.1380, 25.0]
