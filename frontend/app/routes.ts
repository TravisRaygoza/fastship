import { type RouteConfig, index, route } from "@react-router/dev/routes"

export default [
  index("routes/home.tsx"),
  route("/seller/login", "routes/seller-login.tsx"),
  route("/partner/login", "routes/partner-login.tsx"),
  route("/dashboard", "routes/dashboard.tsx"),
  route("/account", "routes/account.tsx"),
  route("/seller/submit-shipment", "routes/submit-shipment.tsx"),
  route("/partner/update-shipment", "routes/update-shipment.tsx"),
] satisfies RouteConfig
