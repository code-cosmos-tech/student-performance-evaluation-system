import { Link } from 'react-router-dom';
import { GraduationCap, ArrowRight, TrendingUp, BrainCircuit, ShieldCheck, BarChart3 } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex flex-col">
      
      {/* --- Hero Section --- */}
      <section className="relative overflow-hidden pt-16 pb-20 lg:pt-32 lg:pb-28">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 text-xs font-semibold mb-6 border border-indigo-100 dark:border-indigo-800">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
            </span>
            AI-Powered Academic Analysis
          </div>

          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white mb-6 leading-tight">
            Predict Your Success. <br />
            <span className="text-indigo-600 dark:text-indigo-400">Evolve Your Future.</span>
          </h1>
          
          <p className="mt-4 max-w-2xl mx-auto text-xl text-slate-600 dark:text-slate-400">
            EvolSys uses advanced Machine Learning to analyze your academic history, 
            study habits, and lifestyle to predict performance outcomes with high precision.
          </p>

          <div className="mt-10 flex justify-center gap-4">
            <Link to="/dashboard" className="px-8 py-3.5 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-200 dark:shadow-none flex items-center gap-2">
              Get Started <ArrowRight size={18} />
            </Link>
            <a href="#features" className="px-8 py-3.5 rounded-xl bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 font-semibold hover:bg-slate-50 dark:hover:bg-slate-700 transition-all">
              Learn More
            </a>
          </div>
        </div>

        {/* Abstract Background Decoration */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10 opacity-30 pointer-events-none">
           <div className="absolute top-20 left-20 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
           <div className="absolute top-20 right-20 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        </div>
      </section>

      {/* --- Features Grid --- */}
      <section id="features" className="py-20 bg-slate-50 dark:bg-slate-900/50 border-y border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white">Scientific Approach to Grading</h2>
            <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
              We move beyond simple GPA calculation. Our system evaluates holistic factors affecting student life.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<BrainCircuit className="text-indigo-600" size={32} />}
              title="ML Predictions"
              desc="Powered by a FastAPI Python Microservice trained on historical student datasets for accurate forecasting."
            />
            <FeatureCard 
              icon={<BarChart3 className="text-indigo-600" size={32} />}
              title="Holistic Metrics"
              desc="We analyze sleep patterns, travel time, and study consistency—not just your exam scores."
            />
            <FeatureCard 
              icon={<ShieldCheck className="text-indigo-600" size={32} />}
              title="Secure & Private"
              desc="Your academic data is encrypted and accessible only to you and authorized administrators."
            />
          </div>
        </div>
      </section>

      {/* --- Simple Stats / Footer CTA --- */}
      <section className="py-20">
        <div className="max-w-5xl mx-auto px-4 text-center bg-indigo-600 rounded-3xl p-12 relative overflow-hidden shadow-2xl">
          {/* Decorative circles */}
          <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 rounded-full bg-indigo-500 opacity-50"></div>
          <div className="absolute bottom-0 left-0 -ml-16 -mb-16 w-64 h-64 rounded-full bg-indigo-700 opacity-50"></div>
          
          <h2 className="relative text-3xl font-bold text-white mb-6">Ready to improve your grades?</h2>
          <p className="relative text-indigo-100 text-lg mb-8 max-w-2xl mx-auto">
            Join students from CSE, IT, and other departments in tracking their academic evolution.
          </p>
          <Link to="/login" className="relative inline-flex items-center gap-2 bg-white text-indigo-600 px-8 py-3.5 rounded-xl font-bold hover:bg-indigo-50 transition-colors">
            <GraduationCap size={20} /> Join Student Portal
          </Link>
        </div>
      </section>

      {/* --- Footer --- */}
      <footer className="border-t border-slate-200 dark:border-slate-800 py-12 bg-white dark:bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center text-sm text-slate-500">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <div className="bg-indigo-600 p-1.5 rounded-lg">
                <GraduationCap size={16} className="text-white" />
            </div>
            <span className="font-semibold text-slate-900 dark:text-white">EvolSys</span>
          </div>
          <div className="flex gap-6">
            <a href="#" className="hover:text-indigo-600 transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-indigo-600 transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-indigo-600 transition-colors">Contact Support</a>
          </div>
          <p className="mt-4 md:mt-0">© 2025 CodeAndCosmos. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, desc }) {
  return (
    <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800 hover:shadow-xl hover:border-indigo-200 dark:hover:border-indigo-900/50 transition-all duration-300 group">
      <div className="mb-6 p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-xl w-fit group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">{title}</h3>
      <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
        {desc}
      </p>
    </div>
  );
}