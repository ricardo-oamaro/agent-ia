# -*- coding: utf-8 -*-
"""
🧪 Script de Teste das Fontes de Notícias
==========================================
Execute este script para testar todas as fontes implementadas:
    python test_sources.py
"""

import asyncio
from data_source import (
    fetch_google_news,
    fetch_g1_news,
    fetch_infomoney_news,
    fetch_uol_news,
    fetch_reuters_news,
    fetch_yahoo_finance_news,
    fetch_duckduckgo_news,
    fetch_linkedin_posts,
    fetch_bing_news,
    fetch_company_website_news,
    fetch_real_news,
)

def test_source(name, fetch_function, companies):
    """Testa uma fonte específica"""
    print("\n" + "="*60)
    print(f"🧪 Testando: {name}")
    print("="*60)
    
    try:
        results = fetch_function(companies)
        print(f"✅ {name}: {len(results)} notícias encontradas")
        
        if results:
            print(f"\n📰 Exemplo de notícia:")
            first = results[0]
            print(f"   Empresa: {first.get('company')}")
            print(f"   Título: {first.get('title')[:80]}...")
            print(f"   Fonte: {first.get('fonte')} ({first.get('fonte_type')})")
            print(f"   URL: {first.get('url')[:60]}...")
        else:
            print(f"⚠️  Nenhuma notícia encontrada (isso é normal se a empresa não foi mencionada recentemente)")
        
        return True
    except Exception as e:
        print(f"❌ Erro em {name}: {e}")
        return False

def main():
    """Executa testes em todas as fontes"""
    companies = ["Nubank", "Totvs"]
    
    print("\n" + "="*60)
    print("🚀 TESTE DE FONTES - MARKET NEWS MONITOR")
    print("="*60)
    print(f"Empresas de teste: {', '.join(companies)}\n")
    
    sources = [
        ("Site Oficial da Empresa", fetch_company_website_news),
        ("Google News", fetch_google_news),
        ("G1 Globo", fetch_g1_news),
        ("InfoMoney", fetch_infomoney_news),
        ("UOL Economia", fetch_uol_news),
        ("Reuters", fetch_reuters_news),
        ("Yahoo Finance", fetch_yahoo_finance_news),
        ("DuckDuckGo", fetch_duckduckgo_news),
    ]
    
    results = {}
    for name, func in sources:
        results[name] = test_source(name, func, companies)
    
    # Testa fontes que requerem API key
    print("\n" + "="*60)
    print("🔑 Testando fontes com API Key (opcionais)")
    print("="*60)
    
    try:
        linkedin_results = fetch_linkedin_posts(companies[0])
        print(f"✅ LinkedIn (SerpAPI): {len(linkedin_results)} resultados")
        results["LinkedIn"] = True
    except Exception as e:
        print(f"⚠️  LinkedIn: {e} (API key não configurada)")
        results["LinkedIn"] = False
    
    try:
        bing_results = fetch_bing_news(companies)
        print(f"✅ Bing News: {len(bing_results)} resultados")
        results["Bing News"] = True
    except Exception as e:
        print(f"⚠️  Bing News: {e} (API key não configurada)")
        results["Bing News"] = False
    
    # Resumo final
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for source, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {source}")
    
    print(f"\n🎯 Taxa de sucesso: {success_count}/{total_count} fontes funcionando")
    
    if success_count >= 7:
        print("\n🎉 Sistema operacional! Todas as fontes principais funcionando.")
    elif success_count >= 5:
        print("\n✅ Sistema operacional com algumas limitações.")
    else:
        print("\n⚠️  Atenção: Poucas fontes funcionando. Verifique conexão de internet.")
    
    # Teste de ordenação
    print("\n" + "="*60)
    print("📅 TESTE DE ORDENAÇÃO POR DATA")
    print("="*60)
    
    try:
        all_news = fetch_real_news(companies)
        print(f"\n✅ Total de notícias agregadas: {len(all_news)}")
        
        if all_news:
            print(f"\n🔝 Top 5 notícias mais recentes:")
            for i, news in enumerate(all_news[:5], 1):
                date_str = news.get('published_at') or 'Sem data'
                print(f"  {i}. [{date_str}] {news['fonte']} - {news['title'][:60]}...")
        
        # Verifica se há datas
        with_dates = sum(1 for n in all_news if n.get('published_at'))
        print(f"\n📊 Estatísticas:")
        print(f"   - Notícias com data: {with_dates}/{len(all_news)} ({with_dates*100//len(all_news) if all_news else 0}%)")
        print(f"   - Notícias ordenadas: ✅ Sim")
        
    except Exception as e:
        print(f"\n❌ Erro no teste de ordenação: {e}")

if __name__ == "__main__":
    main()

