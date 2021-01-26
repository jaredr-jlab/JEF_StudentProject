import parameter_data
import parameter_fit_module
import toy_MC_study_module
import fit_module
import ROOT
ROOT.gROOT.SetBatch(True)


# Start timer
t = ROOT.TStopwatch()
t.Start()


# Script Variables
# --------------------
# --------------------
init_mass_index = 0
final_mass_index = 11

init_medial_mass_index = 0
final_medial_mass_index = 8
# --------------------
# --------------------


# --------------------Call and Run Various Modules as Needed------------------
# __1__Fit the main masses with floating parameters and generate plots with pulls
# for mass_index in range(init_mass_index, final_mass_index + 1):
#     fit_module.main(mass_index, parameter_data.mainDict, False, False)

# __2__Parametrize the fits
# parameter_fit_module.main(init_mass_index, final_mass_index, False)

# __3__Run Toy Monte Carlo Study for main masses
# for mass_index in range(init_mass_index, final_mass_index + 1):
#     toy_MC_study_module.main(mass_index, parameter_data.mainDict, True, False)

# __4__Fit intermediate masses with interpolated floating parameters and plot
# for mass_index in range(init_medial_mass_index, final_medial_mass_index + 1):
#     fit_module.main(mass_index, parameter_data.medialDict, False, True)

# __5__Parametrize the fits
# parameter_fit_module.main(init_medial_mass_index, final_medial_mass_index, True)

# __6__Run Toy Monte Carlo Study for intermediate masses
for mass_index in range(init_medial_mass_index, final_medial_mass_index + 1):
    toy_MC_study_module.main(mass_index, parameter_data.medialDict, True, True)
# ----------------------------------------------------------------------------


# --------------------Run the Fixed Parameter Modules-------------------------
# __7__Fit the main masses with fixed parameter values and generate plots with pulls
# for mass_index in range(init_mass_index, final_mass_index + 1):
#     fit_module.main(mass_index, parameter_data.mainDict, True, False)

# __8__Fit intermediate masses with fixed parameters from param_fct eval and plot
# for mass_index in range(init_medial_mass_index, final_medial_mass_index + 1):
#     fit_module.main(mass_index, parameter_data.medialDict, True, True)
# ----------------------------------------------------------------------------


# --------------------Run the Histogram Model Comparison----------------------
# __9__

# Stop timer and print elapsed time
t.Stop()
t.Print()
