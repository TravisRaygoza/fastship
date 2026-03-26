import { SignupForm } from "~/components/signup-form"

export default function SellerSignupPage() {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center bg-white p-6 md:p-10">
      <div className="w-full max-w-sm md:max-w-4xl">
        <SignupForm user="seller" />
      </div>
    </div>
  )
}
