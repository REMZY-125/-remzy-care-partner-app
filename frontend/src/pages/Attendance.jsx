import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api/v1'

function Attendance({ onBack }) {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/attendance/history`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setRecords(response.data.records || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load history')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <div className="max-w-md mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold">📅 Attendance</h1>
          <button onClick={onBack} className="text-sm bg-blue-700 px-3 py-1 rounded">
            ← Back
          </button>
        </div>
      </header>

      <main className="max-w-md mx-auto p-4">
        {loading && <p className="text-center text-gray-500">Loading...</p>}
        {error && <p className="text-center text-red-500">{error}</p>}

        {!loading && records.length === 0 && (
          <p className="text-center text-gray-500">Koi attendance record nahi hai</p>
        )}

        {records.map((record) => (
          <div key={record.id} className="bg-white rounded-xl shadow p-4 mb-3">
            <div className="flex justify-between mb-2">
              <span className="font-bold text-gray-800">
                {new Date(record.date).toLocaleDateString('en-IN', { 
                  day: 'numeric', month: 'short', year: 'numeric' 
                })}
              </span>
              <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                {record.status}
              </span>
            </div>
            <div className="text-sm text-gray-600">
              {record.check_in && (
                <div>✅ Check In: {new Date(record.check_in).toLocaleTimeString()}</div>
              )}
              {record.check_out && (
                <div>🚪 Check Out: {new Date(record.check_out).toLocaleTimeString()}</div>
              )}
            </div>
          </div>
        ))}
      </main>
    </div>
  )
}

export default Attendance