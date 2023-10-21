import ROOT

# Create a TCanvas to draw the stack plot
canvas = ROOT.TCanvas("canvas", "Stacked Histograms")

# Create a THStack to hold the histograms
stack = ROOT.THStack("stack", "Stacked Histograms")

# Create 10 histograms and set their colors and titles
histograms = []
colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kYellow, ROOT.kMagenta, ROOT.kCyan, ROOT.kOrange, ROOT.kPink, ROOT.kTeal, ROOT.kViolet]
legend_labels = ["Hist 1", "Hist 2", "Hist 3", "Hist 4", "Hist 5", "Hist 6", "Hist 7", "Hist 8", "Hist 9", "Hist 10"]

for i in range(10):
    hist = ROOT.TH1F(f"hist{i}", f"Histogram {i+1}", 25, -5, 5)
    hist.FillRandom("gaus", 1000)
    hist.SetFillColor(colors[i])
    hist.SetLineColor(ROOT.kBlack)  # Set the line color for the histogram borders
    histograms.append(hist)
    stack.Add(hist)

# Create a legend and add entries for each histogram
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)  # Adjust the position as needed
for i, label in enumerate(legend_labels):
    legend.AddEntry(histograms[i], label, "f")  # "f" for filled area

# Draw the stack with a Y-axis range suitable for all histograms
stack.Draw("hist")
stack.SetTitle("Stacked Histograms")
stack.GetYaxis().SetTitle("Y-Axis Title")
stack.GetXaxis().SetTitle("X-Axis Title")

# Draw the legend
legend.Draw()

# Update the canvas
canvas.Update()
canvas.SaveAs("/eos/user/j/jbonetti/outputs_folder/final_eval/stackplot/TEST.png")
# Save the canvas to a file (optional)
# canvas.SaveAs("stacked_histograms.png")

# Keep the script running
#ROOT.gApplication.Run()