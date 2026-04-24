import json
import unicodedata

ARQUIVO = "dados_agro.json"

# ---------------- NORMALIZAÇÃO ---------------- #

def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto


# ---------------- CULTURAS ---------------- #

CULTURAS = {
    "1": ("Milho", {"ph_min": 5.5, "ph_max": 7.0}),
    "2": ("Soja", {"ph_min": 6.0, "ph_max": 6.8}),
    "3": ("Cana-de-açúcar", {"ph_min": 5.5, "ph_max": 6.5})
}


def escolher_cultura():
    print("\nEscolha a cultura:")
    for k, v in CULTURAS.items():
        print(f"{k} - {v[0]}")

    while True:
        entrada = normalizar(input("Escolha: "))

        # Se digitou número
        if entrada in CULTURAS:
            return CULTURAS[entrada]

        # Se digitou nome
        for nome, dados in CULTURAS.values():
            if entrada in normalizar(nome):
                return (nome, dados)

        print("Entrada inválida. Tente novamente (ex: milho, soja, cana).")


# ---------------- VALIDAÇÕES ---------------- #

def validar_opcao(valor, opcoes):
    return valor in opcoes

def validar_float(valor):
    try:
        return float(valor)
    except:
        return None


# ---------------- COLETA ---------------- #

def coletar_dados():
    print("\n=== SISTEMA AGRÍCOLA INTELIGENTE ===")

    cultura_nome, cultura_param = escolher_cultura()

    def coletar_nivel(nome):
        while True:
            print(f"\n{nome}:")
            print("1 - Baixo")
            print("2 - Médio")
            print("3 - Alto")
            val = input("Escolha: ")
            if validar_opcao(val, ["1", "2", "3"]):
                return int(val)
            print("Entrada inválida.")

    N = coletar_nivel("Nitrogênio (N)")
    P = coletar_nivel("Fósforo (P)")
    K = coletar_nivel("Potássio (K)")

    while True:
        ph = validar_float(input("\nInforme o pH do solo (0 a 14): "))
        if ph is not None and 0 <= ph <= 14:
            break
        print("Valor inválido.")

    while True:
        umidade = validar_float(input("Informe a umidade do solo (%): "))
        if umidade is not None and 0 <= umidade <= 100:
            break
        print("Valor inválido.")

    return {
        "cultura": cultura_nome,
        "parametros": cultura_param,
        "npk": (N, P, K),
        "ph": ph,
        "umidade": umidade
    }


# ---------------- INTELIGÊNCIA ---------------- #

def analisar_solo(d):
    rec = []

    cultura = d["cultura"]
    ph_min = d["parametros"]["ph_min"]
    ph_max = d["parametros"]["ph_max"]

    if d["umidade"] < 30:
        rec.append("⚠️ Solo seco → irrigação recomendada")
    elif d["umidade"] > 70:
        rec.append("⚠️ Solo muito úmido")
    else:
        rec.append("✅ Umidade adequada")

    nomes = ["Nitrogênio", "Fósforo", "Potássio"]
    for i, valor in enumerate(d["npk"]):
        if valor == 1:
            rec.append(f"⚠️ {nomes[i]} baixo")
        elif valor == 2:
            rec.append(f"⚠️ {nomes[i]} médio")
        else:
            rec.append(f"✅ {nomes[i]} adequado")

    if d["ph"] < ph_min:
        rec.append(f"⚠️ pH abaixo do ideal para {cultura}")
    elif d["ph"] > ph_max:
        rec.append(f"⚠️ pH acima do ideal para {cultura}")
    else:
        rec.append(f"✅ pH adequado para {cultura}")

    return rec


# ---------------- SALVAR ---------------- #

def salvar_dados(dado):
    try:
        with open(ARQUIVO, "r") as f:
            dados = json.load(f)
    except:
        dados = []

    dados.append(dado)

    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)


# ---------------- EXIBIR ---------------- #

def traduzir(valor):
    return {1: "BAIXO", 2: "MÉDIO", 3: "ALTO"}[valor]


def exibir_dados():
    try:
        with open(ARQUIVO, "r") as f:
            dados = json.load(f)

        print("\n=== HISTÓRICO AGRÍCOLA ===")

        for d in dados:
            N, P, K = d["npk"]

            print(
                f"\nCultura: {d['cultura']}\n"
                f"N: {traduzir(N)} | P: {traduzir(P)} | K: {traduzir(K)}\n"
                f"pH: {d['ph']} | Umidade: {d['umidade']}%"
            )

            print("🔎 Análise:")
            for r in analisar_solo(d):
                print(f"- {r}")

    except:
        print("Nenhum dado encontrado.")


# ---------------- MENU ---------------- #

def main():
    while True:
        print("\n=== SISTEMA DE GESTÃO AGRÍCOLA ===")
        print("1 - Inserir dados")
        print("2 - Ver histórico")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            dado = coletar_dados()
            salvar_dados(dado)

            print("\n📊 Resultado da análise:")
            for r in analisar_solo(dado):
                print(f"- {r}")

        elif opcao == "2":
            exibir_dados()

        elif opcao == "0":
            print("Encerrando sistema...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
