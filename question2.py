filmes = [
    {"titulo": "O Senhor dos Anéis", "ano": 2002, "avaliacao": 8.8},
    {"titulo": "Matrix", "ano": 1999, "avaliacao": 9.3},
    {"titulo": "Interestelar", "ano": 2014, "avaliacao": 8.6}
]

max_rating = filmes[0]
min_rating = filmes[0]
sum_rating = filmes[0]["avaliacao"]

for filme in filmes[1:]:
    sum_rating += filme["avaliacao"]
    if filme["avaliacao"] > max_rating["avaliacao"]:
        max_rating = filme
    elif filme["avaliacao"] < max_rating["avaliacao"]:
        min_rating = filme

average_rating = sum_rating / len(filmes)

print("A média das avaliações dos filmes:", average_rating)
print("O título do filme com a maior avaliação:", max_rating["titulo"])
print("O ano de lançamento do filme com a menor avaliação:", min_rating["ano"])