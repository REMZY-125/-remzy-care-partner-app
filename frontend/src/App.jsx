import { useState } from 'react'
import axios from 'axios'
import Attendance from './pages/Attendance'
import Leave from './pages/Leave'

const API_URL = 'http://localhost:8000/api/v1'

function App() {
  const [phone, setPhone] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [loggedIn, setLoggedIn] = useState(false)
  const [user, setUser] = useState(null)
  const [attendance, setAttendance] = useState(null)
  const [page, setPage] = useState('dashboard')

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        phone: phone,
        password: password,
      })

      const data = response.data
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data))
      setUser(data)
      setLoggedIn(true)
      setMessage('')
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.detail || 'Login fail ho gaya')
      } else {
        setMessage('Server se connection nahi ho raha')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setLoggedIn(false)
    setUser(null)
    setPhone('')
    setPassword('')
    setAttendance(null)
    setPage('dashboard')
  }

  const handleCheckIn = async () => {
    setMessage('')
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `${API_URL}/attendance/check-in`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setMessage(response.data.message || 'Check-in successful!')
      setAttendance(response.data.attendance)
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Check-in failed')
    }
  }

  const handleCheckOut = async () => {
    setMessage('')
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `${API_URL}/attendance/check-out`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setMessage(response.data.message || 'Check-out successful!')
      setAttendance(response.data.attendance)
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Check-out failed')
    }
  }

  if (!loggedIn) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
          <div className="text-center mb-6">
            <h1 className="text-3xl font-bold text-gray-800">🏥 Remzy</h1>
            <p className="text-gray-500 mt-1">Care Partner Login</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Phone Number
              </label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="9999999999"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="test123"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {message && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                {message}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold py-3 rounded-lg transition"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <p className="text-center text-xs text-gray-400 mt-6">
            Test: 9999999999 / test123
          </p>
        </div>
      </div>
    )
  }

  if (page === 'attendance') {
    return <Attendance onBack={() => setPage('dashboard')} />
  }

  if (page === 'leave') {
    return <Leave onBack={() => setPage('dashboard')} />
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <div className="max-w-md mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold">🏥 Remzy</h1>
          <button
            onClick={handleLogout}
            className="text-sm bg-blue-700 px-3 py-1 rounded hover:bg-blue-800"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="max-w-md mx-auto p-4">
        <div className="bg-white rounded-xl shadow p-6 mb-4">
          <h2 className="text-2xl font-bold text-gray-800">
            Namaste, {user?.full_name}!
          </h2>
          <p className="text-gray-500 text-sm mt-1">Aaj ka din shubh ho</p>
        </div>

        {message && (
          <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded-lg text-sm mb-4">
            {message}
          </div>
        )}

        {attendance && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm mb-4">
            {attendance.check_in && `Check-in: ${new Date(attendance.check_in).toLocaleTimeString()}`}
            {attendance.check_out && ` | Check-out: ${new Date(attendance.check_out).toLocaleTimeString()}`}
          </div>
        )}

        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={handleCheckIn}
            className="bg-green-500 text-white p-4 rounded-xl shadow hover:bg-green-600 transition"
          >
            ✅ Check In
          </button>
          <button
            onClick={handleCheckOut}
            className="bg-red-500 text-white p-4 rounded-xl shadow hover:bg-red-600 transition"
          >
            🚪 Check Out
          </button>
          <button
            onClick={() => setPage('attendance')}
            className="bg-blue-500 text-white p-4 rounded-xl shadow hover:bg-blue-600 transition"
          >
            📅 Attendance
          </button>
          <button
            onClick={() => setPage('leave')}
            className="bg-purple-500 text-white p-4 rounded-xl shadow hover:bg-purple-600 transition"
          >
            🌴 Leave
          </button>
        </div>
      </main>
    </div>
  )
}

export default App