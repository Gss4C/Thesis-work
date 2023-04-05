class sample:
    def __init__(self, label, numerino = 5):
        self.label = label
        self.numerino = numerino
    def dammi_il_y(self, from_out):
        zz = self.numerino * 50 - from_out
        return zz 

coso = sample("label_del_coso")
coso.qualcosa = "niente"