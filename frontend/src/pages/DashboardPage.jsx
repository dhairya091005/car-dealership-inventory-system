import { useState, useEffect, useCallback } from 'react'
import { Plus, Search, LogOut, Car, Shield, RefreshCw } from 'lucide-react'
import { getVehicles, searchVehicles } from '../api'
import { useAuth } from '../context/AuthContext'
import VehicleCard from '../components/VehicleCard'
import VehicleFormModal from '../components/VehicleFormModal'

export default function DashboardPage() {
  const { user, isAdmin, signOut } = useAuth()
  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchForm, setSearchForm] = useState({ make: '', model: '', category: '', min_price: '', max_price: '' })
  const [searching, setSearching] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [editVehicle, setEditVehicle] = useState(null)

  const fetchVehicles = useCallback(async () => {
    setLoading(true)
    try {
      const res = await getVehicles()
      setVehicles(res.data)
    } catch {
      /* handled silently */
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchVehicles() }, [fetchVehicles])

  const handleSearch = async (e) => {
    e.preventDefault()
    setSearching(true)
    try {
      const params = {}
      if (searchForm.make) params.make = searchForm.make
      if (searchForm.model) params.model = searchForm.model
      if (searchForm.category) params.category = searchForm.category
      if (searchForm.min_price) params.min_price = parseFloat(searchForm.min_price)
      if (searchForm.max_price) params.max_price = parseFloat(searchForm.max_price)
      const res = await searchVehicles(params)
      setVehicles(res.data)
    } catch {
      /* handled silently */
    } finally {
      setSearching(false)
    }
  }

  const handleReset = () => {
    setSearchForm({ make: '', model: '', category: '', min_price: '', max_price: '' })
    fetchVehicles()
  }

  const handleEdit = (vehicle) => {
    setEditVehicle(vehicle)
    setShowModal(true)
  }

  const handleModalClose = () => {
    setShowModal(false)
    setEditVehicle(null)
  }

  const handleSaved = () => {
    handleModalClose()
    fetchVehicles()
  }

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Navbar */}
      <nav className="sticky top-0 z-40 bg-slate-950/80 backdrop-blur-xl border-b border-slate-800 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Car className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-white text-lg">DriveDesk</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-slate-400">
              {isAdmin && (
                <span className="badge bg-amber-950 text-amber-300 border border-amber-800 flex items-center gap-1">
                  <Shield className="w-3 h-3" /> Admin
                </span>
              )}
              <span>{user?.username}</span>
            </div>
            <button onClick={signOut} className="btn-ghost py-2 px-3 flex items-center gap-2 text-sm">
              <LogOut className="w-4 h-4" /> Sign Out
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Inventory</h1>
            <p className="text-slate-400 mt-1 text-sm">{vehicles.length} vehicles available</p>
          </div>
          <div className="flex gap-3">
            <button onClick={fetchVehicles} className="btn-ghost p-2.5" title="Refresh">
              <RefreshCw className="w-4 h-4" />
            </button>
            {isAdmin && (
              <button id="add-vehicle-btn" onClick={() => setShowModal(true)} className="btn-primary flex items-center gap-2">
                <Plus className="w-4 h-4" /> Add Vehicle
              </button>
            )}
          </div>
        </div>

        {/* Search & Filter */}
        <div className="card p-5 mb-8">
          <form onSubmit={handleSearch} className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            <div className="lg:col-span-1">
              <label className="label">Make</label>
              <input className="input text-sm py-2" placeholder="Toyota"
                value={searchForm.make} onChange={e => setSearchForm({ ...searchForm, make: e.target.value })} />
            </div>
            <div className="lg:col-span-1">
              <label className="label">Model</label>
              <input className="input text-sm py-2" placeholder="Camry"
                value={searchForm.model} onChange={e => setSearchForm({ ...searchForm, model: e.target.value })} />
            </div>
            <div className="lg:col-span-1">
              <label className="label">Category</label>
              <input className="input text-sm py-2" placeholder="SUV"
                value={searchForm.category} onChange={e => setSearchForm({ ...searchForm, category: e.target.value })} />
            </div>
            <div className="lg:col-span-1">
              <label className="label">Min Price</label>
              <input className="input text-sm py-2" type="number" placeholder="10000"
                value={searchForm.min_price} onChange={e => setSearchForm({ ...searchForm, min_price: e.target.value })} />
            </div>
            <div className="lg:col-span-1">
              <label className="label">Max Price</label>
              <input className="input text-sm py-2" type="number" placeholder="80000"
                value={searchForm.max_price} onChange={e => setSearchForm({ ...searchForm, max_price: e.target.value })} />
            </div>
            <div className="lg:col-span-1 flex items-end gap-2">
              <button id="search-btn" type="submit" disabled={searching} className="btn-primary flex-1 py-2 text-sm flex items-center justify-center gap-1.5">
                <Search className="w-3.5 h-3.5" /> Search
              </button>
              <button type="button" onClick={handleReset} className="btn-ghost py-2 px-3 text-sm">
                Reset
              </button>
            </div>
          </form>
        </div>

        {/* Vehicle Grid */}
        {loading ? (
          <div className="flex justify-center items-center py-24">
            <div className="w-10 h-10 border-2 border-slate-700 border-t-blue-500 rounded-full animate-spin" />
          </div>
        ) : vehicles.length === 0 ? (
          <div className="text-center py-24">
            <Car className="w-16 h-16 text-slate-700 mx-auto mb-4" />
            <p className="text-slate-500 text-lg">No vehicles found</p>
            <p className="text-slate-600 text-sm mt-1">Try adjusting your search filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {vehicles.map(v => (
              <VehicleCard
                key={v.id}
                vehicle={v}
                onRefresh={fetchVehicles}
                onEdit={handleEdit}
              />
            ))}
          </div>
        )}
      </div>

      {/* Add / Edit Modal */}
      {showModal && (
        <VehicleFormModal
          vehicle={editVehicle}
          onClose={handleModalClose}
          onSaved={handleSaved}
        />
      )}
    </div>
  )
}
