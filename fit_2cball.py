from user_defined_functions import createDirectories
from user_defined_functions import deleteFiles
import csv
import sys
import ROOT
ROOT.gROOT.SetBatch(True)


def fitFunc(histoFileName):
    """Builds a model from a sum of two CBalls, fits the model
    to the histogram data set, plots the model with pulls to two frames,
    and draws the frames on a canvas.  The boolean, param_fixed=False,
    allows the parameter values to float; set param_fixed=True to fix the
    parameter values.  The boolean, intermediate=False, fits the main
    fixed masses; set intermediate=True to fit the intermediate masses."""

    # File Handling
    # --------------------------------------------------------------
    createDirectories('./fit_2cball_output/parameter_values')
    createDirectories('./fit_2cball_output/fit_plots')
    deleteFiles('./fit_2cball_output/parameter_values/main_*.csv')

    # Initialize Parameter Values
    # --------------------------------------------------------------
    # Create Empty Lists for Parameters
    mass, vonFrac, bisFrac = ([] for i in range(3))
    sigmaL, sigmaL_min, sigmaL_max = ([] for i in range(3))
    sigmaR, sigmaR_min, sigmaR_max = ([] for i in range(3))
    fracL, fracL_min, fracL_max = ([] for i in range(3))
    aL, aL_min, aL_max = ([] for i in range(3))
    aR, aR_min, aR_max = ([] for i in range(3))
    nL, nL_min, nL_max = ([] for i in range(3))
    nR, nR_min, nR_max = ([] for i in range(3))

    # Fill Parameter Lists from csv file
    with open('./mainDict.csv', newline='') as mainDict:
        reader = csv.DictReader(mainDict)
        for row in reader:
            mass.append(float(row['mass']))
            vonFrac.append(float(row['vonFrac']))
            bisFrac.append(float(row['bisFrac']))
            sigmaL.append(float(row['sigmaL']))
            sigmaL_min.append(float(row['sigmaL_min']))
            sigmaL_max.append(float(row['sigmaL_max']))
            sigmaR.append(float(row['sigmaR']))
            sigmaR_min.append(float(row['sigmaR_min']))
            sigmaR_max.append(float(row['sigmaR_max']))
            fracL.append(float(row['fracL']))
            fracL_min.append(float(row['fracL_min']))
            fracL_max.append(float(row['fracL_max']))
            aL.append(float(row['aL']))
            aL_min.append(float(row['aL_min']))
            aL_max.append(float(row['aL_max']))
            aR.append(float(row['aR']))
            aR_min.append(float(row['aR_min']))
            aR_max.append(float(row['aR_max']))
            nL.append(float(row['nL']))
            nL_min.append(float(row['nL_min']))
            nL_max.append(float(row['nL_max']))
            nR.append(float(row['nR']))
            nR_min.append(float(row['nR_min']))
            nR_max.append(float(row['nR_max']))

    # Loop Through Histograms in rootfile
    histoFile = ROOT.TFile(histoFileName)
    for index, key in enumerate(histoFile.GetListOfKeys()):
        kname = key.GetName()
        histo = histoFile.Get(kname)

        # Calculate Other Initial Values
        # ----------------------------------------------------------
        mea = mass[index]
        mea_min = mea - mea * 0.1
        mea_max = mea + mea * 0.1
        von = mea - vonFrac[index] * mea
        bis = mea + bisFrac[index] * mea

        # Set up model
        # ----------------------------------------------------------
        # Declare CBall variables with initial value and range
        xTitle = "#font[42]{#it{m}(#gamma#gamma) [GeV/#it{c}^{2}]}"
        x = ROOT.RooRealVar("x", xTitle, von, bis)
        cbmean = ROOT.RooRealVar("#mu", "", mea, mea_min, mea_max)
        cbsigmaL = ROOT.RooRealVar("#sigma_{1}", "",
                                   sigmaL[index], sigmaL_min[index], sigmaL_max[index])
        cbsigmaR = ROOT.RooRealVar("#sigma_{2}", "",
                                   sigmaR[index], sigmaR_min[index], sigmaR_max[index])
        cbfracL = ROOT.RooRealVar("A_{0}", "",
                                  fracL[index], fracL_min[index], fracL_max[index])
        cbaL = ROOT.RooRealVar("#alpha_{L}", "",
                               aL[index], aL_min[index], aL_max[index])
        cbaR = ROOT.RooRealVar("#alpha_{R}", "",
                               aR[index], aR_min[index], aR_max[index])
        cbnL = ROOT.RooRealVar("n_{L}", "",
                               nL[index], nL_min[index], nL_max[index])
        cbnR = ROOT.RooRealVar("n_{R}", "",
                               nR[index], nR_min[index], nR_max[index])

        # Build data set
        data = ROOT.RooDataHist("data", "dataset", x, histo)

        # Build CBall1 and CBall2
        cball1 = ROOT.RooCBShape("cball1", "crystal ball 1",
                                 x, cbmean, cbsigmaL, cbaL, cbnL)
        cball2 = ROOT.RooCBShape("cball2", "crystal ball 2",
                                 x, cbmean, cbsigmaR, cbaR, cbnR)
        cballSum = ROOT.RooAddPdf("sum", "sum",
                                  ROOT.RooArgList(cball1, cball2),
                                  ROOT.RooArgList(cbfracL))

        # Fit model to data
        # ----------------------------------------------------------
        # Fit CBall sum to data, this is RooFitResults
        cballSum.fitTo(data, ROOT.RooFit.Extended(True), ROOT.RooFit.Save())

        # Plot model with pulls and residuals to frames
        # ----------------------------------------------------------
        # Construct a plot frame in x, this is the RooPlot
        xframe = x.frame(ROOT.RooFit.Title("#font[42]{CBall Sum PDF with Data}"))

        # Plot uncertainties as sum of weights squared in xframe
        data.plotOn(xframe, ROOT.RooFit.XErrorSize(0),
                    ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))

        # Plot CBall sum in xframe
        cballSum.plotOn(xframe, ROOT.RooFit.LineColor(ROOT.kRed))

        # Plot CBall 1 in xframe
        cballSum.plotOn(xframe, ROOT.RooFit.Components("cball1"),
                        ROOT.RooFit.LineColor(ROOT.kGreen),
                        ROOT.RooFit.LineStyle(ROOT.kDashed))

        # Plot CBall 2 in xframe
        cballSum.plotOn(xframe, ROOT.RooFit.Components("cball2"),
                        ROOT.RooFit.LineColor(ROOT.kViolet),
                        ROOT.RooFit.LineStyle(ROOT.kDashed))

        # Xframe draw option, "L"= a simple poly-line between every point
        # This must be included to avoid effects on the fit, pull, and residual
        # from the components CBall 1, and CBall 2
        cballSum.plotOn(xframe, ROOT.RooFit.DrawOption("L"))

        # Construct a histogram with the pulls of the data w.r.t the curve
        hpull = xframe.pullHist()

        # Create a new frame and draw the pull distribution
        xframe2 = x.frame(ROOT.RooFit.Title("#font[42]{Pull Distribution}"))
        xframe2.addPlotable(hpull, "P")

        # Add a box with parameter values
        cballSum.paramOn(xframe,
                         ROOT.RooFit.Format("NEU", ROOT.RooFit.AutoPrecision(1)),
                         ROOT.RooFit.Layout(0.75, 1.0, 0.94))

        # Draw frames on a canvas
        # ----------------------------------------------------------
        c = ROOT.TCanvas("c", "", 800, 800)
        c.Divide(1, 2)
        c.GetPad(1).SetPad(0.0, 0.3, 1.0, 1.0)
        c.GetPad(2).SetPad(0.0, 0.0, 1.0, 0.3)

        c.cd(1)
        ROOT.gPad.SetLeftMargin(0.15)
        ROOT.gPad.SetRightMargin(0.05)
        ROOT.gPad.SetTopMargin(0.08)
        ROOT.gPad.SetBottomMargin(0.15)
        xframe.getAttText().SetTextFont(42)
        xframe.getAttText().SetTextSize(0.03)
        xframe.SetLabelSize(0.05, "X")
        xframe.SetLabelSize(0.05, "Y")
        xframe.SetLabelFont(42, "X")
        xframe.SetLabelFont(42, "Y")
        xframe.SetTitleSize(0.05, "X")
        xframe.SetTitleSize(0.045, "Y")
        xframe.SetNdivisions(505, "X")
        xframe.SetNdivisions(505, "Y")
        xframe.GetXaxis().CenterTitle(True)
        xframe.GetYaxis().CenterTitle(True)
        xframe.SetTitleOffset(1.6, "Y")
        xframe.Draw("EZ")
        t = ROOT.TLatex()
        t.SetTextSize(0.04)
        t.SetTextFont(42)
        t.SetTextAlign(12)
        t.SetTextColor(1)
        t.SetTextFont(12)
        c.Update()
        xmin = ROOT.gPad.GetUxmin()
        ymax = xframe.GetMaximum()
        mTruth = "  #font[42]{#it{m}_{S}^{truth} = %.3f GeV/#it{c}^{2}}" % (mass[index])
        chi2 = "  #font[42]{#chi^{2}/ndf = %.2f/7}" % (xframe.chiSquare())
        t.DrawLatex(xmin, ymax * .95, mTruth)
        t.DrawLatex(xmin, ymax * .87, chi2)

        c.cd(2)
        ROOT.gPad.SetLeftMargin(0.15)
        ROOT.gPad.SetRightMargin(0.05)
        ROOT.gPad.SetTopMargin(0.06)
        ROOT.gPad.SetBottomMargin(0.15)
        xframe2.SetLabelSize(0.05, "X")
        xframe2.SetLabelSize(0.05, "Y")
        xframe2.SetLabelFont(42, "X")
        xframe2.SetLabelFont(42, "Y")
        xframe2.SetTitleSize(0.05, "X")
        xframe2.SetTitleSize(0.05, "Y")
        xframe2.SetNdivisions(505, "X")
        xframe2.SetNdivisions(505, "Y")
        xframe2.GetXaxis().CenterTitle(True)
        xframe2.GetYaxis().CenterTitle(True)
        xframe2.SetTitleOffset(1.1, "Y")
        xframe2.SetYTitle("#font[42]{(fit-data)/#sigma}")
        xframe2.Draw("EZ")
        line = ROOT.TLine()
        line.SetLineColor(2)
        line.SetLineStyle(ROOT.kDashed)
        line.DrawLine(von, 0, bis, 0)
        max_line = ROOT.TLine()
        max_line.SetLineColor(2)
        max_line.DrawLine(von, 2, bis, 2)
        min_line = ROOT.TLine()
        min_line.SetLineColor(2)
        min_line.DrawLine(von, -2, bis, -2)

        # Save a pdf of the canvas
        # ----------------------------------------------------------
        c.SaveAs("./fit_2cball_output/fit_plots/" + kname + ".pdf")

        # Export Fitted Parameters
        # ---------------------------------------------------------
        # Get fitted values
        al = cbaL.getVal()
        eral = cbaL.getError()
        ar = cbaR.getVal()
        erar = cbaR.getError()
        mean = cbmean.getVal()
        ermean = cbmean.getError()
        sigmal = cbsigmaL.getVal()
        ersigmal = cbsigmaL.getError()
        sigmar = cbsigmaR.getVal()
        ersigmar = cbsigmaR.getError()
        A0 = cbfracL.getVal()
        erA0 = cbfracL.getError()
        nl = cbnL.getVal()
        ernl = cbnL.getError()
        nr = cbnR.getVal()
        ernr = cbnR.getError()

        # Write fitted values to files
        with open("./fit_2cball_output/parameter_values/main_al.csv", 'a+') as f_al:
            f_al.write("{},{},0,{}\n".format(mass[index], al, eral))
        with open("./fit_2cball_output/parameter_values/main_ar.csv", 'a+') as f_ar:
            f_ar.write("{},{},0,{}\n".format(mass[index], ar, erar))
        with open("./fit_2cball_output/parameter_values/main_mean.csv", 'a+') as f_mean:
            f_mean.write("{},{},0,{}\n".format(mass[index], mean, ermean))
        with open("./fit_2cball_output/parameter_values/main_sigmaL.csv", 'a+') as f_sigmal:
            f_sigmal.write("{},{},0,{}\n".format(mass[index], sigmal, ersigmal))
        with open("./fit_2cball_output/parameter_values/main_sigmaR.csv", 'a+') as f_sigmar:
            f_sigmar.write("{},{},0,{}\n".format(mass[index], sigmar, ersigmar))
        with open("./fit_2cball_output/parameter_values/main_A0.csv", 'a+') as f_A0:
            f_A0.write("{},{},0,{}\n".format(mass[index], A0, erA0))
        with open("./fit_2cball_output/parameter_values/main_nl.csv", 'a+') as f_nl:
            f_nl.write("{},{},0,{}\n".format(mass[index], nl, ernl))
        with open("./fit_2cball_output/parameter_values/main_nr.csv", 'a+') as f_nr:
            f_nr.write("{},{},0,{}\n".format(mass[index], nr, ernr))


def main():
    try:
        histoFileName = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} </path/to/histograms.root>\n")
    fitFunc(histoFileName)


if __name__ == '__main__':
    main()

