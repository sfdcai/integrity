import { Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import WellDetail from './pages/WellDetail'
import ShellLayout from './components/ShellLayout'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<ShellLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="/wells/:id" element={<WellDetail />} />
      </Route>
    </Routes>
  )
}
