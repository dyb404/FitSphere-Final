import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function ProtectedRoute({ children, requiredRole }) {
  const { isAuthenticated, user, loading } = useAuth()

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && user?.role !== requiredRole) {
    // If user is trainer but trying to access client dashboard, redirect to trainer dashboard
    if (requiredRole === 'client' && user?.role === 'trainer') {
      return <Navigate to="/trainer-dashboard" replace />
    }
    // If user is client but trying to access trainer dashboard, redirect to client dashboard
    if (requiredRole === 'trainer' && user?.role === 'client') {
      return <Navigate to="/dashboard" replace />
    }
    return <Navigate to="/" replace />
  }

  return children
}

export default ProtectedRoute

