import { type RouteConfig, index, route } from "@react-router/dev/routes"

export default [
  index("routes/home.tsx"),
  route("/seller/login", "routes/seller-login.tsx"),
  route("/seller/signup", "routes/seller-signup.tsx"),
  route("/seller/forgot-password", "routes/seller-forgot-password.tsx"),
  route("/seller/dashboard", "routes/seller-dashboard.tsx"),
  route("/seller/submit-shipment", "routes/submit-shipment.tsx"),
  route("/partner/login", "routes/partner-login.tsx"),
  route("/partner/signup", "routes/partner-signup.tsx"),
  route("/partner/forgot-password", "routes/partner-forgot-password.tsx"),
  route("/partner/dashboard", "routes/partner-dashboard.tsx"),
  route("/partner/update-shipment", "routes/update-shipment.tsx"),
  route("/account", "routes/account.tsx"),
] satisfies RouteConfig
