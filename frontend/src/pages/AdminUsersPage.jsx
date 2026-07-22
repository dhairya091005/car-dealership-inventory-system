import { useState, useEffect, useCallback } from 'react'
import { Shield, ShieldAlert, ArrowLeft, UserPlus, Users } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { getUsers, promoteUser } from '../api'
import { useAuth } from '../context/AuthContext'

export default function AdminUsersPage() {
  const { user, isAdmin } = useAuth()
  const navigate = useNavigate()
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [promoteEmail, setPromoteEmail] = useState('')
  const [promoteLoading, setPromoteLoading] = useState(false)
  const [msg, setMsg] = useState(null)

  const flash = (text, type = 'success') => {
    setMsg({ text, type })
    setTimeout(() => setMsg(null), 3000)
  }

  const fetchUsers = useCallback(async () => {
    setLoading(true)
    try {
      const res = await getUsers()
      setUsers(res.data)
    } catch (err) {
      flash('Failed to load users', 'error')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (!isAdmin) {
      navigate('/dashboard')
      return
    }
    fetchUsers()
  }, [isAdmin, navigate, fetchUsers])

  const handlePromote = async (e) => {
    e.preventDefault()
    if (!promoteEmail) return
    
    setPromoteLoading(true)
    try {
      await promoteUser(promoteEmail)
      flash(`Successfully promoted ${promoteEmail} to ADMIN!`)
      setPromoteEmail('')
      fetchUsers()
    } catch (err) {
      flash(err.response?.data?.detail || 'Failed to promote user', 'error')
    } finally {
      setPromoteLoading(false)
    }
  }

  if (!isAdmin) return null // Handled by useEffect redirect

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Navbar Minimal */}
      <nav className="sticky top-0 z-40 bg-slate-950/80 backdrop-blur-xl border-b border-slate-800 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-4">
          <Link to="/dashboard" className="btn-ghost p-2 -ml-2" title="Back to Dashboard">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <span className="font-bold text-white text-lg flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-500" /> Admin Panel
          </span>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-8">
        {msg && (
          <div className={`mb-6 p-4 rounded-xl text-sm border flex items-center justify-between ${
            msg.type === 'success' 
              ? 'bg-emerald-950/60 text-emerald-300 border-emerald-800' 
              : 'bg-red-950/60 text-red-300 border-red-800'
          }`}>
            {msg.text}
          </div>
        )}

        <div className="grid md:grid-cols-3 gap-6">
          {/* Promote Form */}
          <div className="md:col-span-1 space-y-6">
            <div className="card p-6">
              <div className="flex items-center gap-2 mb-4">
                <UserPlus className="w-5 h-5 text-blue-400" />
                <h2 className="text-lg font-semibold text-white">Promote User</h2>
              </div>
              <p className="text-slate-400 text-sm mb-4">
                Grant administrator privileges to an existing user by entering their email address.
              </p>
              
              <form onSubmit={handlePromote} className="space-y-4">
                <div>
                  <label className="label">User Email</label>
                  <input 
                    type="email" 
                    placeholder="user@example.com"
                    className="input"
                    value={promoteEmail}
                    onChange={e => setPromoteEmail(e.target.value)}
                    required
                  />
                </div>
                <button 
                  type="submit" 
                  disabled={promoteLoading} 
                  className="btn-primary w-full flex justify-center gap-2"
                >
                  {promoteLoading 
                    ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    : <Shield className="w-4 h-4" />
                  }
                  Make Admin
                </button>
              </form>
            </div>
          </div>

          {/* User List */}
          <div className="md:col-span-2">
            <div className="card p-6 h-full">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <Users className="w-5 h-5 text-blue-400" />
                  <h2 className="text-lg font-semibold text-white">All Users</h2>
                </div>
                <span className="badge bg-slate-800 text-slate-300 border border-slate-700">
                  {users.length} Total
                </span>
              </div>

              {loading ? (
                <div className="flex justify-center py-12">
                  <div className="w-8 h-8 border-2 border-slate-700 border-t-blue-500 rounded-full animate-spin" />
                </div>
              ) : (
                <div className="space-y-3">
                  {users.map(u => (
                    <div key={u.id} className="flex items-center justify-between p-4 rounded-xl bg-slate-950/50 border border-slate-800/50">
                      <div>
                        <div className="font-medium text-slate-200">{u.username}</div>
                        <div className="text-sm text-slate-500">{u.email}</div>
                      </div>
                      <div>
                        {u.role === 'ADMIN' ? (
                          <span className="badge bg-amber-950/80 text-amber-300 border border-amber-800">
                            ADMIN
                          </span>
                        ) : (
                          <span className="badge bg-slate-800 text-slate-400 border border-slate-700">
                            USER
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
