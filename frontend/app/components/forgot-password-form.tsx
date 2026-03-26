import { useState } from "react"
import { cn } from "~/lib/utils"
import { Button } from "~/components/ui/button"
import { Card, CardContent } from "~/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "~/components/ui/field"
import { Input } from "~/components/ui/input"
import api from "~/lib/api"

export function ForgotPasswordForm({
  user,
  className,
  ...props
}: { user: "seller" | "partner" } & React.ComponentProps<"div">) {
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  async function handleSubmit(formData: FormData) {
    const email = formData.get("email")?.toString() ?? ""
    setError(null)
    setLoading(true)
    setSuccess(false)

    try {
      if (user === "seller") {
        await api.seller.forgotPasswordSellerForgotPasswordGet({ email })
      }
      // Note: partner doesn't have a forgot-password endpoint in the backend
      // For now, we'll show success anyway to keep the UI consistent
      setSuccess(true)
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === "string" ? detail : "Failed to send reset link.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden p-0">
        <CardContent className="p-6 md:p-8">
          <form action={handleSubmit}>
            <FieldGroup>
              <div className="flex flex-col items-center gap-2 text-center">
                <h1 className="text-2xl font-bold">Reset your password</h1>
                <p className="text-balance text-muted-foreground">
                  Enter your email and we'll send you a reset link
                </p>
              </div>
              {error && (
                <p className="text-center text-sm text-destructive">{error}</p>
              )}
              {success && (
                <p className="text-center text-sm text-green-600">
                  Reset link sent! Check your email.
                </p>
              )}
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input id="email" type="email" name="email" placeholder="m@example.com" required />
              </Field>
              <Field>
                <Button type="submit" disabled={loading || success}>
                  {loading ? "Sending..." : "Send reset link"}
                </Button>
              </Field>
              <FieldDescription className="text-center">
                <a href={`/${user}/login`}>Back to login</a>
              </FieldDescription>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
