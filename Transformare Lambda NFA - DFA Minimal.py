def conversie_lambda_nfa_in_nfa(nume_fisier_intrare):
    f = open(nume_fisier_intrare)
    n = int(f.readline())  # numarul de stari
    m = int(f.readline())  # numarul de caractere din alfabet
    l_litere = f.readline().split()  # alfabetul
    initiala = int(f.readline())  # stare initiala
    k = int(f.readline())  # numarul de stari finale
    l_finale = {int(element) for element in f.readline().split()}  # lista starilor finale

    dex = dict([])  # in dex[inceput] vom pune translatiile (litera, destinatie)
    for i in range(n):
        dex[i] = []

    l = int(f.readline())  # numarul de translatatii
    for linie in f:
        linie = linie.split()
        linie[0] = int(linie[0])
        linie[2] = int(linie[2])
        dex[linie[0]].append(tuple([linie[1], linie[2]]))
    f.close()

    # S-a facut citirea datelor

    print("DEX: " + str(dex))

    def functie_inchidere_lambda(dex_sursa, dex_curent, stare_sursa, stare_curenta, litera):
        # dex_sursa e cel din care ne luam starile, dex curent in cel care adaugam
        # avem nevoie de starea_sursa carui adaugam datele si starea_curenta pt parcurgere
        for i in range(len(dex_sursa[stare_curenta])):
            if dex_sursa[stare_curenta][i][0] == litera and v[dex_sursa[stare_curenta][i][1]] == 0:
                v[stare_curenta] = 1
                dex_curent[stare_sursa].add(dex_sursa[stare_curenta][i][1])  # adaugam starea
                functie_inchidere_lambda(dex_sursa, dex_curent, stare_sursa, dex_sursa[stare_curenta][i][1], litera)

    v = [0 for i in range(n)]  # vector de verificare a starilor pentru a nu avea ciclu lambda infinit
    dex_inchidere_lambda_1 = dict([])  # dictionarul cu seturile unde punem starile in care ajungem cu lambda
    for i in range(n):  # (+starea de la care pornim).
        dex_inchidere_lambda_1[i] = {i}

    # Apelam pentru inchiderea lambda.
    for j in range(n):
        functie_inchidere_lambda(dex, dex_inchidere_lambda_1, j, j, '$')
        v = [0 for i in range(n)]  # reactualizam starile prin care putem merge

    print("Inchiderea lambda: " + str(dex_inchidere_lambda_1))

    dex_inchidere_lambda_2 = dict([])  # In acest dex vom avea tabelul in aceasta forma 0: {a: {}, b:{} ...} 1:...
    # ,iar ordinea fiecarui set este asociat ordinii fiecarei stari. Ex: Setul 0 din a este asociat starii 0.

    for i in range(n):
        dex_inchidere_lambda_2[i] = dict([])
        for litera in l_litere:
            dex_inchidere_lambda_2[i].update({litera: set([])})
        for stare in dex_inchidere_lambda_1[i]:
            for litera in l_litere:
                for t in dex[stare]:
                    if t[0] == litera:
                        dex_inchidere_lambda_2[i][litera].add(t[1])

    print("Inchiderea lambda2: " + str(dex_inchidere_lambda_2))

    dex_inchidere_lambda_3 = dict([])

    for i in range(n):
        dex_inchidere_lambda_3[i] = dict([])
        for litera in l_litere:
            dex_inchidere_lambda_3[i].update({litera: set([])})
            # Trebuie sa mai reunium din inchiderea lambda corespunzator fiecarei stari, respectiv, fiecarui caracter
            for j in dex_inchidere_lambda_2[i][litera]:
                dex_inchidere_lambda_3[i][litera] = dex_inchidere_lambda_3[i][litera].union(dex_inchidere_lambda_1[j])

    print("Inchiderea lambda3: " + str(dex_inchidere_lambda_3))

    # Actualizam starile finale
    for stare in dex_inchidere_lambda_1:
        for element in dex_inchidere_lambda_1[stare]:
            if element in l_finale:
                l_finale.add(stare)
    print("Starile finale sunt: " + str(l_finale))

    def functie_de_inlocuire(stare_de_sters, stare_de_inlocuit):
        for fiecare_stare in dex_inchidere_lambda_3:
            for litera in dex_inchidere_lambda_3[fiecare_stare]:
                if stare_de_sters in dex_inchidere_lambda_3[fiecare_stare][litera]:
                    dex_inchidere_lambda_3[fiecare_stare][litera].add(stare_de_inlocuit)
                    dex_inchidere_lambda_3[fiecare_stare][litera].discard(stare_de_sters)

    # Inlocuim starile redundante
    # dex_inlocuire={x:{} for x in range(n)}
    v = [-1 for i in range(n)]

    for stare in dex_inchidere_lambda_3:
        for stare_de_comparat in dex_inchidere_lambda_3:
            if stare != stare_de_comparat:
                if v[stare] == -1:  # FOARTE IMPORTANT: Se face echivalenta pe clase
                    # si se va omite in viitor suprascrierea unei clase din echivalenta cu un alt reprezentant decat cel initial
                    if dex_inchidere_lambda_3[stare] == dex_inchidere_lambda_3[stare_de_comparat]:
                        v[stare_de_comparat] = stare
    # print(v)

    for element in range(len(v)):
        if v[element] != -1:
            functie_de_inlocuire(element, v[element])

    for element in range(len(v)):
        if v[element] != -1:
            dex_inchidere_lambda_3.pop(element)

    print("Inchidere lambda3 noua: " + str(dex_inchidere_lambda_3))
    return dex_inchidere_lambda_3, initiala, l_finale, l_litere


