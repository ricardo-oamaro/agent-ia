export async function fetchNews(companies) {
  try {
    const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
    const params = new URLSearchParams();
    companies.forEach(c => params.append("companies", c));
    
    console.log(`Tentando acessar: ${API_BASE_URL}/news`);
    
    const response = await fetch(`${API_BASE_URL}/news?${params.toString()}`);
    if (!response.ok) {
      console.error(`Erro HTTP: ${response.status}`);
      throw new Error(`Erro ao buscar dados da API: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("Erro na requisição:", error);
    throw new Error(`Falha na conexão: ${error.message}`);
  }
}