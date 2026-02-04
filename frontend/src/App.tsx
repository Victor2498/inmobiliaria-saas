import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, Home, Settings } from 'lucide-react';
import { useEffect, useState } from 'react';
import { ContractService } from './api/services';
import type { DashboardMetrics } from './api/services';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex">
        {/* Sidebar */}
        <aside className="w-64 bg-slate-900 text-white hidden md:flex flex-col">
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
          <header className="bg-white shadow-sm h-16 flex items-center px-8 justify-between">
            <h2 className="text-xl font-semibold text-gray-800">Panel de Control</h2>
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-full bg-brand-500 flex items-center justify-center text-white font-bold">
                A
              </div>
            </div>
          </header>

          <div className="p-8">
            <Routes>
              <Route path="/" element={<DashboardHome />} />
              <Route path="/inquilinos" element={<TenantsPage />} />
              <Route path="/propiedades" element={<PropertiesPage />} />
              <Route path="/configuracion" element={<div className="p-8 text-gray-500">Página de Configuración (Próximamente)</div>} />
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

function DashboardHome() {
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
    return <div className="p-8 text-gray-500">Cargando datos del sistema...</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard
        title="Ingresos Mensuales (Est.)"
        value={`$${metrics.monthlyIncome.toLocaleString()}`}
        trend="Calculado"
      />
      <StatCard
        title="Contratos Activos"
        value={metrics.activeContracts.toString()}
        trend="Actualizado"
      />
      <StatCard
        title="Pagos Pendientes"
        value={metrics.pendingPayments.toString()}
        trend="Verificar"
        isNegative
      />
    </div>
  )
}

function TenantsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-2xl font-bold text-gray-900">Gestión de Inquilinos</h3>
        <button className="bg-brand-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-brand-700 transition-colors">
          + Nuevo Inquilino
        </button>
      </div>
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 text-center text-gray-500">
        No hay inquilinos registrados actualmente.
      </div>
    </div>
  );
}

function PropertiesPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-2xl font-bold text-gray-900">Catálogo de Propiedades</h3>
        <button className="bg-brand-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-brand-700 transition-colors">
          + Nueva Propiedad
        </button>
      </div>
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 text-center text-gray-500">
        No hay propiedades listadas en el sistema.
      </div>
    </div>
  );
}

function StatCard({ title, value, trend, isNegative }: any) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <h3 className="text-gray-500 text-sm font-medium">{title}</h3>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-3xl font-bold text-gray-900">{value}</span>
        <span className={`text-sm font-medium ${isNegative ? 'text-red-500' : 'text-emerald-500'}`}>
          {trend}
        </span>
      </div>
    </div>
  )
}

export default App;
