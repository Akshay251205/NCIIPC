import { useEffect, useState } from 'react'
import { ApiError } from '../api/client'
export function useResource<T>(load: () => Promise<T>, deps: readonly unknown[]) {
  const [data, setData] = useState<T>(); const [loading, setLoading] = useState(true); const [error, setError] = useState<string>()
  const refresh = () => { setLoading(true); setError(undefined); load().then(setData).catch((e: unknown) => setError(e instanceof ApiError ? e.message : 'Unable to load this data.')).finally(() => setLoading(false)) }
  useEffect(refresh, deps) // eslint-disable-line react-hooks/exhaustive-deps
  return { data, loading, error, refresh }
}
