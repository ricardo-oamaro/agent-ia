export default function FilterBar({ eventFilter, setEventFilter, companies, setCompanies, onRefresh }) {
  const eventOptions = ['Todos', 'Aquisição', 'Certificação', 'Lançamento de Produto', 'Outro']

  function handleCompaniesInput(e) {
    const value = e.target.value
    const list = value.split(',').map(s => s.trim()).filter(Boolean)
    setCompanies(list)
  }

  return (
    <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
      <div className="flex-1">
        <label className="block text-sm font-medium text-slate-700">Empresas (separadas por vírgula)</label>
        <input
          type="text"
          defaultValue={companies.join(', ')}
          onChange={handleCompaniesInput}
          className="mt-1 w-full rounded-xl border-slate-200 focus:border-indigo-500 focus:ring-indigo-500"
          placeholder="Nubank, Totvs, Stone"
        />
      </div>

      <div className="flex items-center gap-2">
        <label className="text-sm text-slate-700">Evento</label>
        <select
          value={eventFilter}
          onChange={(e) => setEventFilter(e.target.value)}
          className="rounded-xl border-slate-200 focus:border-indigo-500 focus:ring-indigo-500"
        >
          {eventOptions.map(o => <option key={o} value={o}>{o}</option>)}
        </select>
        <button
          onClick={onRefresh}
          className="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700"
        >
          Atualizar
        </button>
      </div>
    </div>
  )
}