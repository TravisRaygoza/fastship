import { useState } from "react"
import { useMutation } from "@tanstack/react-query"
import { Button } from "~/components/ui/button"
import { Input } from "~/components/ui/input"
import { Field, FieldGroup, FieldLabel } from "~/components/ui/field"
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "~/components/ui/select"
import api from "~/lib/api"
import { ShipmentStatus, type ShipmentUpdate } from "~/lib/client"

export function UpdateShipmentForm({ shipmentId: initialId }: { shipmentId?: string }) {
  const [shipmentId, setShipmentId] = useState(initialId ?? "")
  const [status, setStatus] = useState<string>("")
  const [location, setLocation] = useState("")
  const [description, setDescription] = useState("")
  const [verificationCode, setVerificationCode] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const mutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: ShipmentUpdate }) =>
      api.shipments.shipmentUpdateShipmentsIdPatch(id, data),
    onSuccess: () => {
      setSuccess(true)
      setError(null)
    },
    onError: (err: any) => {
      const detail = err?.response?.data?.detail
      setError(typeof detail === "string" ? detail : "Failed to update shipment.")
      setSuccess(false)
    },
  })

  function handleSubmit(formData: FormData) {
    setSuccess(false)
    if (!shipmentId || !status) return

    const data: ShipmentUpdate = {
      status: status as unknown as ShipmentStatus,
      location: location ? parseInt(location) : null,
      description: description || null,
      verification_code: status === ShipmentStatus.Delivered ? verificationCode : null,
    }
    mutation.mutate({ id: shipmentId, data })
  }

  return (
    <Card className="max-w-lg">
      <CardHeader>
        <CardTitle>Update Shipment</CardTitle>
      </CardHeader>
      <CardContent>
        <form action={handleSubmit}>
          <FieldGroup>
            {error && (
              <p className="text-sm text-destructive">{error}</p>
            )}
            {success && (
              <p className="text-sm text-green-600">Shipment updated successfully!</p>
            )}
            <Field>
              <FieldLabel htmlFor="shipment-id">Shipment ID</FieldLabel>
              <Input
                id="shipment-id"
                value={shipmentId}
                onChange={(e) => setShipmentId(e.target.value)}
                placeholder="Enter shipment UUID"
                required
              />
            </Field>
            <Field>
              <FieldLabel>Status</FieldLabel>
              <Select value={status} onValueChange={(val) => setStatus(val ?? "")}>
                <SelectTrigger>
                  <SelectValue placeholder="Select status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ShipmentStatus.InTransit}>In Transit</SelectItem>
                  <SelectItem value={ShipmentStatus.OutForDelivery}>Out for Delivery</SelectItem>
                  <SelectItem value={ShipmentStatus.Delivered}>Delivered</SelectItem>
                </SelectContent>
              </Select>
            </Field>
            <Field>
              <FieldLabel htmlFor="location">Location ZIP Code</FieldLabel>
              <Input
                id="location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                type="number"
                placeholder="Current location ZIP"
              />
            </Field>
            <Field>
              <FieldLabel htmlFor="description">Description</FieldLabel>
              <Input
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Status description"
              />
            </Field>
            {status === ShipmentStatus.Delivered && (
              <Field>
                <FieldLabel htmlFor="verification-code">Verification Code</FieldLabel>
                <Input
                  id="verification-code"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value)}
                  placeholder="6-digit OTP"
                  required
                />
              </Field>
            )}
            <Button type="submit" disabled={mutation.isPending || !shipmentId || !status}>
              {mutation.isPending ? "Updating..." : "Update Shipment"}
            </Button>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  )
}
