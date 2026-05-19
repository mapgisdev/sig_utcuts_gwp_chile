import { useState } from 'react'
import api from '../api/client'

const REPORT_TYPES = [
  { key: 'national', label: 'Reporte Nacional', icon: '🇨🇱', desc: 'Resumen de inversiones, proyectos e indicadores a nivel nacional' },
  { key: 'mrv', label: 'Reporte MRV', icon: '📋', desc: 'Estado de monitoreo, reporte y verificación' },
  { key: 'data-gaps', label: 'Reporte de Brechas', icon: '⚠️', desc: 'Análisis de datos faltantes y calidad de información' },
]

export default function Reports() {
  const [activeReport, setActiveReport] = useState<string | null>(null)
  const [reportData, setReportData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const loadReport = async (key: string) => {
    setLoading(true)
    setActiveReport(key)
    try {
      const r = await api.get(`/reports/${key}`)
      setReportData(r.data)
    } catch { setReportData(null) }
    setLoading(false)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Reportes</h1>
      <p className="text-ocean-400 text-sm">Generación de reportes del sistema — datos demo</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {REPORT_TYPES.map((rt) => (
          <div key={rt.key} className={`glass-card p-5 cursor-pointer hover:scale-[1.02] transition-transform ${activeReport === rt.key ? 'border-forest-500/50' : ''}`}
               onClick={() => loadReport(rt.key)}>
            <div className="text-3xl mb-3">{rt.icon}</div>
            <h3 className="text-sm font-semibold text-white mb-1">{rt.label}</h3>
            <p className="text-xs text-ocean-400">{rt.desc}</p>
          </div>
        ))}
      </div>

      {loading && <div className="text-center text-ocean-400 py-10 animate-pulse-soft">Generando reporte...</div>}

      {reportData && !loading && (
        <div className="glass-card p-6 animate-fade-in">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-white">{reportData.title}</h2>
            <span className="text-xs text-ocean-500 bg-ocean-800 px-3 py-1 rounded-full">{reportData.note}</span>
          </div>
          <pre className="bg-ocean-800/50 rounded-lg p-4 text-sm text-ocean-300 overflow-x-auto whitespace-pre-wrap">
            {JSON.stringify(reportData.data || reportData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}
