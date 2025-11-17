import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import Dashboard from './pages/Dashboard'
import WellDetail from './pages/WellDetail'
import DataEntry from './pages/DataEntry'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/wells/:id" element={<WellDetail />} />
        <Route path="/data-entry" element={<DataEntry />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
