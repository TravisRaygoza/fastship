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
import { useAuth } from "~/contexts/auth-context"
import api from "~/lib/api"

export function LoginForm({
  user,
  className,
  ...props
}: { user: "seller" | "partner" } & React.ComponentProps<"div">) {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(formData: FormData) {
    const email = formData.get("email")?.toString() ?? ""
    const password = formData.get("password")?.toString() ?? ""

    setError(null)
    setLoading(true)

    try {
      const loginFn =
        user === "seller"
          ? api.seller.loginSellerSellerTokenPost
          : api.partner.loginDeliveryPartnerPartnerTokenPost

      const { data } = await loginFn({ username: email, password })
      login(data.access_token, user)
      navigate("/dashboard")
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === "string" ? detail : "Login failed. Please try again.")
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
                <h1 className="text-2xl font-bold">Welcome back</h1>
                <p className="text-balance text-muted-foreground">
                  Login to your FastShip {user === "seller" ? "Seller" : "Partner"} account
                </p>
              </div>
              {error && (
                <p className="text-center text-sm text-destructive">{error}</p>
              )}
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  id="email"
                  type="email"
                  name="email"
                  placeholder="m@example.com"
                  required
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="password">Password</FieldLabel>
                <Input id="password" type="password" name="password" required />
              </Field>
              <Field>
                <Button type="submit" disabled={loading}>
                  {loading ? "Logging in..." : "Login"}
                </Button>
              </Field>
              <FieldDescription className="text-center">
                Don&apos;t have an account?{" "}
                <a href="#">Sign up</a>
              </FieldDescription>
              <FieldDescription className="text-center">
                <a href={user === "seller" ? "/partner/login" : "/seller/login"}>
                  Login as {user === "seller" ? "Delivery Partner" : "Seller"}
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
