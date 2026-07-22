import { useState } from 'react'
import { X } from 'lucide-react'
import { addVehicle, updateVehicle } from '../api'

const EMPTY = { make: '', model: '', category: '', price: '', quantity: '' }
const CATEGORIES = ['Sedan', 'SUV', 'Truck', 'Coupe', 'Hatchback', 'Van', 'Electric', 'Hybrid', 'Convertible']

export default function VehicleFormModal({ vehicle, onClose, onSaved }) {
  const isEdit = !!vehicle
  const [form, setForm] = useState(isEdit ? {
    make: vehicle.make,
    model: vehicle.model,
    category: vehicle.category,
    price: vehicle.price,
    quantity: vehicle.quantity,
  } : EMPTY)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const payload = { ...form, price: parseFloat(form.price), quantity: parseInt(form.quantity) }
      if (isEdit) {
        await updateVehicle(vehicle.id, payload)
      } else {
        await addVehicle(payload)
      }
      onSaved()
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={onClose} />

      <div className="relative card p-6 w-full max-w-lg shadow-2xl">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-bold text-white">{isEdit ? 'Edit Vehicle' : 'Add New Vehicle'}</h2>
          <button onClick={onClose} className="p-1.5 hover:bg-slate-800 rounded-lg transition-colors">
            <X className="w-5 h-5 text-slate-400" />
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-950/60 border border-red-800 rounded-xl text-red-300 text-sm">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Make</label>
              <input className="input" placeholder="Toyota" value={form.make}
                onChange={e => setForm({ ...form, make: e.target.value })} required />
            </div>
            <div>
              <label className="label">Model</label>
              <input className="input" placeholder="Camry" value={form.model}
                onChange={e => setForm({ ...form, model: e.target.value })} required />
            </div>
          </div>

          <div>
            <label className="label">Category</label>
            <select className="input" value={form.category}
              onChange={e => setForm({ ...form, category: e.target.value })} required>
              <option value="">Select category…</option>
              {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Price ($)</label>
              <input className="input" type="number" min="0" step="0.01" placeholder="25000"
                value={form.price} onChange={e => setForm({ ...form, price: e.target.value })} required />
            </div>
            <div>
              <label className="label">Quantity</label>
              <input className="input" type="number" min="0" placeholder="10"
                value={form.quantity} onChange={e => setForm({ ...form, quantity: e.target.value })} required />
            </div>
          </div>

          <div className="flex gap-3 pt-2">
            <button type="button" onClick={onClose} className="btn-ghost flex-1">Cancel</button>
            <button type="submit" disabled={loading} className="btn-primary flex-1 flex items-center justify-center gap-2">
              {loading && <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />}
              {loading ? 'Saving…' : (isEdit ? 'Save Changes' : 'Add Vehicle')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
