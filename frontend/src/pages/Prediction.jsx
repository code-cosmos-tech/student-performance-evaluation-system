import { useState } from 'react';
import api from '../api/axios';
import { Loader2, TrendingUp, BookOpen, Clock, Gamepad2, Moon, Activity, Briefcase } from 'lucide-react';

export default function Prediction() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    lastSemSPI: '', internalAssessmentAvg: '', attendancePercentage: '', totalBacklogs: 0,
    studyHoursWeekly: 10, gamingHoursWeekly: 2, pyqSolvingFrequency: 0, assignmentDelayCount: 0,
    department: 'CSE', extraCurricularLevel: 'Low', sleepCategory: '6-8', travelTimeCategory: '30-60',
  });

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });
  const handleSlider = (name, value) => setFormData({ ...formData, [name]: value });
  const handleSelect = (name, value) => setFormData({ ...formData, [name]: value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); setError(''); setResult(null);

    // Convert types securely
    const payload = {
      ...formData,
      lastSemSPI: parseFloat(formData.lastSemSPI) || 0,
      internalAssessmentAvg: parseFloat(formData.internalAssessmentAvg) || 0,
      attendancePercentage: parseFloat(formData.attendancePercentage) || 0,
      studyHoursWeekly: parseFloat(formData.studyHoursWeekly),
      gamingHoursWeekly: parseFloat(formData.gamingHoursWeekly),
      totalBacklogs: parseInt(formData.totalBacklogs),
      pyqSolvingFrequency: parseInt(formData.pyqSolvingFrequency),
      assignmentDelayCount: parseInt(formData.assignmentDelayCount),
    };

    try {
      const response = await api.post('/predict', payload);
      setResult(response.data);
      // Smooth scroll to results on mobile
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      setError('Analysis failed. Please check inputs.');
    } finally {
      setLoading(false);
    }
  };

  const formatProb = (val) => `${((val || 0) * 100).toFixed(1)}%`;

  return (
    <div className="grid lg:grid-cols-12 gap-8 items-start">

      {/* LEFT COLUMN: Input Form */}
      <div className="lg:col-span-8 space-y-8">
        <div className="flex items-end justify-between mb-2">
            <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white tracking-tight">Performance Analysis</h1>
                <p className="text-slate-500 dark:text-slate-400 mt-1">AI-driven academic forecasting engine.</p>
            </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">

          {/* Section 1: Academic Metrics (Glassmorphism) */}
          <div className="glass-card p-6 rounded-3xl border-l-4 border-indigo-500 relative overflow-hidden">
             <div className="absolute top-0 right-0 p-4 opacity-5"><BookOpen size={100} /></div>
             <h3 className="text-lg font-bold text-indigo-900 dark:text-indigo-300 flex items-center gap-2 mb-6">
                <span className="p-2 bg-indigo-100 dark:bg-indigo-900/50 rounded-lg"><TrendingUp size={18} className="text-indigo-600" /></span>
                Academic Core
             </h3>
             <div className="grid sm:grid-cols-2 gap-6 relative z-10">
                <FloatingInput label="Last Sem SPI (0-10)" name="lastSemSPI" type="number" step="0.01" value={formData.lastSemSPI} onChange={handleChange} />
                <FloatingInput label="Internal Marks (0-50)" name="internalAssessmentAvg" type="number" step="0.1" value={formData.internalAssessmentAvg} onChange={handleChange} />
                <FloatingInput label="Attendance %" name="attendancePercentage" type="number" value={formData.attendancePercentage} onChange={handleChange} />
                <FloatingInput label="Backlogs" name="totalBacklogs" type="number" value={formData.totalBacklogs} onChange={handleChange} />

                <div className="sm:col-span-2">
                   <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-2 block">Department</label>
                   <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
                      {['CSE', 'IT', 'ECE', 'MECH', 'CIVIL'].map(dept => (
                        <SelectionPill key={dept} active={formData.department === dept} onClick={() => handleSelect('department', dept)} label={dept} />
                      ))}
                   </div>
                </div>
             </div>
          </div>

          {/* Section 2: Habits & Lifestyle */}
          <div className="glass-card p-6 rounded-3xl border-l-4 border-emerald-500 relative overflow-hidden">
             <div className="absolute top-0 right-0 p-4 opacity-5"><Activity size={100} /></div>
             <h3 className="text-lg font-bold text-emerald-900 dark:text-emerald-300 flex items-center gap-2 mb-6">
                <span className="p-2 bg-emerald-100 dark:bg-emerald-900/50 rounded-lg"><Clock size={18} className="text-emerald-600" /></span>
                Habits & Lifestyle
             </h3>

             <div className="space-y-6 relative z-10">
                {/* Sliders for Time */}
                <RangeSlider label="Study Hours / Week" value={formData.studyHoursWeekly} min={0} max={50} onChange={(e) => handleSlider('studyHoursWeekly', e.target.value)} icon={<BookOpen size={14}/>} />
                <RangeSlider label="Gaming Hours / Week" value={formData.gamingHoursWeekly} min={0} max={40} onChange={(e) => handleSlider('gamingHoursWeekly', e.target.value)} color="red" icon={<Gamepad2 size={14}/>} />

                <div className="grid sm:grid-cols-2 gap-6">
                    <FloatingInput label="PYQ Solving (Weekly)" name="pyqSolvingFrequency" type="number" value={formData.pyqSolvingFrequency} onChange={handleChange} />
                    <FloatingInput label="Assignment Delays" name="assignmentDelayCount" type="number" value={formData.assignmentDelayCount} onChange={handleChange} />
                </div>

                {/* Segmented Controls for Categories */}
                <div className="grid sm:grid-cols-2 gap-6">
                    <div>
                        <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-2 block flex items-center gap-2"><Moon size={12}/> Sleep Quality</label>
                        <div className="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
                            {['<6', '6-8', '>8'].map(opt => (
                                <button key={opt} type="button" onClick={() => handleSelect('sleepCategory', opt)}
                                    className={`flex-1 py-2 text-xs font-bold rounded-lg transition-all ${formData.sleepCategory === opt ? 'bg-white dark:bg-slate-700 shadow-sm text-indigo-600' : 'text-slate-400 hover:text-slate-600'}`}>
                                    {opt} hrs
                                </button>
                            ))}
                        </div>
                    </div>
                    <div>
                        <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-2 block flex items-center gap-2"><Briefcase size={12}/> Extra Curricular</label>
                        <div className="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
                            {['Low', 'Medium', 'High'].map(opt => (
                                <button key={opt} type="button" onClick={() => handleSelect('extraCurricularLevel', opt)}
                                    className={`flex-1 py-2 text-xs font-bold rounded-lg transition-all ${formData.extraCurricularLevel === opt ? 'bg-white dark:bg-slate-700 shadow-sm text-emerald-600' : 'text-slate-400 hover:text-slate-600'}`}>
                                    {opt}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
             </div>
          </div>

          <button type="submit" disabled={loading} className="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl font-bold shadow-xl shadow-indigo-500/30 transition-all hover:-translate-y-1 flex justify-center items-center gap-2">
            {loading ? <Loader2 className="animate-spin" /> : <>Run AI Prediction</>}
          </button>
        </form>
      </div>

      {/* RIGHT COLUMN: Sticky Results Dashboard */}
      <div className="lg:col-span-4 space-y-6 lg:sticky lg:top-32">
        {result ? (
            <div className="bg-white dark:bg-slate-900 rounded-[2rem] p-6 shadow-2xl border border-slate-100 dark:border-slate-800 animate-fade-in-up">
                <div className="text-center mb-8 relative">
                    <div className={`inline-flex p-4 rounded-full mb-4 shadow-lg ${
                        result.performance_category === 'Good' ? 'bg-green-100 text-green-600' :
                        result.performance_category === 'Average' ? 'bg-yellow-100 text-yellow-600' : 'bg-red-100 text-red-600'
                    }`}>
                        <TrendingUp size={32} />
                    </div>
                    <h2 className="text-sm font-bold text-slate-400 uppercase tracking-widest">Predicted Outcome</h2>
                    <div className="text-4xl font-black text-slate-800 dark:text-white mt-2 tracking-tight">
                        {result.performance_category}
                    </div>
                </div>

                <div className="space-y-4">
                    <ProbabilityBar label="Good Performance" value={result.probabilities['Good']} color="bg-green-500" />
                    <ProbabilityBar label="Average Performance" value={result.probabilities['Average']} color="bg-yellow-500" />
                    <ProbabilityBar label="At Risk" value={result.probabilities['At Risk']} color="bg-red-500" />
                </div>

                <div className="mt-8 pt-6 border-t border-slate-100 dark:border-slate-800 text-center">
                    <p className="text-xs text-slate-400 leading-relaxed">
                        Based on your profile, focusing on <strong>attendance</strong> and <strong>consistent study hours</strong> will likely improve your score.
                    </p>
                </div>
            </div>
        ) : (
            <div className="h-full min-h-[400px] flex flex-col items-center justify-center p-8 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-[2rem] bg-slate-50/50 dark:bg-slate-900/50">
                <div className="bg-white dark:bg-slate-800 p-4 rounded-full mb-4 shadow-sm">
                    <Activity className="text-slate-300" size={32} />
                </div>
                <h3 className="text-lg font-semibold text-slate-600 dark:text-slate-400">Waiting for Data</h3>
                <p className="text-sm text-slate-400 mt-2">Fill out the academic profile to generate your performance forecast.</p>
            </div>
        )}

        {error && (
            <div className="p-4 bg-red-50 text-red-600 text-sm rounded-xl border border-red-100 text-center font-medium">
                {error}
            </div>
        )}
      </div>
    </div>
  );
}

/* --- UI Components --- */

const FloatingInput = ({ label, ...props }) => (
    <div className="relative group">
        <input {...props} placeholder=" "
            className="peer w-full px-4 pt-5 pb-2 rounded-xl bg-slate-50 dark:bg-slate-950/50 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all font-semibold text-slate-800 dark:text-white"
        />
        <label className="absolute text-xs font-bold text-slate-400 duration-150 transform -translate-y-3 scale-75 top-4 z-10 origin-[0] left-4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-3 peer-focus:text-indigo-500 uppercase tracking-wide">
            {label}
        </label>
    </div>
);

const RangeSlider = ({ label, value, onChange, min, max, icon, color="indigo" }) => (
    <div>
        <div className="flex justify-between text-xs font-bold text-slate-500 uppercase mb-2">
            <span className="flex items-center gap-1">{icon} {label}</span>
            <span className={`text-${color}-600`}>{value} hrs</span>
        </div>
        <input type="range" min={min} max={max} value={value} onChange={onChange}
            className={`w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-${color}-600`}
        />
    </div>
);

const SelectionPill = ({ label, active, onClick }) => (
    <button type="button" onClick={onClick}
        className={`py-2 px-1 text-xs font-bold rounded-lg transition-all border ${
            active
            ? 'bg-indigo-600 text-white border-indigo-600 shadow-lg shadow-indigo-500/30'
            : 'bg-white dark:bg-slate-900 text-slate-500 border-slate-200 dark:border-slate-700 hover:border-indigo-300'
        }`}>
        {label}
    </button>
);

const ProbabilityBar = ({ label, value, color }) => (
    <div>
        <div className="flex justify-between text-xs font-bold mb-1">
            <span className="text-slate-500">{label}</span>
            <span className="text-slate-800 dark:text-white">{(value * 100).toFixed(1)}%</span>
        </div>
        <div className="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2.5 overflow-hidden">
            <div className={`h-2.5 rounded-full ${color} transition-all duration-1000`} style={{ width: `${value * 100}%` }}></div>
        </div>
    </div>
);