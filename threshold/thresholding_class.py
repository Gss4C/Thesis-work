class threshold_evalutator:
    '''
    Classe che dati gli istogrammi (con qualsiasi variabile lungo x) dove ci sono 
    gli eventi True (o di tipo A) e gli eventi False (o di tibo B), permette di 
    gestire tutte le operazioni riguardanti la thrashold per la selezione del segnale
    '''
    def __init__(self, histo_true, histo_false):
        self.histo_true   = histo_true
        self.histo_false  = histo_false
    def threshold_F_seeker(n_bins, bg_efficiency = 0.1):
        full_integral = histo_false.Integral()
        epsilon = 0
        bin_idx = 0
        while(epsilon < bg_efficiency):
            bin_idx += 1
            right_integral = histo_false.Integral(n_bins - bin_idx, n_bins)
            epsilon = right_integral/full_integral
        th_bin = n_bins - bin_idx
        return th_bin, epsilon