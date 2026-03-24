import { useAuth } from "~/contexts/auth-context"
import { Navigate } from "react-router"

export default function Home() {
  const { token } = useAuth()

  if (token === undefined) return <p>Loading...</p>
  if (token) return <Navigate to="/dashboard" />
  return <Navigate to="/seller/login" />
}
