import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createWell } from '../services/api'

export default function DataEntry() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', field: '', operator: '', tvd: '', annuli: [{ name: 'A-annulus', limit_at_depth: 400, gradient_bar_per_m: 0.012, safety_factor: 0.9 }] })

  const submitWell = async (e) => {
    e.preventDefault()
    const payload = {
      ...form,
      tvd: parseFloat(form.tvd),
      annuli: form.annuli.map(a => ({ ...a, limit_at_depth: parseFloat(a.limit_at_depth), gradient_bar_per_m: parseFloat(a.gradient_bar_per_m), safety_factor: parseFloat(a.safety_factor) }))
    }
    const well = await createWell(payload)
    navigate(`/wells/${well.id}`)
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Create Well</h1>
      <form onSubmit={submitWell} className="space-y-4 bg-white p-4 rounded shadow max-w-xl">
        <input className="w-full border rounded p-2" placeholder="Name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required />
        <input className="w-full border rounded p-2" placeholder="Field" value={form.field} onChange={e => setForm({ ...form, field: e.target.value })} />
        <input className="w-full border rounded p-2" placeholder="Operator" value={form.operator} onChange={e => setForm({ ...form, operator: e.target.value })} />
        <input className="w-full border rounded p-2" placeholder="TVD" value={form.tvd} onChange={e => setForm({ ...form, tvd: e.target.value })} />
        <div className="border rounded p-3">
          <h3 className="font-semibold mb-2">Annulus</h3>
          <input className="w-full border rounded p-2 mb-2" placeholder="Name" value={form.annuli[0].name} onChange={e => setForm({ ...form, annuli: [{ ...form.annuli[0], name: e.target.value }] })} />
          <input className="w-full border rounded p-2 mb-2" placeholder="Limit at depth" value={form.annuli[0].limit_at_depth} onChange={e => setForm({ ...form, annuli: [{ ...form.annuli[0], limit_at_depth: e.target.value }] })} />
          <input className="w-full border rounded p-2 mb-2" placeholder="Gradient bar/m" value={form.annuli[0].gradient_bar_per_m} onChange={e => setForm({ ...form, annuli: [{ ...form.annuli[0], gradient_bar_per_m: e.target.value }] })} />
          <input className="w-full border rounded p-2" placeholder="Safety factor" value={form.annuli[0].safety_factor} onChange={e => setForm({ ...form, annuli: [{ ...form.annuli[0], safety_factor: e.target.value }] })} />
        </div>
        <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded">Save Well</button>
      </form>
    </div>
  )
}
