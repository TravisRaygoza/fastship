import { useAuth } from "~/contexts/auth-context"
import { useSearchParams } from "react-router"
import { Sidebar } from "~/components/sidebar"
import { UpdateShipmentForm } from "~/components/update-shipment-form"
import { Navigate } from "react-router"

export default function UpdateShipmentPage() {
  const { token, user } = useAuth()
  const [searchParams] = useSearchParams()
  const shipmentId = searchParams.get("id") ?? undefined

  if (token === undefined) return <p>Loading...</p>
  if (token === null) return <Navigate to="/partner/login" />
  if (user !== "partner") return <Navigate to="/dashboard" />

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold">Update Shipment</h1>
        <UpdateShipmentForm shipmentId={shipmentId} />
      </main>
    </div>
  )
}
