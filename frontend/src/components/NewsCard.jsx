function badgeColor(fonteType) {
  switch (fonteType) {
    case "google":
      return "bg-red-100 text-red-700";
    case "linkedin":
      return "bg-blue-100 text-blue-700";
    default:
      return "bg-gray-100 text-gray-700";
  }
}

export default function NewsCard({ item }) {
  return (
    <a href={item.url} target="_blank" rel="noreferrer" className="block">
      <div className="card">
        <div className="flex items-center justify-between gap-3">
          <div className="text-sm text-slate-500">{item.company}</div>
          <span className={`px-2 py-1 rounded text-xs font-medium ${badgeColor(item.fonte_type)}`}>
            {item.fonte}
          </span>
        </div>

        <p className="mt-2 text-slate-800">{item.title}</p>
        <p className="mt-1 text-slate-500 text-sm">{item.description}</p>
      </div>
    </a>
  );
}
