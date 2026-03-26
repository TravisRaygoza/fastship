import { useAuth } from "~/contexts/auth-context"
import { Button } from "~/components/ui/button"
import { Package, LayoutDashboard, User, Plus, RefreshCw, LogOut } from "lucide-react"
import { useNavigate, useLocation } from "react-router"
import api from "~/lib/api"

export function Sidebar() {
  const { user, userName, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  function handleLogout() {
    if (user === "seller") {
      api.seller.logoutSellerSellerLogoutGet().catch(() => {})
    } else {
      api.partner.logoutDeliveryPartnerPartnerLogoutGet().catch(() => {})
    }
    logout()
    navigate("/seller/login")
  }

  const navItems = [
    { path: user === "seller" ? "/seller/dashboard" : "/partner/dashboard", label: "Dashboard", icon: LayoutDashboard },
    ...(user === "seller"
      ? [{ path: "/seller/submit-shipment", label: "Submit Shipment", icon: Plus }]
      : [{ path: "/partner/update-shipment", label: "Update Shipment", icon: RefreshCw }]),
  ]

  return (
    <div className="flex h-screen w-64 flex-col border-r bg-card">
      <div className="flex items-center gap-2 border-b p-4">
        <Package className="size-5" />
        <span className="text-lg font-bold">FastShip</span>
      </div>

      <nav className="flex flex-1 flex-col gap-1 p-2">
        {navItems.map((item) => (
          <Button
            key={item.path}
            variant={location.pathname === item.path ? "secondary" : "ghost"}
            className="justify-start gap-2"
            onClick={() => navigate(item.path)}
          >
            <item.icon className="size-4" />
            {item.label}
          </Button>
        ))}
      </nav>

      <div className="border-t p-4">
        <p className="mb-2 text-sm text-muted-foreground">
          {userName ?? "User"} ({user})
        </p>
        <Button variant="ghost" className="w-full justify-start gap-2" onClick={handleLogout}>
          <LogOut className="size-4" />
          Logout
        </Button>
      </div>
    </div>
  )
}
