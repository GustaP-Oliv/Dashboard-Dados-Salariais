import pandas as pd
import streamlit as st

# Título
st.title("📊 Dados Salariais")

# Carregar dados
df = pd.read_csv("Salary_Data.csv")

# Mostrar tabela
st.subheader("📂 Dados brutos")
st.dataframe(df)

# =============================
# 1. 📌 ESTATÍSTICAS BÁSICAS
# =============================

st.subheader("📈 Estatísticas Básicas")

# Idade
st.write("**Sobre as Idades**")
st.write(f"Idade Média: {df['Age'].mean():.2f}")
st.write(f"Mediana das idades: {df['Age'].median():.2f}")
st.write(f"Idade Mínima: {df['Age'].min()}")
st.write(f"Idade Máxima: {df['Age'].max()}")

# Salário
st.write("**Sobre os Salários**")
st.write(f"Média Salarial: {df['Salary'].mean():.2f}")
st.write(f"Mediana Salarial: {df['Salary'].median():.2f}")
st.write(f"Desvio Padrão Salarial: {df['Salary'].std():.2f}")
st.write(f"Menor Salário: {df['Salary'].min()}")
st.write(f"Maior Salário: {df['Salary'].max()}")

# Salário médio por gênero
st.write("**Salário Médio por Gênero**")
st.write(df.groupby("Gender")["Salary"].mean())

# Salário médio por nível de escolaridade
st.write("**Salário Médio por Nível de Escolaridade**")
st.write(df.groupby("Education Level")["Salary"].mean())

# --- Gráfico de barras do salário médio por nível de escolaridade ---
import matplotlib.pyplot as plt
import seaborn as sns

# Cria a figura e o tamanho
plt.figure(figsize=(10,6))

# Cria o gráfico de barras
sns.barplot(
    x="Education Level", 
    y="Salary", 
    data=df, 
    estimator=lambda x: x.mean(),   # usa média como estatística
    ci=None                        # remove as barras de erro
)

# 🔹 Ajustes de visualização
plt.title("Média Salarial por Nível de Escolaridade", fontsize=14, fontweight='bold')
plt.xlabel("Nível de Escolaridade", fontsize=12)
plt.ylabel("Salário Médio (R$)", fontsize=12)
plt.xticks(rotation=45)     # Gira os rótulos do eixo X
plt.tight_layout()          # Ajusta o layout para evitar sobreposição

# Exibe o gráfico no Streamlit
st.pyplot(plt)

# Salário médio por cargo
st.write("**Top 10 Cargos mais bem pagos (média salarial)**")
st.write(df.groupby("Job Title")["Salary"].mean().sort_values(ascending=False).head(10))

# =============================
import matplotlib.pyplot as plt
import seaborn as sns

# =============================
# 2. 📌 GRÁFICOS
# =============================

st.subheader("📊 Visualizações de Dados")

