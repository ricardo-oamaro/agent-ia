// src/components/NewsCard.jsx
import React from "react";

// 🔹 Define as cores de badge por tipo de fonte
function badgeColor(type) {
    switch (type) {
        case "google":
            return "bg-blue-100 text-blue-700";
        case "linkedin":
            return "bg-indigo-100 text-indigo-700";
        default:
            return "bg-gray-100 text-gray-600";
    }
}

// 🔹 Formata "Publicado há X tempo"
function timeAgo(publishedAt) {
    if (!publishedAt) return "";
    try {
        // publishedAt vem no formato "dd/mm/yyyy HH:MM"
        const [date, time] = publishedAt.split(" ");
        const [day, month, year] = date.split("/").map(Number);
        const [hour, minute] = time.split(":").map(Number);

        const pubDate = new Date(year, month - 1, day, hour, minute);
        const now = new Date();
        const diffMs = now - pubDate;

        const diffMinutes = Math.floor(diffMs / (1000 * 60));
        const diffHours = Math.floor(diffMinutes / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffMinutes < 60) return `há ${diffMinutes} min`;
        if (diffHours < 24) return `há ${diffHours} h`;
        if (diffDays === 1) return "há 1 dia";
        if (diffDays < 7) return `há ${diffDays} dias`;

        return pubDate.toLocaleDateString("pt-BR", {
            day: "2-digit",
            month: "short",
            year: "numeric",
        });
    } catch {
        return publishedAt;
    }
}

export default function NewsCard({ item }) {
    return (
        <a
            href={item.url}
            target="_blank"
            rel="noreferrer"
            className="block hover:scale-[1.01] transition-transform"
        >
            <div className="card">
                {/* 🔹 Cabeçalho: Empresa + Badge */}
                <div className="flex items-center justify-between gap-3">
                    <div className="text-sm text-slate-500 font-medium">{item.company}</div>
                    <span
                        className={`px-2 py-1 rounded text-xs font-medium ${badgeColor(item.fonte_type)}`}
                    >
                        {item.fonte}
                    </span>
                </div>

                {/* 🔹 Título e Descrição */}
                <p className="mt-2 text-slate-800 font-semibold leading-snug">{item.title}</p>
                <p className="mt-1 text-slate-600 text-sm line-clamp-2">{item.description}</p>

                {/* 🔹 Rodapé: data + origem */}
                <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
                    <span>{item.published_at ? `🕒 ${timeAgo(item.published_at)}` : ""}</span>
                    <span>
                        📎{" "}
                        {item.fonte_type === "google"
                            ? "Google News"
                            : item.fonte_type === "linkedin"
                            ? "LinkedIn"
                            : "Fonte desconhecida"}
                    </span>
                </div>
            </div>
        </a>
    );
}
