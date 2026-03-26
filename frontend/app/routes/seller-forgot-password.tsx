import { ForgotPasswordForm } from "~/components/forgot-password-form"

export default function SellerForgotPasswordPage() {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center bg-white p-6 md:p-10">
      <div className="w-full max-w-sm">
        <ForgotPasswordForm user="seller" />
      </div>
    </div>
  )
}
