import { useAuth } from "~/contexts/auth-context"
import { Sidebar } from "~/components/sidebar"
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card"
import { Navigate } from "react-router"

export default function AccountPage() {
  const { token, user, userName } = useAuth()

  if (token === undefined) return <p>Loading...</p>
  if (token === null) return <Navigate to="/seller/login" />

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold">Account</h1>

        <Card className="max-w-md">
          <CardHeader>
            <CardTitle>Profile</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <p className="text-sm text-muted-foreground">Name</p>
              <p className="font-medium">{userName ?? "—"}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Role</p>
              <p className="font-medium capitalize">{user === "seller" ? "Seller" : "Delivery Partner"}</p>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
