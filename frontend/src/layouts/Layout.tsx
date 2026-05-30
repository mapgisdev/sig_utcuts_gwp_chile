import { useEffect } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAppStore, useAuthStore } from '../store/store'

const navItems = [
  { path: '/', label: 'Inicio', icon: '📊' },
  { path: '/mapa', label: 'Mapa', icon: '🗺️' },
  { path: '/mecanismos', label: 'Mecanismos', icon: '⚙️' },
  { path: '/inversiones', label: 'Inversiones', icon: '💰' },
  { path: '/priorizacion', label: 'Priorización', icon: '🎯' },
  { path: '/mrv', label: 'MRV', icon: '📋' },
  { path: '/brechas', label: 'Brechas', icon: '⚠️' },
  { path: '/reportes', label: 'Reportes', icon: '📄' },
  { path: '/carga', label: 'Carga de Datos', icon: '📤' },
]

export default function Layout() {
  const { sidebarOpen, toggleSidebar } = useAppStore()
  const { token, logout } = useAuthStore()
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) {
      navigate('/login')
    }
  }, [token, navigate])

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-16'} bg-gradient-to-b from-ocean-900 to-ocean-800 border-r border-ocean-800/50 flex flex-col transition-all duration-300 ease-in-out`}>
        {/* Logo */}
        <div className="p-4 border-b border-ocean-800/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-forest-500 to-forest-700 rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-lg shadow-forest-500/20">
              SIG
            </div>
            {sidebarOpen && (
              <div className="animate-fade-in">
                <h1 className="text-sm font-bold text-white leading-tight">SIG-UTCUTS</h1>
                <p className="text-xs text-ocean-300">Chile</p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 space-y-1 px-2 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-forest-600/20 text-forest-400 border border-forest-500/30 shadow-sm shadow-forest-500/10'
                    : 'text-ocean-300 hover:bg-ocean-800/50 hover:text-white'
                }`
              }
            >
              <span className="text-lg">{item.icon}</span>
              {sidebarOpen && <span>{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        {/* Cerrar Sesión */}
        <button
          onClick={logout}
          className="flex items-center gap-3 px-3 py-2.5 mx-2 mb-2 rounded-lg text-sm font-medium text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-all duration-200"
        >
          <span className="text-lg">🚪</span>
          {sidebarOpen && <span>Cerrar Sesión</span>}
        </button>

        {/* Toggle */}
        <button
          onClick={toggleSidebar}
          className="p-3 border-t border-ocean-800/50 text-ocean-400 hover:text-white transition-colors text-sm"
        >
          {sidebarOpen ? '◀ Contraer' : '▶'}
        </button>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto bg-ocean-900">
        {/* Top bar */}
        <header className="sticky top-0 z-10 bg-ocean-900/80 backdrop-blur-xl border-b border-ocean-800/50 px-6 py-3">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-lg font-semibold text-white">
              SIG de Inversiones e Intervenciones UTCUTS
            </h2>
          </div>
        </header>

        {/* Page content */}
        <div className="p-6 animate-fade-in">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
