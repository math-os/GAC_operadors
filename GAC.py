from typing import List
import random

### Constants
_MORT = 0
_VIU = 1
_INC_EPSILO = 1.05
_DEC_EPSILO = 0.95
_RANG_MUTACIO = 3
_MAX_ERROR_GENERACIONS = 5000
_INC_ERROR = 0.0001

###############################################################################
### Funcions auxiliars
### swap: Intercamvia dos elements d'una llista donades les seves posicions
def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


###############################################################################
### Definició de Classes
### Classe _ENTORN
class _ENTORN:
    def __init__(self, _Objectiu: float, _Error: float, _Epsilo: float, _fmut: int, _frep: int, _Operants: list):
        self.Objectiu = _Objectiu
        self.Error = _Error
        self.Epsilo = _Epsilo
        self.Operants = _Operants
        self.f_mut = _fmut
        self.f_rep = _frep
        self.Blocs = int(len(_Operants) / 4)

    def imprimir(self):
        print("OBJ: " + str(self.Objectiu) + " ERR: " + str(self.Error) + " EPSILO: " + str(self.Epsilo))
        print("BLK: " + str(self.Blocs))
        print(self.Operants)

    def variar_Epsilo(self, NP: int, NPA: int):
        if (NP < NPA):
            self.Epsilo = self.Epsilo * _INC_EPSILO
        else:
            self.Epsilo = self.Epsilo * _DEC_EPSILO


### Classe _ADN
class _ADN:
    def __init__(self, _pid, _ppid, _estat, _operador):
        self.pid = _pid
        self.ppid = _ppid
        self.estat = _estat
        self.operador = _operador

    def imprimir(self):
        print("PID: " + str(self.pid) + " PPID: " + str(self.ppid) + " ESTAT: " + str(self.estat))
        print(self.operador)

    def mutacio(self):
        for i in range(_RANG_MUTACIO):
            swap(self.operador, random.randint(0, len(self.operador) - 1), random.randint(0, len(self.operador) - 1))


### Classe principal. Utilitza les altres dos: _ENTORN i _ADN
### Classe _MON
class _MON:
    def __init__(self, _Objectiu: float, _Error: float, _Epsilo: float, _fmut: int, _frep: int, _Operants: list,
                 _n_poblacio: int):
        self.generacio = 0
        self.entorn = _ENTORN(_Objectiu, _Error, _Epsilo, _fmut, _frep, _Operants)
        self.poblacio = List[_ADN]
        self.np = _n_poblacio
        self.npids = 0
        self.best = _ADN(0, 0, 1, [])

    def generar_ADN(self, blocs: int, pid: int, ppid: int) -> _ADN:
        operadors = []
        # Afegir blocs d'operadors. bloc = ( + , - , * , / )
        for i in range(blocs):
            operadors.append("+")
            operadors.append("-")
            operadors.append("*")
            operadors.append("/")
        # Barrejar inicialment els operadors
        for i in range(4 * blocs):
            op1 = random.randint(0, (4 * blocs) - 1)
            op2 = random.randint(0, (4 * blocs) - 1)
            swap(operadors, op1, op2)
        return _ADN(pid, ppid, 1, operadors)

    def copia_ADN(self, A: _ADN, B: _ADN, pid: int):  # A->B
        B.pid = pid
        B.ppid = A.pid
        B.estat = _VIU
        nop = len(A.operador)
        for op in range(nop):
            B.operador[op] = A.operador[op]

    def generar_poblacio(self):
        print("Generar població: ", self.np, self.entorn.Blocs)
        self.poblacio = [self.generar_ADN(self.entorn.Blocs, 0, 0) for _ in range(self.np)]
        pid = 1
        for adn in self.poblacio:
            adn.ppid = 0
            adn.pid = pid
            pid = pid + 1
        self.npids = len(self.poblacio)


    ### Esborrar els adn.estat = _MORT
    def esborrar_eliminats(self):
        self.poblacio = [adn for adn in self.poblacio if adn.estat != _MORT]


    ### Costruieix l'expressió a avaluar en cada cas
    def str_expressio(self, adn: _ADN):
        # Construir l'expressió a avaluar
        calcul = ""
        nop = len(adn.operador)
        for i in range(nop):
            calcul = calcul + str(self.entorn.Operants[i]) + adn.operador[i]
        calcul = calcul + str(self.entorn.Operants[nop])
        return calcul

    def reproduccio_mutacio(self):
        ### Generem una llista buida
        pid = self.npids
        #print(pid)
        Nous_adn = [self.generar_ADN(self.entorn.Blocs, 0, 0) for _ in range(0)]
        for adn in self.poblacio:
            ### Taxa de reproduccio, asexual en aquest problema
            if random.randint(1, 10) > self.entorn.f_mut:
                pid = pid + 1
                nou_adn = self.generar_ADN(self.entorn.Blocs, pid, adn.pid)
                self.copia_ADN(adn, nou_adn, pid)
                nou_adn.mutacio()
                Nous_adn.append(nou_adn)
            ### Taxa de creuament
        for nou_adn in Nous_adn:
            self.poblacio.append(nou_adn)
        #self.npids = self.npids + len(self.poblacio)
        self.npids = self.npids + len(Nous_adn)

    def solucio(self, adn: _ADN):
        # print(self.str_expressio(adn), " = ", str(eval(self.str_expressio(adn))))
        resultat = eval(self.str_expressio(adn))
        solucio = False
        inf = self.entorn.Objectiu - self.entorn.Error
        sup = self.entorn.Objectiu + self.entorn.Error
        if resultat >= inf and resultat <= sup:
            solucio = True
        return solucio, resultat

    def imp_solucio(self, adn: _ADN):
        print("-------------  SOLUCIÓ !!! -------------")
        print("OBJECTIU: ", self.entorn.Objectiu, "ERROR: ", self.entorn.Error)
        print("PID: ", adn.pid, "PPID: ", adn.ppid)
        print(self.str_expressio(adn), " = ", str(eval(self.str_expressio(adn))))

    def imp_best(self, adn: _ADN):
        print("-------------  BEST !!! -------------")
        print("OBJECTIU: ", self.entorn.Objectiu, "ERROR: ", self.entorn.Error)
        print("PID: ", adn.pid, "PPID: ", adn.ppid)
        print(self.str_expressio(adn), " = ", str(eval(self.str_expressio(adn))))

    def fitness(self, resultat: float, inf: float, sup: float):
        if resultat < inf or resultat > sup:
            return _MORT

    def best_ADN(self, A: _ADN, B: _ADN):
        rA = eval(self.str_expressio(A))
        rB = eval(self.str_expressio(B))
        rAd = abs(self.entorn.Objectiu - rA)
        rBd = abs(self.entorn.Objectiu - rB)
        if ( rAd < rBd ):
            return A
        else:
            return B


    ### Recorre la població. Busca solució i extermina als > Epsilo
    def iterar_generacio(self):
        solucio = False
        for adn in self.poblacio:
            solucio, resultat = self.solucio(adn)
            if solucio:
                self.imp_solucio(adn)
                return True
            self.best = self.best_ADN( adn, self.best )
            inf = self.entorn.Objectiu - self.entorn.Epsilo
            sup = self.entorn.Objectiu + self.entorn.Epsilo
            adn.estat = self.fitness(resultat, inf, sup)

    def imprimir_poblacio(self):
        if not self.poblacio:
            return
        for adn in self.poblacio:
