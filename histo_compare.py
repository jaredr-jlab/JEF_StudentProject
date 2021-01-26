import parameter_data
import math
from user_defined_functions import createDirectories
from user_defined_functions import deleteFiles
import toy_MC_study_module
import ROOT
# ROOT.gROOT.SetBatch(True)


def histoBinned(mass_index, init_medial_mass_index):
    # Get Histogram
    # ----------------------------------------------------------------
    # Open the ROOT input file
    histoFileName = "JEF_dark_scalar_MCsimu_signal_v3-QC.root"
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
    Mass = [0.02, 0.03, 0.0375,
            0.04, 0.06, 0.07,
            0.125, 0.175, 0.405]

    # Use +/- 3 sigma
    # vonFrac = [0.5, 0.3, 0.26,
    #            0.2, 0.19, 0.18,
    #            0.11, 0.1, 0.016]

    # bisFrac = [0.5, 0.3, 0.26,
    #            0.2, 0.19, 0.18,
    #            0.14, 0.09, 0.016]

    # Other initial values
    mass = Mass[mass_index]
    mea = mass

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

    ww = math.sqrt(fracL * sigmaL**2 + (1 - fracL) * sigmaR**2)
    von = mass - 3 * ww
    bis = mass + 3 * ww

    # Set up models
    # ------------------------------------------------------------------------
    # Declare main CBall variables
    xTitle = "#font[42]{#it{m}(#gamma#gamma) [GeV/#it{c}^{2}]}"
    x = ROOT.RooRealVar("x", xTitle, von, bis)

    cbmean = ROOT.RooRealVar("mu", "mean", mea, mea, mea)
    cbsigmaL = ROOT.RooRealVar("sigmaL", "#sigma_{1}",
                               sigmaL, sigmaL, sigmaL)
    cbsigmaR = ROOT.RooRealVar("sigmaR", "#sigma_{2}",
                               sigmaR, sigmaR, sigmaR)
    cbalphaL = ROOT.RooRealVar("alphaL", "#alpha_{L}", aL, aL, aL)
    cbalphaR = ROOT.RooRealVar("alphaR", "#alpha_{R}", aR, aR, aR)
    cbnL = ROOT.RooRealVar("nL", "n_{L}", nL, nL, nL)
    cbnR = ROOT.RooRealVar("nR", "n_{R}", nR, nR, nR)

    # Build main CBall1, CBall2 and signal fraction component
    cball1 = ROOT.RooCBShape("cball1", "crystal ball 1",
                             x, cbmean, cbsigmaL,
                             cbalphaL, cbnL)
    cball2 = ROOT.RooCBShape("cball2", "crystal ball 2",
                             x, cbmean, cbsigmaR,
                             cbalphaR, cbnR)
    cbfracL = ROOT.RooRealVar("A0", "A_{0}", fracL, fracL, fracL)
    model = ROOT.RooAddPdf("sum", "sum",
                           ROOT.RooArgList(cball1, cball2),
                           ROOT.RooArgList(cbfracL))

    # Creating binned histograms
    # ------------------------------------------------------------------------
    nBins = histo.GetNbinsX()
    xmin = histo.GetXaxis().GetXmin()
    xmax = histo.GetXaxis().GetXmax()
    with open('./toy_MC_study_module/files/medial_nSig.txt') as f_nSig:
        NSig = f_nSig.readlines()
    nSig = float(NSig[mass_index - init_medial_mass_index])
    data_model = model.generate(x, nSig)
    histo_model = data_model.createHistogram(
                      'histo_medial_model_{}'.format(mass_index),
                      x, ROOT.RooFit.Binning(nBins, xmin, xmax))
    
    # Write histograms to root file
    histoFileName = './histo_compare/files/medial_model.root'
    ofile = ROOT.TFile(histoFileName, "UPDATE")
    histo_model.Write('histo_medial_model_{}'.format(mass_index))
    ofile.Close()


