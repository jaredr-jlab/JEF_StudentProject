from user_defined_functions import createDirectories
from user_defined_functions import deleteFiles
import ROOT
ROOT.gROOT.SetBatch(True)


def toyMCFunc(mass_index, Dictionary, param_fixed=True, intermediate=False):

    if not intermediate:
        # Get number of entries from main mass Histograms
        # --------------------------------------------------------------------
        # Open the ROOT input file
        histoFileName = "JEF_dark_scalar_MCsimu_signal_v3.root"
        histoFile = ROOT.TFile.Open(histoFileName, "READ")

        # Retrieve the histogram
        histoName = "sm_sig1_10_" + str(mass_index)
        histo = histoFile.Get(histoName)

        # Get the number of entries
        num_entries = histo.GetEntries()

        # Close the ROOT input file
        histo.SetDirectory(0)
        histoFile.Close()
    else:
        # Get number of entries from intermediate mass Histograms
        # --------------------------------------------------------------------
        # Open the ROOT input file
        medial_histoFileName = "JEF_dark_scalar_MCsimu_signal_v3-QC.root"
        medial_histoFile = ROOT.TFile.Open(medial_histoFileName, "READ")

        # Retrieve the histogram
        medial_histoName = "sm_sig1_10_" + str(mass_index)
        medial_histo = medial_histoFile.Get(medial_histoName)

        # Get the number of entries
        num_entries = medial_histo.GetEntries()

        # Close the ROOT input file
        medial_histo.SetDirectory(0)
        medial_histoFile.Close()

    # Initialize useful variables
    # ------------------------------------------------------------------------
    # List of Mass values
    if not intermediate:
        Mass = [0.01, 0.025, 0.05,
                0.075, 0.1, 0.15,
                0.2, 0.25, 0.3,
                0.35, 0.4, 0.41]
    else:
        Mass = [0.02, 0.03, 0.0375,
                0.04, 0.06, 0.07,
                0.125, 0.175, 0.405]

    mass = Mass[mass_index]
    mea = mass
    von = mea - 0.02
    bis = mea + 0.02

    mea_min = Dictionary['mean_min'][mass_index]
    mea_max = Dictionary['mean_max'][mass_index]
    sigmaL_min = Dictionary['sigmaL_min'][mass_index]
    sigmaL_max = Dictionary['sigmaL_max'][mass_index]
    sigmaR_min = Dictionary['sigmaR_min'][mass_index]
    sigmaR_max = Dictionary['sigmaR_max'][mass_index]
    aL_min = Dictionary['aL_min'][mass_index]
    aL_max = Dictionary['aL_max'][mass_index]
    aR_min = Dictionary['aR_min'][mass_index]
    aR_max = Dictionary['aR_max'][mass_index]
    nL_min = Dictionary['nL_min'][mass_index]
    nL_max = Dictionary['nL_max'][mass_index]
    nR_min = Dictionary['nR_min'][mass_index]
    nR_max = Dictionary['nR_max'][mass_index]

    # Get parameter values from parameter functions
    # ------------------------------------------------------------------------
    # Open the parameter ROOT files
    if not intermediate:
        sigma1File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/main_sigma1.root", "READ")
        sigma2File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/main_sigma2.root", "READ")
        A0File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/main_A0.root", "READ")
        alFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/main_al.root", "READ")
        arFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/main_ar.root", "READ")
        nlFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/main_nl.root", "READ")
        nrFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/main_nr.root", "READ")
    else:
        sigma1File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_sigma1.root", "READ")
        sigma2File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_sigma2.root", "READ")
        A0File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_A0.root", "READ")
        alFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_al.root", "READ")
        arFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_ar.root", "READ")
        nlFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_nl.root", "READ")
        nrFile = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_nr.root", "READ")

    # Retrieve the parameter function files
    fct_sigma1 = sigma1File.Get('fct_sigma1')
    fct_sigma2 = sigma2File.Get('fct_sigma2')
    fct_A0 = A0File.Get('fct_A0')
    fct_al = alFile.Get('fct_al')
    fct_ar = arFile.Get('fct_ar')
    fct_nl = nlFile.Get('fct_nl')
    fct_nr = nrFile.Get('fct_nr')

    # Close the parameter ROOT files
    sigma1File.Close()
    sigma2File.Close()
    A0File.Close()
    alFile.Close()
    arFile.Close()
    nlFile.Close()
    nrFile.Close()

    # Evaluate parameter functions at masses
    sigma1 = fct_sigma1.Eval(mass)
    sigma2 = fct_sigma2.Eval(mass)
    fracL = fct_A0.Eval(mass)
    aL = fct_al.Eval(mass)
    aR = fct_ar.Eval(mass)
    nL = fct_nl.Eval(mass)
    nR = fct_nr.Eval(mass)

    # Set up model
    # ----------------------------------------------------------------
    # Declare CBall variables with initial value and range
    xTitle = "#font[42]{#it{m}(#gamma#gamma) [GeV/#it{c}^{2}]}"
    x = ROOT.RooRealVar("x", xTitle, von, bis)
    if param_fixed:
        cbmean = ROOT.RooRealVar("mu", "mean", mea, mea, mea)
        cbsigmaL = ROOT.RooRealVar("sigma1", "#sigma_{1}",
                                   sigma1, sigma1, sigma1)
        cbsigmaR = ROOT.RooRealVar("sigma2", "#sigma_{2}",
                                   sigma2, sigma2, sigma2)
        cbaL = ROOT.RooRealVar("alphaL", "#alpha_{L}", aL, aL, aL)
        cbaR = ROOT.RooRealVar("alphaR", "#alpha_{R}", aR, aR, aR)
        cbnL = ROOT.RooRealVar("nL", "n_{L}", nL, nL, nL)
        cbnR = ROOT.RooRealVar("nR", "n_{R}", nR, nR, nR)
    else:
        cbmean = ROOT.RooRealVar("mu", "mean", mea, mea_min, mea_max)
        cbsigmaL = ROOT.RooRealVar("sigma1", "#sigma_{1}",
                                   sigma1, sigmaL_min, sigmaL_max)
        cbsigmaR = ROOT.RooRealVar("sigma2", "#sigma_{2}",
                                   sigma2, sigmaR_min, sigmaR_max)
        cbaL = ROOT.RooRealVar("alphaL", "#alpha_{L}", aL, aL_min, aL_max)
        cbaR = ROOT.RooRealVar("alphaR", "#alpha_{R}", aR, aR_min, aR_max)
        cbnL = ROOT.RooRealVar("nL", "n_{L}", nL, nL_min, nL_max)
        cbnR = ROOT.RooRealVar("nR", "n_{R}", nR, nR_min, nR_max)

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
    nsig = ROOT.RooRealVar("nsig", "N_{sig}",
                           1000, 0, num_entries)
    model = ROOT.RooAddPdf("model", "CBallSum + nsig",
                           ROOT.RooArgList(cballSum),
                           ROOT.RooArgList(nsig))

    # ----------------!!!!!!!!!!!!!!!!!FIX MAKE ROBUST!!!!!!!!!!!!------------
    histo_data = ROOT.RooDataHist("histo_data", "dataset", x, medial_histo)
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

    if param_fixed:
        # Plot results to frames
        # ----------------------------------------------------------------
        xframe1 = mcstudy.plotParam(nsig, ROOT.RooFit.Bins(65))
        xframe2 = mcstudy.plotError(nsig, ROOT.RooFit.Bins(65))
        xframe3 = mcstudy.plotPull(nsig, ROOT.RooFit.Bins(65),
                                   ROOT.RooFit.FitGauss(ROOT.kTRUE))

        # Draw frames on a canvas
        # ------------------------------------------------------------
        c = ROOT.TCanvas("c", "", 1200, 400)
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
        if not intermediate:
            c.SaveAs("./toy_MC_study_module/plots/toyMC_" + str(mass_index) + "_nsig" + ".png")
        else:
            c.SaveAs("./toy_MC_study_module/plots/medial_toyMC_" + str(mass_index) + "_nsig" + ".png")
    
    nSig = nsig.getVal()
    if not intermediate:
        if mass_index == 0:
            deleteFiles('./toy_MC_study_module/files/main_nSig.txt')
        with open('./toy_MC_study_module/files/main_nSig.txt', 'a+') as f_nSig:
            f_nSig.write('{}\n'.format(nSig))
    else:
        if mass_index == 0:
            deleteFiles('./toy_MC_study_module/files/medial_nSig.txt')
        with open('./toy_MC_study_module/files/medial_nSig.txt', 'a+') as f_nSig:
            f_nSig.write('{}\n'.format(nSig))


def main(mass_index, Dictionary, param_fixed=True, intermediate=False):
    createDirectories('./toy_MC_study_module/plots')
    createDirectories('./toy_MC_study_module/files')
    toyMCFunc(mass_index, Dictionary, param_fixed, intermediate)


if __name__ == '__main__':
    main()
