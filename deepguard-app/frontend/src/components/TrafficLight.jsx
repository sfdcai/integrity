import React from 'react'

const colors = {
  'GREEN': 'bg-green-500',
  'AMBER': 'bg-amber-400',
  'HIGH-AMBER': 'bg-orange-500',
  'RED': 'bg-red-600',
  'unknown': 'bg-gray-400'
}

export default function TrafficLight({ status }) {
  const color = colors[status] || colors['unknown']
  return <span className={`px-2 py-1 rounded text-white text-xs ${color}`}>{status || 'unknown'}</span>
}
