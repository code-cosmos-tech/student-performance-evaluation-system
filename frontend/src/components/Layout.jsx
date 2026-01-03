import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sun, Moon, LogOut, GraduationCap, LayoutDashboard, UserCircle, ShieldCheck } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [darkMode, setDarkMode] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  // Add shadow on scroll
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const NavItem = ({ to, icon: Icon, label }) => {
    const isActive = location.pathname === to;
    return (
      <Link
        to={to}
        className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
          isActive
            ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/30'
            : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
        }`}
      >
        <Icon size={18} />
        <span>{label}</span>
      </Link>
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-100/40 via-slate-50 to-slate-50 dark:from-slate-900 dark:via-slate-950 dark:to-slate-950 transition-colors duration-300">

      {/* Floating Navbar */}
      <div className="fixed top-0 left-0 right-0 z-50 flex justify-center pt-4 px-4">
        <nav className={`w-full max-w-5xl transition-all duration-300 rounded-2xl ${
          scrolled
            ? 'bg-white/80 dark:bg-slate-900/80 backdrop-blur-md shadow-xl border border-white/20 dark:border-slate-800 py-3 px-6'
            : 'bg-transparent py-4 px-4'
        }`}>
          <div className="flex justify-between items-center">

            {/* Logo */}
            <Link to="/" className="flex items-center gap-2 group">
              <div className="bg-indigo-600 p-2 rounded-xl group-hover:rotate-12 transition-transform duration-300 shadow-lg shadow-indigo-500/30">
                <GraduationCap className="h-10 w-10 text-white" />
              </div>
              <span className="font-bold text-lg tracking-tight text-slate-900 dark:text-white">
                  <span className="text-indigo-600 text-2xl">Student Performance</span>
                  <br/>
                  <span className="font-semibold">Evaluation System</span>
              </span>
            </Link>

            {/* Desktop Nav */}
            <div className="hidden md:flex items-center gap-2 bg-white/50 dark:bg-slate-800/50 p-1.5 rounded-full border border-slate-200/50 dark:border-slate-700/50 backdrop-blur-sm">
              {user ? (
                <>
                  <NavItem to="/dashboard" icon={LayoutDashboard} label="Predict" />
                  <NavItem to="/profile" icon={UserCircle} label="Profile" />
                  {user.role === 'ADMIN' && <NavItem to="/admin" icon={ShieldCheck} label="Admin" />}
                </>
              ) : (
                <NavItem to="/" icon={LayoutDashboard} label="Home" />
              )}
            </div>

            {/* Actions */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2.5 rounded-full bg-white dark:bg-slate-800 text-slate-600 dark:text-indigo-400 shadow-sm border border-slate-200 dark:border-slate-700 hover:scale-105 transition-all"
              >
                {darkMode ? <Sun size={18} /> : <Moon size={18} />}
              </button>

              {user ? (
                <button onClick={handleLogout} className="p-2.5 rounded-full bg-red-50 text-red-500 hover:bg-red-100 hover:scale-105 transition-all">
                  <LogOut size={18} />
                </button>
              ) : (
                <Link to="/login" className="px-5 py-2.5 rounded-full bg-indigo-600 text-white font-semibold text-sm shadow-lg shadow-indigo-500/30 hover:bg-indigo-700 transition-all hover:-translate-y-0.5">
                  Sign In
                </Link>
              )}
            </div>
          </div>
        </nav>
      </div>

      {/* Main Content Spacer for Floating Nav */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-12">
        <Outlet />
      </main>
    </div>
  );
}