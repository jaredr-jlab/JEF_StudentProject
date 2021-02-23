from user_defined_functions import createDirectories
import csv
import ROOT
ROOT.gROOT.SetBatch(True)


def parameterFitFunc(paramName):
    """Fit parameters with respect to mass
    and draw the fit on the a canvas"""

    # File Handling
    createDirectories('./output/parameter_fit_output/parameter_rootfiles')
    createDirectories('./output/parameter_fit_output/parameter_fit_plots')

    # Get Mass Values
    mass = []
    with open('./mainDict.csv', newline='') as mainDict:
        reader = csv.DictReader(mainDict)
        for row in reader:
            mass.append(float(row['mass']))

    # Add fit data to frame
    ROOT.gStyle.SetOptFit(111)

    # Create canvas
    c1 = ROOT.TCanvas("c1", "c1", 1000, 500)
    c1.GetFrame().SetFillColor(21)
    c1.GetFrame().SetBorderSize(12)

    # Specifiy .csv file containing parameter values
    fileFormat = "%lg%lg%lg%lg"
    filename = "./output/fit_2cball_output/parameter_values/main_{}.csv".format(paramName)

    # Create TGraphErrors
    graph = ROOT.TGraphErrors(filename, fileFormat, ",")
    graph.SetTitle("Parametrize %s WRT Mass; m(#gamma#gamma)[GeV/c^{2}]; %s" % (paramName, paramName))
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(24)
    graph.SetLineColor(4)
    if paramName == 'ar':
        graph.SetMaximum(0)
    else:
        graph.SetMinimum(0)
    graph.Draw('AEP')   

    # Select order of polynomial for parameters
    if paramName == 'sigmaL' or paramName == 'sigmaR':
        pol = "pol5"
    elif paramName == 'al' or paramName == 'ar':
        pol = "pol4"
    elif paramName == 'nl' or paramName == 'nr':
        pol = "pol3"
    elif paramName == 'A0':
        pol = "pol3"
    elif paramName == 'mean':
        pol = "pol2"

    # Fit the parameters to a polynomial
    f = ROOT.TF1("", pol, mass[0], mass[-1])
    f.SetLineColor(2)
    f.SetLineStyle(1)
    graph.Fit(f, "MRS")
    f.Draw("Same")

    # Save an image of the canvas
    c1.SaveAs("./output/parameter_fit_output/parameter_fit_plots/main_{}_fit.pdf".format(paramName))

    # Create ROOT file of fit
    rootFileName = "./output/parameter_fit_output/parameter_rootfiles/main_{}.root".format(paramName)
    ofile = ROOT.TFile(rootFileName,  "RECREATE")
    f.Write("fct_{}".format(paramName))
    ofile.Close()


def main():
    paramNameList = ['al', 'ar', 'mean', 'sigmaL', 'sigmaR', 'A0', 'nl', 'nr']
    for paramName in paramNameList:
        parameterFitFunc(paramName)


if __name__ == '__main__':
    main()

