from user_defined_functions import createDirectories
import csv
import sys
import math
import ROOT
ROOT.gROOT.SetBatch(True)


def histoCompare(modelFileName, histoFileName):
    """..."""

    # File handling
    #--------------------------------------------------------------------------
    outputDir = './output/histo_compare/'
    createDirectories(outputDir)

    # Retrieve some parameter values for setting axis ranges
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

    # Retrieve the parameter function files
    fct_sigmaL = sigmaLFile.Get('fct_sigmaL')
    fct_sigmaR = sigmaRFile.Get('fct_sigmaR')
    fct_A0 = A0File.Get('fct_A0')

    # Close the parameter ROOT files
    sigmaLFile.Close()
    sigmaRFile.Close()
    A0File.Close()

    # Loop Through Histogram and Model
    #--------------------------------------------------------------------------
    modelFile = ROOT.TFile(modelFileName)
    histoFile = ROOT.TFile(histoFileName)
    for index, (mKey, hKey) in enumerate(zip(modelFile.GetListOfKeys(), histoFile.GetListOfKeys())):
        mKeyName = mKey.GetName()
        model = modelFile.Get(mKeyName)
        hKeyName = hKey.GetName()
        histo = histoFile.Get(hKeyName)

        mea = mass[index]
        sigmaL = fct_sigmaL.Eval(mea)
        sigmaR = fct_sigmaR.Eval(mea)
        fracL = fct_A0.Eval(mea)

        ww = math.sqrt(fracL * sigmaL**2 + (1 - fracL) * sigmaR**2)
        von = mea - 3 * ww
        bis = mea + 3 * ww

        # Draw Model and Histo
        #----------------------------------------------------------------------
        c = ROOT.TCanvas("c{}".format(index), "c{}".format(index), 500, 500)
        c.GetFrame().SetFillColor(21)
        c.GetFrame().SetBorderSize(12)
        histo.GetXaxis().SetRangeUser(von, bis)
        histo.SetLineColor(1)
        histo.SetTitle("Histo m={}".format(mea))
        histo.Draw()
        model.SetLineColor(2)
        model.Draw('Same')        
        c.SaveAs(outputDir + 'histos_{}.png'.format(index))        

        # Ratio Test
        #----------------------------------------------------------------
        c1 = ROOT.TCanvas("c1{}".format(index), "c1{}".format(index), 500, 500)
        c1.GetFrame().SetFillColor(21)
        c1.GetFrame().SetBorderSize(12)
        h_ratio = histo.Clone()
        h_ratio.Divide(model)
        # h_ratio.Add(model, -1)
        h_ratio_histo = ROOT.TH1F('Histo_Ratio{}'.format(index), '', 100, -2.0, 2.0)
        binMin = h_ratio.FindBin(von)
        binMax = h_ratio.FindBin(bis)
        for i in range(binMin, binMax + 1):
            err = h_ratio.GetBinError(i)
            if err > 0:
                h_ratio_histo.Fill((1 - h_ratio.GetBinContent(i)) / err)
                # h_ratio_histo.Fill((h_ratio.GetBinContent(i)) / err)
        rms = h_ratio_histo.GetRMS()
        h_ratio.SetTitle("Histo/Model m={}".format(mea))
        h_ratio.Draw()
        print(rms)
        print(h_ratio_histo.GetMean())  # systematic error
        c1.SaveAs(outputDir + 'Ratio_{}.png'.format(index))

        # Pull
        # --------------------------------------------------------------------
        c2 = ROOT.TCanvas("c2{}".format(index), "c2{}".format(index), 500, 500)
        c2.GetFrame().SetFillColor(21)
        c2.GetFrame().SetBorderSize(12)
        pull_histo = ROOT.TH1F('Pull_{}'.format(mea), '', 50, -5.0, 5.0)
        nBins = histo.GetNbinsX()
        for i in range(1, nBins + 1):
            h_entries = histo.GetBinContent(i)
            m_entries = model.GetBinContent(i)
            # m_entries_err = ROOT.TMath.Sqrt(m_entries)
            if h_entries > 0 and m_entries > 0:
                pull = m_entries / h_entries  # / m_entries_err
                pull_histo.Fill(pull)
        pull_histo.Draw()
        c2.SaveAs(outputDir + 'Pull_{}.png'.format(index))


def main():
    try:
        modelFileName = sys.argv[1]
        histoFileName = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} </path/to/model.root> </path/to/histogram.root\n")
    histoCompare(modelFileName, histoFileName)


if __name__ == '__main__':
    main()

