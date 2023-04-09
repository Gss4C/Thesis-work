class sample:
    def __init__(self, label, numerino = 5,altrastringa = 'a'):
        self.label = label
        self.numerino = numerino
        self.altrastringa = altrastringa

    def dammi_il_y(self, from_out):
        zz = self.numerino * 50 - from_out
        return zz
    def stringcombo(self):
        zz = self.label + self.altrastringa
        return zz 

coso = sample(label="label_del_coso", altrastringa= "/altra string")
coso.qualcosa = "niente"

stocazzo = sample(label="label_del_coso", altrastringa= "/altra string")

tizio = [4532 ,35 ,235 , 635]