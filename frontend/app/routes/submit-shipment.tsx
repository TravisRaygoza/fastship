import { useAuth } from "~/contexts/auth-context"
import { Sidebar } from "~/components/sidebar"
import { SubmitShipmentForm } from "~/components/submit-shipment-form"
import { Navigate } from "react-router"

export default function SubmitShipmentPage() {
  const { token, user } = useAuth()

  if (token === undefined) return <p>Loading...</p>
  if (token === null) return <Navigate to="/seller/login" />
  if (user !== "seller") return <Navigate to="/dashboard" />

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold">Submit Shipment</h1>
        <SubmitShipmentForm />
      </main>
    </div>
  )
}
