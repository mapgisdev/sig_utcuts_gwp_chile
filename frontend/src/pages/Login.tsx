import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import { useAuthStore } from '../store/store'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { setAuth } = useAuthStore()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const form = new URLSearchParams()
      form.append('username', username)
      form.append('password', password)
      const r = await api.post('/auth/login', form, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
      setAuth(r.data.access_token, { username })
      navigate('/')
    } catch {
      setError('Credenciales inválidas')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-ocean-900 via-ocean-800 to-forest-900 flex items-center justify-center p-4">
      <div className="glass-card w-full max-w-md p-8 animate-fade-in">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-forest-500 to-forest-700 rounded-2xl flex items-center justify-center text-white font-bold text-xl mx-auto mb-4 shadow-lg shadow-forest-500/30">
            SIG
          </div>
          <h1 className="text-2xl font-bold text-white">SIG-UTCUTS Chile</h1>
          <p className="text-ocean-400 text-sm mt-1">Plataforma de Inteligencia Territorial</p>
        </div>
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="text-xs text-ocean-400 block mb-1">Usuario</label>
            <input type="text" value={username} onChange={e => setUsername(e.target.value)}
              className="w-full bg-ocean-800 border border-ocean-700 rounded-lg px-4 py-2.5 text-sm text-white focus:border-forest-500 focus:outline-none transition-colors" placeholder="admin" />
          </div>
          <div>
            <label className="text-xs text-ocean-400 block mb-1">Contraseña</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)}
              className="w-full bg-ocean-800 border border-ocean-700 rounded-lg px-4 py-2.5 text-sm text-white focus:border-forest-500 focus:outline-none transition-colors" placeholder="••••••" />
          </div>
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button type="submit" className="w-full py-2.5 bg-gradient-to-r from-forest-600 to-forest-700 hover:from-forest-500 hover:to-forest-600 text-white rounded-lg text-sm font-medium transition-all shadow-lg shadow-forest-500/20">
            Iniciar Sesión
          </button>
        </form>
        <div className="mt-6 text-center">
          <p className="text-xs text-ocean-500">Usuarios demo: admin/admin123, editor/editor123, viewer/viewer123</p>
        </div>
      </div>
    </div>
  )
}
