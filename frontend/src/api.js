const API_BASE = 'http://localhost:8000'

export async function fetchNews(companies) {
  const params = new URLSearchParams()
  companies.forEach(c => params.append('companies', c))
  const url = `${API_BASE}/news?${params.toString()}`
  const res = await fetch(url)
  if (!res.ok) throw new Error('Falha ao buscar notícias')
  return res.json()
}