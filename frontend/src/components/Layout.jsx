import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sun, Moon, LogOut, GraduationCap, User, LayoutDashboard } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [darkMode, setDarkMode] = useState(false);

  // Handle Dark Mode Class
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-200">
      {/* Navbar */}
      <nav className="border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center gap-2">
              <GraduationCap className="h-8 w-8 text-indigo-600 dark:text-indigo-400" />
              <Link to="/" className="font-bold text-indigo-600 text-xl tracking-tight">Student Performance Evalution System</Link>
            </div>

            <div className="flex items-center gap-6">
              {user && (
                <>
                  <Link to="/dashboard" className="hover:text-indigo-600 text-sm font-medium">Predict</Link>
                  <Link to="/profile" className="hover:text-indigo-600 text-sm font-medium">Profile</Link>
                  {user.role === 'ADMIN' && (
                     <Link to="/admin" className="hover:text-indigo-600 text-sm font-medium">Admin Panel</Link>
                  )}
                </>
              )}
              
              <button onClick={() => setDarkMode(!darkMode)} className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800">
                {darkMode ? <Sun size={20} /> : <Moon size={20} />}
              </button>

              {user ? (
                <button onClick={handleLogout} className="text-red-500 hover:text-red-600">
                  <LogOut size={20} />
                </button>
              ) : (
                <Link to="/login" className="text-sm font-medium hover:text-indigo-600">Login</Link>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
}