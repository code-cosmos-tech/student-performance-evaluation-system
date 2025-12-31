import { useState } from 'react';
import api from '../api/axios';
import { Loader2, AlertCircle, CheckCircle2, LayoutDashboard } from 'lucide-react';

export default function Prediction() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  // Initial State
  const [formData, setFormData] = useState({
    lastSemSPI: '',
    internalAssessmentAvg: '',
    attendancePercentage: '',
    totalBacklogs: 0,
    studyHoursWeekly: '',
    gamingHoursWeekly: 0,
    pyqSolvingFrequency: 0,
    assignmentDelayCount: 0,
    department: 'CSE', 
    extraCurricularLevel: 'Low', 
    sleepCategory: '6-8',       
    travelTimeCategory: '30-60',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    // DATA CLEANING: Ensure numbers are actually numbers before sending
    const payload = {
      ...formData,
      lastSemSPI: formData.lastSemSPI === '' ? 0.0 : parseFloat(formData.lastSemSPI),
      internalAssessmentAvg: formData.internalAssessmentAvg === '' ? 0.0 : parseFloat(formData.internalAssessmentAvg),
      attendancePercentage: formData.attendancePercentage === '' ? 0.0 : parseFloat(formData.attendancePercentage),
      studyHoursWeekly: formData.studyHoursWeekly === '' ? 0.0 : parseFloat(formData.studyHoursWeekly),
      gamingHoursWeekly: formData.gamingHoursWeekly === '' ? 0.0 : parseFloat(formData.gamingHoursWeekly),
      
      // Integers
      totalBacklogs: parseInt(formData.totalBacklogs) || 0,
      pyqSolvingFrequency: parseInt(formData.pyqSolvingFrequency) || 0,
      assignmentDelayCount: parseInt(formData.assignmentDelayCount) || 0,
    };

    try {
      const response = await api.post('/predict', payload);
      setResult(response.data);
      console.log("API Response:", response.data);
    } catch (err) {
      console.error("Prediction Error:", err);
      const serverMsg = err.response?.data?.message || err.response?.data?.detail?.[0]?.msg;
      setError(serverMsg || 'Prediction failed. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

  // Helper to safely format probability to percentage string
  const formatProb = (val) => {
    if (val === undefined || val === null) return "0.00%";
    // Convert scientific notation/decimals to percentage
    return `${(val * 100).toFixed(2)}%`;
  };

  return (
    <div className="grid md:grid-cols-3 gap-8 animate-fade-in">
      {/* Input Section */}
      <div className="md:col-span-2 space-y-6">
        <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800">
          <h2 className="text-2xl font-bold mb-1 dark:text-white">Academic Metrics</h2>
          <p className="text-slate-500 text-sm mb-6">Provide accurate data for the best prediction.</p>
          
          <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Core Academics */}
            <div className="sm:col-span-2 text-xs font-bold text-indigo-600 uppercase tracking-wider mt-2">Academics</div>
            <InputField label="Last Sem SPI (0-10)" name="lastSemSPI" type="number" step="0.01" max="10" value={formData.lastSemSPI} onChange={handleChange} />
            <InputField label="Internal Avg (0-50)" name="internalAssessmentAvg" type="number" step="0.1" value={formData.internalAssessmentAvg} onChange={handleChange} />
            <InputField label="Attendance %" name="attendancePercentage" type="number" max="100" value={formData.attendancePercentage} onChange={handleChange} />
            <InputField label="Backlogs" name="totalBacklogs" type="number" value={formData.totalBacklogs} onChange={handleChange} />

            {/* Study & Habits */}
            <div className="sm:col-span-2 text-xs font-bold text-indigo-600 uppercase tracking-wider mt-4">Habits & Lifestyle</div>
            <InputField label="Study Hours/Week" name="studyHoursWeekly" type="number" value={formData.studyHoursWeekly} onChange={handleChange} />
            <InputField label="PYQ Solving (Times/Week)" name="pyqSolvingFrequency" type="number" value={formData.pyqSolvingFrequency} onChange={handleChange} />
            <InputField label="Assignment Delays" name="assignmentDelayCount" type="number" value={formData.assignmentDelayCount} onChange={handleChange} />
            <InputField label="Gaming Hours/Week" name="gamingHoursWeekly" type="number" value={formData.gamingHoursWeekly} onChange={handleChange} />
            
            <SelectField 
                label="Sleep Quality" 
                name="sleepCategory" 
                value={formData.sleepCategory} 
                onChange={handleChange} 
                options={["<6", "6-8", ">8"]} 
            />
            <SelectField 
                label="Travel Time (Mins)" 
                name="travelTimeCategory" 
                value={formData.travelTimeCategory} 
                onChange={handleChange} 
                options={["<30", "30-60", ">60"]} 
            />
            
            {/* Profile */}
            <div className="sm:col-span-2 text-xs font-bold text-indigo-600 uppercase tracking-wider mt-4">Profile</div>
            <SelectField 
                label="Extra Curricular" 
                name="extraCurricularLevel" 
                value={formData.extraCurricularLevel} 
                onChange={handleChange} 
                options={["Low", "Medium", "High"]} 
            />
            <SelectField 
                label="Department" 
                name="department" 
                value={formData.department} 
                onChange={handleChange} 
                options={["CSE", "IT", "ECE", "MECH", "CIVIL"]} 
            />

            <div className="sm:col-span-2 pt-6">
              <button 
                type="submit" 
                disabled={loading}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-6 rounded-xl transition-all flex justify-center items-center gap-2 disabled:opacity-50 shadow-lg shadow-indigo-200 dark:shadow-none"
              >
                {loading ? <Loader2 className="animate-spin" /> : "Analyze Student Performance"}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Result Section - FIXED */}
      <div className="md:col-span-1">
        {result ? (
          <div className="sticky top-24 bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-xl border-t-4 border-indigo-500 animate-slide-up">
            <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <CheckCircle2 className="text-green-500" /> Analysis Complete
            </h3>
            
            <div className="mt-8 text-center py-8 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-800">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Prediction</span>
              <div className="text-3xl font-black text-indigo-600 dark:text-indigo-400 mt-2">
                {/* Use the correct key from JSON: 'performance_category' */}
                {result.performance_category}
              </div>
            </div>

            <div className="mt-6 space-y-4">
              <div className="flex flex-col gap-3 text-sm dark:text-slate-300">
                {/* <div className="text-slate-500 font-medium pb-2 border-b border-slate-100 dark:border-slate-800 flex justify-between">
                    <span>Model Confidence</span>
                    <span className="text-slate-900 dark:text-white font-bold">{(result.confidence * 100).toFixed(1)}%</span>
                </div> */}
                
                {/* Probability Breakdowns - Using Bracket Notation for keys with spaces */}
                <div className="flex justify-between items-center">
                    <span className="font-medium text-red-500 dark:text-red-400">At Risk</span>
                    <span className="font-mono font-bold text-slate-700 dark:text-slate-200">
                      {formatProb(result.probabilities["At Risk"])}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-medium text-yellow-600 dark:text-yellow-400">Average</span>
                    <span className="font-mono font-bold text-slate-700 dark:text-slate-200">
                      {formatProb(result.probabilities["Average"])}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="font-medium text-green-600 dark:text-green-400">Good</span>
                    <span className="font-mono font-bold text-slate-700 dark:text-slate-200">
                      {formatProb(result.probabilities["Good"])}
                    </span>
                </div>
              </div>

              {/* Confidence Bar */}
              {/* <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 mt-4">
                <div 
                  className="bg-indigo-600 h-2 rounded-full transition-all duration-1000 ease-out" 
                  style={{ width: `${result.confidence * 100}%` }}
                ></div>
              </div> */}
            </div>
          </div>
        ) : (
          <div className="sticky top-24 h-64 bg-slate-100 dark:bg-slate-900/50 border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-2xl flex flex-col items-center justify-center p-6 text-center text-slate-400">
            <LayoutDashboard className="h-10 w-10 mb-3 opacity-50" />
            <p className="text-sm">Results will appear here after analysis.</p>
          </div>
        )}
        
        {error && (
            <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-xl flex items-start gap-3 text-sm border border-red-100 dark:border-red-900/50">
                <AlertCircle size={18} className="shrink-0 mt-0.5" /> 
                <span className="break-words w-full">{error}</span>
            </div>
        )}
      </div>
    </div>
  );
}

// Reusable Components
const InputField = ({ label, ...props }) => (
  <div className="flex flex-col gap-1.5">
    <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">{label}</label>
    <input 
      {...props} 
      className="w-full p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all text-sm font-medium dark:text-white placeholder:text-slate-400" 
    />
  </div>
);

const SelectField = ({ label, options, ...props }) => (
  <div className="flex flex-col gap-1.5">
    <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">{label}</label>
    <select 
      {...props} 
      className="w-full p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all text-sm font-medium dark:text-white"
    >
      {options.map(opt => (
        <option 
          key={opt} 
          value={opt} 
          className="bg-white text-slate-900 dark:bg-slate-800 dark:text-slate-100"
        >
          {opt}
        </option>
      ))}
    </select>
  </div>
);