// src/contexts/AuthContext.tsx
import React, { createContext, useContext, ReactNode } from "react";
import useSWR from "swr";

interface User {
  username: string;
  upn: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: any;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  error: null,
});

const fetcher = (url: string) =>
  fetch(url, { credentials: "include" }).then((res) => res.json());

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const { data, error } = useSWR("/api/auth/session", fetcher, {
    dedupingInterval: 5000,
  });

  const user: User | null = data || null;
  const loading = !error && !data;

  return (
    <AuthContext.Provider value={{ user, loading, error }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
