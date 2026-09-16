import { createContext, useContext } from "react";

export const FeedbackContext = createContext<(title: string, message?: string) => void>(() => undefined);

export function useFeedback() {
  return useContext(FeedbackContext);
}
