import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchWells, fetchTasks } from '../services/api'
import TrafficLight from '../components/TrafficLight'
import TaskList from '../components/TaskList'

export default function Dashboard() {
  const [wells, setWells] = useState([])
  const [tasks, setTasks] = useState([])

  useEffect(() => {
    fetchWells().then(setWells)
    fetchTasks().then(setTasks)
  }, [])

  return (
    <div className="p-6 space-y-6">
      <header className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">DeepGuard Dashboard</h1>
          <p className="text-gray-600 text-sm">Well integrity overview and tasks</p>
        </div>
        <Link to="/data-entry" className="bg-indigo-600 text-white px-4 py-2 rounded">Add Data</Link>
      </header>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {wells.map(well => (
          <Link key={well.id} to={`/wells/${well.id}`} className="p-4 bg-white rounded shadow hover:shadow-lg transition">
            <div className="flex justify-between items-center mb-2">
              <div>
                <h3 className="font-semibold">{well.name}</h3>
                <p className="text-xs text-gray-500">{well.field}</p>
              </div>
              <TrafficLight status={well.annuli?.[0]?.status} />
            </div>
            <p className="text-sm">Annuli: {well.annuli.length}</p>
            <p className="text-sm">Tasks: {well.tasks.length}</p>
          </Link>
        ))}
      </div>
      <TaskList tasks={tasks} />
    </div>
  )
}
