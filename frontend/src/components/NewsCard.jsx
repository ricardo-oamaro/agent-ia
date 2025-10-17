function badgeClass(evento) {
    switch (evento) {
        case "Aquisição": return "badge badge-green";
        case "Certificação": return "badge badge-primary";
        case "Lançamento de Produto": return "badge badge-amber";
        default: return "badge badge-slate";
    }
}

// Mostra domínio + 20 chars do path e “...”
function formatUrl(url) {
    try {
        const u = new URL(url);
        const domain = u.hostname.replace(/^www\./, "");
        const path = u.pathname && u.pathname !== "/" ? u.pathname.slice(0, 20) : "";
        const ellipsis = u.pathname.length > 20 ? "..." : "";
        return `${domain}${path}${ellipsis}`;
    } catch {
        return "Fonte desconhecida";
    }
}

export default function NewsCard({ item }) {
    const href = item.fonte || item.url; // backend envia 'fonte'; se não, usa 'url'
    return (
        <a href={href} target="_blank" rel="noreferrer" className="block">
            <div className="card">
                <div className="flex items-center justify-between gap-3">
                    <div className="text-sm text-slate-500">{item.empresa}</div>
                    <span className={badgeClass(item.evento)}>{item.evento}</span>
                </div>

                <p
                    className="mt-2 text-slate-800"
                    dangerouslySetInnerHTML={{
                        __html: item.resumo
                            ?.replace(/<a[^>]*>(.*?)<\/a>/gi, "$1") // remove <a> tags, deixa só o texto
                            ?.replace(/<\/?[^>]+(>|$)/g, "")        // remove qualquer HTML remanescente
                    }}
                />

                <div className="mt-3 text-xs text-slate-400 underline">
                    {formatUrl(href)}
                </div>
            </div>
        </a>
    );
}
