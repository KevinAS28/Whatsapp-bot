class tes(object):
   def __init__(self, a=10):
        self.a = a
        print(self.a, "yay")
   def tripleA(self):
        var = self.a*3
        return var
class main(tes):
    def __init__(self, b):
        tes_initial = super()
        tes_initial.__init__()
        a = tes_initial.a
        aaa = tes_initial.tripleA()
        print(a)
        print(aaa)
        print(b)


main(2)