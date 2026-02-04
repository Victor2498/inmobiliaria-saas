import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, Home, Settings, Moon, Sun } from 'lucide-react';
import { useEffect, useState } from 'react';
import { ContractService } from './api/services';
import type { DashboardMetrics } from './api/services';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const saved = localStorage.getItem('theme');
    return saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDarkMode]);

  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  return (
    <Router>
      <div className={`min-h-screen flex transition-colors duration-300 ${isDarkMode ? 'bg-slate-950 text-slate-100' : 'bg-gray-50 text-gray-900'}`}>
        {/* Sidebar */}
        <aside className="w-64 bg-slate-900 text-white hidden md:flex flex-col border-r border-slate-800">
          <div className="p-6">
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
              Inmonea
            </h1>
            <p className="text-sm text-slate-400">Gestión Integral</p>
          </div>

          <nav className="flex-1 px-4 space-y-2 mt-4">
            <NavItem to="/" icon={<LayoutDashboard size={20} />} text="Dashboard" />
            <NavItem to="/inquilinos" icon={<Users size={20} />} text="Inquilinos" />
            <NavItem to="/propiedades" icon={<Home size={20} />} text="Propiedades" />
          </nav>

          <div className="p-4 border-t border-slate-800">
            <NavItem to="/configuracion" icon={<Settings size={20} />} text="Configuración" />
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto">
          <header className={`h-16 flex items-center px-8 justify-between shadow-sm transition-colors duration-300 ${isDarkMode ? 'bg-slate-900 border-b border-slate-800' : 'bg-white'}`}>
            <h2 className={`text-xl font-semibold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>Panel de Control</h2>
            <div className="flex items-center gap-6">
              <button
                onClick={toggleTheme}
                className={`p-2 rounded-lg transition-colors ${isDarkMode ? 'hover:bg-slate-800 text-yellow-400' : 'hover:bg-gray-100 text-slate-600'}`}
                title={isDarkMode ? "Cambiar a Modo Claro" : "Cambiar a Modo Oscuro"}
              >
                {isDarkMode ? <Sun size={22} /> : <Moon size={22} />}
              </button>
              <div className="flex items-center gap-4">
                <div className="w-8 h-8 rounded-full bg-brand-500 flex items-center justify-center text-white font-bold shadow-lg shadow-brand-500/20">
                  A
                </div>
              </div>
            </div>
          </header>

          <div className="p-8">
            <Routes>
              <Route path="/" element={<DashboardHome isDarkMode={isDarkMode} />} />
              <Route path="/inquilinos" element={<TenantsPage isDarkMode={isDarkMode} />} />
              <Route path="/propiedades" element={<PropertiesPage isDarkMode={isDarkMode} />} />
              <Route path="/configuracion" element={<div className="p-8 text-slate-500">Página de Configuración (Próximamente)</div>} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

function NavItem({ to, icon, text }: { to: string, icon: any, text: string }) {
  const location = useLocation();
  const active = location.pathname === to;

  return (
    <Link to={to} className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 
      ${active ? 'bg-brand-600 text-white shadow-lg shadow-brand-500/30' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}>
      {icon}
      <span className="font-medium">{text}</span>
    </Link>
  )
}

function DashboardHome({ isDarkMode }: { isDarkMode: boolean }) {
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    activeContracts: 0,
    monthlyIncome: 0,
    pendingPayments: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await ContractService.getMetrics();
        setMetrics(data);
      } catch (error) {
        console.error("Failed to fetch dashboard data", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className={`p-8 ${isDarkMode ? 'text-slate-400' : 'text-gray-500'}`}>Cargando datos del sistema...</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard
        title="Ingresos Mensuales (Est.)"
        value={`$${metrics.monthlyIncome.toLocaleString()}`}
        trend="Calculado"
        isDarkMode={isDarkMode}
      />
      <StatCard
        title="Contratos Activos"
        value={metrics.activeContracts.toString()}
        trend="Actualizado"
        isDarkMode={isDarkMode}
      />
      <StatCard
        title="Pagos Pendientes"
        value={metrics.pendingPayments.toString()}
        trend="Verificar"
        isNegative
        isDarkMode={isDarkMode}
      />
    </div>
  )
}

function TenantsPage({ isDarkMode }: { isDarkMode: boolean }) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>Gestión de Inquilinos</h3>
        <button className="bg-brand-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-brand-700 transition-colors shadow-lg shadow-brand-500/20">
          + Nuevo Inquilino
        </button>
      </div>
      <div className={`rounded-2xl shadow-sm border p-8 text-center transition-colors duration-300
        ${isDarkMode ? 'bg-slate-900 border-slate-800 text-slate-500' : 'bg-white border-gray-100 text-gray-500'}`}>
        No hay inquilinos registrados actualmente.
      </div>
    </div>
  );
}

function PropertiesPage({ isDarkMode }: { isDarkMode: boolean }) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>Catálogo de Propiedades</h3>
        <button className="bg-brand-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-brand-700 transition-colors shadow-lg shadow-brand-500/20">
          + Nueva Propiedad
        </button>
      </div>
      <div className={`rounded-2xl shadow-sm border p-8 text-center transition-colors duration-300
        ${isDarkMode ? 'bg-slate-900 border-slate-800 text-slate-500' : 'bg-white border-gray-100 text-gray-500'}`}>
        No hay propiedades listadas en el sistema.
      </div>
    </div>
  );
}

function StatCard({ title, value, trend, isNegative, isDarkMode }: any) {
  return (
    <div className={`p-6 rounded-2xl shadow-sm border transition-all duration-300 hover:shadow-md
      ${isDarkMode ? 'bg-slate-900 border-slate-800 hover:border-slate-700' : 'bg-white border-gray-100'}`}>
      <h3 className={isDarkMode ? 'text-slate-400 text-sm font-medium' : 'text-gray-500 text-sm font-medium'}>{title}</h3>
      <div className="mt-2 flex items-baseline gap-2">
        <span className={`text-3xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>{value}</span>
        <span className={`text-sm font-medium ${isNegative ? 'text-red-500' : 'text-emerald-500'}`}>
          {trend}
        </span>
      </div>
    </div>
  )
}

export default App;
