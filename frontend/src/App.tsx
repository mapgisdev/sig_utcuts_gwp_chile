import { Routes, Route } from 'react-router-dom'
import Layout from './layouts/Layout'
import Dashboard from './pages/Dashboard'
import MapPage from './pages/MapPage'
import Mechanisms from './pages/Mechanisms'
import Investments from './pages/Investments'
import Prioritization from './pages/Prioritization'
import MRV from './pages/MRV'
import DataGaps from './pages/DataGaps'
import Reports from './pages/Reports'
import Login from './pages/Login'

import DataIngestion from './pages/DataIngestion'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="mapa" element={<MapPage />} />
        <Route path="mecanismos" element={<Mechanisms />} />
        <Route path="inversiones" element={<Investments />} />
        <Route path="priorizacion" element={<Prioritization />} />
        <Route path="mrv" element={<MRV />} />
        <Route path="brechas" element={<DataGaps />} />
        <Route path="reportes" element={<Reports />} />
        <Route path="carga" element={<DataIngestion />} />
      </Route>
    </Routes>
  )
}
