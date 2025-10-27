# 🔑 Guia de Configuração do .env

Este guia explica como configurar as variáveis de ambiente opcionais para expandir as fontes de dados.

---

## 📋 Passo a Passo

### 1. Crie o arquivo `.env`

Na pasta `backend/`, crie um arquivo chamado `.env`:

```bash
cd backend
touch .env
```

### 2. Adicione as variáveis (opcional)

Copie e cole o conteúdo abaixo no arquivo `.env`:

```bash
# ==============================================================
# 🔑 Market News Monitor - Configurações de API (OPCIONAL)
# ==============================================================
# 
# O sistema funciona SEM nenhuma chave de API!
# As seguintes chaves são OPCIONAIS e aumentam as fontes de busca:
#

# ------------------------------------------------------------
# SerpAPI - Para buscar postagens do LinkedIn
# ------------------------------------------------------------
# Obtenha sua chave em: https://serpapi.com/
# SERP_API_KEY=sua_chave_serpapi_aqui

# ------------------------------------------------------------
# Bing News API - Para buscar notícias via Bing
# ------------------------------------------------------------
# Obtenha sua chave em: https://www.microsoft.com/en-us/bing/apis/bing-news-search-api
# BING_API_KEY=sua_chave_bing_aqui

# ------------------------------------------------------------
# OpenAI API - Para classificação inteligente com IA
# ------------------------------------------------------------
# Obtenha sua chave em: https://platform.openai.com/api-keys
# OPENAI_API_KEY=sua_chave_openai_aqui
```

### 3. Configure as chaves desejadas

Para ativar uma fonte, **remova o `#`** e substitua pela chave real:

**Exemplo:**
```bash
# ❌ Desativado (comentado)
# SERP_API_KEY=sua_chave_aqui

# ✅ Ativado
SERP_API_KEY=abc123def456ghi789
```

---

## 🔐 Como Obter as API Keys

### 🔗 SerpAPI (LinkedIn)

**Para que serve:** Buscar postagens oficiais das empresas no LinkedIn

**Custo:** 
- ✅ **Grátis:** 100 buscas/mês
- 💰 **Pago:** $50/mês para 5.000 buscas

**Como obter:**
1. Acesse [serpapi.com](https://serpapi.com/)
2. Clique em "Get Started Free"
3. Crie uma conta (GitHub, Google ou email)
4. Na dashboard, copie sua "API Key"
5. Cole no `.env`: `SERP_API_KEY=sua_chave_aqui`

---

### 🔵 Bing News API

**Para que serve:** Buscar notícias via Microsoft Bing News

**Custo:**
- ✅ **Grátis:** 1.000 transações/mês
- 💰 **S1:** $3 por 1.000 transações adicionais

**Como obter:**
1. Acesse [portal.azure.com](https://portal.azure.com/)
2. Crie uma conta Microsoft Azure (requer cartão, mas tem tier gratuito)
3. Crie um recurso "Bing Search v7"
4. Na página do recurso, vá em "Keys and Endpoint"
5. Copie a "Key 1" ou "Key 2"
6. Cole no `.env`: `BING_API_KEY=sua_chave_aqui`

---

### 🤖 OpenAI API

**Para que serve:** Classificação inteligente de notícias com GPT-4

**Custo:**
- 💰 **Pago:** ~$0.15 por 1000 notícias (modelo gpt-4o-mini)
- ⚠️ Não tem tier gratuito permanente (apenas créditos iniciais)

**Como obter:**
1. Acesse [platform.openai.com](https://platform.openai.com/)
2. Crie uma conta OpenAI
3. Adicione crédito (mínimo $5)
4. Vá em "API Keys"
5. Clique em "Create new secret key"
6. Copie a chave (não será mostrada novamente!)
7. Cole no `.env`: `OPENAI_API_KEY=sua_chave_aqui`

**Nota:** Esta feature está implementada mas comentada no código. Para ativar, descomente o código em `analyzer.py`.

---

## ✅ Testando a Configuração

Após configurar as chaves, teste se estão funcionando:

```bash
cd backend
python test_sources.py
```

Você verá um relatório como:

```
🧪 Testando: SerpAPI (LinkedIn)
✅ LinkedIn: 5 resultados encontrados

🧪 Testando: Bing News API  
✅ Bing News: 10 resultados encontrados
```

---

## 🔒 Segurança

### ⚠️ IMPORTANTE: Nunca faça commit do arquivo `.env`!

O arquivo `.env` deve estar no `.gitignore` para não expor suas chaves.

**Verifique se `.env` está ignorado:**
```bash
cat .gitignore | grep .env
```

Deve aparecer:
```
.env
*.env
```

### 🛡️ Boas Práticas

1. **Nunca compartilhe suas API keys publicamente**
2. **Regenere as chaves se forem expostas acidentalmente**
3. **Use variáveis de ambiente em produção** (não arquivos .env)
4. **Configure limites de uso** nas dashboards das APIs
5. **Monitore o uso mensal** para evitar cobranças inesperadas

---

## 🆘 Troubleshooting

### Erro: "SERP_API_KEY não configurada"
- ✅ Verifique se o arquivo `.env` existe na pasta `backend/`
- ✅ Verifique se não há espaços antes/depois do `=`
- ✅ Verifique se a linha não está comentada (sem `#`)

### Erro: "Invalid API Key"
- ✅ Verifique se copiou a chave completa
- ✅ Teste a chave no site da API
- ✅ Verifique se a conta não foi suspensa por falta de pagamento

### Erro: "Rate limit exceeded"
- ✅ Você excedeu o limite gratuito do mês
- ✅ Aguarde o reset mensal ou faça upgrade do plano

---

## 📊 Resumo de Fontes

| Fonte | Requer .env? | Grátis? | Qualidade |
|-------|-------------|---------|-----------|
| Google News | ❌ Não | ✅ | ⭐⭐⭐⭐⭐ |
| G1 Globo | ❌ Não | ✅ | ⭐⭐⭐⭐⭐ |
| InfoMoney | ❌ Não | ✅ | ⭐⭐⭐⭐ |
| UOL Economia | ❌ Não | ✅ | ⭐⭐⭐⭐ |
| Reuters | ❌ Não | ✅ | ⭐⭐⭐⭐⭐ |
| Yahoo Finance | ❌ Não | ✅ | ⭐⭐⭐⭐ |
| DuckDuckGo | ❌ Não | ✅ | ⭐⭐⭐ |
| **LinkedIn** | ✅ Sim | ⚠️ Limitado | ⭐⭐⭐⭐ |
| **Bing News** | ✅ Sim | ⚠️ Limitado | ⭐⭐⭐⭐ |

**Resultado:** 7 fontes funcionam sem configuração! 🎉

---

## 💡 Dicas

- **Economize suas requisições:** Use as APIs pagas apenas quando as gratuitas não forem suficientes
- **Cache local:** Considere implementar cache para reduzir chamadas de API
- **Priorize fontes:** Google News + G1 + InfoMoney já cobrem bem o mercado brasileiro

---

**Precisa de ajuda?** Abra uma issue no GitHub!

**Última atualização:** Outubro 2025

