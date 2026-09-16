import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.tsx'
import { InteractionProvider } from './components/InteractionProvider.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <InteractionProvider><App /></InteractionProvider>
    </BrowserRouter>
  </StrictMode>,
)
