import { useEffect, useState } from "react";

export function useApiHealth() {
  const [online, setOnline] = useState<boolean | null>(null);

  useEffect(() => {
    let active = true;
    fetch("/health")
      .then((response) => { if (!response.ok) throw new Error("API unavailable"); return response.json(); })
      .then(() => { if (active) setOnline(true); })
      .catch(() => { if (active) setOnline(false); });
    return () => { active = false; };
  }, []);

  return online;
}