# automat_nfa,stare_initiala,l_finale,l_litere=conversie_lambda_nfa_in_nfa('laborator.txt')


def conversie_nfa_in_dfa(automat_nfa, stare_initiala, l_finale, l_litere):
    print(automat_nfa)
    coada = [stare_initiala]
    v = [{stare_initiala}]
    automat_dfa = {}

    retine = max(automat_nfa) + 1  # Pentru pasul de redenumire

    print('Coada: ' + str(coada))
    print('Vectorul de vizitari: ' + str(v))

    def transf_submultime(submultime):
        cuvant = ""
        for element in submultime:
            cuvant += str(element)
        return cuvant

    while len(coada) > 0:
        primul_element = coada[0]
        # Schita din DFA:
        automat_dfa[primul_element] = {}
        for litera in l_litere:
            automat_dfa[primul_element][litera] = set()

        if {primul_element} not in v:
            v.append({primul_element})

        # Caz special: daca starea noastra e cuvant, atunci e compusa, deci
        # trebuie sa ii aflam starile in care poate sa mearga. Punem tot in NFA starea si tranzitia ei
        if primul_element not in automat_nfa:
            automat_nfa[primul_element] = {}
            for litera in l_litere:
                automat_nfa[primul_element][litera] = set()

            for element in primul_element:
                int_element = int(element)
                # for int_element in automat_nfa:
                for litera in l_litere:
                    for elemente in automat_nfa[int_element][litera]:
                        automat_nfa[primul_element][litera].add(elemente)

        # Acum intram in cele 2 cazuri, pentru fiecare stare:
        # Cazul 1: Avem mai multe stari prin care putem merge cu o litera
        # Cazul 2: Avem o stare sau niciuna in care putem merge

        for litera in l_litere:
            # Pentru fiece stare, fiece litera, luam setul respectiv
            sub_stare = automat_nfa[primul_element][litera]
            if len(sub_stare) > 1:  # Cazul 1
                if sub_stare not in v and {transf_submultime(sub_stare)} not in v:
                    sub_stare = transf_submultime(sub_stare)  # Returneaza multime formata
                    # dintr-un singur element
                    # si anume "stare_tranz1+stare_tranz2..."
                    coada.append(sub_stare)
                    automat_dfa[primul_element][litera] = {sub_stare}
                else:
                    automat_dfa[primul_element][litera] = {transf_submultime(sub_stare)}
            else:  # Cazul 2
                if sub_stare not in v:
                    # Daca sub_starea nu e vizitata
                    # trebuie sa o parcurgem in dfa

                    # Daca submultimea sub_stare de 1
                    # element ar fi vizitat, atunci nu mai trebuie
                    # sa il parcurgem in dfa.
                    for unic_element in sub_stare:
                        coada.append(unic_element)
                # Totusi, poate avem probleme la submultime cu mai multe stari
                automat_dfa[primul_element][litera] = sub_stare
        coada.pop(0)

    print("Automatul DFA: " + str(automat_dfa))

    for element in automat_dfa:
        if isinstance(element, str):
            for atom in element:
                atom = int(atom)
                if atom in l_finale:
                    l_finale.append(element)

    for element in automat_dfa:
        if isinstance(element, str):
            automat_dfa.update({retine: automat_dfa[element]})
            automat_dfa.pop(element)
            if element in l_finale:
                l_finale.append(retine)
                l_finale.remove(element)
            for orice_stare in automat_dfa:
                for orice_litera in l_litere:
                    if automat_dfa[orice_stare][orice_litera] == {element}:
                        automat_dfa[orice_stare][orice_litera].pop()
                        automat_dfa[orice_stare][orice_litera].add(retine)
            retine += 1
    print("Starile finale (cu starile inlocuite): " + str(l_finale))
    print("Automatul DFA final (cu starile inlocuite): " + str(automat_dfa))


# automat_nfa, stare_initiala, l_finale, l_litere = {0: {'a': {0,1}, 'b': {}}, 1: {'a': {1}, 'b': {1,2}},2: {'a': {1}, 'b': {2}}}, 0, [2], ['a', 'b']
# conversie_nfa_in_dfa(automat_nfa, stare_initiala,l_finale,l_litere)