#           print("PID: ", adn.pid, "PPID: ", adn.ppid)
            print("PID: ", ";", adn.pid, ";","PPID: ",";", adn.ppid,";", self.str_expressio(adn), ";",str(eval(self.str_expressio(adn))))

    def rodar_mon(self):
        solucio = False
        self.generacio = 0
        NPA = self.np
        while not solucio and self.poblacio:
            NP = self.np
            print("GENERACIO", self.generacio, "N: ", self.np, "EPSILO: ", self.entorn.Epsilo, "NPIDS: ", self.npids)
            solucio = self.iterar_generacio()
            self.esborrar_eliminats()
            self.reproduccio_mutacio()
            self.entorn.variar_Epsilo(NP, NPA)
            self.np = len(self.poblacio)
            NPA = NP
            self.generacio = self.generacio + 1
            if ( self.generacio % _MAX_ERROR_GENERACIONS == 0 ):
                self.entorn.Error = self.entorn.Error + _INC_ERROR
        if not solucio:
            self.imp_best(self.best)


# Permutacions amb Repetició de n elements
# on el primer element es repeteix n1, el segon n2 ... i el darrer nr vegades
# P(n)(n1,n2, ...,nr) = n! / (n1!·n2!· ... ·nr!)
# Si n = 24 i ni = 6
# P(24)(6,6,6,6) = 24!/(6!·6!·6!·6!) = 2.308.743.493.056 (Un nombre considerable de possibilitats ... )
# A un ritme de 1000 comprovacions per segon
# seg	                hores	        dies	     anys
# 2.308.743.493,05	    641.317,63	    26.721,56     73,20

Error = 0.0
Epsilo = 20000
fmut = 5
frep = 6
Objectiu = 15
Operants = [2, 5, 10, 15, \
            20, 25, 30, 35, \
            456, 83, 290, 1135, \
            45, 183, 1290, 135, \
            56, 283, 90, 2135, \
            5, 383, 1290, 3135, \
            856, 483, 2290, 1335, \
            156, 583, 3290, 1133, \
            456, 83, 290, 1135, \
            40, 45, 50, 55, \
            60, 4, 67, 79, \
            23, 36, 1200, 456, \
            83, 34, 234, 567, \
            6]
Poblacio_Inicial = 100
mon = _MON(Objectiu, Error, Epsilo, fmut, frep, Operants, Poblacio_Inicial)
mon.entorn.imprimir()
mon.generar_poblacio()
mon.rodar_mon()
mon.entorn.imprimir()











# Testejant ...
### Exemple 1 bloc
#Operants = [2, 5, 10, 15, 20]
#Objectiu = -4
### Exemple 2 blocs

### Operants = [2, 5, 10, 15, 20, 25, 30, 35, 40]

### Exemple 5 blocs
#Objectiu = 29890.2632011909