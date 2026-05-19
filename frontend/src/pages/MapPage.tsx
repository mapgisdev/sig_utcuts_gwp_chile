import { useEffect, useRef, useState } from 'react'
import maplibregl from 'maplibre-gl'
import api from '../api/client'

const PRIORITY_COLORS: Record<string, string> = {
  muy_alta: '#16a34a', alta: '#22c55e', media: '#eab308', baja: '#f97316', muy_baja: '#ef4444'
}

export default function MapPage() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<maplibregl.Map | null>(null)
  const [loaded, setLoaded] = useState(false)
  const [selectedTerritory, setSelectedTerritory] = useState<any>(null)
  const [layerToggles, setLayerToggles] = useState({ communes: true, regions: true })

  useEffect(() => {
    if (!mapContainer.current) return
    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: { version: 8, sources: {
        'osm-tiles': { type: 'raster', tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'], tileSize: 256, attribution: '© OpenStreetMap' }
      }, layers: [{ id: 'osm', type: 'raster', source: 'osm-tiles' }] },
      center: [-71.5, -35.0],
      zoom: 5,
    })
    map.current.addControl(new maplibregl.NavigationControl(), 'top-right')
    map.current.on('load', () => {
      setLoaded(true)
      loadGeoData()
    })
    return () => { map.current?.remove() }
  }, [])

  const loadGeoData = async () => {
    try {
      // Load regions
      const regionsRes = await api.get('/territories/geojson/all?type=region')
      if (map.current && regionsRes.data.features.length > 0) {
        map.current.addSource('regions', { type: 'geojson', data: regionsRes.data })
        map.current.addLayer({ id: 'regions-fill', type: 'fill', source: 'regions',
          paint: { 'fill-color': '#3b82f6', 'fill-opacity': 0.15 } })
        map.current.addLayer({ id: 'regions-line', type: 'line', source: 'regions',
          paint: { 'line-color': '#60a5fa', 'line-width': 2 } })
      }
      // Load communes with priority colors
      const communesRes = await api.get('/territories/geojson/all?type=commune')
      if (map.current && communesRes.data.features.length > 0) {
        map.current.addSource('communes', { type: 'geojson', data: communesRes.data })
        map.current.addLayer({ id: 'communes-fill', type: 'fill', source: 'communes',
          paint: {
            'fill-color': ['match', ['get', 'priority_class'],
              'muy_alta', '#16a34a', 'alta', '#22c55e', 'media', '#eab308', 'baja', '#f97316', 'muy_baja', '#ef4444', '#64748b'],
            'fill-opacity': 0.5
          } })
        map.current.addLayer({ id: 'communes-line', type: 'line', source: 'communes',
          paint: { 'line-color': '#94a3b8', 'line-width': 1 } })
        map.current.addLayer({ id: 'communes-label', type: 'symbol', source: 'communes',
          layout: { 'text-field': ['get', 'name'], 'text-size': 11 },
          paint: { 'text-color': '#ffffff', 'text-halo-color': '#000000', 'text-halo-width': 1 } })
        // Click handler
        map.current.on('click', 'communes-fill', (e) => {
          if (e.features && e.features[0]) {
            setSelectedTerritory(e.features[0].properties)
          }
        })
        map.current.on('mouseenter', 'communes-fill', () => { if (map.current) map.current.getCanvas().style.cursor = 'pointer' })
        map.current.on('mouseleave', 'communes-fill', () => { if (map.current) map.current.getCanvas().style.cursor = '' })
      }
    } catch (err) {
      console.error('Error loading geo data:', err)
    }
  }

  return (
    <div className="flex h-[calc(100vh-120px)] gap-4">
      {/* Layer panel */}
      <div className="w-64 glass-card p-4 space-y-4 overflow-y-auto flex-shrink-0">
        <h3 className="text-sm font-semibold text-white">Capas</h3>
        <div className="space-y-2">
          {[
            { key: 'regions', label: 'Regiones', color: '#3b82f6' },
            { key: 'communes', label: 'Comunas (Prioridad)', color: '#22c55e' },
          ].map((layer) => (
            <label key={layer.key} className="flex items-center gap-2 text-sm text-ocean-300 cursor-pointer hover:text-white transition-colors">
              <input type="checkbox" checked={layerToggles[layer.key as keyof typeof layerToggles]}
                onChange={() => {
                  const next = !layerToggles[layer.key as keyof typeof layerToggles]
                  setLayerToggles(prev => ({ ...prev, [layer.key]: next }))
                  if (map.current) {
                    const vis = next ? 'visible' : 'none'
                    map.current.setLayoutProperty(`${layer.key}-fill`, 'visibility', vis)
                    map.current.setLayoutProperty(`${layer.key}-line`, 'visibility', vis)
                  }
                }}
                className="rounded accent-forest-500" />
              <span className="w-3 h-3 rounded-full" style={{ background: layer.color }}></span>
              {layer.label}
            </label>
          ))}
        </div>

        {/* Legend */}
        <div className="pt-4 border-t border-ocean-700/50">
          <h4 className="text-xs font-semibold text-ocean-400 mb-2 uppercase tracking-wider">Leyenda de prioridad</h4>
          {Object.entries(PRIORITY_COLORS).map(([key, color]) => (
            <div key={key} className="flex items-center gap-2 text-xs text-ocean-300 mb-1">
              <span className="w-3 h-3 rounded" style={{ background: color }}></span>
              {key === 'muy_alta' ? 'Muy Alta' : key === 'alta' ? 'Alta' : key === 'media' ? 'Media' : key === 'baja' ? 'Baja' : 'Muy Baja'}
            </div>
          ))}
        </div>
      </div>

      {/* Map */}
      <div className="flex-1 rounded-xl overflow-hidden border border-ocean-800/50">
        <div ref={mapContainer} className="map-container w-full h-full" />
      </div>

      {/* Info panel */}
      {selectedTerritory && (
        <div className="w-72 glass-card p-4 space-y-3 overflow-y-auto flex-shrink-0 animate-slide-in">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white">Ficha Territorial</h3>
            <button onClick={() => setSelectedTerritory(null)} className="text-ocean-400 hover:text-white text-lg">×</button>
          </div>
          <div className="space-y-2">
            <div><span className="text-xs text-ocean-400">Nombre</span><p className="text-sm text-white font-medium">{selectedTerritory.name}</p></div>
            <div><span className="text-xs text-ocean-400">Código</span><p className="text-sm text-ocean-300">{selectedTerritory.code}</p></div>
            <div><span className="text-xs text-ocean-400">Superficie</span><p className="text-sm text-ocean-300">{selectedTerritory.area_ha?.toLocaleString()} ha</p></div>
            <div><span className="text-xs text-ocean-400">Puntaje de Prioridad</span><p className="text-lg font-bold text-white">{selectedTerritory.priority_score?.toFixed(1) || '—'}</p></div>
            <div>
              <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium badge-${selectedTerritory.priority_class}`}>
                {selectedTerritory.priority_class === 'muy_alta' ? 'Muy Alta' : selectedTerritory.priority_class === 'alta' ? 'Alta' : selectedTerritory.priority_class === 'media' ? 'Media' : selectedTerritory.priority_class === 'baja' ? 'Baja' : 'Muy Baja'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
