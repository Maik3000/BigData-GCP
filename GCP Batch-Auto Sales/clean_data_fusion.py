import pandas as pd  

df = pd.read_csv("data/Auto Sales data.csv", quotechar='"', delimiter=",")  

print(df.shape)  # Debe imprimir (2550, 20)

# Reemplazar comas dentro de los valores de texto por otro carácter (ejemplo: punto y coma `;`)
df = df.applymap(lambda x: x.replace(",", ";") if isinstance(x, str) else x)

df_sample =df.head(10)
# Guardar el dataset limpio
df_sample.to_csv("data/subset_limpio.csv", index=False)
print("Archivo 'subset.csv' guardado con éxito.")
