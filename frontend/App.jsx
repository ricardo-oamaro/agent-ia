import { useEffect, useMemo, useState } from 'react'
import { fetchNews } from './api'
import FilterBar from './components/FilterBar'
import NewsCard from './components/NewsCard'
import './index.css'

export default function App() {
  const [companies, setCompanies] = useState(['Nubank', 'Totvs', 'Stone'])
  const [items, setItems] = useState([])
  const [eventFilter, setEventFilter] = useState('Todos')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function load() {
    try {
      setLoading(true)
      setError('')
      const data = await fetchNews(companies)
      setItems(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const filtered = useMemo(() => {
    if (eventFilter === 'Todos') return items
    return items.filter(i => i.evento === eventFilter)
  }, [items, eventFilter])

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="mx-auto max-w-5xl px-4 py-8">
        <h1 className="text-2xl font-semibold tracking-tight">Market News Monitor</h1>
        <p className="mt-1 text-slate-600">Monitore eventos de empresas e filtre por tipo.</p>
      </header>

      <main className="mx-auto max-w-5xl px-4 pb-16">
        <div className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
          <FilterBar
            eventFilter={eventFilter}
            setEventFilter={setEventFilter}
            companies={companies}
            setCompanies={setCompanies}
            onRefresh={load}
          />
        </div>

        {loading && <div className="mt-6 text-slate-600">Carregando…</div>}
        {error && <div className="mt-6 text-red-600">{error}</div>}

        <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">
          {filtered.map((item, idx) => (
            <NewsCard key={idx} item={item} />
          ))}
        </div>

        {!loading && filtered.length === 0 && (
          <div className="mt-10 text-center text-slate-500">Nenhuma notícia encontrada com os filtros atuais.</div>
        )}
      </main>

      <footer className="mx-auto max-w-5xl px-4 py-10 text-xs text-slate-400">
        Feito com FastAPI, React e Tailwind.
      </footer>
    </div>
  )
}