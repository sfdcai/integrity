import React from 'react'
import TrafficLight from './TrafficLight'

export default function AnnulusCard({ annulus }) {
  return (
    <div className="p-4 bg-white rounded shadow">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="font-semibold">{annulus.name}</h3>
          <p className="text-xs text-gray-500">MAASP: {annulus.maasp ? annulus.maasp.toFixed(1) : 'N/A'} bar</p>
        </div>
        <TrafficLight status={annulus.status} />
      </div>
      <div className="mt-2 text-sm">
        <p>Utilisation: {annulus.utilisation ? (annulus.utilisation * 100).toFixed(1) : 'N/A'}%</p>
        <p>Gradient: {annulus.gradient_bar_per_m} bar/m</p>
      </div>
    </div>
  )
}
