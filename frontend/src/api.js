const API_BASE_URL = "http://localhost:8000";

export async function fetchNews(companies) {
  const params = new URLSearchParams();
  companies.forEach(c => params.append("companies", c));

  const response = await fetch(`${API_BASE_URL}/news?${params.toString()}`);

  // 🧩 Diagnóstico: se não for JSON, mostra o HTML que veio
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    const text = await response.text();
    console.error("❌ API retornou HTML em vez de JSON:\n", text.slice(0, 300));
    throw new Error(`Resposta inválida da API. Verifique o console.`);
  }

  return response.json();
}
