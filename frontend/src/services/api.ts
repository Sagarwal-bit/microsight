const base=import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
export async function request<T>(path:string, init?:RequestInit):Promise<T>{const response=await fetch(`${base}${path}`,init);if(!response.ok)throw new Error(await response.text()||response.statusText);return response.json() as Promise<T>}
export {base};
