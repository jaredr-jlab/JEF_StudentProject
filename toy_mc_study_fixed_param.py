from user_defined_functions import createDirectories
from user_defined_functions import deleteFiles
import csv
import sys
import ROOT
ROOT.gROOT.SetBatch(True)


def toyMCFunc(histoFileName):
    """..."""

    # File handling
    #--------------------------------------------------------------------------
    outputDir = '../output/toy_mc_study_fixed_param_output/plots/'
    createDirectories(outputDir)

    # Retrieve parameter values
    #--------------------------------------------------------------------------
    # Fill mass list from csv file
    mass = []
    with open('./mainDict.csv', newline='') as mainDict:
        reader = csv.DictReader(mainDict)
        for row in reader:
            mass.append(float(row['mass']))
            
    # Open the parameter ROOT files
    sigmaLFile = ROOT.TFile.Open("../output/parameter_fit_output"\
                                 "/parameter_rootfiles/main_sigmaL.root",
                                 "READ")
    sigmaRFile = ROOT.TFile.Open("../output/parameter_fit_output"\
                                 "/parameter_rootfiles/main_sigmaR.root",
                                 "READ")
    A0File = ROOT.TFile.Open("../output/parameter_fit_output"\
                             "/parameter_rootfiles/main_A0.root",
                             "READ")
    alFile = ROOT.TFile.Open("../output/parameter_fit_output"\
                             "/parameter_rootfiles/main_al.root",
                             "READ")
    arFile = ROOT.TFile.Open("../output/parameter_fit_output"\
                             "/parameter_rootfiles/main_ar.root",
                             "READ")
    nlFile = ROOT.TFile.Open("../output/parameter_fit_output"\
                             "/parameter_rootfiles/main_nl.root",
                             "READ")
    nrFile = ROOT.TFile.Open("../output/parameter_fit_output"\
                             "/parameter_rootfiles/main_nr.root",
                             "READ")

    # Retrieve the parameter function files
    fct_sigmaL = sigmaLFile.Get('fct_sigmaL')
    fct_sigmaR = sigmaRFile.Get('fct_sigmaR')
    fct_A0 = A0File.Get('fct_A0')
    fct_al = alFile.Get('fct_al')
    fct_ar = arFile.Get('fct_ar')
    fct_nl = nlFile.Get('fct_nl')
    fct_nr = nrFile.Get('fct_nr')

    # Close the parameter ROOT files
    sigmaLFile.Close()
    sigmaRFile.Close()
    A0File.Close()
    alFile.Close()
    arFile.Close()
    nlFile.Close()
    nrFile.Close()

    # Loop Through Histograms in rootfile
    histoFile = ROOT.TFile(histoFileName)
    for index, key in enumerate(histoFile.GetListOfKeys()):
        kname = key.GetName()
        histo = histoFile.Get(kname)

        # Calculate Parameter Values
        # ---------------------------------------------------------------------
        mea = mass[index]
        von = mea - 0.2
        bis = mea + 0.2
    
        # Evaluate parameter functions at masses
        sigmaL = fct_sigmaL.Eval(mea)
        sigmaR = fct_sigmaR.Eval(mea)
        fracL = fct_A0.Eval(mea)
        aL = fct_al.Eval(mea)
        aR = fct_ar.Eval(mea)
        nL = fct_nl.Eval(mea)
        nR = fct_nr.Eval(mea)

        # Set up model
        # ---------------------------------------------------------------------
        # Declare CBall variables
        xTitle = "#font[42]{#it{m}(#gamma#gamma) [GeV/#it{c}^{2}]}"
        x = ROOT.RooRealVar("x", xTitle, von, bis)
        cbmean = ROOT.RooRealVar("mu", "mean", mea, mea, mea)
        cbsigmaL = ROOT.RooRealVar("sigmaL", "#sigma_{L}",
                                   sigmaL, sigmaL, sigmaL)
        cbsigmaR = ROOT.RooRealVar("sigmaR", "#sigma_{R}",
                                   sigmaR, sigmaR, sigmaR)
        cbaL = ROOT.RooRealVar("alphaL", "#alpha_{L}", aL, aL, aL)
        cbaR = ROOT.RooRealVar("alphaR", "#alpha_{R}", aR, aR, aR)
        cbnL = ROOT.RooRealVar("nL", "n_{L}", nL, nL, nL)
        cbnR = ROOT.RooRealVar("nR", "n_{R}", nR, nR, nR)

        # Build CBall1 and CBall2 and fracL component
        cball1 = ROOT.RooCBShape("cball1", "crystal ball 1",
                                 x, cbmean, cbsigmaL, cbaL, cbnL)
        cball2 = ROOT.RooCBShape("cball2", "crystal ball 2",
                                 x, cbmean, cbsigmaR, cbaR, cbnR)
        cbfracL = ROOT.RooRealVar("A0", "A_{0}", fracL, fracL, fracL)
        cballSum = ROOT.RooAddPdf("sum", "sum",
                                  ROOT.RooArgList(cball1, cball2),
                                  ROOT.RooArgList(cbfracL))

        # Sum the CBall sum with the the number of fracL events
        num_entries = histo.GetEntries()
        nsig = ROOT.RooRealVar("nsig", "N_{sig}",
                               1000, 0, num_entries)
        model = ROOT.RooAddPdf("model", "CBallSum + nsig",
                               ROOT.RooArgList(cballSum),
                               ROOT.RooArgList(nsig))

        # Fit model to dataset
        #----------------------------------------------------------------------
        histo_data = ROOT.RooDataHist("histo_data", "dataset", x, histo)
        model.fitTo(histo_data, ROOT.RooFit.Extended(True), ROOT.RooFit.Save())

        # Create RooMCStudy manager
        # ----------------------------------------------------------------
        mcstudy = ROOT.RooMCStudy(model,
                                  ROOT.RooArgSet(x),
                                  ROOT.RooFit.Binned(True),
                                  ROOT.RooFit.Silence(),
                                  ROOT.RooFit.Extended(),
                                  ROOT.RooFit.FitOptions(
                                      ROOT.RooFit.Save(True),
                                      ROOT.RooFit.PrintEvalErrors(0)))

        # Generate and fit events
        # ----------------------------------------------------------------
        mcstudy.generateAndFit(1000)

        # Plot results to frames
        # ----------------------------------------------------------------
        xframe1 = mcstudy.plotParam(nsig, ROOT.RooFit.Bins(65))
        xframe2 = mcstudy.plotError(nsig, ROOT.RooFit.Bins(65))
        xframe3 = mcstudy.plotPull(nsig, ROOT.RooFit.Bins(65),
                                   ROOT.RooFit.FitGauss(ROOT.kTRUE))

        # Draw frames on a canvas
        # ------------------------------------------------------------
        c = ROOT.TCanvas("c", "c", 1200, 400)
        c.Divide(3)

        c.cd(1)
        ROOT.gPad.SetLeftMargin(0.15)
        ROOT.gPad.SetRightMargin(0.05)
        ROOT.gPad.SetTopMargin(0.08)
        ROOT.gPad.SetBottomMargin(0.15)
        xframe1.SetLabelSize(0.05, "X")
        xframe1.SetLabelSize(0.05, "Y")
        xframe1.SetLabelFont(42, "X")
        xframe1.SetLabelFont(42, "Y")
        xframe1.SetTitleSize(0.05, "X")
        xframe1.SetTitleSize(0.05, "Y")
        xframe1.SetNdivisions(505, "X")
        xframe1.SetNdivisions(505, "Y")
        xframe1.GetXaxis().CenterTitle(True)
        xframe1.GetYaxis().CenterTitle(True)
        xframe1.SetTitleOffset(1.6, "Y")
        xframe1.Draw("EZ")

        c.cd(2)
        ROOT.gPad.SetLeftMargin(0.15)
        ROOT.gPad.SetRightMargin(0.05)
        ROOT.gPad.SetTopMargin(0.08)
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
        xframe2.SetTitleOffset(1.6, "Y")
        xframe2.Draw("EZ")

        c.cd(3)
        ROOT.gPad.SetLeftMargin(0.15)
        ROOT.gPad.SetRightMargin(0.05)
        ROOT.gPad.SetTopMargin(0.08)
        ROOT.gPad.SetBottomMargin(0.15)
        xframe3.SetLabelSize(0.05, "X")
        xframe3.SetLabelSize(0.05, "Y")
        xframe3.SetLabelFont(42, "X")
        xframe3.SetLabelFont(42, "Y")
        xframe3.SetTitleSize(0.05, "X")
        xframe3.SetTitleSize(0.05, "Y")
        xframe3.SetNdivisions(505, "X")
        xframe3.SetNdivisions(505, "Y")
        xframe3.GetXaxis().CenterTitle(True)
        xframe3.GetYaxis().CenterTitle(True)
        xframe3.SetTitleOffset(1.6, "Y")
        xframe3.Draw("EZ")

        # Save an image of the canvas
        c.SaveAs(outputDir + "toyMC_{}_nsig.pdf".format(index))


def main():
    try:
        histoFileName = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} </path/to/histograms.root>\n")
    toyMCFunc(histoFileName)


if __name__ == '__main__':
    main()

