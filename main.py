import math
from classes import *


def print_list(list):
    """
    Prints a list passed as a parameter
    :param list:
    :return:
    """
    for index, el in enumerate(list):
        print("{ind}/ {el}".format(ind=index, el=el))
    print("\n\n")


def binarymodel(option, rf, sigma, N, size_steps):
    """
    Uses the binary model to price an option
    We chose to use one time step for each day, the number of time steps is the number of days until maturity
    :param N: Number of steps in the binomial tree
    :param size_steps: Size of the steps in years
    :param option: The options we want to price
    :param rf: Risk-free interest rate
    :param sigma: Volatility
    :return:
    """
    # First we calculate the model parameters
    n = N
    u = math.exp(sigma * math.sqrt(size_steps))
    d = 1 / u
    p = (math.exp(rf * size_steps) - d) / (u - d)
    print("n={}, u={}, p={}, d={}".format(n, u, p, d))

    # Creating an empty tree that we store as a bidimensional list
    tree = [[None] * (n + 1) for i in range(n + 1)]

    # Setting the first value at the actual price of our option (the underlying asset price)
    tree[0][0] = option.asset.actual_price

    for i in range(1, n + 1):
        # Creating the tree
        tree[i] = [el * u if el is not None else None for el in tree[0:i][i - 1]]
        tree[i][i] = tree[i - 1][i - 1] * d

    valueTree = [[0] * (n + 1) for i in range(n + 1)]
    # Calculating the value at expiry
    if isinstance(option, PutOption):
        valueTree[-1] = [max(0, x - option.strike) if x is not None else None for x in tree[-1]]
    else:
        valueTree[-1] = [max(0, option.strike - x) if x is not None else None for x in tree[-1]]
    return [tree, valueTree]


