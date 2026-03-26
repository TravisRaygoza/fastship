import { useQuery } from "@tanstack/react-query"
import { useAuth } from "~/contexts/auth-context"
import { Sidebar } from "~/components/sidebar"
import { ShipmentCard } from "~/components/shipment-card"
import api from "~/lib/api"
import type { ShipmentRead } from "~/lib/client"
import { Navigate } from "react-router"

export default function SellerDashboardPage() {
  const { token, user } = useAuth()

  if (token === undefined) return <p>Loading...</p>
  if (token === null) return <Navigate to="/seller/login" />
  if (user !== "seller") return <Navigate to="/partner/dashboard" />

  const { data: shipments, isLoading, error } = useQuery<ShipmentRead[]>({
    queryKey: ["shipments", "seller"],
    queryFn: async () => {
      const { data } = await api.shipments.getAllSellerShipmentsShipmentsSellerGet()
      return data
    },
    retry: false,
  })

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold">Seller Dashboard</h1>

        {isLoading && <p className="text-muted-foreground">Loading shipments...</p>}

        {error && (
          <p className="text-sm text-destructive">Failed to load shipments</p>
        )}

        {shipments && shipments.length === 0 && (
          <p className="text-muted-foreground">No shipments yet. Create one from the sidebar.</p>
        )}

        {shipments && shipments.length > 0 && (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {shipments.map((shipment) => (
              <ShipmentCard key={shipment.id} shipment={shipment} />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
