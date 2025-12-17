import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import "../cssfiles/TrainerDashboard.css";
import {
  getClients,
  getMyCreatedWorkouts,
  createWorkout,
  updateWorkout,
  deleteWorkout,
  getAssignments,
  assignWorkout,
  removeAssignment,
  getMyProgressLogs
} from '../api/api'
import Modal from '../components/Modal'

function TrainerDashboard() {
  const { user } = useAuth()
  const [clients, setClients] = useState([])
  const [workouts, setWorkouts] = useState([])
  const [assignments, setAssignments] = useState([])
  const [progressLogs, setProgressLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [showWorkoutModal, setShowWorkoutModal] = useState(false)
  const [showAssignModal, setShowAssignModal] = useState(false)
  const [editingWorkout, setEditingWorkout] = useState(null)
  const [workoutForm, setWorkoutForm] = useState({ title: '', description: '' })
  const [assignForm, setAssignForm] = useState({ clientId: '', workoutId: '' })
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (user?.id) {
      fetchData()
    }
  }, [user])

  const fetchData = async () => {
    if (!user?.id) return
    
    try {
      setLoading(true)
      const [clientsData, workoutsData, assignmentsData, logsData] = await Promise.all([
        getClients(),
        getMyCreatedWorkouts(user.id),
        getAssignments(user.id),
        getMyProgressLogs()
      ])
      setClients(clientsData)
      setWorkouts(workoutsData)
      setAssignments(assignmentsData)
      setProgressLogs(logsData)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateWorkout = async (e) => {
    e.preventDefault()
    setSubmitting(true)

    try {
      if (editingWorkout) {
        await updateWorkout(editingWorkout.id, workoutForm, user.id)
      } else {
        await createWorkout(workoutForm, user.id)
      }
      await fetchData()
      setShowWorkoutModal(false)
      setEditingWorkout(null)
      setWorkoutForm({ title: '', description: '' })
    } catch (error) {
      console.error('Error saving workout:', error)
      alert('Failed to save workout. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleEditWorkout = (workout) => {
    setEditingWorkout(workout)
    setWorkoutForm({ title: workout.title, description: workout.description || '' })
    setShowWorkoutModal(true)
  }

  const handleDeleteWorkout = async (id) => {
    if (!window.confirm('Are you sure you want to delete this workout?')) {
      return
    }

    try {
      await deleteWorkout(id, user.id)
      await fetchData()
    } catch (error) {
      console.error('Error deleting workout:', error)
      alert('Failed to delete workout. Please try again.')
    }
  }

  const handleAssignWorkout = async (e) => {
    e.preventDefault()
    setSubmitting(true)

    try {
      await assignWorkout(parseInt(assignForm.clientId), parseInt(assignForm.workoutId))
      await fetchData()
      setShowAssignModal(false)
      setAssignForm({ clientId: '', workoutId: '' })
    } catch (error) {
      console.error('Error assigning workout:', error)
      alert(error.response?.data?.detail || 'Failed to assign workout. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleRemoveAssignment = async (id) => {
    if (!window.confirm('Are you sure you want to remove this assignment?')) {
      return
    }

    try {
      await removeAssignment(id)
      await fetchData()
    } catch (error) {
      console.error('Error removing assignment:', error)
      alert('Failed to remove assignment. Please try again.')
    }
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard-page">
      <div className="container">
        <div className="dashboard-header">
          <h1>Welcome, {user?.name}!</h1>
          <p>Manage your clients, workouts, and assignments</p>
        </div>

        <div className="dashboard-flexbox-1">
          <section className="dashboard-section-trainer">
            <h2>Clients</h2>
            {clients.length === 0 ? (
              <div className="empty-state">
                <p>No clients yet.</p>
              </div>
            ) : (
              <div className="clients-grid">
                {clients.map((client) => (
                  <div key={client.id} className="client-card">
                    <h3>{client.name}</h3>
                    <p>{client.email}</p>
                  </div>
                ))}
              </div>
            )}
          </section>
          <section className="dashboard-section-trainer">
            <h2>All Progress Logs</h2>
            {progressLogs.length === 0 ? (
              <div className="empty-state">
                <p>No progress logs yet.</p>
              </div>
            ) : (
              <div className="progress-table-container">
                <table className="progress-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Weight (kg)</th>
                      <th>Calories</th>
                      <th>Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {progressLogs.map((log) => (
                      <tr key={log.id}>
                        <td>{new Date(log.date).toLocaleDateString()}</td>
                        <td>{log.weight || '-'}</td>
                        <td>{log.calories || '-'}</td>
                        <td>{log.notes || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
          
        </div>
        <div className='dashboard-flexbox-2'>
          <section className="dashboard-section-trainer">
            <div className="section-header">
              <h2>Assign Workouts</h2>
              <button
                className="assgnworkoutbtn"
                onClick={() => setShowAssignModal(true)}
              >
                Assign Workout
              </button>
            </div>

            {assignments.length === 0 ? (
              <div className="empty-state">
                <p>No assignments yet. Assign workouts to your clients!</p>
              </div>
            ) : (
              <div className="assignments-list">
                {assignments.map((assignment) => (
                  <div key={assignment.id} className="assignment-card">
                    <div>
                      <strong>{assignment.client_name}</strong> - {assignment.workout_title}
                    </div>
                    <button
                      className="btn-delete"
                      onClick={() => handleRemoveAssignment(assignment.id)}
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>
          <section className="dashboard-section-trainer">
            <div className="section-header">
              <h2>My Workouts</h2>
              <button
                className="createworkoutbtn"
                onClick={() => {
                  setEditingWorkout(null)
                  setWorkoutForm({ title: '', description: '' })
                  setShowWorkoutModal(true)
                }}
              >
                Create Workout
              </button>
            </div>

            {workouts.length === 0 ? (
              <div className="empty-state">
                <p>No workouts created yet. Create your first workout!</p>
              </div>
            ) : (
              <div className="workouts-list">
                {workouts.map((workout) => (
                  <div key={workout.id} className="workout-card">
                    <h3>{workout.title}</h3>
                    {workout.description && (
                      <p className="workout-description">{workout.description}</p>
                    )}
                    <div className="workout-actions">
                      <button
                        className="btn"
                        onClick={() => handleEditWorkout(workout)}
                      >
                        Edit
                      </button>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDeleteWorkout(workout.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>  
          
        </div>
        
      </div>

      <Modal
        isOpen={showWorkoutModal}
        onClose={() => {
          setShowWorkoutModal(false)
          setEditingWorkout(null)
          setWorkoutForm({ title: '', description: '' })
        }}
        title={editingWorkout ? 'Edit Workout' : 'Create Workout'}
      >
        <form onSubmit={handleCreateWorkout} className="form">
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              id="title"
              value={workoutForm.title}
              onChange={(e) => setWorkoutForm({ ...workoutForm, title: e.target.value })}
              required
              disabled={submitting}
              placeholder="Enter workout title"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              value={workoutForm.description}
              onChange={(e) => setWorkoutForm({ ...workoutForm, description: e.target.value })}
              disabled={submitting}
              placeholder="Enter workout description"
              rows="4"
            />
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => {
                setShowWorkoutModal(false)
                setEditingWorkout(null)
                setWorkoutForm({ title: '', description: '' })
              }}
              disabled={submitting}
            >
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Saving...' : editingWorkout ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={showAssignModal}
        onClose={() => {
          setShowAssignModal(false)
          setAssignForm({ clientId: '', workoutId: '' })
        }}
        title="Assign Workout to Client"
      >
        <form onSubmit={handleAssignWorkout} className="form">
          <div className="form-group">
            <label htmlFor="clientId">Client</label>
            <select
              id="clientId"
              value={assignForm.clientId}
              onChange={(e) => setAssignForm({ ...assignForm, clientId: e.target.value })}
              required
              disabled={submitting}
            >
              <option value="">Select a client</option>
              {clients.map((client) => (
                <option key={client.id} value={client.id}>
                  {client.name} ({client.email})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="workoutId">Workout</label>
            <select
              id="workoutId"
              value={assignForm.workoutId}
              onChange={(e) => setAssignForm({ ...assignForm, workoutId: e.target.value })}
              required
              disabled={submitting}
            >
              <option value="">Select a workout</option>
              {workouts.map((workout) => (
                <option key={workout.id} value={workout.id}>
                  {workout.title}
                </option>
              ))}
            </select>
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => {
                setShowAssignModal(false)
                setAssignForm({ clientId: '', workoutId: '' })
              }}
              disabled={submitting}
            >
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Assigning...' : 'Assign'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default TrainerDashboard

