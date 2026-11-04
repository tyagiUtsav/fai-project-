import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Capture from "./pages/Capture";
import DecisionDetail from "./pages/DecisionDetail";

export default function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Verdikt</div>
        <div className="brand-sub">Decision Accountability</div>
        <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
          Dashboard
        </NavLink>
        <NavLink to="/capture" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
          Capture a Decision
        </NavLink>
      </aside>
      <main className="main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/capture" element={<Capture />} />
          <Route path="/decisions/:id" element={<DecisionDetail />} />
        </Routes>
      </main>
    </div>
  );
}
