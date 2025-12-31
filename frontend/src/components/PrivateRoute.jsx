import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Loader2 } from 'lucide-react';

const PrivateRoute = ({ role }) => {
  const { user, loading } = useAuth();

  // 1. Show a loader while checking the token/state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <Loader2 className="h-8 w-8 animate-spin text-indigo-600" />
      </div>
    );
  }

  // 2. If no user is logged in, redirect to login
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // 3. If a specific role is required (e.g., 'ADMIN') and user doesn't have it
  if (role && user.role !== role) {
    // Redirect to home or an unauthorized page
    return <Navigate to="/" replace />;
  }

  // 4. If all checks pass, render the child routes
  return <Outlet />;
};

export default PrivateRoute;