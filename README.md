# DivulgaCidades - Resultados Eleitorais por Município

Este é um sistema web responsivo e esteticamente premium para consulta de resultados eleitorais no Brasil. Ele permite buscar resultados para qualquer Estado e Cidade, exibindo de forma clara os dados de Prefeito e Vice, Vereadores, Senadores, Deputados Estaduais e Federais.

---

## 🎨 Principais Recursos

1. **Design de Alto Nível (Glassmorphism)**: Estilo visual em modo escuro usando fundos semitransparentes desvanecidos, bordas com gradientes luminosos e micro-interações suaves para dar uma sensação moderna e fluida.
2. **Seleção de Cidades Inteligente (Combobox Autocomplete)**: Em vez de dropdowns tradicionais lentos, os campos de Estado e Cidade funcionam com autocompletar inteligente que filtra resultados enquanto você digita.
3. **Busca e Filtro nos Resultados**: Uma barra de pesquisa rápida permite filtrar os candidatos de qualquer cargo na aba ativa instantaneamente por nome ou partido.
4. **Detalhes do Candidato em Modal**: Clicar em qualquer candidato abre um modal interativo com informações completas (número de urna, percentual de votos válidos, coligação, situação, etc.).
5. **Dados de Amostra Reais (Showcases)**: Dados reais de 2024 para Prefeito e Vereadores, e 2022 para Senadores e Deputados para as cidades de **São Paulo (SP)** e **Rio de Janeiro (RJ)**.
6. **Motor Procedural Baseado em Semente (Seed-Based Generator)**: Para todas as outras 5.568 cidades do Brasil, um algoritmo determinístico cria candidatos fictícios baseados em dados de semente únicos (nome do município + sigla do estado). Desta forma, a votação e os nomes de uma cidade serão **sempre consistentes** e idênticos a cada carregamento, simulando um banco de dados global gigante sem impacto na performance de rede.

---

## 📁 Estrutura de Arquivos

- `index.html`: Estrutura semântica e esqueleto do Dashboard.
- `styles.css`: Estilização e design responsivo, incluindo variáveis de cor, transições e efeitos vidro.
- `data.js`: Base de dados contendo listas geográficas, dados reais de SP/RJ e o motor de geração procedural.
- `app.js`: Comportamento lógico dos seletores, abas de navegação, pesquisa em tempo real e modais de detalhe.

---

## 🚀 Como Executar Localmente

Como a aplicação foi construída utilizando tecnologias web nativas (HTML5, Vanilla CSS e Vanilla JS), **não há necessidade de instalar dependências complexas** (Node.js, Webpack, etc.).

Você pode abri-la de duas formas simples:

### Opção 1: Abertura Direta
Basta dar um duplo clique no arquivo `index.html` para abri-lo diretamente em qualquer navegador moderno.

### Opção 2: Servidor Local Simples (Recomendado)
Para garantir o perfeito funcionamento de todos os recursos do navegador, você pode rodar um servidor de desenvolvimento leve.

Se você tem o **Python** instalado:
```bash
python -m http.server 8000
```
Depois acesse `http://localhost:8000` no seu navegador.

Ou usando o **Node.js**:
```bash
npx live-server
```
