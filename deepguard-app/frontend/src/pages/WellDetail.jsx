import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchWell, fetchSchematic, createMeasurement } from '../services/api'
import AnnulusCard from '../components/AnnulusCard'
import WellSchematic from '../d3/WellSchematic'

export default function WellDetail() {
  const { id } = useParams()
  const [well, setWell] = useState(null)
  const [schematic, setSchematic] = useState(null)
  const [form, setForm] = useState({ annulusId: '', pressure: '', tvd: '' })

  useEffect(() => {
    fetchWell(id).then(setWell)
    fetchSchematic(id).then(data => {
      setSchematic(data)
    })
  }, [id])

  const submitMeasurement = async (e) => {
    e.preventDefault()
    await createMeasurement(form.annulusId, { pressure: parseFloat(form.pressure), tvd: parseFloat(form.tvd) })
    fetchWell(id).then(setWell)
    fetchSchematic(id).then(setSchematic)
  }

  if (!well) return <div className="p-6">Loading...</div>

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">{well.name}</h1>
          <p className="text-gray-600 text-sm">{well.field} • {well.operator}</p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {well.annuli.map(annulus => (
          <AnnulusCard key={annulus.id} annulus={annulus} />
        ))}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded shadow p-4">
          <h3 className="font-semibold mb-2">Measurements</h3>
          <form onSubmit={submitMeasurement} className="space-y-2">
            <select className="w-full border rounded p-2" value={form.annulusId} onChange={e => setForm({ ...form, annulusId: e.target.value })}>
              <option value="">Select annulus</option>
              {well.annuli.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
            </select>
            <input className="w-full border rounded p-2" placeholder="Pressure (bar)" value={form.pressure} onChange={e => setForm({ ...form, pressure: e.target.value })} />
            <input className="w-full border rounded p-2" placeholder="TVD (m)" value={form.tvd} onChange={e => setForm({ ...form, tvd: e.target.value })} />
            <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded">Add measurement</button>
          </form>
        </div>
        <div>
          {schematic && <WellSchematic schematic={schematic} />}
        </div>
      </div>
      <div className="bg-white rounded shadow p-4">
        <h3 className="font-semibold">Critical Points</h3>
        <ul className="grid grid-cols-2 gap-2 mt-2">
          {well.critical_points.map(cp => (
            <li key={cp.id} className="p-2 border rounded text-sm">{cp.name} @ {cp.depth} m</li>
          ))}
        </ul>
      </div>
    </div>
  )
}
