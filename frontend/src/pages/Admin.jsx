import { useEffect, useState } from 'react';
import api from '../api/axios';
import { Loader2, Plus, X, Save, AlertCircle } from 'lucide-react';

export default function Admin() {
  const [profiles, setProfiles] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [activeTab, setActiveTab] = useState('profiles'); // profiles | predictions
  const [loading, setLoading] = useState(false);
  
  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);

  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'profiles') {
        const res = await api.get('/admin/allProfile');
        setProfiles(res.data);
      } else {
        const res = await api.get('/admin/allPredictions');
        setPredictions(res.data);
      }
    } catch (e) {
      console.error("Failed to fetch admin data", e);
    } finally {
      setLoading(false);
    }
  };

  const handlePredictAll = async () => {
      try {
        await api.post('/admin/predictAll');
        alert('Batch prediction triggered successfully.');
      } catch (e) {
        alert('Failed to trigger batch prediction.');
      }
  };

  const openAddDataModal = (student) => {
    setSelectedStudent(student);
    setIsModalOpen(true);
  };

  return (
    <div className="space-y-6 relative">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold dark:text-white">Admin Console</h1>
        <button onClick={handlePredictAll} className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700 transition-colors">
            Trigger Batch Prediction
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-200 dark:border-slate-800">
        <button
          onClick={() => setActiveTab('profiles')}
          className={`px-6 py-3 text-sm font-medium capitalize transition-colors ${
            activeTab === 'profiles' 
            ? 'border-b-2 border-indigo-600 text-indigo-600 dark:text-indigo-400' 
            : 'text-slate-500 hover:text-slate-700 dark:text-slate-400'
          }`}
        >
          All Profiles
        </button>
        <button
          onClick={() => setActiveTab('predictions')}
          className={`px-6 py-3 text-sm font-medium capitalize transition-colors ${
            activeTab === 'predictions' 
            ? 'border-b-2 border-indigo-600 text-indigo-600 dark:text-indigo-400' 
            : 'text-slate-500 hover:text-slate-700 dark:text-slate-400'
          }`}
        >
          All Predictions
        </button>
      </div>

      {/* Data Table */}
      <div className="overflow-x-auto bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
        <table className="w-full text-left text-sm text-slate-600 dark:text-slate-300">
          <thead className="bg-slate-50 dark:bg-slate-800 text-xs uppercase font-semibold text-slate-500">
            <tr>
              <th className="px-6 py-4">ID</th>
              <th className="px-6 py-4">{activeTab === 'profiles' ? 'Name' : 'Prediction'}</th>
              <th className="px-6 py-4">{activeTab === 'profiles' ? 'Department' : 'Confidence'}</th>
              {activeTab === 'profiles' && <th className="px-6 py-4 text-right">Actions</th>}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
            {loading ? (
               <tr><td colSpan="4" className="p-8 text-center"><Loader2 className="animate-spin inline" /></td></tr>
            ) : (activeTab === 'profiles' ? profiles : predictions).map((item) => (
              <tr key={item.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                <td className="px-6 py-4 font-mono text-xs">{item.id || item.userId}</td>
                <td className="px-6 py-4 font-medium text-slate-900 dark:text-white">
                  {activeTab === 'profiles' ? `${item.firstName} ${item.lastName}` : item.prediction?.performance_category}
                </td>
                <td className="px-6 py-4">
                  {activeTab === 'profiles' ? item.department : (item.prediction?.confidence * 100).toFixed(1) + '%'}
                </td>
                {activeTab === 'profiles' && (
                  <td className="px-6 py-4 text-right">
                    <button 
                      onClick={() => openAddDataModal(item)}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 rounded-lg text-xs font-medium hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-colors"
                    >
                      <Plus size={14} /> Add Data
                    </button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Add Data Modal */}
      {isModalOpen && selectedStudent && (
        <AddDataModal 
          student={selectedStudent} 
          onClose={() => setIsModalOpen(false)} 
        />
      )}
    </div>
  );
}

// --- Internal Modal Component ---
function AddDataModal({ student, onClose }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // PRE-FILL LOGIC: Check if student has existing predictionData
  const existing = student.predictionData || {};

  const [formData, setFormData] = useState({
    // Use existing data OR fall back to defaults
    lastSemSPI: existing.lastSemSPI || '',
    internalAssessmentAvg: existing.internalAssessmentAvg || '',
    attendancePercentage: existing.attendancePercentage || '',
    totalBacklogs: existing.totalBacklogs || 0,
    
    studyHoursWeekly: existing.studyHoursWeekly || '',
    gamingHoursWeekly: existing.gamingHoursWeekly || 0,
    pyqSolvingFrequency: existing.pyqSolvingFrequency || 0,
    assignmentDelayCount: existing.assignmentDelayCount || 0,
    
    // Dropdowns (Ensure valid defaults if data is missing)
    department: existing.department || student.department || 'CSE', 
    extraCurricularLevel: existing.extraCurricularLevel || 'Low',
    sleepCategory: existing.sleepCategory || '6-8',
    travelTimeCategory: existing.travelTimeCategory || '30-60',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const payload = {
      ...formData,
      lastSemSPI: parseFloat(formData.lastSemSPI) || 0.0,
      internalAssessmentAvg: parseFloat(formData.internalAssessmentAvg) || 0.0,
      attendancePercentage: parseFloat(formData.attendancePercentage) || 0.0,
      studyHoursWeekly: parseFloat(formData.studyHoursWeekly) || 0.0,
      gamingHoursWeekly: parseFloat(formData.gamingHoursWeekly) || 0.0,
      
      totalBacklogs: parseInt(formData.totalBacklogs) || 0,
      pyqSolvingFrequency: parseInt(formData.pyqSolvingFrequency) || 0,
      assignmentDelayCount: parseInt(formData.assignmentDelayCount) || 0,
    };

    try {
      await api.post(`/admin/addData/${student.userId}`, payload);
      alert('Data saved successfully!');
      // Optional: Refresh the parent table here if you pass a refresh function
      onClose();
      window.location.reload(); // Simple reload to show updated data immediately
    } catch (err) {
      console.error(err);
      const msg = err.response?.data?.message || 'Failed to save data.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
      <div className="bg-white dark:bg-slate-900 w-full max-w-2xl rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 max-h-[90vh] overflow-y-auto">
        
        <div className="flex justify-between items-center p-6 border-b border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 sticky top-0 z-10">
          <div>
            <h2 className="text-lg font-bold dark:text-white">
              {student.predictionData ? 'Edit' : 'Add'} Student Data
            </h2>
            <p className="text-xs text-slate-500">For {student.firstName} {student.lastName}</p>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors">
            <X size={20} className="text-slate-500" />
          </button>
        </div>

        {/* ... Rest of the form remains exactly the same ... */}
        <form onSubmit={handleSubmit} className="p-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
           {/* Same Inputs as before... */}
           <div className="sm:col-span-2 text-xs font-bold text-indigo-600 uppercase tracking-wider mb-1">Academic Metrics</div>
           <InputField label="Last Sem SPI" name="lastSemSPI" type="number" step="0.01" value={formData.lastSemSPI} onChange={handleChange} />
           <InputField label="Internal Avg" name="internalAssessmentAvg" type="number" step="0.1" value={formData.internalAssessmentAvg} onChange={handleChange} />
           <InputField label="Attendance %" name="attendancePercentage" type="number" value={formData.attendancePercentage} onChange={handleChange} />
           <InputField label="Backlogs" name="totalBacklogs" type="number" value={formData.totalBacklogs} onChange={handleChange} />

           <div className="sm:col-span-2 text-xs font-bold text-indigo-600 uppercase tracking-wider mt-4 mb-1">Habits & Lifestyle</div>
           <InputField label="Study Hours/Week" name="studyHoursWeekly" type="number" value={formData.studyHoursWeekly} onChange={handleChange} />
           <InputField label="PYQ Solving (Times/Week)" name="pyqSolvingFrequency" type="number" value={formData.pyqSolvingFrequency} onChange={handleChange} />
           <InputField label="Assignment Delays" name="assignmentDelayCount" type="number" value={formData.assignmentDelayCount} onChange={handleChange} />
           <InputField label="Gaming Hours" name="gamingHoursWeekly" type="number" value={formData.gamingHoursWeekly} onChange={handleChange} />

           <SelectField label="Sleep Quality" name="sleepCategory" value={formData.sleepCategory} onChange={handleChange} options={["<6", "6-8", ">8"]} />
           <SelectField label="Travel Time" name="travelTimeCategory" value={formData.travelTimeCategory} onChange={handleChange} options={["<30", "30-60", ">60"]} />
          
           <div className="sm:col-span-2 text-xs font-bold text-indigo-600 uppercase tracking-wider mt-4 mb-1">Profile</div>
           <SelectField label="Extra Curricular" name="extraCurricularLevel" value={formData.extraCurricularLevel} onChange={handleChange} options={["Low", "Medium", "High"]} />
           <SelectField label="Department" name="department" value={formData.department} onChange={handleChange} options={["CSE", "IT", "ECE", "MECH", "CIVIL"]} />

           {error && (
            <div className="sm:col-span-2 mt-2 p-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm rounded-lg flex items-center gap-2">
              <AlertCircle size={16} /> {error}
            </div>
           )}

           <div className="sm:col-span-2 pt-6 flex gap-3 justify-end border-t border-slate-100 dark:border-slate-800 mt-4">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm text-slate-600 dark:text-slate-400 font-medium hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg">Cancel</button>
            <button type="submit" disabled={loading} className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg flex items-center gap-2 disabled:opacity-50">
              {loading ? <Loader2 className="animate-spin h-4 w-4" /> : <><Save size={16} /> Save Data</>}
            </button>
           </div>
        </form>
      </div>
    </div>
  );
}

// Reusable Components (Keep consistent with other pages)
const InputField = ({ label, ...props }) => (
  <div className="flex flex-col gap-1">
    <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wide">{label}</label>
    <input {...props} className="w-full p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all text-sm dark:text-white" />
  </div>
);

const SelectField = ({ label, options, ...props }) => (
  <div className="flex flex-col gap-1">
    <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wide">{label}</label>
    <select {...props} className="w-full p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all text-sm dark:text-white">
      {options.map(opt => <option key={opt} value={opt} className="bg-white text-slate-900 dark:bg-slate-800 dark:text-white">{opt}</option>)}
    </select>
  </div>
);