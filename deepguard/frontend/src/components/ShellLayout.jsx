import { Outlet, Link, useLocation } from 'react-router-dom'
import { ShieldCheck, Bell, LogOut } from 'lucide-react'

export default function ShellLayout() {
  const location = useLocation()
  return (
    <div className="min-h-screen text-white">
      <header className="sticky top-0 z-20 backdrop-blur-lg bg-midnight/80 border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-r from-teal to-amber p-2 rounded-xl shadow-soft">
              <ShieldCheck className="text-midnight" size={24} />
            </div>
            <div>
              <h1 className="text-xl font-semibold">DeepGuard</h1>
              <p className="text-xs text-white/60">Well integrity SaaS</p>
            </div>
            <nav className="ml-8 flex gap-6 text-sm text-white/70">
              <Link className={location.pathname === '/' ? 'text-white' : ''} to="/">Dashboard</Link>
              <Link className={location.pathname.includes('wells') ? 'text-white' : ''} to="/wells/1">Well detail</Link>
            </nav>
          </div>
          <div className="flex items-center gap-4 text-white/80 text-sm">
            <button className="flex items-center gap-2 px-3 py-1 rounded-lg bg-white/5 border border-white/10">
              <Bell size={16}/> Alerts
            </button>
            <button className="flex items-center gap-2 px-3 py-1 rounded-lg bg-white/5 border border-white/10">
              <LogOut size={16}/> Logout
            </button>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-6 py-8">
        <Outlet />
      </main>
    </div>
  )
}
