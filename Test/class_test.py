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
class contino:
    def __init__(self, listino = [0], numerino = 0):
        self.listino = listino
        self.numerino = numerino
    def counterino(self):
        kakkola = len(self.listino)
        for i in range(self.numerino):
            kakkola += i
        return kakkola


coso = sample(label="label_del_coso", altrastringa= "/altra string")
coso.qualcosa = "niente"

stocazzo = sample(label="label_del_coso", altrastringa= "/altra string")

tizio = [4532 ,35 ,235 , 635]