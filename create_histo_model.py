from user_defined_functions import createDirectories
from user_defined_functions import deleteFiles
import csv
import sys
import math
import ROOT
ROOT.gROOT.SetBatch(True)


def createHistoModel(histoFileName_QC):
    """..."""

    # File handling
    #--------------------------------------------------------------------------
    outputDir = './output/create_histo_model/'
    createDirectories(outputDir)
    deleteFiles(outputDir + 'histo_model.root')


    # Retrieve parameter values
    #--------------------------------------------------------------------------
    # Fill mass list from csv file
    mass = []
    with open('./mainDict.csv', newline='') as mainDict:
        reader = csv.DictReader(mainDict)
        for row in reader:
            mass.append(float(row['qc_mass']))
            
    # Open the parameter ROOT files
    sigmaLFile = ROOT.TFile.Open("./output/parameter_fit_output"\
                                 "/parameter_rootfiles/main_sigmaL.root",
                                 "READ")
    sigmaRFile = ROOT.TFile.Open("./output/parameter_fit_output"\
                                 "/parameter_rootfiles/main_sigmaR.root",
                                 "READ")
    A0File = ROOT.TFile.Open("./output/parameter_fit_output"\
                             "/parameter_rootfiles/main_A0.root",
                             "READ")
    alFile = ROOT.TFile.Open("./output/parameter_fit_output"\
                             "/parameter_rootfiles/main_al.root",
                             "READ")
    arFile = ROOT.TFile.Open("./output/parameter_fit_output"\
                             "/parameter_rootfiles/main_ar.root",
                             "READ")
    nlFile = ROOT.TFile.Open("./output/parameter_fit_output"\
                             "/parameter_rootfiles/main_nl.root",
                             "READ")
    nrFile = ROOT.TFile.Open("./output/parameter_fit_output"\
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
    histoFile = ROOT.TFile(histoFileName_QC)
    for index, key in enumerate(histoFile.GetListOfKeys()):
        kname = key.GetName()
        histo = histoFile.Get(kname)

        # Calculate Parameter Values
        # ---------------------------------------------------------------------
        mea = mass[index]
    
        # Evaluate parameter functions at masses
        sigmaL = fct_sigmaL.Eval(mea)
        sigmaR = fct_sigmaR.Eval(mea)
        fracL = fct_A0.Eval(mea)
        aL = fct_al.Eval(mea)
        aR = fct_ar.Eval(mea)
        nL = fct_nl.Eval(mea)
        nR = fct_nr.Eval(mea)

        ww = math.sqrt(fracL * sigmaL**2 + (1 - fracL) * sigmaR**2)
        von = mea - 3 * ww
        bis = mea + 3 * ww

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

        # Create a model with CBall sum and number of fracL events (get nSig)
        # ---------------------------------------------------------------------
        num_entries = histo.GetEntries()
        nsig = ROOT.RooRealVar("nsig", "N_{sig}",
                               1000, 0, num_entries)
        model = ROOT.RooAddPdf("model", "CBallSum + nsig",
                               ROOT.RooArgList(cballSum),
                               ROOT.RooArgList(nsig))
        histo_data = ROOT.RooDataHist("histo_data", "dataset", x, histo)
        model.fitTo(histo_data, ROOT.RooFit.Extended(True), ROOT.RooFit.Save())
        nSig = nsig.getVal()

        # Create binned histograms
        # ------------------------------------------------------------------------
        nBins = histo.GetNbinsX()
        xmin = histo.GetXaxis().GetXmin()
        xmax = histo.GetXaxis().GetXmax()
        data_model = cballSum.generate(x, nSig)
        histo_model = data_model.createHistogram(
                          'histo_model_mass{}'.format(index),
                          x, ROOT.RooFit.Binning(nBins, xmin, xmax))
        
        # Write histograms to root file
        ofile = ROOT.TFile(outputDir + 'histo_model.root', "UPDATE")
        histo_model.Write('histo_model_mass{}'.format(index))
        ofile.Close()


def main():
    try:
        histoFileName_QC = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} </path/to/histograms.root>\n")
    createHistoModel(histoFileName_QC)


if __name__ == '__main__':
    main()

