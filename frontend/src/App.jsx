import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Configuration from './pages/Configuration';
import TestExecution from './pages/Execution';
import TestDetail from './pages/TestDetail';
import Dashboard from './pages/Dashboard';
import Monitoring from './pages/Monitoring';
import RealTimeView from './pages/RealTime';

// Placeholder pages for other routes
const Placeholder = ({ title }) => <div className="w-full text-center"><h1 className="text-4xl font-bold">{title}</h1></div>;


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<RealTimeView />} />
          <Route path="monitoring" element={<Monitoring />} />
          <Route path="execution" element={<TestExecution />} />
          <Route path="tests/:id" element={<TestDetail />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="configuration" element={<Configuration />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App; 