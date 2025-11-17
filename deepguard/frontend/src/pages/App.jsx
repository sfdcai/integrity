import { useState } from 'react'
import LoginPage from './Login'
import Dashboard from './Dashboard'
import WellDetail from './WellDetail'
import { fetchWells } from '../services/api'

export default function App() {
  const [token, setToken] = useState(null)
  const [selectedWell, setSelectedWell] = useState(null)
  const [wells, setWells] = useState([])

  const handleAuthenticated = async () => {
    const data = await fetchWells()
    setWells(data)
  }

  if (!token) {
    return <LoginPage onAuthenticated={(t) => {setToken(t); handleAuthenticated()}} />
  }

  return selectedWell ? (
    <WellDetail wellId={selectedWell} onBack={() => setSelectedWell(null)} />
  ) : (
    <Dashboard wells={wells} onSelectWell={(id) => setSelectedWell(id)} />
  )
}
