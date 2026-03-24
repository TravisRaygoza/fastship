import { useState } from "react"
import type { ShipmentRead, ShipmentStatus } from "~/lib/client"
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card"
import { Badge } from "~/components/ui/badge"
import { Button } from "~/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog"

const statusColors: Record<string, string> = {
  placed: "bg-blue-100 text-blue-800",
  in_transit: "bg-yellow-100 text-yellow-800",
  out_for_delivery: "bg-orange-100 text-orange-800",
  delivered: "bg-green-100 text-green-800",
  cancelled: "bg-red-100 text-red-800",
}

function formatStatus(status: string) {
  return status.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  })
}

export function ShipmentCard({ shipment }: { shipment: ShipmentRead }) {
  const status = shipment.timeline?.length
    ? shipment.timeline[shipment.timeline.length - 1].status
    : "placed"

  return (
    <Dialog>
      <DialogTrigger>
        <Card className="cursor-pointer transition-shadow hover:shadow-md">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium">
                {shipment.content}
              </CardTitle>
              <Badge className={statusColors[status] ?? ""} variant="outline">
                {formatStatus(status)}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>{shipment.weight} lbs</span>
              <span>ZIP: {shipment.destination}</span>
            </div>
          </CardContent>
        </Card>
      </DialogTrigger>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Shipment Details</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>
              <p className="text-muted-foreground">Content</p>
              <p className="font-medium">{shipment.content}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Weight</p>
              <p className="font-medium">{shipment.weight} lbs</p>
            </div>
            <div>
              <p className="text-muted-foreground">Destination</p>
              <p className="font-medium">{shipment.destination}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Est. Delivery</p>
              <p className="font-medium">{formatDate(shipment.estimated_delivery)}</p>
            </div>
          </div>

          {shipment.tags && shipment.tags.length > 0 && (
            <div>
              <p className="mb-1 text-sm text-muted-foreground">Tags</p>
              <div className="flex flex-wrap gap-1">
                {shipment.tags.map((tag) => (
                  <Badge key={tag.id} variant="outline">
                    {tag.name}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {shipment.timeline && shipment.timeline.length > 0 && (
            <div>
              <p className="mb-2 text-sm text-muted-foreground">Timeline</p>
              <div className="space-y-2">
                {[...shipment.timeline].reverse().map((event) => (
                  <div
                    key={event.id}
                    className="flex items-start gap-3 rounded-md border p-2 text-sm"
                  >
                    <Badge className={statusColors[event.status] ?? ""} variant="outline">
                      {formatStatus(event.status)}
                    </Badge>
                    <div className="flex-1">
                      <p className="text-muted-foreground">
                        ZIP: {event.location_zipcode}
                      </p>
                      {event.description && <p>{event.description}</p>}
                      <p className="text-xs text-muted-foreground">
                        {formatDate(event.created_at)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