# 1. Distribuição das idades
st.write("### Distribuição das Idades")
fig, ax = plt.subplots()
sns.histplot(df['Age'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# 2. Distribuição dos salários
st.write("### Distribuição dos Salários")
fig, ax = plt.subplots()
sns.histplot(df['Salary'], bins=30, kde=True, ax=ax, color="green")
st.pyplot(fig)

# 3. Salário médio por gênero (gráfico de barras)
st.write("### Salário Médio por Gênero")
fig, ax = plt.subplots()
sns.barplot(x="Gender", y="Salary", data=df, estimator=lambda x: sum(x)/len(x), ax=ax)
st.pyplot(fig)

# 4. Salário médio por nível de escolaridade
st.write("### Salário Médio por Nível de Escolaridade")
fig, ax = plt.subplots()
sns.barplot(x="Education Level", y="Salary", data=df, ax=ax, order=df["Education Level"].unique())
st.pyplot(fig)

# 5. Relação entre anos de experiência e salário
st.write("### Salário x Anos de Experiência")
fig, ax = plt.subplots()
sns.scatterplot(x="Years of Experience", y="Salary", data=df, hue="Gender", ax=ax)
st.pyplot(fig)


# -------------------------
# 3. FILTROS INTERATIVOS
# -------------------------

st.subheader("🎯 Filtros")

# Filtro por gênero
generos = df["Gender"].unique()  # pega os valores únicos da coluna Gender
genero_escolhido = st.multiselect("Selecione o gênero:", generos, default=generos)

# Filtro por nível educacional
educacao = df["Education Level"].unique()
educacao_escolhida = st.multiselect("Selecione o nível de educação:", educacao, default=educacao)

# Filtro por cargo (Job Title)
cargos = df["Job Title"].unique()
cargo_escolhido = st.multiselect("Selecione o cargo:", cargos, default=cargos)

# -------------------------
# 4. FILTRO POR PALAVRA-CHAVE
# -------------------------
st.subheader("🔍 Busca por palavra-chave")
busca = st.text_input("Digite um termo para buscar (ex: 'Engineer', 'Manager', 'PhD'):")

# -------------------------
# 5. APLICAR FILTROS
# -------------------------
df_filtrado = df[
    (df["Gender"].isin(genero_escolhido)) &
    (df["Education Level"].isin(educacao_escolhida)) &
    (df["Job Title"].isin(cargo_escolhido))
]

# Aplicar busca (se tiver texto digitado)
if busca:
    df_filtrado = df_filtrado[df_filtrado.apply(lambda row: row.astype(str).str.contains(busca, case=False).any(), axis=1)]

# -------------------------
# 6. MOSTRAR RESULTADOS FILTRADOS
# -------------------------
st.subheader("📋 Dados filtrados")
st.dataframe(df_filtrado)

#==================================================================================================================================================================
# AQUI JÁ É UMA SEGUNDA PARTE, ONDE EU INCLUÍ MAIS CÓDIGOS DE ANÁLISE, A MEDIDA EM QUE EU IA PENSANDO EM MAIS ANÁLISES A SEREM INCLUÍDAS PARA MELHORAR O DASHBOARD.
#==================================================================================================================================================================

# --------------------------
# 7. ESTATÍSTICAS ADICIONAIS
# --------------------------

st.subheader("📊 Estatísticas Descritivas")

# Mostra estatísticas básicas (contagem, média, desvio padrão, min, max, quartis)
st.write("Resumo estatístico das colunas numéricas:")
st.write(df.describe())

# Estatísticas personalizadas
st.write("🔹 Estatísticas personalizadas:")

# Exemplo: média de uma coluna (substitua 'coluna_numerica' pelo nome da sua tabela)
if "coluna_numerica" in df.columns:
    media = df["coluna_numerica"].mean()
    mediana = df["coluna_numerica"].median()
    desvio = df["coluna_numerica"].std()

    st.metric("Média", f"{media:.2f}")
    st.metric("Mediana", f"{mediana:.2f}")
    st.metric("Desvio Padrão", f"{desvio:.2f}")

# --------------------------
# 8. ADIÇÃO DE MAIS GRÁFICOS
# --------------------------
st.subheader("📈 Visualização dos Dados")

# Histograma (distribuição de valores de uma coluna)
if "coluna_numerica" in df.columns:
    st.write("Distribuição de valores:")
    fig, ax = plt.subplots()
    sns.histplot(df["coluna_numerica"], kde=True, ax=ax)
    st.pyplot(fig)

# Gráfico de barras (frequência de valores em uma coluna categórica)
if "coluna_categorica" in df.columns:
    st.write("Frequência de categorias:")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="coluna_categorica", ax=ax)
    plt.xticks(rotation=45)  # gira rótulos para melhor leitura
    st.pyplot(fig)

# Boxplot (detectar outliers)
if "coluna_numerica" in df.columns and "coluna_categorica" in df.columns:
    st.write("Boxplot por categoria:")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="coluna_categorica", y="coluna_numerica", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ---------------------------------
# 9. FILTROS INTERATIVOS ADICIONAIS
# ---------------------------------
st.subheader("🎛️ Filtros Interativos")

# Selecionar coluna numérica para análise
colunas_numericas = df.select_dtypes(include="number").columns.tolist()
coluna_escolhida = st.selectbox("Escolha uma coluna numérica:", colunas_numericas)

if coluna_escolhida:
    # Slider para escolher intervalo de valores
    min_val = float(df[coluna_escolhida].min())
    max_val = float(df[coluna_escolhida].max())
    faixa = st.slider("Selecione o intervalo de valores:",
                      min_value=min_val, max_value=max_val,
                      value=(min_val, max_val))

    df_filtrado = df[(df[coluna_escolhida] >= faixa[0]) & (df[coluna_escolhida] <= faixa[1])]
    st.write("Tabela filtrada:")
    st.dataframe(df_filtrado)

    # Gráfico do filtro aplicado
    fig, ax = plt.subplots()
    sns.histplot(df_filtrado[coluna_escolhida], kde=True, ax=ax)
    st.pyplot(fig)

# --------------------------
# 10.EXPLORAÇÃO AVANÇADA
# --------------------------
st.subheader("🔍 Busca avançada")

# Escolher coluna para pesquisar
coluna_pesquisa = st.selectbox("Escolha uma coluna para pesquisar:", df.columns)

# Campo de texto para buscar palavra-chave ou número
busca = st.text_input("Digite o termo para buscar:")

if busca:
    df_busca = df[df[coluna_pesquisa].astype(str).str.contains(busca, case=False, na=False)]
    st.write(f"Resultados para '{busca}':")
    st.dataframe(df_busca)

    # Exportar CSV filtrado
    csv = df_busca.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar resultados filtrados", data=csv, file_name="dados_filtrados.csv", mime="text/csv")