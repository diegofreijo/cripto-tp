FINAL=30

class _Score:
    ptosMios=None
    ptosOtro=None

    def __init__(self):
        self.ptosMios=0
        self.ptosOtro=0
        
    def incrementarSocreMio(self,n):
        self.ptosMios=self.ptosMios+n
        
    def incrementarScoreOtro(self,n):
        self.ptosOtro=self.ptosOtro+n
        
    def partidoGanado(self):
        if self.ptosMios >= FINAL and self.ptosOtro >= FINAL:
            return 2
        elif self.ptosMios >= FINAL:
            return 1
        elif self.ptosOtro >= FINAL:
            return -1
        else:
            return 0

    def __str__(self):
        return "\t    SCORE\n" + "\tYO    |   OTRO\n" + "\t---------------\n" \
               "\t  " + str(self.ptosMios) +  "\t   " + str(self.ptosOtro) + "\n"
