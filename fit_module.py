import parameter_data
from user_defined_functions import createDirectories
from user_defined_functions import deleteFiles
import ROOT
ROOT.gROOT.SetBatch(True)


def fitFunc(mass_index, Dictionary, param_fixed=False, intermediate=False):
    """Builds a model from a sum of two CBalls, fits the model
    to the histogram data set, plots the model with pulls to two frames,
    and draws the frames on a canvas.  The boolean, param_fixed=False,
    allows the parameter values to float; set param_fixed=True to fix the
    parameter values.  The boolean, intermediate=False, fits the main
    fixed masses; set intermediate=True to fit the intermediate masses."""

    # Get Histogram
    # ----------------------------------------------------------------
    # Open the ROOT input file
    if not intermediate:
        histoFileName = "./rootfiles/JEF_dark_scalar_MCsimu_signal_v3.root"
    else:
        histoFileName = "./rootfiles/JEF_dark_scalar_MCsimu_signal_v3-QC.root"

    histoFile = ROOT.TFile.Open(histoFileName, "READ")

    # Retrieve the histogram
    histoName = "sm_sig1_10_" + str(mass_index)
    histo = histoFile.Get(histoName)

    # Close the ROOT input file
    histo.SetDirectory(0)
    histoFile.Close()

    # Initialize useful variables
    # ----------------------------------------------------------------
    # List of Mass values
    if not intermediate:
        Mass = [0.01, 0.025, 0.05,
                0.075, 0.1, 0.15,
                0.2, 0.25, 0.3,
                0.35, 0.4, 0.41]

        vonFrac = [0.6, 0.32, 0.2,
                   0.18, 0.12, 0.11,
                   0.075, 0.06, 0.05,
                   0.03, 0.018, 0.012]

        bisFrac = [0.85, 0.35, 0.2,
                   0.15, 0.12, 0.11,
                   0.075, 0.06, 0.05,
                   0.03, 0.018, 0.009]
    else:
        Mass = [0.02, 0.03, 0.0375,
                0.04, 0.06, 0.07,
                0.125, 0.175, 0.405]

        vonFrac = [0.5, 0.3, 0.26,
                   0.2, 0.19, 0.18,
                   0.11, 0.1, 0.016]

        bisFrac = [0.5, 0.3, 0.26,
                   0.2, 0.19, 0.18,
                   0.14, 0.09, 0.016]

    # Other initial values
    mass = Mass[mass_index]
    mea = mass
    mea_min = mea - mea * 0.1
    mea_max = mea + mea * 0.1
    von = mea - vonFrac[mass_index] * mea
    bis = mea + bisFrac[mass_index] * mea

    if intermediate and param_fixed:
        # Open the ROOT files
        sigma1File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_sigma1.root", "READ")
        sigma2File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_sigma2.root", "READ")
        A0File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_A0.root", "READ")
        alFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_al.root", "READ")
        arFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_ar.root", "READ")
        nlFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_nl.root", "READ")
        nrFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_nr.root", "READ")

        # Retrieve the function files
        fct_sigma1 = sigma1File.Get('fct_sigma1')
        fct_sigma2 = sigma2File.Get('fct_sigma2')
        fct_A0 = A0File.Get('fct_A0')
        fct_al = alFile.Get('fct_al')
        fct_ar = arFile.Get('fct_ar')
        fct_nl = nlFile.Get('fct_nl')
        fct_nr = nrFile.Get('fct_nr')

        # Close the ROOT files
        sigma1File.Close()
        sigma2File.Close()
        A0File.Close()
        alFile.Close()
        arFile.Close()
        nlFile.Close()
        nrFile.Close()

        # Evaluate functions at intermediate masses and define variables
        sigmaL = fct_sigma1.Eval(mass)
        sigmaR = fct_sigma2.Eval(mass)
        fracL = fct_A0.Eval(mass)
        aL = fct_al.Eval(mass)
        aR = fct_ar.Eval(mass)
        nL = fct_nl.Eval(mass)
        nR = fct_nr.Eval(mass)
    else:
        sigmaL = Dictionary['sigmaL'][mass_index]
        sigmaL_min = Dictionary['sigmaL_min'][mass_index]
        sigmaL_max = Dictionary['sigmaL_max'][mass_index]
        sigmaR = Dictionary['sigmaR'][mass_index]
        sigmaR_min = Dictionary['sigmaR_min'][mass_index]
        sigmaR_max = Dictionary['sigmaR_max'][mass_index]
        fracL = Dictionary['fracL'][mass_index]
        fracL_min = Dictionary['fracL_min'][mass_index]
        fracL_max = Dictionary['fracL_max'][mass_index]
        aL = Dictionary['aL'][mass_index]
        aL_min = Dictionary['aL_min'][mass_index]
        aL_max = Dictionary['aL_max'][mass_index]
        aR = Dictionary['aR'][mass_index]
        aR_min = Dictionary['aR_min'][mass_index]
        aR_max = Dictionary['aR_max'][mass_index]
        nL = Dictionary['nL'][mass_index]
        nL_min = Dictionary['nL_min'][mass_index]
        nL_max = Dictionary['nL_min'][mass_index]
        nR = Dictionary['nR'][mass_index]
        nR_min = Dictionary['nR_min'][mass_index]
        nR_max = Dictionary['nR_max'][mass_index]

    # Set up model
    # ----------------------------------------------------------------
    # Declare CBall variables with initial value and range
    xTitle = "#font[42]{#it{m}(#gamma#gamma) [GeV/#it{c}^{2}]}"
    if not param_fixed:
        x = ROOT.RooRealVar("x", xTitle, von, bis)
        cbmean = ROOT.RooRealVar("#mu", "", mea, mea_min, mea_max)
        cbsigmaL = ROOT.RooRealVar("#sigma_{1}", "", sigmaL, sigmaL_min, sigmaL_max)
        cbsigmaR = ROOT.RooRealVar("#sigma_{2}", "", sigmaR, sigmaR_min, sigmaR_max)
        cbfracL = ROOT.RooRealVar("A_{0}", "", fracL, fracL_min, fracL_max)
        cbaL = ROOT.RooRealVar("#alpha_{L}", "", aL, aL_min, aL_max)
        cbaR = ROOT.RooRealVar("#alpha_{R}", "", aR, aR_min, aR_max)
        cbnL = ROOT.RooRealVar("n_{L}", "", nL, nL_min, nL_max)
        cbnR = ROOT.RooRealVar("n_{R}", "", nR, nR_min, nR_max)
    else:
        x = ROOT.RooRealVar("x", xTitle, von, bis)
        cbmean = ROOT.RooRealVar("#mu", "", mea, mea, mea)
        cbsigmaL = ROOT.RooRealVar("#sigma_{1}", "", sigmaL, sigmaL, sigmaL)
        cbsigmaR = ROOT.RooRealVar("#sigma_{2}", "", sigmaR, sigmaR, sigmaR)
        cbfracL = ROOT.RooRealVar("A_{0}", "", fracL, fracL, fracL)
        cbaL = ROOT.RooRealVar("#alpha_{L}", "", aL, aL, aL)
        cbaR = ROOT.RooRealVar("#alpha_{R}", "", aR, aR, aR)
        cbnL = ROOT.RooRealVar("n_{L}", "", nL, nL, nL)
        cbnR = ROOT.RooRealVar("n_{R}", "", nR, nR, nR)

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
    # ----------------------------------------------------------------
    # Fit CBall sum to data, this is RooFitResults
    cballSum.fitTo(data, ROOT.RooFit.Extended(True), ROOT.RooFit.Save())
    # if not param_fixed:
    #     cballSum.fitTo(data, ROOT.RooFit.Extended(True), ROOT.RooFit.Save())
    # else:
    #     cballSum.fitTo(data, ROOT.RooFit.Extended(True))

    # Plot model with pulls and residuals to frames
    # ----------------------------------------------------------------
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
    if not param_fixed:
        cballSum.paramOn(xframe,
                         ROOT.RooFit.Format("NEU", ROOT.RooFit.AutoPrecision(1)),
                         ROOT.RooFit.Layout(0.75, 1.0, 0.94))
    else:
        cballSum.paramOn(xframe,
                         ROOT.RooFit.Format("NU", ROOT.RooFit.FixedPrecision(5)),
                         ROOT.RooFit.Layout(0.75, 1.0, 0.94))

    # Draw frames on a canvas
    # ----------------------------------------------------------------
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
    mTruth = "  #font[42]{#it{m}_{S}^{truth} = %.3f GeV/#it{c}^{2}}" % (mass)
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

    if not param_fixed and not intermediate:
        #Floating parameters from final Dictionary; main fixed masses
        # --------------------------------------------------------------------
        # Save a pdf of canvas
        c.SaveAs("./fit_module/fit_plots/main_" + histoName + ".png")

        # Get fitted values for writing to files
        al = cbaL.getVal()
        eral = cbaL.getError()
        ar = cbaR.getVal()
        erar = cbaR.getError()
        mean = cbmean.getVal()
        ermean = cbmean.getError()
        sigmaL = cbsigmaL.getVal()
        ersigma1 = cbsigmaL.getError()
        sigmaR = cbsigmaR.getVal()
        ersigma2 = cbsigmaR.getError()
        A0 = cbfracL.getVal()
        erA0 = cbfracL.getError()
        nl = cbnL.getVal()
        ernl = cbnL.getError()
        nr = cbnR.getVal()
        ernr = cbnR.getError()

        # Write fitted values to files
        with open("./fit_module/parameter_values/main_al.csv", 'a+') as f_al:
            f_al.write("{},{},0,{}\n".format(mass, al, eral))
        with open("./fit_module/parameter_values/main_ar.csv", 'a+') as f_ar:
            f_ar.write("{},{},0,{}\n".format(mass, ar, erar))
        with open("./fit_module/parameter_values/main_mean.csv", 'a+') as f_mean:
            f_mean.write("{},{},0,{}\n".format(mass, mean, ermean))
        with open("./fit_module/parameter_values/main_sigma1.csv", 'a+') as f_sigma1:
            f_sigma1.write("{},{},0,{}\n".format(mass, sigmaL, ersigma1))
        with open("./fit_module/parameter_values/main_sigma2.csv", 'a+') as f_sigma2:
            f_sigma2.write("{},{},0,{}\n".format(mass, sigmaR, ersigma2))
        with open("./fit_module/parameter_values/main_A0.csv", 'a+') as f_A0:
            f_A0.write("{},{},0,{}\n".format(mass, A0, erA0))
        with open("./fit_module/parameter_values/main_nl.csv", 'a+') as f_nl:
            f_nl.write("{},{},0,{}\n".format(mass, nl, ernl))
        with open("./fit_module/parameter_values/main_nr.csv", 'a+') as f_nr:
            f_nr.write("{},{},0,{}\n".format(mass, nr, ernr))

    elif param_fixed and not intermediate:
        # Fixed parameters from final Dictionary; main fixed masses
        # --------------------------------------------------------------------
        # Save a pdf of canvas
        c.SaveAs("./fit_module/fit_plots/fixed_main_" + histoName + ".png")

    elif not param_fixed and intermediate:
        #Floating parameters from interpolated Dictionary; intermediate masses
        # --------------------------------------------------------------------
        # Save a pdf of canvas
        c.SaveAs("./fit_module/fit_plots/medial_" + histoName + ".png")

        # Get fitted values for writing to files
        al = cbaL.getVal()
        eral = cbaL.getError()
        ar = cbaR.getVal()
        erar = cbaR.getError()
        mean = cbmean.getVal()
        ermean = cbmean.getError()
        sigmaL = cbsigmaL.getVal()
        ersigma1 = cbsigmaL.getError()
        sigmaR = cbsigmaR.getVal()
        ersigma2 = cbsigmaR.getError()
        A0 = cbfracL.getVal()
        erA0 = cbfracL.getError()
        nl = cbnL.getVal()
        ernl = cbnL.getError()
        nr = cbnR.getVal()
        ernr = cbnR.getError()

        # Write fitted values to files
        with open("./fit_module/parameter_values/medial_al.csv", 'a+') as f_al:
            f_al.write("{},{},0,{}\n".format(mass, al, eral))
        with open("./fit_module/parameter_values/medial_ar.csv", 'a+') as f_ar:
            f_ar.write("{},{},0,{}\n".format(mass, ar, erar))
        with open("./fit_module/parameter_values/medial_mean.csv", 'a+') as f_mean:
            f_mean.write("{},{},0,{}\n".format(mass, mean, ermean))
        with open("./fit_module/parameter_values/medial_sigma1.csv", 'a+') as f_sigma1:
            f_sigma1.write("{},{},0,{}\n".format(mass, sigmaL, ersigma1))
        with open("./fit_module/parameter_values/medial_sigma2.csv", 'a+') as f_sigma2:
            f_sigma2.write("{},{},0,{}\n".format(mass, sigmaR, ersigma2))
        with open("./fit_module/parameter_values/medial_A0.csv", 'a+') as f_A0:
            f_A0.write("{},{},0,{}\n".format(mass, A0, erA0))
        with open("./fit_module/parameter_values/medial_nl.csv", 'a+') as f_nl:
            f_nl.write("{},{},0,{}\n".format(mass, nl, ernl))
        with open("./fit_module/parameter_values/medial_nr.csv", 'a+') as f_nr:
            f_nr.write("{},{},0,{}\n".format(mass, nr, ernr))

    elif param_fixed and intermediate:
        # Fixed parameters from evaluating function from parameter root files;
        # intermediate masses
        # --------------------------------------------------------------------
        # Save a pdf of canvas
        c.SaveAs("./fit_module/fit_plots/fixed_medial_" + histoName + ".png")


def main(mass_index, Dictionary=parameter_data.mainDict, param_fixed=False, intermediate=False):
    if mass_index == 0:
        createDirectories('./fit_module/parameter_values')
        createDirectories('./fit_module/fit_plots')
        if not param_fixed and not intermediate:
            deleteFiles('./fit_module/parameter_values/main_*.csv')
        if not param_fixed and intermediate:
            deleteFiles('./fit_module/parameter_values/medial_*.csv')

    fitFunc(mass_index, Dictionary, param_fixed, intermediate)


if __name__ == '__main__':
    main()
