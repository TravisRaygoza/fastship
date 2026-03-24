import { Api } from "./client"

const api = new Api({
  baseURL: "http://localhost:8000",
  securityWorker: (token: string | null) => {
    if (token) {
      return { headers: { Authorization: `Bearer ${token}` } }
    }
  },
})

export default api
