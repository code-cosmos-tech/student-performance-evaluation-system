import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Login from './pages/Login';
import Home from './pages/Home'; // Import the new Home page
import Prediction from './pages/Prediction';
import Admin from './pages/Admin';
import PrivateRoute from './components/PrivateRoute';
import Profile from './components/Profile';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      
      <Route element={<Layout />}>
        {/* Public Route */}
        <Route path="/" element={<Home />} />

        {/* Protected Routes */}
        <Route element={<PrivateRoute />}>
           {/* Moved Prediction to /dashboard */}
           <Route path="/dashboard" element={<Prediction />} />
           <Route path="/profile" element={<Profile />} />
        </Route>

        {/* Admin Route */}
        <Route element={<PrivateRoute role="ADMIN" />}>
           <Route path="/admin" element={<Admin />} />
        </Route>
      </Route>
    </Routes>
  );
}