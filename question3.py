import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn
from pathlib import Path

# frag the data in chunks between [min, max)
def frag_between(total_data: pd.DataFrame, data: pd.DataFrame, min_percentage: float, max_percentage: float):
    aux = data[data["Valor"] >= total_data["Valor"].quantile(min_percentage)]
    return len(aux[aux["Valor"] < total_data["Valor"].quantile(max_percentage)])


# frag the data in chunks
def frag(total_data: pd.DataFrame, data: pd.DataFrame, slices: int = 4):
    # Setting slices values
    limit = 1 / slices

    limits = list()
    i = 1
    while(limit * i < 1):
        limits.append(limit * i)
        i += 1

    # First
    labels = [f"{0:.2f}% - {limits[0]*100:.2f}%"]
    chunk = [len(data[data["Valor"] < total_data["Valor"].quantile(limits[0])])]

    # Intermediates
    for low_limit, high_limit in zip(limits[:-1],limits[1:]):
        labels.append(f"{low_limit*100:.2f}% - {high_limit*100:.2f}%")
        chunk.append(frag_between(total_data, data, low_limit, high_limit))

    # Final
    labels.append(f"{limits[-1]*100:.2f}% - {100:.2f}%")
    chunk.append(len(data[data["Valor"] >= total_data["Valor"].quantile(limits[-1])]))

    return {"Intervalo de valores": labels, "Quantidade de compras": chunk}


df = pd.read_json(Path.cwd() / "dados_compras.json")

# Total purchases
total_purchases = len(df)

# Min, max and mean prices
min_price = df['Valor'].min()
mean_price = df['Valor'].mean()
max_price = df['Valor'].max()


# Min and max products
df6 = df[["Nome do Item", "Valor"]].drop_duplicates()
df6 = df6.groupby("Valor").aggregate(lambda x: x)
min_price_products = df6.iloc[0]["Nome do Item"]
max_price_products = df6.iloc[-1]["Nome do Item"]

# Purchases by gender
df2 = None
total_solo_gender = dict()
for gender in df["Sexo"].unique():
    df_solo_gender = df[df["Sexo"].str.contains(gender)]

    total_solo_gender[gender] = len(df_solo_gender)

    slices = 9 # Using Sturge
    df2_solo_gender = frag(df, df_solo_gender, slices)
    df2_solo_gender["Sexo"] = [gender] * slices
    df2_solo_gender = pd.DataFrame(df2_solo_gender)

    if df2 is None:
        df2 = df2_solo_gender
    else:
        df2 = df2_solo_gender.merge(df2, how='outer')

sbn.barplot(df2, x="Intervalo de valores", y="Quantidade de compras", hue="Sexo", ).set(title="Distribuição de compras por gênero")
figure = plt.gcf() # get current figure
figure.set_size_inches(18, 10)
df2_path = Path.cwd() / "Gráfico de barras.png"
plt.savefig(df2_path, dpi=100)

# Clients by gender
df3 = df[["Sexo", "Login"]]
df3 = df3.groupby("Sexo").aggregate(lambda x: x.drop_duplicates('Login', keep='first').count())
df3.rename(columns={"Login": "Total de usuários"}, inplace=True)

# Total spent by gender
df4 = df.groupby("Sexo").aggregate({"Valor": "sum"})
df4.rename(columns={"Valor": "Total gasto"}, inplace=True)

print("Quantidade total de compras realizadas:", total_purchases)
print("")
print("Preço médio das compras:", "R${:0.2f}".format(mean_price))
print("Preço mínimo de compra:", "R${:0.2f}".format(min_price))
print("Preço máximo de compra:", "R${:0.2f}".format(max_price))
print("")
print("O(s) produto(s) mais caro(s):", end=" ")
if isinstance(max_price_products, str):
    print(max_price_products)
else:
    print(*max_price_products, sep=", ")
print("O(s) produto(s) mais barato(s):", end=" ")
if isinstance(min_price_products, str):
    print(min_price_products)
else:
    print(*min_price_products, sep=', ')
print("")
print("A distribuição de gênero:")
print(df3.to_string())
print("")
print("Gasto total por gênero:")
print(df4.to_string())
print("")
print(f"Gráfico de barras de compras por faixa de valor para cada gênero salvo em {df2_path}")