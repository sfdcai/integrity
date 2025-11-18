import { Shield } from 'lucide-react'

export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-midnight via-slate to-black text-white">
      <div className="glass rounded-2xl p-10 w-full max-w-md shadow-soft">
        <div className="flex items-center gap-3 mb-8">
          <div className="bg-gradient-to-r from-teal to-amber p-2 rounded-xl">
            <Shield size={24} className="text-midnight" />
          </div>
          <div>
            <h2 className="text-2xl font-semibold">DeepGuard</h2>
            <p className="text-sm text-white/60">Enterprise well integrity</p>
          </div>
        </div>
        <form className="space-y-4">
          <div>
            <label className="block text-sm text-white/60 mb-2">Email</label>
            <input className="w-full rounded-lg bg-white/5 border border-white/10 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-teal" placeholder="you@company.com" />
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-2">Password</label>
            <input type="password" className="w-full rounded-lg bg-white/5 border border-white/10 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-teal" placeholder="••••••••" />
          </div>
          <div className="flex items-center justify-between text-sm text-white/70">
            <label className="flex items-center gap-2"><input type="checkbox" className="accent-teal"/> Remember me</label>
            <a className="text-teal" href="#">Forgot password?</a>
          </div>
          <button type="button" className="w-full py-3 rounded-lg bg-gradient-to-r from-teal to-amber text-midnight font-semibold shadow-soft">Login</button>
        </form>
      </div>
    </div>
  )
}
