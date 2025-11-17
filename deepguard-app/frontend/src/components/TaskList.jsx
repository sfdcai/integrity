import React from 'react'

export default function TaskList({ tasks }) {
  return (
    <div className="bg-white rounded shadow p-4">
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-semibold">Tasks & Reminders</h3>
      </div>
      <ul className="divide-y divide-gray-200">
        {tasks.map(task => (
          <li key={task.id} className="py-2 flex justify-between">
            <div>
              <p className="font-medium">{task.title}</p>
              <p className="text-xs text-gray-500">Due: {task.due_date ? new Date(task.due_date).toLocaleDateString() : 'n/a'}</p>
            </div>
            <span className="text-sm capitalize">{task.priority}</span>
          </li>
        ))}
        {tasks.length === 0 && <li className="text-sm text-gray-500 py-2">No tasks</li>}
      </ul>
    </div>
  )
}
