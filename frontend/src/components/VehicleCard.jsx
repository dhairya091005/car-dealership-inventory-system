import { useState } from 'react'
import { ShoppingCart, Pencil, Trash2, Package, RotateCcw } from 'lucide-react'
import { purchaseVehicle, deleteVehicle, restockVehicle } from '../api'
import { useAuth } from '../context/AuthContext'

export default function VehicleCard({ vehicle, onRefresh, onEdit }) {
  const { isAdmin } = useAuth()
  const [purchasing, setPurchasing] = useState(false)
  const [restocking, setRestocking] = useState(false)
  const [restockQty, setRestockQty] = useState('')
  const [showRestock, setShowRestock] = useState(false)
  const [msg, setMsg] = useState(null) // { text, type: 'success'|'error' }

  const flash = (text, type = 'success') => {
    setMsg({ text, type })
    setTimeout(() => setMsg(null), 3000)
  }

  const handlePurchase = async () => {
    setPurchasing(true)
    try {
      await purchaseVehicle(vehicle.id)
      flash('Purchase successful!')
      onRefresh()
    } catch (err) {
      flash(err.response?.data?.detail || 'Purchase failed', 'error')
    } finally {
      setPurchasing(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm(`Delete ${vehicle.make} ${vehicle.model}?`)) return
    try {
      await deleteVehicle(vehicle.id)
      onRefresh()
    } catch (err) {
      flash(err.response?.data?.detail || 'Delete failed', 'error')
    }
  }

  const handleRestock = async () => {
    const qty = parseInt(restockQty)
    if (!qty || qty <= 0) return flash('Enter a valid quantity', 'error')
    setRestocking(true)
    try {
      await restockVehicle(vehicle.id, qty)
      flash(`Restocked +${qty} units!`)
      setRestockQty('')
      setShowRestock(false)
      onRefresh()
    } catch (err) {
      flash(err.response?.data?.detail || 'Restock failed', 'error')
    } finally {
      setRestocking(false)
    }
  }

  const inStock = vehicle.quantity > 0

  return (
    <div className="card p-5 flex flex-col gap-4 hover:border-slate-700 transition-colors group">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <span className="badge bg-blue-950 text-blue-300 border border-blue-800">
            {vehicle.category}
          </span>
          <h3 className="mt-2 text-lg font-bold text-white leading-tight">
            {vehicle.make} {vehicle.model}
          </h3>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-white">
            ${vehicle.price.toLocaleString()}
          </div>
          <div className={`text-xs font-medium mt-0.5 flex items-center justify-end gap-1 ${inStock ? 'text-emerald-400' : 'text-red-400'}`}>
            <Package className="w-3 h-3" />
            {inStock ? `${vehicle.quantity} in stock` : 'Out of stock'}
          </div>
        </div>
      </div>

      {/* Flash message */}
      {msg && (
        <div className={`text-xs px-3 py-2 rounded-lg ${msg.type === 'success' ? 'bg-emerald-950/60 text-emerald-300 border border-emerald-800' : 'bg-red-950/60 text-red-300 border border-red-800'}`}>
          {msg.text}
        </div>
      )}

      {/* Restock input (admin only) */}
      {isAdmin && showRestock && (
        <div className="flex gap-2">
          <input
            type="number"
            min="1"
            placeholder="Qty to add"
            className="input text-sm py-2 flex-1"
            value={restockQty}
            onChange={e => setRestockQty(e.target.value)}
          />
          <button
            onClick={handleRestock}
            disabled={restocking}
            className="btn-primary text-sm py-2 px-4 flex items-center gap-1"
          >
            {restocking
              ? <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              : <RotateCcw className="w-3.5 h-3.5" />}
            Add
          </button>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-2 mt-auto pt-2 border-t border-slate-800">
        <button
          id={`purchase-${vehicle.id}`}
          onClick={handlePurchase}
          disabled={!inStock || purchasing}
          className="btn-primary flex-1 flex items-center justify-center gap-2 text-sm py-2"
        >
          {purchasing
            ? <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            : <ShoppingCart className="w-3.5 h-3.5" />}
          {!inStock ? 'Out of Stock' : purchasing ? 'Processing…' : 'Purchase'}
        </button>

        {isAdmin && (
          <>
            <button
              onClick={() => setShowRestock(v => !v)}
              className="btn-ghost p-2 text-blue-400 hover:text-blue-300"
              title="Restock"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              onClick={() => onEdit(vehicle)}
              className="btn-ghost p-2 text-amber-400 hover:text-amber-300"
              title="Edit"
            >
              <Pencil className="w-4 h-4" />
            </button>
            <button
              onClick={handleDelete}
              className="btn-ghost p-2 text-red-400 hover:text-red-300"
              title="Delete"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </>
        )}
      </div>
    </div>
  )
}
