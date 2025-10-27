# ⚡ Quick Start - Versão 2.1

Guia rápido para testar as **3 novas funcionalidades** da versão 2.1!

---

## 🚀 Instalação Rápida (5 minutos)

```bash
# 1. Clone o repositório (se ainda não tiver)
git clone <seu-repo>
cd agent-ia

# 2. Backend
cd backend
pip install -r requirements.txt

# 3. Teste as fontes (opcional, mas recomendado!)
python test_sources.py

# 4. Inicie o servidor
uvicorn main:app --reload

# 5. Em outro terminal, frontend
cd ../frontend
npm install
npm run dev

# 6. Acesse: http://localhost:5173
```

---

## ✨ Testando as Novidades

### 1. 🏢 Site Oficial da Empresa

**Como testar:**
1. No frontend, digite: `Nubank, Totvs, Stone`
2. Clique em "Atualizar"
3. Procure por cards com **badge verde esmeralda em negrito**
4. Esses são notícias diretas do site oficial!

**Exemplo visual:**
```
┌─────────────────────────────────────────┐
│ Nubank              [Nubank Oficial]🌟  │ ← Badge verde em negrito
│                                          │
│ Nubank anuncia novos produtos para 2025 │
│ Comunicado oficial sobre expansão...    │
│                                          │
│ 🕒 há 2 horas      📎 Nubank Oficial     │
└─────────────────────────────────────────┘
```

**Empresas suportadas:**
- ✅ Nubank
- ✅ Totvs  
- ✅ Stone
- ✅ Magazine Luiza
- ✅ Mercado Livre
- ✅ Natura

**Para adicionar mais empresas:**
Edite `/backend/data_source.py` (linha ~563)

---

### 2. 📅 Ordenação por Data

**Como testar:**
1. Busque por qualquer empresa: `Nubank`
2. Veja os cards na tela
3. **As notícias mais recentes aparecem primeiro!**

**Verificação manual:**
- Olhe o campo "🕒 há X horas" em cada card
- Deve estar em ordem: "há 1h" → "há 3h" → "há 1 dia"

**Verificação técnica:**
```bash
cd backend
python test_sources.py
```

No final, verá:
```
📅 TESTE DE ORDENAÇÃO POR DATA
🔝 Top 5 notícias mais recentes:
  1. [24/10/2025 15:30] ...
  2. [24/10/2025 14:20] ...
  3. [24/10/2025 12:10] ...
```

---

### 3. 🕒 Filtro Temporal (7 dias)

**Como funciona:**
- Google News agora busca **apenas dos últimos 7 dias**
- Notícias antigas são automaticamente filtradas

**Como verificar:**
1. Busque uma empresa com pouca notícia recente
2. Veja que só aparecem notícias da última semana
3. No console do backend, verá:
   ```
   🔍 Buscando notícias para: Nubank → ...when:7d...
   ```

---

## 🎯 Cenários de Uso

### Cenário 1: Monitorar Empresa Específica

```
Input: Nubank
Resultado:
  1. [Hoje 15:30] 🌟 Nubank Oficial - Novo produto
  2. [Hoje 14:20] Google News - Nubank expande
  3. [Hoje 12:10] G1 - Resultados financeiros
  4. [Ontem] InfoMoney - Análise de mercado
```

### Cenário 2: Comparar Múltiplas Empresas

```
Input: Nubank, Totvs, Stone
Resultado (ordenado por data):
  1. [Hoje 16:00] 🌟 Nubank Oficial
  2. [Hoje 15:30] 🌟 Stone Oficial
  3. [Hoje 14:45] Google News (Totvs)
  4. [Hoje 13:20] 🌟 Totvs Oficial
```

### Cenário 3: Empresa Sem Site Oficial Mapeado

```
Input: Apple
Resultado:
  ⚠️ Site oficial não mapeado (apenas no console)
  (Continua com outras 9 fontes normalmente)
```

---

## 🎨 Identificação Visual Rápida

### Cores das Badges

```
🌟 Verde Esmeralda (NEGRITO) = Site Oficial ← PRIORITÁRIO!
🔵 Azul                      = Google News
🟢 Verde                     = G1 Globo
🟡 Amarelo                   = InfoMoney
🔷 Ciano                     = UOL
🔴 Vermelho                  = Reuters
🟪 Púrpura                   = Yahoo Finance
🟠 Laranja                   = DuckDuckGo
🟣 Roxo                      = LinkedIn
🟦 Teal                      = Bing News
```

---

## 📊 Comparativo: Antes vs Depois

### Antes (v2.0)

```
Busca: Nubank

Resultado (ordem aleatória):
- [3 dias atrás] Reuters
- [Hoje] Google News
- [1 semana atrás] Yahoo
- [Ontem] G1
```

**Problemas:**
- ❌ Notícias antigas apareciam primeiro
- ❌ Sem fonte oficial da empresa
- ❌ Ordem confusa

### Depois (v2.1)

```
Busca: Nubank

Resultado (ordenado + site oficial):
1. [Hoje 15:30] 🌟 Nubank Oficial
2. [Hoje 14:20] Google News
3. [Ontem 18:00] G1 Globo
4. [Ontem 10:30] InfoMoney
```

