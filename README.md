
# 📊 Streamlit RFV – Análise e Segmentação de Clientes

Este projeto é um painel interativo desenvolvido em **Streamlit** que aplica a metodologia **RFV (Recência, Frequência, Valor)** para análise e segmentação de clientes com base no comportamento de compra.

---

## 🚀 Acesse o App Online

🔗 [https://streamlit-rfv-an-lise.onrender.com](https://streamlit-rfv-an-lise.onrender.com)

---

## 🎯 Objetivo

Permitir que empresas e analistas visualizem e segmentem sua base de clientes de forma simples e eficaz, com sugestões automáticas de ações estratégicas para cada grupo (ex: fidelizar, recuperar, reengajar).

---

## 🧠 O que é RFV?

- **Recência (R)** – Quantos dias se passaram desde a última compra.
- **Frequência (F)** – Quantas compras o cliente realizou.
- **Valor (V)** – Quanto ele gastou no total.

Cada cliente recebe uma classificação do tipo `RFV Score` (ex: AAA, DDD, ABC), e o sistema sugere ações de marketing com base nesses perfis.

---

## ⚙️ Funcionalidades

✅ Upload de arquivos `.csv` ou `.xlsx` com histórico de compras  
✅ Cálculo automático dos indicadores RFV  
✅ Classificação dos clientes em quartis (A, B, C, D)  
✅ Geração do **RFV Score** (ex: ABC, DAA, AAA etc)  
✅ Sugestões de ações de marketing para cada grupo  
✅ Filtro interativo por grupo RFV  
✅ Exportação em Excel com todos os resultados  
✅ Gráfico com distribuição dos perfis

---

## 📁 Exemplo de entrada

O sistema espera um arquivo com as colunas abaixo:

| ID_cliente | DiaCompra   | CodigoCompra | ValorTotal |
|------------|-------------|--------------|-------------|
| 101        | 2023-01-01  | A0001        | 120.00      |
| 102        | 2023-01-02  | A0002        | 240.50      |

Um exemplo pode ser encontrado em:  
📄 [`clientes_compras_exemplo.csv`](./clientes_compras_exemplo.csv)

---

## 📦 Instalação local (opcional)

Clone o projeto:

```bash
git clone https://github.com/Barbo541/Streamlit-RFV-An-lise-.git
cd Streamlit-RFV-An-lise-
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o app:

```bash
streamlit run Streamlit-RFV.py
```

---

## 🛠️ Tecnologias utilizadas

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [XlsxWriter](https://xlsxwriter.readthedocs.io/)

---

## 👤 Autor

**[@Barbo541](https://github.com/Barbo541)**  
Desenvolvido como parte de portfólio de Arquiteto de Dados com foco em aplicações reais de negócio.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
