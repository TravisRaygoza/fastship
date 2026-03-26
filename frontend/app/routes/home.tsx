import { useAuth } from "~/contexts/auth-context"
import { Navigate } from "react-router"

export default function Home() {
  const { token, user } = useAuth()

  if (token === undefined) return <p>Loading...</p>
  if (token && user === "partner") return <Navigate to="/partner/dashboard" />
  if (token) return <Navigate to="/seller/dashboard" />
  return <Navigate to="/seller/login" />
}
