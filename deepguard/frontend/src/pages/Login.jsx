import { useState } from 'react'
import { login } from '../services/api'
import { LockKeyhole, ShieldCheck } from 'lucide-react'

export default function LoginPage({ onAuthenticated }) {
  const [email, setEmail] = useState('admin@deepguard.io')
  const [password, setPassword] = useState('admin')
  const [error, setError] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    try {
      const token = await login(email, password)
      onAuthenticated(token)
    } catch (err) {
      setError('Login failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-midnight via-slate-900 to-black">
      <div className="glass-card p-10 w-full max-w-md">
        <div className="flex items-center gap-3 mb-6">
          <ShieldCheck className="text-neon" />
          <div>
            <p className="text-sm text-slate-400">DeepGuard</p>
            <h1 className="text-2xl font-semibold">Well Integrity Login</h1>
          </div>
        </div>
        <form className="space-y-4" onSubmit={submit}>
          <div>
            <label className="text-sm text-slate-400">Email</label>
            <input value={email} onChange={(e)=>setEmail(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 focus:outline-none focus:border-neon" />
          </div>
          <div>
            <label className="text-sm text-slate-400">Password</label>
            <div className="relative">
              <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 pr-10 focus:outline-none focus:border-neon" />
              <LockKeyhole className="absolute right-3 top-3 text-slate-500" />
            </div>
          </div>
          {error && <p className="text-ember text-sm">{error}</p>}
          <button type="submit" className="w-full py-3 rounded-lg bg-gradient-to-r from-neon to-indigo-400 text-midnight font-semibold shadow-lg shadow-neon/20">Sign in</button>
        </form>
      </div>
    </div>
  )
}
