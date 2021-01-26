from user_defined_functions import createDirectories
from user_defined_functions import deleteFiles
import ROOT
ROOT.gROOT.SetBatch(True)


def parameterFitFunc(fitParam, init_mass_index, final_mass_index, intermediate):
    """Fit parameters with respect to mass
    and draw the fit on the a canvas"""

    # Initialize useful variables
    # ------------------------------------------------------------------------
    if not intermediate:
        # List of Mass values
        Mass = [0.01, 0.025, 0.05,
                0.075, 0.1, 0.15,
                0.2, 0.25, 0.3,
                0.35, 0.4, 0.41]
    else:
        # List of intermediate mass values
        Mass = [0.02, 0.03, 0.0375,
                0.04, 0.06, 0.07,
                0.125, 0.175, 0.405]

    # Add fit data to frame
    ROOT.gStyle.SetOptFit(111)

    # Create canvas
    c1 = ROOT.TCanvas("c1", "c1", 1000, 500)
    c1.GetFrame().SetFillColor(21)
    c1.GetFrame().SetBorderSize(12)

    # Specifiy .csv file containing parameter values
    fileFormat = "%lg%lg%lg%lg"
    if not intermediate:
        filename = "./fit_module/parameter_values/main_{}.csv".format(fitParam)
    else:
        filename = "./fit_module/parameter_values/medial_{}.csv".format(fitParam)

    # Create TGraphErrors
    graph = ROOT.TGraphErrors(filename, fileFormat, ",")
    graph.SetTitle("Parametrize %s WRT Mass; m(#gamma#gamma)[GeV/c^{2}]; %s" % (fitParam, fitParam))
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(24)
    graph.SetLineColor(4)
     # Try graph.SetMinimum(0)
    graph.Draw('AEP')   

    # Select order of polynomial for parameters
    if fitParam == 'sigma1' or fitParam == 'sigma2':
        pol = "pol5"
    elif fitParam == 'al' or fitParam == 'ar':
        pol = "pol4"
    elif fitParam == 'nl' or fitParam == 'nr':
        pol = "pol3"
    elif fitParam == 'A0':
        pol = "pol3"
    elif fitParam == 'mean':
        pol = "pol2"

    # Fit the parameters to a polynomial
    f = ROOT.TF1("", pol, Mass[init_mass_index], Mass[final_mass_index])
    f.SetLineColor(2)
    f.SetLineStyle(1)
    graph.Fit(f, "MRS")  # Options "MRS"
    f.Draw("Same")

    # Evaluate the parameter at each mass value and write to .txt file
    if not intermediate:
        for i in range(init_mass_index, final_mass_index + 1):
            value = f.Eval(Mass[i])
            with open("./parameter_fit_module/function_eval_values/main_{}_Eval.txt".format(fitParam), 'a+') as f_eval:
                f_eval.write("{}\n".format(value))
    else:
        for i in range(init_mass_index, final_mass_index + 1):
            value = f.Eval(Mass[i])
            with open("./parameter_fit_module/function_eval_values/medial_{}_Eval.txt".format(fitParam), 'a+') as f_eval:
                f_eval.write("{}\n".format(value))

    # Update the canvas
    # c1.Update()

    # Save an image of the canvas
    if not intermediate:
        c1.SaveAs("./parameter_fit_module/parameter_fit_plots/main_{}_fit.png".format(fitParam))
    else:
        c1.SaveAs("./parameter_fit_module/parameter_fit_plots/medial_{}_fit.png".format(fitParam))

    # Create ROOT file of fit
    if not intermediate:
        TFileName = "./parameter_fit_module/parameter_rootfiles/main_{}.root".format(fitParam)
    else:
        TFileName = "./parameter_fit_module/parameter_rootfiles/medial_{}.root".format(fitParam)
    ofile = ROOT.TFile(TFileName, "RECREATE")
    f.Write("fct_{}".format(fitParam))
    ofile.Close()

    return f


def main(init_mass_index=3, final_mass_index=9, intermediate=False):
    createDirectories('./parameter_fit_module/parameter_rootfiles')
    createDirectories('./parameter_fit_module/parameter_fit_plots')
    createDirectories('./parameter_fit_module/function_eval_values')
    if not intermediate:
        deleteFiles('./parameter_fit_module/parameter_rootfiles/main_*.root')
        deleteFiles('./parameter_fit_module/function_eval_values/main_*.txt')
        outfile = ROOT.TFile("./parameter_fit_module/parameter_rootfiles/main_parameters.root", "RECREATE")
    if intermediate:
        deleteFiles('./parameter_fit_module/parameter_rootfiles/medial_*.root')
        deleteFiles('./parameter_fit_module/function_eval_values/medial_*.txt')
        outfile = ROOT.TFile("./parameter_fit_module/parameter_rootfiles/median_parameters.root", "RECREATE")
    paramNameList = ["al", "ar", "mean", "sigma1",
                     "sigma2", "A0", "nl", "nr"]
    
    for paramName in paramNameList:
        f = parameterFitFunc(paramName, init_mass_index, final_mass_index, intermediate)
        f.Write()  # Write fit data for each parameter to combined ROOT file
    outfile.Close()


if __name__ == '__main__':
    main()