def main():
    list_option_type = ["Call", "Put", "Loopback Call", "Loopback Put", "Barrier Up and In Call",
                        "Barrier Up and Out Call", "Barrier Down and In Call", "Barrier Down and Out Call",
                        "Barrier Up and In Put", "Barrier Up and Out Put", "Barrier Down and In Put",
                        "Barrier Down and Out Put"]
    list_asset = []
    list_options = []
    mychar = ""
    while mychar != "q":
        print("""
### MENU PRINCIPAL ###

Bienvenue dans le menu principal du pricer d'options. Vous pourrez créer votre portefeuille d'options et jouer 
avec leur valeurs suivant les différentes options proposées ci dessous. Pour créer une option vous devez avoir au préalable créé un asset.
Veuillez effectuer un choix à l'aide de votre clavier !

1/ Créer un asset
2/ Créer une option
3/ Voir mon portefeuille
4/ Modifier la valeur d'un asset (simulation d'un changement de prix a date actuelle)
5/ Pricer une option en utilisation les arbres binomiaux
q/ Quitter
""")
        mychar = input("Choix: ")
        if isinstance(mychar, (str)) and mychar in ["1", "2", "3", "4", "5", "q"]:
            if mychar == "1":
                print("\n### CREATION ASSET ###\n\n")
                name = input("Veuillez saisir le nom de votre asset:\n")
                init_price = input("Veuillez saisir la valeur de l'asset:\n")
                try:
                    list_asset.append(Asset(name=name, initial_price=float(init_price)))
                except ValueError:
                    print("Veuillez saisir des valeurs valides\n\n")

            elif mychar == "2":
                if len(list_asset) == 0:
                    # If the list of assets is empty
                    print("Veuillez d'abord créer un asset\n\n")
                else:
                    print("\n### CREATION OPTION ###\n\n")
                    print_list(list_asset)
                    try:
                        # We first need to choose an asset
                        # The whole code is in a try clause to catch exception when parsing input into integer - float
                        choice = int(input("Veuillez choisir un asset: "))
                        if choice >= len(list_asset) or choice < 0:
                            raise (ValueError())
                        else:
                            # Then we choose the type of option we want to create
                            print("### CHOIX TYPE OPTION ###")
                            print_list(list_option_type)
                            choice_type = int(input("Veuillez choisir un type d'option: "))
                            if choice_type >= len(list_option_type) or choice < 0:
                                # Wrong choice
                                raise (ValueError)
                            else:
                                myasset = list_asset[choice]
                                strike = float(input("Veuillez saisir un prix strike: "))
                                matur = int(input("Veuillez saisir une maturité (en jours): "))
                                barr = float(input("Veuillez saisir un prix barriere (0 si pas d'option barriere): "))

                                if strike <= 0 or matur < 0 or barr < 0:
                                    # Checking if values are positive
                                    raise (ValueError())

                                if choice_type == 0:
                                    o = CallOption(asset=myasset, strike=strike, days=matur)
                                elif choice_type == 1:
                                    o = PutOption(asset=myasset, strike=strike, days=matur)
                                elif choice_type == 2:
                                    o = LoopbackCall(asset=myasset, strike=strike, days=matur)
                                elif choice_type == 3:
                                    o = LoopbackPut(asset=myasset, strike=strike, days=matur)
                                elif choice_type == 4:
                                    o = UpAndInCall(asset=myasset, strike=strike, days=matur, barrier=barr)
                                elif choice_type == 5:
                                    o = UpAndOutCall(asset=myasset, strike=strike, days=matur, barrier=barr)
                                elif choice_type == 6:
                                    o = DownAndInCall(asset=myasset, strike=strike, days=matur, barrier=barr)
                                elif choice_type == 7:
                                    o = DownAndOutCall(asset=myasset, strike=strike, days=matur, barrier=barr)
                                elif choice_type == 8:
                                    o = UpAndInPut(asset=myasset, strike=strike, days=matur, barrier=barr)
                                elif choice_type == 9:
                                    o = UpAndOutPut(asset=myasset, strike=strike, days=matur, barrier=barr)
                                elif choice_type == 10:
                                    o = DownAndInPut(asset=myasset, strike=strike, days=matur, barrier=barr)
                                elif choice_type == 11:
                                    o = DownAndOutPut(asset=myasset, strike=strike, days=matur, barrier=barr)
                            list_options.append(o)
                    except ValueError:
                        print("Veuillez saisir des valeurs valides")

            elif mychar == "3":
                print("\n### LIST ASSET ###\n")
                print_list(list_asset)
                print("\n### LIST OPTIONS ###\n")
                print_list(list_options)

            elif mychar == "4":
                if len(list_asset) > 0:
                    print("\n### CHANGEMENT DE VALEUR ASSET ###\n")
                    print_list(list_asset)
                    try:
                        choice = int(input("Veuillez choisir un asset dont la valeur est à changer: "))
                        if choice >= len(list_asset) or choice < 0:
                            # Checking if the value chosen by the user is right or not
                            raise (ValueError())
                        else:
                            myasset = list_asset[choice]
                            new_value = float(input("Veuillez entrer le prix actuel de l'asset: "))

                            if new_value <= 0:
                                # If the new value of the asset is lower than 0, raising an exception
                                raise (ValueError)
                            myasset.actual_price = new_value
                    except ValueError:
                        print("Veuillez entrer des valeurs valides")
                else:
                    print("Veuillez d'abord créer un asset")
            elif mychar == "5":
                if len(list_options) > 0:
                    print("\nPRICING D'OPTION AVEC ARBRES BINOMIAUX\n")
                    print_list(list_options)
                    try:
                        choice = int(input("Veuillez choisir une option à pricer: "))
                        if choice >= len(list_options) or choice < 0:
                            # Checking if the value chosen by the user is right or not
                            raise (ValueError())
                        else:
                            o = list_options[choice]
                            vol = float(input("Veuillez saisir une valeur pour la volatilité: "))
                            N = int(input("Veuillez saisir un nombre de steps (hauteur de l'arbre): "))
                            size_steps = float(input("Veuillez saisir une taille de pas (en année - 0.25 = 3 mois): "))
                            [tree, valueTree] = binarymodel(o, 0, vol, N, size_steps)
                            print("Voici l'arbre binomial correspondant a vos valeurs "
                                  "et la derniere colonne de l'arbre corrigée (max(0, payoff)): "
                                  "{tree}\n{valueTree}\n".format(
                                tree=tree, valueTree = valueTree[-1]
                            ))
                    except ValueError:
                        print("Veuillez saisir des valeurs correctes")
                else:
                    print("Veuillez d'abord créer une option")
        else:
            print("Veuillez saisir un caractère valide")


main()
