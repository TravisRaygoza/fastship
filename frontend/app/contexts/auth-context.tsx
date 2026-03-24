import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import api from "~/lib/api"

type UserType = "seller" | "partner"

interface AuthContextType {
  token: string | undefined | null
  user: UserType | null
  userName: string | null
  login: (token: string, user: UserType) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType>({
  token: undefined,
  user: null,
  userName: null,
  login: () => {},
  logout: () => {},
})

function decodeTokenPayload(token: string): Record<string, any> | null {
  try {
    const payload = token.split(".")[1]
    return JSON.parse(atob(payload))
  } catch {
    return null
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | undefined | null>(undefined)
  const [user, setUser] = useState<UserType | null>(null)
  const [userName, setUserName] = useState<string | null>(null)

  useEffect(() => {
    const savedToken = localStorage.getItem("token")
    const savedUser = localStorage.getItem("user") as UserType | null
    if (savedToken && savedUser) {
      setToken(savedToken)
      setUser(savedUser)
      api.setSecurityData(savedToken)
      const payload = decodeTokenPayload(savedToken)
      if (payload?.user?.name) {
        setUserName(payload.user.name)
      }
    } else {
      setToken(null)
    }
  }, [])

  function login(newToken: string, userType: UserType) {
    localStorage.setItem("token", newToken)
    localStorage.setItem("user", userType)
    setToken(newToken)
    setUser(userType)
    api.setSecurityData(newToken)
    const payload = decodeTokenPayload(newToken)
    if (payload?.user?.name) {
      setUserName(payload.user.name)
    }
  }

  function logout() {
    localStorage.removeItem("token")
    localStorage.removeItem("user")
    setToken(null)
    setUser(null)
    setUserName(null)
    api.setSecurityData(null)
  }

  return (
    <AuthContext.Provider value={{ token, user, userName, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}

export { AuthContext }
