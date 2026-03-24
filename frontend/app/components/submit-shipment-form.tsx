import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { Button } from "~/components/ui/button"
import { Input } from "~/components/ui/input"
import { Field, FieldGroup, FieldLabel } from "~/components/ui/field"
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card"
import api from "~/lib/api"
import type { ShipmentCreate } from "~/lib/client"

export function SubmitShipmentForm() {
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (data: ShipmentCreate) =>
      api.shipments.submitShipmentShipmentsPost(data),
    onSuccess: () => {
      setSuccess(true)
      setError(null)
      queryClient.invalidateQueries({ queryKey: ["shipments"] })
    },
    onError: (err: any) => {
      const detail = err?.response?.data?.detail
      setError(typeof detail === "string" ? detail : "Failed to submit shipment.")
      setSuccess(false)
    },
  })

  function handleSubmit(formData: FormData) {
    setSuccess(false)
    const data: ShipmentCreate = {
      content: formData.get("content")?.toString() ?? "",
      weight: parseFloat(formData.get("weight")?.toString() ?? "0"),
      destination: parseInt(formData.get("destination")?.toString() ?? "0"),
      client_contact_email: formData.get("client_contact_email")?.toString() || null,
      client_contact_phone: formData.get("client_contact_phone")?.toString() || null,
    }
    mutation.mutate(data)
  }

  return (
    <Card className="max-w-lg">
      <CardHeader>
        <CardTitle>Submit New Shipment</CardTitle>
      </CardHeader>
      <CardContent>
        <form action={handleSubmit}>
          <FieldGroup>
            {error && (
              <p className="text-sm text-destructive">{error}</p>
            )}
            {success && (
              <p className="text-sm text-green-600">Shipment submitted successfully!</p>
            )}
            <Field>
              <FieldLabel htmlFor="content">Content</FieldLabel>
              <Input
                id="content"
                name="content"
                placeholder="Package contents"
                maxLength={50}
                required
              />
            </Field>
            <Field>
              <FieldLabel htmlFor="weight">Weight (lbs)</FieldLabel>
              <Input
                id="weight"
                name="weight"
                type="number"
                placeholder="0.5 - 49.9"
                min={0.5}
                max={49.9}
                step={0.1}
                required
              />
            </Field>
            <Field>
              <FieldLabel htmlFor="destination">Destination ZIP Code</FieldLabel>
              <Input
                id="destination"
                name="destination"
                type="number"
                placeholder="12345"
                required
              />
            </Field>
            <Field>
              <FieldLabel htmlFor="client_contact_email">Client Email (optional)</FieldLabel>
              <Input
                id="client_contact_email"
                name="client_contact_email"
                type="email"
                placeholder="client@example.com"
              />
            </Field>
            <Field>
              <FieldLabel htmlFor="client_contact_phone">Client Phone (optional)</FieldLabel>
              <Input
                id="client_contact_phone"
                name="client_contact_phone"
                type="tel"
                placeholder="+1234567890"
              />
            </Field>
            <Button type="submit" disabled={mutation.isPending}>
              {mutation.isPending ? "Submitting..." : "Submit Shipment"}
            </Button>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  )
}