def main(init_medial_mass_index=0, final_medial_mass_index=8):
    createDirectories('./histo_compare/files')
    createDirectories('./histo_compare/plots')
    deleteFiles('./histo_compare/files/medial_model.root')
    for mass_index in range(init_medial_mass_index, final_medial_mass_index + 1):
        histoBinned(mass_index, init_medial_mass_index, parameter_data.mainDict)

    # pull_histo.Draw()
    Mass = [0.02, 0.03, 0.0375,
            0.04, 0.06, 0.07,
            0.125, 0.175, 0.405]

    for mass_index in range(0, 9):
        # Other initial values
        mass = Mass[mass_index]
        mea = mass

        # Open the ROOT files
        sigma1File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_sigma1.root", "READ")
        sigma2File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_sigma2.root", "READ")
        A0File = ROOT.TFile.Open("./parameter_fit_module/parameter_rootfiles/medial_A0.root", "READ")

        # Retrieve the function files
        fct_sigma1 = sigma1File.Get('fct_sigma1')
        fct_sigma2 = sigma2File.Get('fct_sigma2')
        fct_A0 = A0File.Get('fct_A0')

        # Close the ROOT files
        sigma1File.Close()
        sigma2File.Close()
        A0File.Close()

        # Evaluate functions at intermediate masses and define variables
        sigmaL = fct_sigma1.Eval(mass)
        sigmaR = fct_sigma2.Eval(mass)
        fracL = fct_A0.Eval(mass)

        ww = math.sqrt(fracL * sigmaL**2 + (1 - fracL) * sigmaR**2)
        von = mass - 3 * ww
        bis = mass + 3 * ww

        # Open the ROOT files
        histoFileName = "JEF_dark_scalar_MCsimu_signal_v3-QC.root"
        histoFile = ROOT.TFile.Open(histoFileName, "READ")

        modelFileName = './histo_compare/files/medial_model.root'
        modelFile = ROOT.TFile.Open(modelFileName, "READ")

        # Retrieve the histograms
        histoName = "sm_sig1_10_" + str(mass_index)
        histo = histoFile.Get(histoName)

        modelName = 'histo_medial_model_' + str(mass_index)
        model = modelFile.Get(modelName)

        # Close the ROOT files
        histo.SetDirectory(0)
        histoFile.Close()
        model.SetDirectory(0)
        modelFile.Close()

        # Histo and model draw()
        c = ROOT.TCanvas("c{}".format(mass_index), "c{}".format(mass_index), 500, 500)
        c.GetFrame().SetFillColor(21)
        c.GetFrame().SetBorderSize(12)
        histo.GetXaxis().SetRangeUser(von, bis)
        histo.SetLineColor(1)
        histo.SetTitle('Histo_Compare_{}'.format(Mass[mass_index]))
        histo.Draw()
        model.SetLineColor(2)
        model.Draw('Same')        
        c.SaveAs('./histo_compare/plots/histos_{}.png'.format(mass_index))        

        #----------------------------Ratio Test--------------------------
        c1 = ROOT.TCanvas("c1{}".format(mass_index), "c1{}".format(mass_index), 500, 500)
        c1.GetFrame().SetFillColor(21)
        c1.GetFrame().SetBorderSize(12)
        h_ratio = histo.Clone()
        h_ratio.Divide(model)
        # h_ratio.Add(model, -1)
        h_ratio_histo = ROOT.TH1F('Histo_Ratio{}'.format(mass_index), '', 100, -2.0, 2.0)
        binMin = h_ratio.FindBin(von)
        binMax = h_ratio.FindBin(bis)
        for i in range(binMin, binMax + 1):
            err = h_ratio.GetBinError(i)
            if err > 0:
                h_ratio_histo.Fill((1 - h_ratio.GetBinContent(i)) / err)
                # h_ratio_histo.Fill((h_ratio.GetBinContent(i)) / err)
        rms = h_ratio_histo.GetRMS()
        h_ratio.Draw()
        print(rms)
        print(h_ratio_histo.GetMean())  # systematic error
        c1.SaveAs('./histo_compare/plots/Ratio_{}.png'.format(mass_index))
        
        # ---------------------------PULL-------------------------------------
        c2 = ROOT.TCanvas("c{}".format(mass_index), "c2{}".format(mass_index), 500, 500)
        c2.GetFrame().SetFillColor(21)
        c2.GetFrame().SetBorderSize(12)
        pull_histo = ROOT.TH1F('Pull_{}'.format(mass_index), '', 50, -5.0, 5.0)
        nBins = histo.GetNbinsX()
        for i in range(1, nBins + 1):
            h_entries = histo.GetBinContent(i)
            m_entries = model.GetBinContent(i)
            # m_entries_err = ROOT.TMath.Sqrt(m_entries)
            if h_entries > 0 and m_entries > 0:
                pull = m_entries / h_entries  # / m_entries_err
                pull_histo.Fill(pull)
        pull_histo.Draw()
        c2.SaveAs('./histo_compare/plots/Pull_{}.png'.format(mass_index))


if __name__ == '__main__':
    main()
