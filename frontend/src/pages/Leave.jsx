import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api/v1'

function Leave({ onBack }) {
  const [leaveType, setLeaveType] = useState('sick')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [reason, setReason] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/leave/history`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setHistory(response.data.records || [])
    } catch (err) {
      console.error('Failed to load leave history')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const token = localStorage.getItem('token')
      await axios.post(
        `${API_URL}/leave/apply`,
        {
          leave_type: leaveType,
          start_date: startDate,
          end_date: endDate,
          reason: reason
        },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setMessage('Leave application submitted successfully!')
      setLeaveType('sick')
      setStartDate('')
      setEndDate('')
      setReason('')
      setShowForm(false)
      fetchHistory()
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Failed to submit')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-purple-600 text-white p-4 shadow-md">
        <div className="max-w-md mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold">🌴 Leave</h1>
          <button onClick={onBack} className="text-sm bg-purple-700 px-3 py-1 rounded">
            ← Back
          </button>
        </div>
      </header>

      <main className="max-w-md mx-auto p-4">
        {message && (
          <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded-lg text-sm mb-4">
            {message}
          </div>
        )}

        {!showForm && (
          <button
            onClick={() => setShowForm(true)}
            className="w-full bg-purple-500 text-white p-4 rounded-xl shadow hover:bg-purple-600 mb-4"
          >
            + Apply New Leave
          </button>
        )}

        {showForm && (
          <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow p-4 mb-4 space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Leave Type</label>
              <select
                value={leaveType}
                onChange={(e) => setLeaveType(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg"
              >
                <option value="sick">Sick Leave</option>
                <option value="casual">Casual Leave</option>
                <option value="emergency">Emergency Leave</option>
                <option value="vacation">Vacation</option>
                <option value="personal">Personal Leave</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
                className="w-full px-3 py-2 border rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                required
                className="w-full px-3 py-2 border rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Reason</label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                rows="3"
                className="w-full px-3 py-2 border rounded-lg"
                placeholder="Reason for leave..."
              />
            </div>

            <div className="flex gap-2">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-purple-600 text-white py-2 rounded-lg"
              >
                {loading ? 'Submitting...' : 'Submit'}
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        <h3 className="font-bold text-gray-700 mb-2">My Leave History</h3>
        {history.length === 0 && (
          <p className="text-center text-gray-500 text-sm">Koi leave record nahi hai</p>
        )}

        {history.map((leave) => (
          <div key={leave.id} className="bg-white rounded-xl shadow p-4 mb-3">
            <div className="flex justify-between mb-2">
              <span className="font-bold text-gray-800 capitalize">{leave.leave_type}</span>
              <span className={`text-xs px-2 py-1 rounded ${
                leave.status === 'approved' ? 'bg-green-100 text-green-700' :
                leave.status === 'rejected' ? 'bg-red-100 text-red-700' :
                'bg-yellow-100 text-yellow-700'
              }`}>
                {leave.status}
              </span>
            </div>
            <div className="text-sm text-gray-600">
              {new Date(leave.start_date).toLocaleDateString()} → {new Date(leave.end_date).toLocaleDateString()}
            </div>
            {leave.reason && (
              <div className="text-xs text-gray-500 mt-1">{leave.reason}</div>
            )}
          </div>
        ))}
      </main>
    </div>
  )
}

export default Leave