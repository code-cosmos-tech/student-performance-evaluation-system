import { useState, useEffect } from 'react';
import api from '../api/axios';
import { User, Save, Edit2, Building2, BookOpen, GraduationCap, Loader2 } from 'lucide-react';

export default function Profile() {
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [profileExists, setProfileExists] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    college: '',
    department: '',
    semester: 1
  });

  // Fetch Profile on Load
  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await api.get('/profile');
      if (res.data) {
        setFormData({
          firstName: res.data.firstName,
          lastName: res.data.lastName,
          college: res.data.college,
          department: res.data.department,
          semester: res.data.semester
        });
        setProfileExists(true);
      }
    } catch (error) {
      // 404 or null means no profile created yet
      setProfileExists(false);
      setIsEditing(true); // Auto-enable edit mode for new users
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      if (profileExists) {
        // Update existing profile
        await api.put('/profile/update', formData);
        setMessage({ type: 'success', text: 'Profile updated successfully.' });
      } else {
        // Create new profile
        await api.post('/profile/create', formData);
        setMessage({ type: 'success', text: 'Profile created successfully.' });
        setProfileExists(true);
      }
      setIsEditing(false);
    } catch (error) {
      console.error(error);
      setMessage({ type: 'error', text: 'Failed to save profile. Please check inputs.' });
    } finally {
      setLoading(false);
    }
  };

  if (loading && !isEditing && !profileExists) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="animate-spin h-8 w-8 text-indigo-600" />
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 overflow-hidden">
        
        {/* Header Section */}
        <div className="bg-slate-50 dark:bg-slate-800/50 p-6 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <div className="h-12 w-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center text-indigo-600 dark:text-indigo-400">
              <User size={24} />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900 dark:text-white">Student Profile</h1>
              <p className="text-sm text-slate-500">Manage your academic identity</p>
            </div>
          </div>
          
          {profileExists && !isEditing && (
            <button 
              onClick={() => setIsEditing(true)}
              className="flex items-center gap-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 dark:text-indigo-400"
            >
              <Edit2 size={16} /> Edit Profile
            </button>
          )}
        </div>

        {/* Form Section */}
        <div className="p-8">
          {message.text && (
            <div className={`mb-6 p-4 rounded-lg text-sm flex items-center gap-2 ${
              message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
            }`}>
              {message.text}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Personal Info Group */}
            <div className="grid md:grid-cols-2 gap-6">
              <ProfileField 
                label="First Name" 
                name="firstName" 
                value={formData.firstName} 
                onChange={handleChange} 
                disabled={!isEditing} 
                icon={<User size={16} />}
              />
              <ProfileField 
                label="Last Name" 
                name="lastName" 
                value={formData.lastName} 
                onChange={handleChange} 
                disabled={!isEditing} 
                icon={<User size={16} />}
              />
            </div>

            <div className="h-px bg-slate-100 dark:bg-slate-800 my-4" />

            {/* Academic Info Group */}
            <div className="grid md:grid-cols-2 gap-6">
              <ProfileField 
                label="College / University" 
                name="college" 
                value={formData.college} 
                onChange={handleChange} 
                disabled={!isEditing} 
                icon={<Building2 size={16} />}
                fullWidth
              />
              <ProfileField 
                label="Department" 
                name="department" 
                value={formData.department} 
                onChange={handleChange} 
                disabled={!isEditing} 
                icon={<BookOpen size={16} />}
              />
              
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-500 uppercase flex items-center gap-2">
                   <GraduationCap size={14} /> Semester
                </label>
                <select 
                  name="semester" 
                  value={formData.semester} 
                  onChange={handleChange} 
                  disabled={!isEditing}
                  className="w-full p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none transition-all disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  {[1,2,3,4,5,6,7,8].map(sem => (
                    <option key={sem} value={sem}>Semester {sem}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Action Buttons */}
            {isEditing && (
              <div className="pt-6 flex justify-end gap-3">
                {profileExists && (
                  <button 
                    type="button" 
                    onClick={() => { setIsEditing(false); fetchProfile(); }}
                    className="px-4 py-2 text-slate-600 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200"
                  >
                    Cancel
                  </button>
                )}
                <button 
                  type="submit" 
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors shadow-sm"
                >
                  <Save size={18} /> {profileExists ? 'Update Profile' : 'Create Profile'}
                </button>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}

// Reusable Field Component
const ProfileField = ({ label, icon, disabled, fullWidth, ...props }) => (
  <div className={`space-y-1 ${fullWidth ? 'md:col-span-2' : ''}`}>
    <label className="text-xs font-semibold text-slate-500 uppercase flex items-center gap-2">
      {icon} {label}
    </label>
    <input 
      {...props} 
      disabled={disabled}
      className="w-full p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-indigo-500 outline-none transition-all disabled:opacity-60 disabled:cursor-not-allowed disabled:bg-slate-100 dark:disabled:bg-slate-800/50" 
    />
  </div>
);