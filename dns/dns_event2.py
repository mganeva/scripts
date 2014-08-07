ws = Load("/backup/build/jcns-mantid/datafiles/dns/test_event")
sumws = SumSpectra(ws)
sumws_rebinned = Rebin(sumws, 1)
graph_spec = plotSpectrum(sumws_rebinned, 0)