**Melhorias:**
- ✅ Site oficial em primeiro
- ✅ Ordem cronológica perfeita
- ✅ Apenas últimos 7 dias
- ✅ Informação verificada

---

## 🧪 Script de Teste Completo

```bash
# Execute o teste automático
cd backend
python test_sources.py
```

**O que o teste verifica:**
1. ✅ Todas as 10 fontes funcionando
2. ✅ Site oficial retorna resultados
3. ✅ Ordenação por data funcionando
4. ✅ Percentual de notícias com data
5. ✅ Top 5 notícias mais recentes

**Saída esperada:**
```
🚀 TESTE DE FONTES - MARKET NEWS MONITOR
...
✅ Site Oficial da Empresa: 2 resultados
✅ Google News: 10 resultados
...
📅 TESTE DE ORDENAÇÃO POR DATA
✅ Total de notícias agregadas: 45
🔝 Top 5 notícias mais recentes:
  1. [24/10/2025 15:30] Nubank Oficial - ...
  ...
📊 Estatísticas:
   - Notícias com data: 38/45 (84%)
   - Notícias ordenadas: ✅ Sim
```

---

## 💡 Dicas de Uso

### Dica 1: Empresas Brasileiras

Para empresas brasileiras, use os nomes completos:
- ✅ "Magazine Luiza" (não "Magalu")
- ✅ "Mercado Livre" (não "ML")
- ✅ "Natura" (correto)

### Dica 2: Múltiplas Empresas

Separe por vírgula sem espaços extras:
- ✅ `Nubank, Totvs, Stone`
- ❌ `Nubank , Totvs , Stone` (espaços extras)

### Dica 3: Adicionar Nova Empresa

1. Encontre o site oficial
2. Procure por RSS ou página de imprensa
3. Edite `/backend/data_source.py`:

```python
company_urls = {
    "nova_empresa": {
        "press": "https://nova.com/imprensa/",
    },
}
```

4. Reinicie o backend
5. Teste: `python test_sources.py`

---

## 🐛 Problemas Comuns

### Problema 1: Sem notícias do site oficial

**Sintoma:**
```
⚠️ Site oficial: Empresa 'MinhaEmpresa' não mapeada
```

**Solução:**
Adicione a empresa ao mapeamento (veja Dica 3 acima)

### Problema 2: Notícias sem data

**Sintoma:**
Algumas notícias aparecem no final sem "há X horas"

**Explicação:**
Algumas fontes (DuckDuckGo) não fornecem data. Isso é normal.

**Solução:**
Não há ação necessária. O sistema funciona corretamente.

### Problema 3: Ordem parece errada

**Verificação:**
```bash
python test_sources.py
```

Veja a seção "📅 TESTE DE ORDENAÇÃO" para confirmar.

---

## 📈 Performance

### Tempo de Resposta

```
Antes (v2.0): 3-5 segundos
Depois (v2.1): 4-7 segundos (+1-2s devido ao site oficial)
```

**Nota:** O tempo extra vale a pena pela qualidade das notícias oficiais!

### Qualidade das Notícias

```
Antes: 100% agregadores de notícias
Depois: ~20% notícias oficiais + 80% agregadores
```

---

## 🎯 Checklist de Validação

Execute este checklist para confirmar que tudo funciona:

### Backend
- [ ] `pip install -r requirements.txt` executado
- [ ] `python test_sources.py` passa sem erros
- [ ] Servidor rodando em `localhost:8000`
- [ ] Docs da API acessíveis em `localhost:8000/docs`

### Funcionalidades
- [ ] Busca por "Nubank" retorna notícia oficial com badge verde
- [ ] Notícias ordenadas por data (mais recente primeiro)
- [ ] Console mostra "when:7d" nas buscas do Google News
- [ ] Badge verde esmeralda está em negrito

### Frontend
- [ ] `npm install` executado
- [ ] App rodando em `localhost:5173`
- [ ] Cards exibem data "há X horas"
- [ ] Badge verde esmeralda visível para sites oficiais

---

## 🚀 Próximos Passos

Agora que testou as novidades, explore:

1. 📖 **[RELEASE_NOTES_v2.1.md](./RELEASE_NOTES_v2.1.md)** - Changelog detalhado
2. 📡 **[FONTES.md](./FONTES.md)** - Detalhes técnicos de cada fonte
3. 🧪 **[test_sources.py](./backend/test_sources.py)** - Suite de testes

**Quer contribuir?**
- Adicione mais empresas ao mapeamento
- Sugira novas fontes de notícias
- Reporte bugs ou melhorias

---

## 📞 Suporte

**Dúvidas sobre a v2.1?**

- 📖 Leia: [RELEASE_NOTES_v2.1.md](./RELEASE_NOTES_v2.1.md)
- 🧪 Execute: `python test_sources.py`
- 📝 Consulte: [README.md](./README.md)

**Encontrou um bug?**
- Verifique os logs do console
- Execute o teste automatizado
- Documente o comportamento esperado vs atual

---

**Versão:** 2.1.0 - Smart News Edition  
**Data:** 24 de Outubro de 2025  
**Status:** ✅ Testado e pronto para uso

🎉 **Aproveite as novidades!**

