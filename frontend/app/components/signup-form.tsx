import { useState } from "react"
import { useNavigate } from "react-router"
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

export function SignupForm({
  user,
  className,
  ...props
}: { user: "seller" | "partner" } & React.ComponentProps<"div">) {
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  async function handleSubmit(formData: FormData) {
    setError(null)
    setLoading(true)
    setSuccess(false)

    try {
      if (user === "seller") {
        await api.seller.registerSellerSellerSignupPost({
          name: formData.get("name")?.toString() ?? "",
          email: formData.get("email")?.toString() ?? "",
          password: formData.get("password")?.toString() ?? "",
        })
      } else {
        const zipCodes = formData.get("zip_codes")?.toString() ?? ""
        await api.partner.registerDeliveryPartnerPartnerSignupPost({
          name: formData.get("name")?.toString() ?? "",
          email: formData.get("email")?.toString() ?? "",
          password: formData.get("password")?.toString() ?? "",
          serviceable_zip_codes: zipCodes.split(",").map((z) => parseInt(z.trim())).filter((z) => !isNaN(z)),
          max_handling_capacity: parseInt(formData.get("capacity")?.toString() ?? "10"),
        })
      }
      setSuccess(true)
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === "string" ? detail : "Signup failed. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden p-0">
        <CardContent className="grid p-0 md:grid-cols-2">
          <form className="p-6 md:p-8" action={handleSubmit}>
            <FieldGroup>
              <div className="flex flex-col items-center gap-2 text-center">
                <h1 className="text-2xl font-bold">Create an account</h1>
                <p className="text-balance text-muted-foreground">
                  Sign up as a {user === "seller" ? "Seller" : "Delivery Partner"}
                </p>
              </div>
              {error && (
                <p className="text-center text-sm text-destructive">{error}</p>
              )}
              {success && (
                <div className="text-center">
                  <p className="text-sm text-green-600">Account created! Check your email to verify.</p>
                  <a href={`/${user}/login`} className="text-sm underline">Go to login</a>
                </div>
              )}
              <Field>
                <FieldLabel htmlFor="name">Name</FieldLabel>
                <Input id="name" name="name" placeholder="Your name" required />
              </Field>
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input id="email" type="email" name="email" placeholder="m@example.com" required />
              </Field>
              <Field>
                <FieldLabel htmlFor="password">Password</FieldLabel>
                <Input id="password" type="password" name="password" required />
              </Field>
              {user === "partner" && (
                <>
                  <Field>
                    <FieldLabel htmlFor="zip_codes">Serviceable ZIP Codes</FieldLabel>
                    <Input
                      id="zip_codes"
                      name="zip_codes"
                      placeholder="90210, 90211, 90212"
                      required
                    />
                    <FieldDescription>Comma-separated ZIP codes you can deliver to</FieldDescription>
                  </Field>
                  <Field>
                    <FieldLabel htmlFor="capacity">Max Handling Capacity</FieldLabel>
                    <Input
                      id="capacity"
                      name="capacity"
                      type="number"
                      placeholder="10"
                      min={1}
                      required
                    />
                  </Field>
                </>
              )}
              <Field>
                <Button type="submit" disabled={loading || success}>
                  {loading ? "Creating account..." : "Sign up"}
                </Button>
              </Field>
              <FieldDescription className="text-center">
                Already have an account?{" "}
                <a href={`/${user}/login`}>Login</a>
              </FieldDescription>
              <FieldDescription className="text-center">
                <a href={user === "seller" ? "/partner/signup" : "/seller/signup"}>
                  Sign up as {user === "seller" ? "Delivery Partner" : "Seller"}
                </a>
              </FieldDescription>
            </FieldGroup>
          </form>
          <div className="relative hidden bg-muted md:block">
            <img
              src="/login_pic.png"
              alt="Image"
              className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
