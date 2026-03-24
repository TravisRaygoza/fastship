import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { useAuth } from "~/contexts/auth-context"
import { Sidebar } from "~/components/sidebar"
import { ShipmentCard } from "~/components/shipment-card"
import { Input } from "~/components/ui/input"
import { Button } from "~/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card"
import api from "~/lib/api"
import type { ShipmentRead } from "~/lib/client"
import { Navigate } from "react-router"

export default function DashboardPage() {
  const { token, user } = useAuth()
  const [searchId, setSearchId] = useState("")
  const [shipmentId, setShipmentId] = useState<string | null>(null)

  if (token === undefined) return <p>Loading...</p>
  if (token === null) return <Navigate to="/seller/login" />

  const { data: shipment, isLoading, error } = useQuery<ShipmentRead>({
    queryKey: ["shipment", shipmentId],
    queryFn: async () => {
      const { data } = await api.shipments.getShipmentShipmentsIdGet(shipmentId!)
      return data
    },
    enabled: !!shipmentId,
    retry: false,
  })

  function handleSearch(formData: FormData) {
    const id = formData.get("shipment-id")?.toString()
    if (id) setShipmentId(id)
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold">Dashboard</h1>

        <Card className="mb-6 max-w-lg">
          <CardHeader>
            <CardTitle className="text-sm">Look up a shipment</CardTitle>
          </CardHeader>
          <CardContent>
            <form action={handleSearch} className="flex gap-2">
              <Input
                name="shipment-id"
                value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
                placeholder="Enter shipment UUID"
              />
              <Button type="submit">Search</Button>
            </form>
          </CardContent>
        </Card>

        {isLoading && <p className="text-muted-foreground">Loading shipment...</p>}

        {error && (
          <p className="text-sm text-destructive">
            {(error as any)?.response?.status === 404
              ? "Shipment not found"
              : "Failed to load shipment"}
          </p>
        )}

        {shipment && (
          <div className="max-w-lg">
            <ShipmentCard shipment={shipment} />
          </div>
        )}

        {!shipmentId && !isLoading && (
          <p className="text-muted-foreground">
            Enter a shipment ID above to view its details.
          </p>
        )}
      </main>
    </div>
  )
}
